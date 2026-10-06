\set ON_ERROR_STOP on
-- 1. semua node pada 5 learning path yang tampil (tanpa cabang yang ditahan)
create temp table sc as
with recursive t as (
  select m.id, m.parent_id, m.title, m.is_folder, m.source_module_id src, m.title as root, 0 d, m.title::text as jalur
  from modules m where m.parent_id is null and m.title in ('Belajar Bahasa Inggris','Kurikulum Indonesia','Kurikulum Cambridge','Fokus Ujian TKA','Persiapan Ujian Masuk Perguruan Tinggi')
  union all
  select c.id, c.parent_id, c.title, c.is_folder, c.source_module_id, t.root, t.d+1, t.jalur || ' > ' || c.title
  from modules c join t on c.parent_id=t.id
  where not exists (select 1 from canon_held_titles h where c.title ilike h.pattern)
)
select * from t;
create index on sc(id);

-- 2. statistik bab per topik pustaka (topik = modul yang punya bab)
create temp table tb as
select b.module_id topic,
  count(*) bab,
  count(*) filter (where exists (select 1 from module_items a where a.parent_id=b.id and a.content_type='article' and jsonb_array_length(coalesce(a.lesson_plan->'sections','[]'::jsonb))>0)) materi,
  count(*) filter (where coalesce(s.total,0)>=15) bank,
  count(*) filter (where coalesce(s.total,0)>=15 and exists (select 1 from module_items a where a.parent_id=b.id and a.content_type='article' and jsonb_array_length(coalesce(a.lesson_plan->'sections','[]'::jsonb))>0)) lengkap,
  count(*) filter (where coalesce(s.total,0)>0 and coalesce(s.total,0)<15) bank_tipis
from module_items b left join bab_bank_stats s on s.bab_id=b.id where b.node_type='section' group by b.module_id;
create index on tb(topic);

-- 3. daun jalur: alias -> topik sumber (dan folder pembungkusnya)
create temp table leaf as
select sc.root, sc.parent_id bundle, (select title from modules where id=sc.parent_id) bundle_title,
  (select jalur from sc s2 where s2.id=sc.parent_id) bundle_jalur, sc.src topic,
  (select title from modules where id=sc.src) topic_title,
  coalesce(tb.bab,0) bab, coalesce(tb.materi,0) materi, coalesce(tb.bank,0) bank, coalesce(tb.lengkap,0) lengkap, coalesce(tb.bank_tipis,0) bank_tipis
from sc left join tb on tb.topic=sc.src where sc.src is not null;

-- 4. mapel dan Tahap pustaka dari topik sumber
create temp table lib as
with recursive up as (select id, parent_id, title, 0 d, id origin from modules where id in (select topic from leaf)
  union all select m.id, m.parent_id, m.title, up.d+1, up.origin from modules m join up on m.id=up.parent_id)
select origin topic,
  (select title from up u2 where u2.origin=up.origin and u2.parent_id=(select id from modules where parent_id is null and title='Semua Mata Pelajaran') limit 1) mapel,
  (select title from up u3 where u3.origin=up.origin and u3.parent_id in (select id from modules where parent_id=(select id from modules where parent_id is null and title='Semua Mata Pelajaran')) limit 1) tahap
from up group by origin;
create index on lib(topic);

\echo === A. RINGKASAN PER LEARNING PATH (aliran topik, dihitung per alias) ===
select root, count(*) alias_topik, count(distinct topic) topik_unik,
  count(*) filter (where bab=0) topik_tanpa_bab, sum(bab) bab, sum(materi) bab_bermateri, sum(bank) bab_berbank, sum(lengkap) bab_lengkap
from leaf group by root order by root;

\echo
\echo === B. TOPIK UNIK DI SELURUH JALUR (tanpa hitung ganda) ===
select count(*) topik_unik, count(*) filter (where bab=0) tanpa_bab, count(*) filter (where bab>0 and lengkap=0) ada_bab_tapi_tak_ada_yang_lengkap,
  count(*) filter (where bab>0 and lengkap>0 and lengkap<bab) sebagian_lengkap, count(*) filter (where bab>0 and lengkap=bab) semua_lengkap,
  sum(bab) bab_total, sum(materi) bab_bermateri, sum(bank) bab_berbank, sum(lengkap) bab_lengkap
from (select distinct on (topic) * from leaf) x;
