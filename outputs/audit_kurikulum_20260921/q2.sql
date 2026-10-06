\echo === C. topik tanpa bab (10) ===
select distinct on (topic) root, bundle_jalur, topic_title from leaf where bab=0 order by topic, root;

\echo
\echo === D. sebaran jumlah bab per topik (topik unik) ===
select case when bab=0 then '0' when bab=1 then '1' when bab=2 then '2' when bab=3 then '3' when bab between 4 and 5 then '4-5' when bab between 6 and 9 then '6-9' else '10+' end jumlah_bab, count(*) topik
from (select distinct on (topic) * from leaf) x group by 1 order by 1;

\echo
\echo === E. KESESUAIAN 1: folder mapel vs mapel pustaka asal topiknya (alias tersasar) ===
with m as (select distinct title from modules where parent_id=(select id from modules where parent_id is null and title='Semua Mata Pelajaran'))
select l.root, l.bundle_title folder, lb.mapel mapel_asal, count(*) topik
from leaf l join lib lb on lb.topic=l.topic
where l.bundle_title in (select title from m) and lb.mapel is distinct from l.bundle_title
group by 1,2,3 order by 4 desc limit 15;

\echo
\echo === F. KESESUAIAN 2: Tahap pustaka asal topik per jenjang Kurikulum Indonesia / TKA ===
select case when l.bundle_jalur like 'Kurikulum Indonesia > SD%' then 'KI SD' when l.bundle_jalur like 'Kurikulum Indonesia > SMP%' then 'KI SMP' when l.bundle_jalur like 'Kurikulum Indonesia > SMA%' then 'KI SMA'
  when l.bundle_jalur like 'Fokus Ujian TKA > TKA SD%' then 'TKA SD' when l.bundle_jalur like 'Fokus Ujian TKA > TKA SMP%' then 'TKA SMP' when l.bundle_jalur like 'Fokus Ujian TKA > TKA SMA%' then 'TKA SMA' end jenjang,
  substr(lb.tahap,1,7) tahap, count(*) alias_topik
from leaf l join lib lb on lb.topic=l.topic
where l.bundle_jalur like 'Kurikulum Indonesia > %' or l.bundle_jalur like 'Fokus Ujian TKA > TKA S%'
group by 1,2 having case when l.bundle_jalur like 'Kurikulum Indonesia > SD%' then 'KI SD' when l.bundle_jalur like 'Kurikulum Indonesia > SMP%' then 'KI SMP' when l.bundle_jalur like 'Kurikulum Indonesia > SMA%' then 'KI SMA'
  when l.bundle_jalur like 'Fokus Ujian TKA > TKA SD%' then 'TKA SD' when l.bundle_jalur like 'Fokus Ujian TKA > TKA SMP%' then 'TKA SMP' when l.bundle_jalur like 'Fokus Ujian TKA > TKA SMA%' then 'TKA SMA' end is not null
order by 1,2;
