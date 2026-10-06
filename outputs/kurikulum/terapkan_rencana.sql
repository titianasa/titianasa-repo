-- Menerapkan satu rencana kurikulum (JSON) ke perpustakaan modul dan ke jalur turunan.
-- Isi rencana: lihat STANDAR_PENGEMBANGAN_KURIKULUM_MAPEL_TOPIK_BAB_V1.md sec. 4.
-- Dipakai lewat terapkan.py, yang menaruh JSON di setting `app.plan`. Satu transaksi; aman diulang.

create or replace function pg_temp.ensure_folder(p_parent uuid, p_title text, p_ord int, p_status text) returns uuid language plpgsql as $f$
declare v uuid;
begin
  select id into v from modules where parent_id = p_parent and title = p_title and is_folder limit 1;
  if v is null then
    insert into modules (parent_id, is_folder, title, order_index, status, generated_by) values (p_parent, true, p_title, p_ord, p_status, 'human') returning id into v;
  end if;
  return v;
end $f$;

create or replace function pg_temp.set_aliases(p_bundle uuid, p_topics uuid[], p_status text) returns int language plpgsql as $f$
declare n int;
begin
  delete from modules where parent_id = p_bundle and source_module_id is not null;
  -- Bundle hasil rencana: urutan alias adalah urutan pedagogis (dibaca oleh services/canon_path.rs).
  update modules set metadata = coalesce(metadata, '{}'::jsonb) || '{"urut": "alias"}'::jsonb where id = p_bundle;
  insert into modules (parent_id, is_folder, subject_id, code, title, order_index, status, generated_by, source_module_id)
  select p_bundle, false, s.subject_id, 'ref-cur-' || substr(md5(p_bundle::text || s.id::text), 1, 12), s.title, (u.ord - 1)::int, p_status, 'human', s.id
  from unnest(p_topics) with ordinality as u(tid, ord) join modules s on s.id = u.tid;
  get diagnostics n = row_count;
  return n;
end $f$;

create temp table plan_topics (kelas int, ord int, topic uuid, is_new boolean, cam boolean default true, primary key (kelas, ord));
create temp table plan_bab (bab uuid primary key);
create temp table topic_alias (topic uuid, old_title text);

do $body$
declare
  p jsonb := current_setting('app.plan')::jsonb;
  v_tahap uuid; v_status text; v_subject uuid; v_tahaps uuid[]; tgt uuid; band text; kur text; jal text; ki_jn text; ki_kl text; n_hapus int := 0; n_tmp int;
  jenj text := p->>'jenjang';
  grp_map jsonb := '{}'::jsonb;
  g record; k record; t record; b record;
  grp uuid; topic_id uuid; bab_id uuid; is_new boolean; v_title text; src_title text; v_new text;
  n_topic_new int := 0; n_topic_reuse int := 0; n_bab_new int := 0; n_bab_move int := 0; n_arsip int := 0; n_alias int := 0;
  a record; orphan record; n_orphan int := 0;
  ki uuid; ki_j uuid; ki_k uuid; bundle uuid; cam uuid; cam_s uuid; cam_st uuid; tka uuid; tka_f uuid; x record; arr uuid[]; sec_title text;
begin
  select id, status into v_tahap, v_status from modules where title = p->>'tahap' and parent_id is not null limit 1;
  if v_tahap is null then raise exception 'Tahap % tidak ditemukan', p->>'tahap'; end if;
  select array_agg(id) into v_tahaps from modules where parent_id is not null and title = any (coalesce((select array_agg(value #>> '{}') from jsonb_array_elements(p->'tahaps')), array[p->>'tahap']));
  if v_tahaps is null or not (v_tahap = any (v_tahaps)) then v_tahaps := coalesce(v_tahaps, '{}') || v_tahap; end if;
  select s.subject_id into v_subject from modules s where s.parent_id in (select id from modules where parent_id = any (v_tahaps)) and not s.is_folder and s.subject_id is not null limit 1;

  -- kelompok (grup) topik, berurutan
  for g in select value #>> '{}' as title, ordinality as i from jsonb_array_elements(p->'grup') with ordinality loop
    grp := pg_temp.ensure_folder(v_tahap, g.title, g.i::int - 1, v_status);
    update modules set order_index = g.i::int - 1 where id = grp;
    grp_map := grp_map || jsonb_build_object(g.title, grp);
  end loop;

  for k in select key::int as n, value as topics from jsonb_each(p->'kelas') order by key::int loop
    for t in select value as e, ordinality::int as i from jsonb_array_elements(k.topics) with ordinality loop
      grp := null;
      if t.e ? 'grup' then
        if t.e ? 'tahap' then
          select id into tgt from modules where parent_id is not null and title = t.e->>'tahap' limit 1;
          grp := pg_temp.ensure_folder(tgt, t.e->>'grup', 99, v_status);
        else
          grp := (grp_map->>(t.e->>'grup'))::uuid;
          if grp is null then grp := pg_temp.ensure_folder(v_tahap, t.e->>'grup', 99, v_status); end if;
        end if;
      end if;
      band := case when jenj = 'AUTO' then (case when k.n <= 6 then 'SD' when k.n <= 9 then 'SMP' else 'SMA' end) else jenj end;
      topic_id := null; is_new := false;
      if t.e ? 'pakai' then
        select m.id into topic_id from modules m where not m.is_folder and m.title = t.e->>'pakai' and m.parent_id in (select id from modules where parent_id = any (v_tahaps)) limit 1;
      end if;
      if topic_id is null then
        select m.id into topic_id from modules m where not m.is_folder and m.title = t.e->>'topik' and m.parent_id in (select id from modules where parent_id = any (v_tahaps)) limit 1;
      end if;
      if topic_id is null then
        if grp is null then raise exception 'topik baru "%" butuh grup', t.e->>'topik'; end if;
        insert into modules (parent_id, is_folder, subject_id, code, title, order_index, status, generated_by)
        values (grp, false, v_subject, coalesce(p->>'kode', 'kur') || '-' || substr(md5(random()::text || clock_timestamp()::text), 1, 8), t.e->>'topik', k.n * 10 + t.i, v_status, 'ai') returning id into topic_id;
        is_new := true; n_topic_new := n_topic_new + 1;
      else
        insert into topic_alias select id, title from modules where id = topic_id and title <> t.e->>'topik';
        update modules set title = t.e->>'topik', parent_id = coalesce(grp, parent_id), order_index = k.n * 10 + t.i where id = topic_id;
        n_topic_reuse := n_topic_reuse + 1;
      end if;
      insert into plan_topics values (k.n, t.i, topic_id, is_new, coalesce((t.e->>'cam')::boolean, true));

      -- label kelas dan padanan Cambridge
      delete from module_labels where module_id = topic_id and (kind = 'jenjang' or (kind = 'cambridge' and (p->>'cambridge_label')::boolean is true));
      insert into module_labels (module_id, kind, value, source) values (topic_id, 'jenjang', band || '-' || k.n, 'human');
      if (p->>'cambridge_label')::boolean is true then
        insert into module_labels (module_id, kind, value, source) values (topic_id, 'cambridge', case when k.n <= 6 then 'primary-' else 'lower-sec-' end || k.n, 'human');
      end if;
      if is_new then
        for x in select key as kind, value #>> '{}' as val from jsonb_each(p->'label') loop
          insert into module_labels (module_id, kind, value, source) values (topic_id, x.kind, x.val, 'human') on conflict do nothing;
        end loop;
        if jenj = 'AUTO' then
          insert into module_labels (module_id, kind, value, source) values
            (topic_id, 'kurikulum', case band when 'SD' then 'merdeka-sd' when 'SMP' then 'merdeka-smp' else 'merdeka-sma' end, 'human'),
            (topic_id, 'jalur', case band when 'SD' then 'sd-mi' when 'SMP' then 'smp-mts' else 'sma-ma' end, 'human') on conflict do nothing;
        end if;
      end if;

      -- bab
      for b in select value as e, ordinality::int as j from jsonb_array_elements(t.e->'bab') with ordinality loop
        bab_id := null;
        if jsonb_typeof(b.e) = 'string' then
          v_title := b.e #>> '{}';
          select id into bab_id from module_items where node_type = 'section' and module_id = topic_id and title = v_title and status <> 'archived' limit 1;
          if bab_id is null then
            insert into module_items (module_id, node_type, depth, title, order_index, status, generated_by) values (topic_id, 'section', 0, v_title, b.j - 1, 'draft', 'ai') returning id into bab_id;
            insert into module_items (module_id, parent_id, node_type, depth, title, order_index, content_type, status, generated_by) values (topic_id, bab_id, 'item', 1, 'Pembahasan — ' || v_title, 0, 'article', 'draft', 'ai');
            insert into module_items (module_id, parent_id, node_type, depth, title, order_index, content_type, status, generated_by, quiz_config) values (topic_id, bab_id, 'item', 1, 'Latihan 3 — ' || v_title, 3, 'quiz', 'draft', 'ai', '{"question_groups": []}'::jsonb);
            n_bab_new := n_bab_new + 1;
          end if;
        else
          src_title := b.e->>'dari'; v_title := b.e->>'judul'; v_new := coalesce(b.e->>'baru', v_title);
          select id into bab_id from module_items where node_type = 'section' and module_id = topic_id and title = v_new and status <> 'archived' limit 1;
          if bab_id is null then
            select mi.id into bab_id from module_items mi join modules m on m.id = mi.module_id
              where mi.node_type = 'section' and mi.title = v_title and mi.status <> 'archived'
                and m.parent_id in (select id from modules where parent_id = any (v_tahaps))
                and (m.title = src_title or m.id in (select topic from topic_alias where old_title = src_title)) limit 1;
            if bab_id is null then raise exception 'bab "%" di topik "%" tidak ditemukan (posisi bab kini: %)', v_title, src_title, (select string_agg(m.title || '/' || mi.status || '/' || coalesce(m.parent_id::text,'-'), ' ; ') from module_items mi join modules m on m.id = mi.module_id where mi.title = v_title and mi.node_type = 'section'); end if;
            update module_items set module_id = topic_id where id = bab_id or parent_id = bab_id;
            n_bab_move := n_bab_move + 1;
          end if;
          if v_new <> v_title then
            update module_items set title = v_new where id = bab_id;
            update module_items set title = replace(title, v_title, v_new) where parent_id = bab_id;
          end if;
        end if;
        update module_items set order_index = b.j - 1 where id = bab_id;
        insert into plan_bab values (bab_id) on conflict do nothing;
      end loop;
    end loop;
  end loop;

  -- arsip: bab kembar diarsipkan, tidak dihapus
  for a in select value as e from jsonb_array_elements(coalesce(p->'arsip', '[]'::jsonb)) loop
    update module_items set status = 'archived' where node_type = 'section' and status <> 'archived' and id in (
      select mi.id from module_items mi join modules m on m.id = mi.module_id where mi.title = a.e->>'bab' and m.parent_id in (select id from modules where parent_id = any (v_tahaps)) and (m.title = a.e->>'topik' or m.id in (select topic from topic_alias where old_title = a.e->>'topik')));
    get diagnostics n_arsip = row_count;
    update module_items set status = 'archived' where parent_id in (select mi.id from module_items mi where mi.status = 'archived' and mi.title = a.e->>'bab');
  end loop;

  -- hapus: bab dan topik yang memang tidak sesuai (aplikasi belum live); jejak alias ikut dihapus
  for a in select value as e from jsonb_array_elements(coalesce(p->'hapus', '[]'::jsonb)) loop
    delete from module_items where id in (
      select mi.id from module_items mi join modules m on m.id = mi.module_id
      where mi.node_type = 'section' and mi.title = a.e->>'bab' and m.parent_id in (select id from modules where parent_id = any (v_tahaps))
        and (m.title = a.e->>'topik' or m.id in (select topic from topic_alias where old_title = a.e->>'topik'))
        and mi.id not in (select bab from plan_bab)
    ) or parent_id in (
      select mi.id from module_items mi join modules m on m.id = mi.module_id
      where mi.node_type = 'section' and mi.title = a.e->>'bab' and m.parent_id in (select id from modules where parent_id = any (v_tahaps))
        and (m.title = a.e->>'topik' or m.id in (select topic from topic_alias where old_title = a.e->>'topik'))
        and mi.id not in (select bab from plan_bab)
    );
    get diagnostics n_tmp = row_count; n_hapus := n_hapus + n_tmp;
  end loop;
  for a in select value #>> '{}' as title from jsonb_array_elements(coalesce(p->'hapus_topik', '[]'::jsonb)) loop
    for x in select m.id from modules m where not m.is_folder and m.title = a.title and m.parent_id in (select id from modules where parent_id = any (v_tahaps))
             and not exists (select 1 from plan_topics pt where pt.topic = m.id) loop
      delete from modules where source_module_id = x.id;
      delete from module_items where module_id = x.id;
      delete from modules where id = x.id;
      n_hapus := n_hapus + 1;
    end loop;
  end loop;

  -- bab yang masih tertinggal di topik tahap ini tetapi tidak ada di rencana
  for orphan in select mi.title bab, m.title topik from module_items mi join modules m on m.id = mi.module_id
      where mi.node_type = 'section' and mi.status <> 'archived' and m.parent_id in (select id from modules where parent_id = any (v_tahaps))
        and mi.id not in (select bab from plan_bab)
        and m.title not in (select value #>> '{}' from jsonb_array_elements(coalesce(p->'biarkan', '[]'::jsonb))) loop
    n_orphan := n_orphan + 1;
    raise notice 'TERTINGGAL: "%" di topik "%"', orphan.bab, orphan.topik;
  end loop;

  -- jalur turunan
  if p ? 'ki' then
    select id into ki from modules where parent_id is null and title = 'Kurikulum Indonesia';
    for k in select distinct kelas from plan_topics order by kelas loop
      band := case when k.kelas <= 6 then 'SD' when k.kelas <= 9 then 'SMP' else 'SMA' end;
      ki_jn := case when jsonb_typeof(p->'ki'->'jenjang') = 'object' then p->'ki'->'jenjang'->>band else p->'ki'->>'jenjang' end;
      ki_kl := case when jsonb_typeof(p->'ki'->'kelas') = 'object' then p->'ki'->'kelas'->>band else p->'ki'->>'kelas' end;
      select id into ki_j from modules where parent_id = ki and title = ki_jn;
      select id into ki_k from modules where parent_id = ki_j and title = replace(ki_kl, '{n}', k.kelas::text);
      if ki_k is null then raise notice 'folder KI kelas % tidak ada', k.kelas; continue; end if;
      bundle := pg_temp.ensure_folder(ki_k, p->'ki'->>'bundle', 0, v_status);
      select array_agg(topic order by ord) into arr from plan_topics where kelas = k.kelas;
      n_alias := n_alias + pg_temp.set_aliases(bundle, arr, v_status);
    end loop;
  end if;

  if p ? 'cambridge' then
    select id into cam from modules where parent_id is null and title = 'Kurikulum Cambridge';
    for k in select distinct kelas from plan_topics order by kelas loop
      sec_title := case when k.kelas <= 6 then 'Cambridge Primary%' else 'Cambridge Lower Secondary%' end;
      select id into cam_s from modules where parent_id = cam and title like sec_title limit 1;
      select id into cam_st from modules where parent_id = cam_s and title = 'Stage ' || k.kelas;
      if cam_st is null then continue; end if;
      bundle := pg_temp.ensure_folder(cam_st, p->'cambridge'->>'bundle', 0, v_status);
      select array_agg(topic order by ord) into arr from plan_topics where plan_topics.kelas = k.kelas and plan_topics.cam;
      n_alias := n_alias + pg_temp.set_aliases(bundle, arr, v_status);
    end loop;
  end if;

  if p ? 'tka' then
    select id into tka from modules where parent_id is null and title = 'Fokus Ujian TKA';
    for x in select value as e from jsonb_array_elements(p->'tka') loop
      tka_f := coalesce((select id from modules where parent_id is null and title = x.e->>'root'), tka);
      if x.e ? 'via' then
        for a in select value #>> '{}' as title from jsonb_array_elements(x.e->'via') loop
          select id into tka_f from modules where parent_id = tka_f and title = a.title;
        end loop;
      else
        select id into tka_f from modules where parent_id = tka and title = x.e->>'folder';
      end if;
      if tka_f is null then continue; end if;
      bundle := pg_temp.ensure_folder(tka_f, x.e->>'bundle', 0, v_status);
      select array_agg(pt.topic order by pt.kelas, pt.ord) into arr from plan_topics pt where pt.kelas in (select (value #>> '{}')::int from jsonb_array_elements(x.e->'kelas'));
      n_alias := n_alias + pg_temp.set_aliases(bundle, arr, v_status);
    end loop;
  end if;

  -- kelompok (grup) yang kosong setelah topik dipindah dibuang
  delete from modules f where f.is_folder and f.source_module_id is null and f.parent_id = any (v_tahaps)
    and not exists (select 1 from modules c where c.parent_id = f.id);

  raise notice 'topik baru % | topik dipakai ulang % | bab baru % | bab dipindah % | bab diarsip % | dihapus % | tertinggal % | alias dibangun %', n_topic_new, n_topic_reuse, n_bab_new, n_bab_move, n_arsip, n_hapus, n_orphan, n_alias;
end $body$;
