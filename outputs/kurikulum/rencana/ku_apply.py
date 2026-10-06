#!/usr/bin/env python3
"""Menerapkan judul bab 'Kesalahan Umum' yang spesifik (ku_a..ku_g) dan bab isi tambahan. Idempoten. --dry membatalkan."""
import json, subprocess, sys
import ku_a, ku_b, ku_c, ku_d, ku_e, ku_f, ku_g
KU = {}
for m in (ku_a, ku_b, ku_c, ku_d, ku_e, ku_f, ku_g): KU.update(m.KU)
EXTRA = {
 ("Akuntansi","Laporan Perubahan Ekuitas"):"Hubungan Laporan Perubahan Ekuitas dengan Laporan Posisi Keuangan",
 ("Akuntansi","Profesi & Etika Akuntan"):"Lembaga dan Regulasi Profesi Akuntan di Indonesia",
 ("Akuntansi","Neraca Saldo Setelah Penutupan"):"Perbedaan Neraca Saldo Sebelum dan Sesudah Penutupan",
 ("Akuntansi","Neraca Saldo"):"Menelusuri dan Memperbaiki Selisih pada Neraca Saldo",
 ("Bahasa Inggris","Infinitives of Purpose"):"Menyusun Kalimat Tujuan dalam Konteks Nyata",
 ("Bahasa Inggris","Past Perfect Continuous"):"Menyusun Narasi Latar Belakang dengan Past Perfect Continuous",
 ("Bahasa Inggris","Verbs Followed by Gerund"):"Menyusun Kalimat Lengkap dengan Verba dan Gerund",
 ("Bahasa Inggris","Interjections"):"Penggunaan Interjeksi dalam Dialog Tertulis",
 ("Bahasa Inggris","Future Perfect"):"Future Perfect dalam Prediksi dan Perencanaan Target",
 ("Bahasa Inggris","Past Perfect"):"Penerapan Past Perfect dalam Narasi Tertulis",
 ("Bahasa Inggris","Past Continuous"):"Penerapan Past Continuous dalam Cerita Naratif",
 ("Biologi","Perbandingan Mitosis & Meiosis"):"Tabel dan Diagram Perbandingan Tahap Mitosis dan Meiosis",
 ("Biologi","Persilangan Dihibrid"):"Rasio Fenotipe 9:3:3:1 dan Variasinya",
 ("Ekonomi","Devisa & Cadangan Devisa"):"Devisa dalam Neraca Pembayaran Indonesia",
 ("Ekonomi","Utilitas Total & Marginal"):"Soal Hitungan Utilitas dan Pembacaan Tabel Kepuasan",
 ("Geografi","Wilayah & Perwilayahan"):"Studi Kasus Wilayah Formal dan Fungsional di Indonesia",
 ("IPA","Hukum Newton Sederhana"):"Penerapan Hukum Newton pada Situasi Sehari-hari",
 ("IPA","Hukum Pascal"):"Soal Cerita Sistem Hidrolik",
 ("IPA","Resultan Gaya"):"Menggambar Diagram Gaya pada Benda",
 ("IPA","Tekanan Hidrostatis"):"Soal Cerita Tekanan pada Kedalaman Berbeda",
 ("IPA","Tekanan pada Zat Padat"):"Soal Cerita Tekanan dan Perhitungan Satuan",
 ("Penalaran & Logika","Fakta vs Opini"):"Latihan Membedakan Fakta dan Opini dalam Wacana Panjang",
 ("Sejarah","Kausalitas dalam Sejarah"):"Diagram Sebab-Akibat Peristiwa Sejarah Indonesia",
 ("Sejarah","Konsep Ruang & Waktu"):"Menganalisis Peristiwa dengan Peta dan Garis Waktu",
 ("Sosiologi","Sifat: Terbuka, Tertutup & Campuran"):"Contoh Stratifikasi Terbuka dan Tertutup di Masyarakat Indonesia",
 ("Sosiologi","Fungsi Stratifikasi"):"Analisis Kasus Stratifikasi dalam Organisasi",
 ("Matematika","Luas Permukaan Bangun Ruang"):"Menghitung Bahan yang Dibutuhkan untuk Melapisi Bangun Ruang",
 ("Matematika","Irisan Bidang pada Bangun Ruang"):"Latihan Menggambar Irisan pada Kubus dan Limas",
 ("Bahasa Indonesia","Keteladanan Tokoh dalam Biografi"):"Membandingkan Keteladanan Dua Tokoh dari Bidang Berbeda",
 ("Bahasa Indonesia","Menceritakan Kembali Isi Biografi"):"Menceritakan Kembali Biografi dengan Kata Sendiri secara Tertulis",
 ("Bahasa Indonesia","Menyunting Teks LHO"):"Menyunting Teks LHO Temannya dengan Lembar Koreksi",
 ("Bahasa Indonesia","Menulis Teks LHO"):"Menyempurnakan Draf Teks LHO Menjadi Teks Akhir",
 ("Bahasa Indonesia","Fakta & Klasifikasi dalam LHO"):"Menyusun Bagan Klasifikasi dari Hasil Observasi",
 ("Sosiologi","Status & Peran Sosial"):"Konflik Peran dan Pembedaan Status dengan Peran",
}
payload = {"ku": [{"s": s, "t": t, "k": k} for s, d in KU.items() for t, k in d.items()],
           "extra": [{"s": s, "t": t, "x": x} for (s, t), x in EXTRA.items()]}
sql = r"""begin;
do $x$ begin perform set_config('app.ku', $p$""" + json.dumps(payload, ensure_ascii=False) + r"""$p$, false); end $x$;
do $b$
declare p jsonb := current_setting('app.ku')::jsonb; e jsonb; tp record; bab uuid; kub uuid; ordx int; n_ren int := 0; n_add int := 0; n_ext int := 0; root uuid;
begin
  select id into root from modules where title = 'Semua Mata Pelajaran' and parent_id is null;
  for e in select value from jsonb_array_elements(p->'ku') loop
    for tp in select m.id, m.title from modules s join modules t on t.parent_id = s.id join modules g on g.parent_id = t.id join modules m on m.parent_id = g.id and not m.is_folder
        where s.parent_id = root and s.title = e->>'s' and m.source_module_id is null and m.title = e->>'t' loop
      select id into bab from module_items where module_id = tp.id and node_type = 'section' and status <> 'archived' and title = 'Kesalahan Umum: ' || tp.title limit 1;
      if bab is not null then
        update module_items set title = 'Kesalahan Umum: ' || (e->>'k') where id = bab;
        update module_items set title = replace(title, 'Kesalahan Umum: ' || tp.title, 'Kesalahan Umum: ' || (e->>'k')) where parent_id = bab;
        n_ren := n_ren + 1;
      elsif not exists (select 1 from module_items where module_id = tp.id and node_type = 'section' and status <> 'archived' and title like 'Kesalahan Umum%')
            and exists (select 1 from module_items where module_id = tp.id and node_type = 'section' and status <> 'archived') then
        select coalesce(max(order_index), -1) + 1 into ordx from module_items where module_id = tp.id and node_type = 'section' and status <> 'archived';
        insert into module_items (module_id, node_type, depth, title, order_index, status, generated_by) values (tp.id, 'section', 0, 'Kesalahan Umum: ' || (e->>'k'), ordx, 'draft', 'ai') returning id into bab;
        insert into module_items (module_id, parent_id, node_type, depth, title, order_index, content_type, status, generated_by) values (tp.id, bab, 'item', 1, 'Pembahasan — Kesalahan Umum: ' || (e->>'k'), 0, 'article', 'draft', 'ai');
        insert into module_items (module_id, parent_id, node_type, depth, title, order_index, content_type, status, generated_by, quiz_config) values (tp.id, bab, 'item', 1, 'Latihan 3 — Kesalahan Umum: ' || (e->>'k'), 3, 'quiz', 'draft', 'ai', '{"question_groups": []}'::jsonb);
        n_add := n_add + 1;
      end if;
    end loop;
  end loop;
  for e in select value from jsonb_array_elements(p->'extra') loop
    for tp in select m.id, m.title from modules s join modules t on t.parent_id = s.id join modules g on g.parent_id = t.id join modules m on m.parent_id = g.id and not m.is_folder
        where s.parent_id = root and s.title = e->>'s' and m.source_module_id is null and m.title = e->>'t' loop
      if not exists (select 1 from module_items where module_id = tp.id and node_type = 'section' and status <> 'archived' and title = e->>'x') then
        select id, order_index into kub, ordx from module_items where module_id = tp.id and node_type = 'section' and status <> 'archived' and title like 'Kesalahan Umum%' order by order_index desc limit 1;
        if kub is null then continue; end if;
        update module_items set order_index = ordx + 1 where id = kub;
        insert into module_items (module_id, node_type, depth, title, order_index, status, generated_by) values (tp.id, 'section', 0, e->>'x', ordx, 'draft', 'ai') returning id into bab;
        insert into module_items (module_id, parent_id, node_type, depth, title, order_index, content_type, status, generated_by) values (tp.id, bab, 'item', 1, 'Pembahasan — ' || (e->>'x'), 0, 'article', 'draft', 'ai');
        insert into module_items (module_id, parent_id, node_type, depth, title, order_index, content_type, status, generated_by, quiz_config) values (tp.id, bab, 'item', 1, 'Latihan 3 — ' || (e->>'x'), 3, 'quiz', 'draft', 'ai', '{"question_groups": []}'::jsonb);
        n_ext := n_ext + 1;
      end if;
    end loop;
  end loop;
  raise notice 'KU diganti % | KU ditambah % | bab isi tambahan %', n_ren, n_add, n_ext;
end $b$;
""" + ("rollback;" if "--dry" in sys.argv else "commit;")
r = subprocess.run(["docker","exec","-i","titian-bun-postgres","psql","-U","titian","titian_bun","-v","ON_ERROR_STOP=1","-q"], input=sql, text=True, capture_output=True)
print(r.stdout.strip()[:400]); print("\n".join(l for l in r.stderr.splitlines() if "NOTICE" in l or "ERROR" in l or "DETAIL" in l)[:2000])
