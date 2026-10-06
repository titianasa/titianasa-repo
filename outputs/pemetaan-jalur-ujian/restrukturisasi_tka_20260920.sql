-- Fokus Ujian TKA: jenjang -> (SMA: kelompok) -> mapel -> topik.
--
--   Fokus Ujian TKA
--   ├─ TKA SD/MI        Bahasa Indonesia · Matematika · IPAS
--   ├─ TKA SMP/MTs      Bahasa Indonesia · Matematika · Bahasa Inggris · IPA · IPS
--   └─ TKA SMA/MA
--       ├─ Mata Pelajaran Wajib   Bahasa Indonesia · Matematika · Bahasa Inggris
--       ├─ Pilihan Saintek        Biologi · Fisika · Kimia
--       └─ Pilihan Soshum         Akuntansi · Ekonomi · Geografi · Sejarah · Sosiologi
--
-- SMA reuses the folders that already existed (moved, not copied). SD and SMP
-- are built from ALIASES of the topics already listed under Kurikulum
-- Indonesia (Kelas 4-6 / 7-9), so they add no content, only a way in.
-- Runs once (guarded) and inside one transaction.

begin;

do $$
declare
  root uuid; sd uuid; smp uuid; sma uuid; wajib uuid; saintek uuid; soshum uuid; f uuid;
  st text;
begin
  select id into root from modules where parent_id is null and title = 'Fokus Ujian TKA';
  if root is null then raise exception 'folder Fokus Ujian TKA tidak ada'; end if;
  if exists (select 1 from modules where parent_id = root and title = 'TKA SMA/MA') then
    raise exception 'sudah dijalankan';
  end if;
  select status into st from modules where id = root;

  insert into modules (parent_id, is_folder, title, order_index, status, generated_by) values (root, true, 'TKA SD/MI', 0, st, 'human') returning id into sd;
  insert into modules (parent_id, is_folder, title, order_index, status, generated_by) values (root, true, 'TKA SMP/MTs', 1, st, 'human') returning id into smp;
  insert into modules (parent_id, is_folder, title, order_index, status, generated_by) values (root, true, 'TKA SMA/MA', 2, st, 'human') returning id into sma;
  insert into modules (parent_id, is_folder, title, order_index, status, generated_by) values (sma, true, 'Mata Pelajaran Wajib', 0, st, 'human') returning id into wajib;

  -- SMA: the existing folders move in.
  update modules set parent_id = wajib, order_index = 0 where parent_id = (select id from modules where parent_id = root and title = 'TKA Literasi Membaca') and title = 'Bahasa Indonesia';
  update modules set parent_id = wajib, order_index = 1 where parent_id = (select id from modules where parent_id = root and title = 'TKA Numerasi') and title = 'Matematika';
  update modules set parent_id = wajib, order_index = 2 where parent_id = (select id from modules where parent_id = root and title = 'TKA Bahasa Inggris') and title = 'Bahasa Inggris';
  update modules set parent_id = sma, title = 'Pilihan Saintek', order_index = 1 where parent_id = root and title = 'TKA Pilihan — Saintek' returning id into saintek;
  update modules set parent_id = sma, title = 'Pilihan Soshum', order_index = 2 where parent_id = root and title = 'TKA Pilihan — Soshum' returning id into soshum;

  -- IPAS and IPS are lower-secondary subjects: they leave the SMA electives.
  update modules set parent_id = sd, order_index = 2 where parent_id = saintek and title = 'IPAS';
  update modules set parent_id = smp, order_index = 4 where parent_id = soshum and title = 'IPS';

  -- The three wrappers are empty now. Refuse to drop one that is not.
  for f in select id from modules where parent_id = root and title in ('TKA Literasi Membaca', 'TKA Numerasi', 'TKA Bahasa Inggris') loop
    if exists (select 1 from modules where parent_id = f) then raise exception 'folder pembungkus % masih berisi', f; end if;
    delete from modules where id = f;
  end loop;

  -- SD and SMP: a bundle per subject, listing the topics of that subject over the grades.
  perform 1;
end $$;

-- Bundles for SD / SMP built from Kurikulum Indonesia (aliases, deduplicated by source topic).
do $$
declare
  root uuid; sd uuid; smp uuid; st text; spec record; bundle uuid; n int;
begin
  select id into root from modules where parent_id is null and title = 'Fokus Ujian TKA';
  select id into sd from modules where parent_id = root and title = 'TKA SD/MI';
  select id into smp from modules where parent_id = root and title = 'TKA SMP/MTs';
  select status into st from modules where id = root;

  for spec in
    select * from (values
      (sd,  'Bahasa Indonesia', 0, array['Kelas 4 SD/MI','Kelas 5 SD/MI','Kelas 6 SD/MI']),
      (sd,  'Matematika',       1, array['Kelas 4 SD/MI','Kelas 5 SD/MI','Kelas 6 SD/MI']),
      (smp, 'Bahasa Indonesia', 0, array['Kelas 7 SMP/MTs','Kelas 8 SMP/MTs','Kelas 9 SMP/MTs']),
      (smp, 'Matematika',       1, array['Kelas 7 SMP/MTs','Kelas 8 SMP/MTs','Kelas 9 SMP/MTs']),
      (smp, 'Bahasa Inggris',   2, array['Kelas 7 SMP/MTs','Kelas 8 SMP/MTs','Kelas 9 SMP/MTs']),
      (smp, 'IPA',              3, array['Kelas 7 SMP/MTs','Kelas 8 SMP/MTs','Kelas 9 SMP/MTs'])
    ) as t(parent, subject, ord, grades)
  loop
    insert into modules (parent_id, is_folder, title, order_index, status, generated_by) values (spec.parent, true, spec.subject, spec.ord, st, 'human') returning id into bundle;
    insert into modules (parent_id, is_folder, subject_id, code, title, order_index, status, generated_by, source_module_id)
    select bundle, false, src.subject_id, 'ref-tka2-' || substr(md5(bundle::text || src.src_id::text), 1, 12), src.title, (row_number() over (order by src.gord, src.ord, src.title))::int - 1, st, 'human', src.src_id
    from (
      select distinct on (a.source_module_id) a.source_module_id as src_id, s.subject_id, s.title, g.order_index as gord, a.order_index as ord
      from modules g
      join modules m on m.parent_id = g.id and m.title = spec.subject
      join modules a on a.parent_id = m.id and a.source_module_id is not null
      join modules s on s.id = a.source_module_id
      where g.title = any (spec.grades) and g.parent_id in (select id from modules where title like 'SD / MI%' or title like 'SMP / MTs%')
      order by a.source_module_id, g.order_index, a.order_index
    ) src;
    get diagnostics n = row_count;
    raise notice '% > %: % topik', (select title from modules where id = spec.parent), spec.subject, n;
  end loop;
end $$;

commit;
