\echo === K. Kurikulum Indonesia: jenjang x mapel (topik unik, bab, bermateri, lengkap) ===
select case when l.bundle_jalur like 'Kurikulum Indonesia > SD%' then '1 SD' when l.bundle_jalur like 'Kurikulum Indonesia > SMP%' then '2 SMP' else '3 SMA' end jenjang,
  l.bundle_title mapel, count(distinct l.topic) topik, sum(l.bab) bab, sum(l.materi) materi, sum(l.lengkap) lengkap, sum(l.bab)-sum(l.lengkap) kurang
from (select distinct on (bundle, topic) * from leaf where root='Kurikulum Indonesia') l
where l.bundle_title in (select title from modules where parent_id=(select id from modules where parent_id is null and title='Semua Mata Pelajaran'))
group by 1,2 order by 1,7 desc;

\echo
\echo === L. Matematika per Kelas (Kurikulum Indonesia) vs jumlah unit kanonik di level padanan ===
with kelas as (select l.bundle, substring(k.title from 'Kelas (\d+)')::int n, l.topic, l.bab, l.lengkap
  from leaf l join modules k on k.id=(select parent_id from modules where id=l.bundle) where l.root='Kurikulum Indonesia' and l.bundle_title='Matematika' and k.title like 'Kelas %')
select n kelas, count(distinct topic) topik, sum(bab) bab, sum(lengkap) lengkap,
  (select count(*) from canon_units u join canon_concepts c on c.id=u.concept_id join canon_strands st on st.id=c.strand_id where st.subject_code='matematika' and u.level=k.n) unit_kanonik_level
from (select distinct on (bundle, topic) * from kelas) k group by n order by n;
