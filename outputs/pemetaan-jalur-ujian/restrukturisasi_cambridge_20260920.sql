-- Kurikulum Cambridge: Primary (Stage 1-6) and Lower Secondary (Stage 7-9)
-- carried copies of the Indonesian school subjects (Akidah Akhlak, PJOK,
-- Bahasa Indonesia...). Cambridge teaches Mathematics, English and Science, so
-- each Stage now holds exactly those three, pointing at the SAME library topics
-- as Kurikulum Indonesia (Stage N = Kelas N): one bab, one progress, two ways in.
--
--   Stage N > Mathematics (Matematika) · English (Bahasa Inggris) · Science (IPAS/IPA)
--
-- Only ALIAS rows inside the Cambridge tree are removed; no library topic, bab
-- or question is touched. Runs once (guarded), in one transaction.

begin;

do $$
declare
  cam uuid; stg record; kelas uuid; english uuid; st text; n int; removed int := 0;
begin
  select id into cam from modules where parent_id is null and title = 'Kurikulum Cambridge';
  if cam is null then raise exception 'Kurikulum Cambridge tidak ada'; end if;
  if exists (select 1 from modules where title = 'English (Bahasa Inggris)' and parent_id in (select id from modules where parent_id in (select id from modules where parent_id = cam))) then
    raise exception 'sudah dijalankan';
  end if;

  for stg in
    select s.id, s.status, (regexp_replace(s.title, '\D', '', 'g'))::int as num
    from modules s
    where s.parent_id in (select id from modules where parent_id = cam and (title like 'Cambridge Primary%' or title like 'Cambridge Lower Secondary%'))
      and s.title ~ '^Stage \d+$'
  loop
    -- 1. drop the subject folders Cambridge does not teach (alias rows only).
    delete from modules a where a.parent_id in (select f.id from modules f where f.parent_id = stg.id and f.title not in ('Matematika', 'IPAS', 'IPA'))
      and a.source_module_id is not null;
    get diagnostics n = row_count; removed := removed + n;
    delete from modules f where f.parent_id = stg.id and f.title not in ('Matematika', 'IPAS', 'IPA')
      and not exists (select 1 from modules c where c.parent_id = f.id)
      and not exists (select 1 from module_items b where b.module_id = f.id);

    -- 2. Cambridge names for what stays.
    update modules set title = 'Mathematics (Matematika)', order_index = 0 where parent_id = stg.id and title = 'Matematika';
    update modules set title = 'Science (IPAS)', order_index = 2 where parent_id = stg.id and title = 'IPAS';
    update modules set title = 'Science (IPA)', order_index = 2 where parent_id = stg.id and title = 'IPA';

    -- 3. English: the topics of that Kelas' Bahasa Inggris, as aliases.
    select k.id into kelas from modules k
      where k.title = case when stg.num <= 6 then 'Kelas ' || stg.num || ' SD/MI' else 'Kelas ' || stg.num || ' SMP/MTs' end
        and k.parent_id in (select id from modules where parent_id = (select id from modules where parent_id is null and title = 'Kurikulum Indonesia'))
      limit 1;
    if kelas is not null and exists (select 1 from modules e where e.parent_id = kelas and e.title = 'Bahasa Inggris') then
      insert into modules (parent_id, is_folder, title, order_index, status, generated_by)
        values (stg.id, true, 'English (Bahasa Inggris)', 1, stg.status, 'human') returning id into english;
      insert into modules (parent_id, is_folder, subject_id, code, title, order_index, status, generated_by, source_module_id)
      select english, false, s.subject_id, 'ref-cam2-' || substr(md5(english::text || a.source_module_id::text), 1, 12), s.title,
             (row_number() over (order by a.order_index, s.title))::int - 1, stg.status, 'human', a.source_module_id
      from modules e
      join modules a on a.parent_id = e.id and a.source_module_id is not null
      join modules s on s.id = a.source_module_id
      where e.parent_id = kelas and e.title = 'Bahasa Inggris';
      get diagnostics n = row_count;
      raise notice 'Stage %: English % topik', stg.num, n;
    else
      raise notice 'Stage %: tidak ada Bahasa Inggris di Kelas padanannya', stg.num;
    end if;
  end loop;
  raise notice 'baris alias salinan dihapus: %', removed;
end $$;

commit;
