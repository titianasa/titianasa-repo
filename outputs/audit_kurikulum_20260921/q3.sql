\echo === G. TINGKAT TIDAK SESUAI: topik dari Tahap lanjut/pascasarjana di jenjang rendah ===
select case when l.bundle_jalur like '%SD/MI%' or l.bundle_jalur like '%SD%' then 'SD' when l.bundle_jalur like '%SMP%' then 'SMP' when l.bundle_jalur like '%SMA%' then 'SMA' end jenjang,
  lb.mapel, lb.tahap, count(*) alias_topik, count(distinct l.topic) topik_unik
from leaf l join lib lb on lb.topic=l.topic
where (l.bundle_jalur like 'Kurikulum Indonesia > SD%' or l.bundle_jalur like 'Kurikulum Indonesia > SMP%' or l.bundle_jalur like 'Kurikulum Indonesia > SMA%')
  and ((l.bundle_jalur like 'Kurikulum Indonesia > SD%' and lb.tahap ~ 'Tahap [3-9] —')
    or (l.bundle_jalur like 'Kurikulum Indonesia > SMP%' and lb.tahap ~ 'Tahap [4-9] —')
    or (l.bundle_jalur like 'Kurikulum Indonesia > SMA%' and lb.tahap ~ 'Tahap [5-9] —'))
group by 1,2,3 order by 1, 4 desc;

\echo
\echo === H. contoh judul Tahap asing (Tahap A/B/C/D/E/P) ===
select lb.mapel, lb.tahap, count(distinct l.topic) from leaf l join lib lb on lb.topic=l.topic where lb.tahap !~ '^Tahap [0-9]' group by 1,2 order by 3 desc limit 12;

\echo
\echo === I. bab BERJUDUL SAMA dalam scope (duplikasi antar-topik) ===
with sb as (select b.id, b.title, b.module_id from module_items b where b.node_type='section' and b.module_id in (select topic from leaf))
select count(*) judul_ganda, sum(n) bab_terlibat from (select title, count(*) n, count(distinct module_id) topik from sb group by title having count(*)>1) d;
select title, count(*) kali, count(distinct module_id) topik from (select b.title, b.module_id from module_items b where b.node_type='section' and b.module_id in (select topic from leaf)) z group by title having count(*)>1 order by 2 desc limit 8;

\echo
\echo === J. bab yang SUDAH bermateri tapi banknya belum >=15 soal (murah dilengkapi) ===
select count(*) from module_items b left join bab_bank_stats s on s.bab_id=b.id
where b.node_type='section' and b.module_id in (select topic from leaf) and coalesce(s.total,0)<15
 and exists (select 1 from module_items a where a.parent_id=b.id and a.content_type='article' and jsonb_array_length(coalesce(a.lesson_plan->'sections','[]'::jsonb))>0);
