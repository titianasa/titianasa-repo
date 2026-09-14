#!/usr/bin/env python3
"""One-time bulk fill of curriculum_standards for every tahap that
doesn't have one yet — pure admin metadata (jenjang description, which
curriculum it follows, question style), NOT AI output. Nothing here
calls a model; it's typed judgment about what each tahap actually is,
based on its title and its subject's own place in Indonesian K-12
(Kurikulum Merdeka Fase A-F), madrasah (MI/MTs/MA), university (S1) and
postgraduate (S2/S3) conventions, or — for skill/exam-prep subjects
that aren't grade-based — "Umum" with a level description.

Idempotent: only inserts where a tahap has no standard row yet, so the
12 already seeded from Claude's Fisika/Kimia/Matematika work (and
Matematika Tahap 1, filled by hand earlier) are left untouched.

Usage: python3 seed_all_curriculum_standards.py [--dry-run]
"""
import json
import subprocess
import sys

DRY_RUN = "--dry-run" in sys.argv


def psql(sql: str) -> str:
    return subprocess.run(
        ["docker", "exec", "titian-bun-postgres", "psql", "-U", "titian", "-d", "titian_bun", "-t", "-A", "-F", "\x1f", "-c", sql],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


# jenjang, [standar acuan...], bahasa, jenis_soal — one entry per tahap,
# IN ORDER, matching each subject's tahap order_index.
CP = "Kurikulum Merdeka — Capaian Pembelajaran"
BSKAP = "BSKAP No. 033/H/KR/2022"

def fase(letter, grade_range, subject):
    return f"SD/MI {grade_range} (Fase {letter})", [f"{CP} Fase {letter} — {subject} ({BSKAP})"]

SUBJECTS: dict[str, list[tuple[str, list[str], str, str]]] = {
    # ── Kurikulum Merdeka Fase letter-named tahaps ──
    "Bahasa Indonesia": [
        (*fase("A", "kelas 1-2", "Bahasa Indonesia"), "id", "bahasa"),
        ("SMP/MTs kelas 7-9 (Fase D)", [f"{CP} Fase D — Bahasa Indonesia ({BSKAP})"], "id", "bahasa"),
        ("SMA/SMK kelas 10-12 — persiapan AKM & TKA", ["Kerangka Asesmen Kompetensi Minimum (AKM) — Literasi Membaca, Kemendikbudristek", "Kisi-kisi Tes Kompetensi Akademik (TKA)"], "id", "bahasa"),
        ("SMA/MA kelas 10-12 (Fase E-F)", [f"{CP} Fase E-F — Bahasa Indonesia ({BSKAP})"], "id", "bahasa"),
        ("SMA/MA kelas 11-12 (Fase F, lanjut)", [f"{CP} Fase F — Bahasa Indonesia ({BSKAP})"], "id", "bahasa"),
        ("perguruan tinggi S1 Bahasa/Sastra Indonesia", ["Standar Kompetensi Lulusan Program Studi Bahasa Indonesia, Ditjen Diktiristek"], "id", "bahasa"),
    ],
    "IPA": [
        ("SMP/MTs kelas 7 (Fase D)", [f"{CP} Fase D — IPA ({BSKAP})"], "id", "hitungan"),
        ("SMP/MTs kelas 8-9 (Fase D lanjut)", [f"{CP} Fase D — IPA ({BSKAP})"], "id", "hitungan"),
    ],
    "IPAS": [
        (*fase("B", "kelas 3-4", "IPAS"), "id", "hitungan"),
        ("SD/MI kelas 1-4 (Fase A-B)", [f"{CP} Fase A-B — IPAS ({BSKAP})"], "id", "hitungan"),
    ],
    "IPS": [
        ("SMP/MTs kelas 7-9 (Fase D)", [f"{CP} Fase D — IPS ({BSKAP})"], "id", "konsep"),
    ],
    "Pendidikan Kewarganegaraan": [
        ("SMA/MA kelas 10-12 (Fase E-F)", [f"{CP} Fase E-F — Pendidikan Pancasila ({BSKAP})"], "id", "konsep"),
        ("SD/MI kelas 1-6 (Fase A-C)", [f"{CP} Fase A-C — Pendidikan Pancasila ({BSKAP})"], "id", "konsep"),
        ("SMP/MTs kelas 7-9 (Fase D)", [f"{CP} Fase D — Pendidikan Pancasila (PPKn) ({BSKAP})"], "id", "konsep"),
    ],

    # ── Madrasah subjects with explicit MI/MTs/MA/S1 markers ──
    "Al-Qur'an Hadist": [
        ("MI kelas 1-6 (SD)", ["Kurikulum Madrasah — Al-Qur'an Hadis MI, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
        ("MTs kelas 7-9 (SMP)", ["Kurikulum Madrasah — Al-Qur'an Hadis MTs, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
        ("MA kelas 10-12 (SMA)", ["Kurikulum Madrasah — Al-Qur'an Hadis MA, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
        ("perguruan tinggi S1/S2 Ilmu Al-Qur'an dan Tafsir", ["Standar Kompetensi Lulusan Program Studi Ilmu Al-Qur'an dan Tafsir, PTKI"], "id", "konsep"),
    ],
    "Bahasa Arab": [
        ("MI kelas 1-6 (SD)", ["Kurikulum Madrasah — Bahasa Arab MI, Kementerian Agama RI (KMA 183/2019)"], "id", "bahasa"),
        ("MTs kelas 7-9 (SMP)", ["Kurikulum Madrasah — Bahasa Arab MTs, Kementerian Agama RI (KMA 183/2019)"], "id", "bahasa"),
        ("MA kelas 10-12 (SMA)", ["Kurikulum Madrasah — Bahasa Arab MA, Kementerian Agama RI (KMA 183/2019)"], "id", "bahasa"),
        ("perguruan tinggi S1 Bahasa Arab / Sastra Arab", ["Standar Kompetensi Lulusan Program Studi Bahasa Arab, PTKI"], "id", "bahasa"),
    ],
    "Fiqih": [
        ("MI kelas 1-6 (SD)", ["Kurikulum Madrasah — Fikih MI, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
        ("MTs kelas 7-9 (SMP)", ["Kurikulum Madrasah — Fikih MTs, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
        ("MA kelas 10-12 (SMA)", ["Kurikulum Madrasah — Fikih MA, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
        ("perguruan tinggi S1/S2 Hukum Keluarga / Perbandingan Mazhab", ["Standar Kompetensi Lulusan Program Studi Hukum Keluarga Islam, PTKI"], "id", "konsep"),
    ],
    "Sejarah Kebudayaan Islam (SKI)": [
        ("MI kelas 1-6 (SD)", ["Kurikulum Madrasah — SKI MI, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
        ("MTs kelas 7-9 (SMP)", ["Kurikulum Madrasah — SKI MTs, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
        ("MA kelas 10-12 (SMA)", ["Kurikulum Madrasah — SKI MA, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
        ("perguruan tinggi S1/S2 Sejarah Peradaban Islam", ["Standar Kompetensi Lulusan Program Studi Sejarah Peradaban Islam, PTKI"], "id", "konsep"),
    ],

    # ── Non-Islamic religion subjects, already SD/SMP/SMA-marked ──
    **{
        subj: [
            ("SD kelas 1-6", [f"{CP} — Pendidikan Agama {label} dan Budi Pekerti Jenjang SD ({BSKAP})"], "id", "konsep"),
            ("SMP kelas 7-9", [f"{CP} — Pendidikan Agama {label} dan Budi Pekerti Jenjang SMP ({BSKAP})"], "id", "konsep"),
            ("SMA kelas 10-12", [f"{CP} — Pendidikan Agama {label} dan Budi Pekerti Jenjang SMA ({BSKAP})"], "id", "konsep"),
        ]
        for subj, label in [
            ("Pendidikan Agama Buddha", "Buddha"),
            ("Pendidikan Agama Hindu", "Hindu"),
            ("Pendidikan Agama Katolik", "Katolik"),
            ("Pendidikan Agama Khonghucu", "Khonghucu"),
            ("Pendidikan Agama Kristen", "Kristen"),
        ]
    },

    # ── Islamic studies without explicit grade markers (pesantren/MA-Aliyah depth) ──
    "Akhlak Tasawuf": [
        ("MA/pesantren kelas 10-12 (SMA)", ["Kurikulum Pesantren/Madrasah — Akhlak Tasawuf tingkat Aliyah"], "id", "konsep"),
        ("MA/pesantren kelas 10-12, lanjut (SMA)", ["Kurikulum Pesantren/Madrasah — Ilmu Tasawuf tingkat Aliyah"], "id", "konsep"),
        ("perguruan tinggi S1 Tasawuf dan Psikoterapi", ["Standar Kompetensi Lulusan Program Studi Tasawuf dan Psikoterapi, PTKI"], "id", "konsep"),
    ],
    "Akidah Akhlak": [
        ("MI kelas 1-6 (SD)", ["Kurikulum Madrasah — Akidah Akhlak MI, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
        ("MTs kelas 7-9 (SMP)", ["Kurikulum Madrasah — Akidah Akhlak MTs, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
        ("MTs kelas 7-9, lanjut (SMP)", ["Kurikulum Madrasah — Akidah Akhlak MTs, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
        ("MA kelas 10-12 (SMA)", ["Kurikulum Madrasah — Akidah Akhlak MA, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
        ("MA kelas 10-12, lanjut (SMA)", ["Kurikulum Madrasah — Akidah Akhlak MA, Kementerian Agama RI (KMA 183/2019)"], "id", "konsep"),
    ],
    "Ilmu Hadis": [
        ("MA/pesantren kelas 10-12 (SMA)", ["Kurikulum Pesantren/Madrasah — Ilmu Hadis tingkat Aliyah"], "id", "konsep"),
        ("MA/pesantren kelas 10-12, lanjut (SMA)", ["Kurikulum Pesantren/Madrasah — Ilmu Hadis tingkat Aliyah"], "id", "konsep"),
        ("perguruan tinggi S1 Ilmu Hadis", ["Standar Kompetensi Lulusan Program Studi Ilmu Hadis, PTKI"], "id", "konsep"),
    ],
    "Ilmu Kalam": [
        ("MA/pesantren kelas 10-12 (SMA)", ["Kurikulum Pesantren/Madrasah — Ilmu Kalam tingkat Aliyah"], "id", "konsep"),
        ("MA/pesantren kelas 10-12, lanjut (SMA)", ["Kurikulum Pesantren/Madrasah — Ilmu Kalam tingkat Aliyah"], "id", "konsep"),
        ("perguruan tinggi S1 Akidah dan Filsafat Islam", ["Standar Kompetensi Lulusan Program Studi Akidah dan Filsafat Islam, PTKI"], "id", "konsep"),
    ],
    "Ilmu Tafsir": [
        ("MA/pesantren kelas 10-12 (SMA)", ["Kurikulum Pesantren/Madrasah — Ilmu Tafsir tingkat Aliyah"], "id", "konsep"),
        ("MA/pesantren kelas 10-12, lanjut (SMA)", ["Kurikulum Pesantren/Madrasah — Ilmu Tafsir tingkat Aliyah"], "id", "konsep"),
        ("perguruan tinggi S1 Ilmu Al-Qur'an dan Tafsir", ["Standar Kompetensi Lulusan Program Studi Ilmu Al-Qur'an dan Tafsir, PTKI"], "id", "konsep"),
    ],
    "Ushul Fikih": [
        ("MA/pesantren kelas 10-12 (SMA)", ["Kurikulum Pesantren/Madrasah — Ushul Fikih tingkat Aliyah"], "id", "konsep"),
        ("MA/pesantren kelas 10-12, lanjut (SMA)", ["Kurikulum Pesantren/Madrasah — Ushul Fikih tingkat Aliyah"], "id", "konsep"),
        ("perguruan tinggi S1 Hukum Ekonomi Syariah / Perbandingan Mazhab", ["Standar Kompetensi Lulusan Program Studi Hukum Ekonomi Syariah, PTKI"], "id", "konsep"),
    ],

    # ── Foreign languages: proficiency-based (CEFR-like), not grade-based ──
    **{
        subj: [
            ("umum — pemula (setara CEFR A1)", [f"Kerangka CEFR A1 — {subj}"], "id", "bahasa"),
            ("umum — pemula lanjut (setara CEFR A2)", [f"Kerangka CEFR A2 — {subj}"], "id", "bahasa"),
            ("umum — menengah (setara CEFR B1)", [f"Kerangka CEFR B1 — {subj}"], "id", "bahasa"),
            ("umum — menengah lanjut (setara CEFR B2)", [f"Kerangka CEFR B2 — {subj}"], "id", "bahasa"),
        ]
        for subj in ["Bahasa Jepang", "Bahasa Jerman", "Bahasa Korea", "Bahasa Mandarin", "Bahasa Prancis"]
    },
    "Bahasa Inggris": [
        ("umum — pemula (setara CEFR A1)", ["Kerangka CEFR A1 — Bahasa Inggris"], "id", "bahasa"),
        ("umum — pemula lanjut (setara CEFR A2)", ["Kerangka CEFR A2 — Bahasa Inggris — tata bahasa inti"], "id", "bahasa"),
        ("umum — menengah (setara CEFR B1)", ["Kerangka CEFR B1 — Bahasa Inggris — kosakata & ekspresi"], "id", "bahasa"),
        ("umum — menengah lanjut (setara CEFR B2)", ["Kerangka CEFR B2 — Bahasa Inggris — empat keterampilan (listening/speaking/reading/writing)"], "id", "bahasa"),
        ("umum — menengah lanjut (setara CEFR B2, jenis teks)", ["Kerangka CEFR B2 — Bahasa Inggris — genre teks akademik & fungsional"], "id", "bahasa"),
        ("umum — mahir (setara CEFR C1)", ["Kerangka CEFR C1 — Bahasa Inggris — profesional & akademik"], "id", "bahasa"),
        ("perguruan tinggi S1 Sastra Inggris / Linguistik", ["Standar Kompetensi Lulusan Program Studi Sastra Inggris, Ditjen Diktiristek"], "id", "bahasa"),
        ("pascasarjana S2/S3 Linguistik Terapan", ["Standar Kompetensi Lulusan Program Studi Linguistik Terapan (S2), Ditjen Diktiristek"], "id", "bahasa"),
        ("umum/dewasa — persiapan IELTS/TOEFL/TOEIC", ["IELTS Band Descriptors", "TOEFL iBT Score Guide", "TOEIC Score Descriptors"], "id", "bahasa"),
    ],

    # ── Numbered SMP→SMA→S1→S2/S3 progression, explicit tail markers ──
    "Akuntansi": [
        ("SMA/SMK kelas 10-11", ["Standar Kompetensi Akuntansi Dasar SMK, Kemendikbudristek"], "id", "hitungan"),
        ("SMA/SMK kelas 11", ["Standar Kompetensi Akuntansi Perusahaan Jasa SMK, Kemendikbudristek"], "id", "hitungan"),
        ("SMA/SMK kelas 12", ["Standar Kompetensi Akuntansi Perusahaan Dagang SMK, Kemendikbudristek"], "id", "hitungan"),
        ("SMK kelas 12 (kejuruan)", ["Standar Kompetensi Lulusan Akuntansi dan Keuangan Lembaga, SMK"], "id", "hitungan"),
        ("perguruan tinggi S1 Akuntansi", ["Standar Kompetensi Lulusan Program Studi Akuntansi, Ditjen Diktiristek"], "id", "hitungan"),
        ("pascasarjana S2/S3 Akuntansi", ["Standar Kompetensi Lulusan Program Magister/Doktor Akuntansi, Ditjen Diktiristek"], "id", "hitungan"),
    ],
    "Antropologi": [
        ("SMA/MA kelas 10-11 (peminatan Bahasa/IPS)", ["Standar Isi Antropologi SMA, Kemendikbudristek"], "id", "konsep"),
        ("SMA/MA kelas 11-12", ["Standar Isi Antropologi SMA, Kemendikbudristek"], "id", "konsep"),
        ("perguruan tinggi S1 Antropologi", ["Standar Kompetensi Lulusan Program Studi Antropologi, Ditjen Diktiristek"], "id", "konsep"),
        ("pascasarjana S2/S3 Antropologi", ["Standar Kompetensi Lulusan Program Magister/Doktor Antropologi, Ditjen Diktiristek"], "id", "konsep"),
    ],
    "Biologi": [
        ("SMA/MA kelas 10-11 (Fase E-F)", [f"{CP} Fase E-F — Biologi (Sel & Jaringan) ({BSKAP})"], "id", "hitungan"),
        ("SMA/MA kelas 11 (Fase F)", [f"{CP} Fase F — Biologi (Fisiologi Manusia) ({BSKAP})"], "id", "hitungan"),
        ("SMA/MA kelas 12 (Fase F)", [f"{CP} Fase F — Biologi (Metabolisme & Genetika) ({BSKAP})"], "id", "hitungan"),
        ("SMA/MA kelas 12 (Fase F)", [f"{CP} Fase F — Biologi (Evolusi, Ekologi, Bioteknologi) ({BSKAP})"], "id", "hitungan"),
        ("perguruan tinggi S1 Biologi", ["Standar Kompetensi Lulusan Program Studi Biologi, Ditjen Diktiristek"], "id", "hitungan"),
        ("pascasarjana S2/S3 Biologi", ["Standar Kompetensi Lulusan Program Magister/Doktor Biologi, Ditjen Diktiristek"], "id", "hitungan"),
    ],
    "Bisnis & Manajemen": [
        ("SMA/SMK kelas 10-11", ["Standar Kompetensi Bisnis dan Manajemen SMK, Kemendikbudristek"], "id", "konsep"),
        ("perguruan tinggi S1 Manajemen", ["Standar Kompetensi Lulusan Program Studi Manajemen, Ditjen Diktiristek"], "id", "konsep"),
        ("perguruan tinggi S1 Manajemen (lanjut)", ["Standar Kompetensi Lulusan Program Studi Manajemen, Ditjen Diktiristek"], "id", "konsep"),
        ("pascasarjana S2/S3 Manajemen", ["Standar Kompetensi Lulusan Program Magister/Doktor Manajemen (MBA), Ditjen Diktiristek"], "id", "konsep"),
    ],
    "Ekonomi": [
        ("SMA/MA kelas 10 (Fase E)", [f"{CP} Fase E — Ekonomi ({BSKAP})"], "id", "hitungan"),
        ("SMA/MA kelas 11 (Fase F)", [f"{CP} Fase F — Ekonomi (Mikro) ({BSKAP})"], "id", "hitungan"),
        ("SMA/MA kelas 11-12 (Fase F)", [f"{CP} Fase F — Ekonomi (Makro) ({BSKAP})"], "id", "hitungan"),
        ("SMA/MA kelas 12 (Fase F)", [f"{CP} Fase F — Ekonomi Terapan & Internasional ({BSKAP})"], "id", "hitungan"),
        ("perguruan tinggi S1 Ekonomi/Ekonomi Pembangunan", ["Standar Kompetensi Lulusan Program Studi Ilmu Ekonomi, Ditjen Diktiristek"], "id", "hitungan"),
        ("pascasarjana S2/S3 Ilmu Ekonomi", ["Standar Kompetensi Lulusan Program Magister/Doktor Ilmu Ekonomi, Ditjen Diktiristek"], "id", "hitungan"),
    ],
    "Filsafat": [
        ("perguruan tinggi S1 Filsafat, pengantar", ["Standar Kompetensi Lulusan Program Studi Filsafat, Ditjen Diktiristek"], "id", "konsep"),
        ("perguruan tinggi S1 Filsafat", ["Standar Kompetensi Lulusan Program Studi Filsafat — Sejarah Filsafat Barat, Ditjen Diktiristek"], "id", "konsep"),
        ("perguruan tinggi S1 Filsafat", ["Standar Kompetensi Lulusan Program Studi Filsafat — Cabang-cabang Filsafat, Ditjen Diktiristek"], "id", "konsep"),
        ("perguruan tinggi S1 Filsafat", ["Standar Kompetensi Lulusan Program Studi Filsafat — Filsafat Timur & Nusantara, Ditjen Diktiristek"], "id", "konsep"),
        ("pascasarjana S2/S3 Filsafat", ["Standar Kompetensi Lulusan Program Magister/Doktor Filsafat, Ditjen Diktiristek"], "id", "konsep"),
    ],
    "Geografi": [
        ("SMA/MA kelas 10 (Fase E)", [f"{CP} Fase E — Geografi ({BSKAP})"], "id", "konsep"),
        ("SMA/MA kelas 11 (Fase F)", [f"{CP} Fase F — Geografi (Fisik) ({BSKAP})"], "id", "konsep"),
        ("SMA/MA kelas 11 (Fase F)", [f"{CP} Fase F — Geografi (Manusia) ({BSKAP})"], "id", "konsep"),
        ("SMA/MA kelas 12 (Fase F)", [f"{CP} Fase F — Geografi (Kebencanaan & Global) ({BSKAP})"], "id", "konsep"),
        ("perguruan tinggi S1 Geografi", ["Standar Kompetensi Lulusan Program Studi Geografi, Ditjen Diktiristek"], "id", "konsep"),
        ("pascasarjana S2/S3 Geografi", ["Standar Kompetensi Lulusan Program Magister/Doktor Geografi, Ditjen Diktiristek"], "id", "konsep"),
    ],
    "Informatika": [
        ("SMP/MTs kelas 7-9 (Fase D)", [f"{CP} Fase D — Informatika (Literasi Digital) ({BSKAP})"], "id", "hitungan"),
        ("SMA/MA kelas 10 (Fase E)", [f"{CP} Fase E — Informatika (Berpikir Komputasional) ({BSKAP})"], "id", "hitungan"),
        ("SMA/MA kelas 11 (Fase F)", [f"{CP} Fase F — Informatika (Sistem Komputer & Jaringan) ({BSKAP})"], "id", "hitungan"),
        ("SMA/MA kelas 11-12 (Fase F)", [f"{CP} Fase F — Informatika (Data, Web & Aplikasi) ({BSKAP})"], "id", "hitungan"),
        ("perguruan tinggi S1 Ilmu Komputer/Informatika", ["Standar Kompetensi Lulusan Program Studi Informatika, Ditjen Diktiristek"], "id", "hitungan"),
    ],
    "Matematika": [
        # Tahap 1 (SD, Fase A-C) was filled by hand earlier — these 4 are
        # Tahap 2-5: SMP -> SMA -> S1 -> S2/S3.
        ("SMP/MTs kelas 7-9 (Fase D)", [f"{CP} Fase D — Matematika ({BSKAP})"], "id", "hitungan"),
        ("SMA/MA kelas 10-11 (Fase E-F)", [f"{CP} Fase E-F — Matematika ({BSKAP})"], "id", "hitungan"),
        ("SMA/MA kelas 12 (Fase F) — Matematika Tingkat Lanjut / mahir", [f"{CP} Fase F — Matematika Tingkat Lanjut ({BSKAP})"], "id", "hitungan"),
        ("pascasarjana S2/S3 Matematika", ["Standar Kompetensi Lulusan Program Magister/Doktor Matematika, Ditjen Diktiristek"], "id", "hitungan"),
    ],
    "PJOK": [
        ("SD/MI kelas 1-6 (Fase A-C)", [f"{CP} Fase A-C — PJOK ({BSKAP})"], "id", "konsep"),
        ("SMP/MTs kelas 7-9 (Fase D)", [f"{CP} Fase D — PJOK ({BSKAP})"], "id", "konsep"),
        ("SMA/MA kelas 10-12 (Fase E-F)", [f"{CP} Fase E-F — PJOK (Kesehatan) ({BSKAP})"], "id", "konsep"),
        ("perguruan tinggi S1 Ilmu Keolahragaan", ["Standar Kompetensi Lulusan Program Studi Ilmu Keolahragaan, Ditjen Diktiristek"], "id", "konsep"),
    ],
    "Penalaran & Logika": [
        ("umum/dewasa — tes seleksi (CPNS/BUMN/sekolah kedinasan)", ["Kisi-kisi Tes Potensi Skolastik (TPS) — Penalaran Verbal, SNBT"], "id", "konsep"),
        ("umum/dewasa — tes seleksi (CPNS/BUMN/sekolah kedinasan)", ["Kisi-kisi Tes Potensi Skolastik (TPS) — Penalaran Kuantitatif, SNBT"], "id", "hitungan"),
        ("umum/dewasa — tes seleksi (CPNS/BUMN/sekolah kedinasan)", ["Kisi-kisi Tes Potensi Skolastik (TPS) — Pengetahuan & Pemahaman Umum (figural/spasial), SNBT"], "id", "konsep"),
        ("umum/dewasa — tes seleksi (CPNS/BUMN/sekolah kedinasan)", ["Kisi-kisi Tes Intelegensia Umum (TIU) — Penalaran Analitis & Logis, SKD CPNS"], "id", "konsep"),
        ("umum/dewasa — tes seleksi (CPNS/BUMN/sekolah kedinasan)", ["Strategi umum tes potensi skolastik dan intelegensia — simulasi paket lengkap"], "id", "konsep"),
    ],
    "Prakarya & Kewirausahaan": [
        ("SMP/MTs kelas 7-9 (Fase D)", [f"{CP} Fase D — Prakarya ({BSKAP})"], "id", "konsep"),
        ("SMA/MA kelas 10-12 (Fase E-F)", [f"{CP} Fase E-F — Kewirausahaan ({BSKAP})"], "id", "konsep"),
        ("SMA/SMK kelas 12 (kejuruan)", ["Standar Kompetensi Produk Kreatif dan Kewirausahaan, SMK"], "id", "konsep"),
    ],
    "Psikologi": [
        ("SMA/MA kelas 11-12 (peminatan)", ["Standar Isi Psikologi Peminatan SMA, Kemendikbudristek"], "id", "konsep"),
        ("perguruan tinggi S1 Psikologi", ["Standar Kompetensi Lulusan Program Studi Psikologi, Ditjen Diktiristek"], "id", "konsep"),
        ("perguruan tinggi S1 Psikologi (terapan)", ["Standar Kompetensi Lulusan Program Studi Psikologi, Ditjen Diktiristek"], "id", "konsep"),
        ("pascasarjana S2/S3 Psikologi (Profesi/Magister/Doktor)", ["Standar Kompetensi Lulusan Program Magister/Doktor/Profesi Psikologi, Ditjen Diktiristek"], "id", "konsep"),
    ],
    "Sastra Indonesia": [
        ("SMA/MA kelas 10-11 (peminatan Bahasa)", ["Standar Isi Sastra Indonesia Peminatan SMA, Kemendikbudristek"], "id", "bahasa"),
        ("SMA/MA kelas 11-12 (peminatan Bahasa)", ["Standar Isi Sastra Indonesia Peminatan SMA, Kemendikbudristek"], "id", "bahasa"),
        ("SMA/MA kelas 12 (peminatan Bahasa)", ["Standar Isi Sastra Indonesia Peminatan SMA, Kemendikbudristek"], "id", "bahasa"),
        ("perguruan tinggi S1/S2 Sastra Indonesia", ["Standar Kompetensi Lulusan Program Studi Sastra Indonesia, Ditjen Diktiristek"], "id", "bahasa"),
    ],
    "Sejarah": [
        ("SMA/MA kelas 10 (Fase E)", [f"{CP} Fase E — Sejarah ({BSKAP})"], "id", "konsep"),
        ("SMA/MA kelas 10-11 (Fase E-F)", [f"{CP} Fase E-F — Sejarah Indonesia (Praaksara-Islam) ({BSKAP})"], "id", "konsep"),
        ("SMA/MA kelas 11 (Fase F)", [f"{CP} Fase F — Sejarah Indonesia (Kolonialisme & Pergerakan) ({BSKAP})"], "id", "konsep"),
        ("SMA/MA kelas 12 (Fase F)", [f"{CP} Fase F — Sejarah Indonesia (Kemerdekaan) ({BSKAP})"], "id", "konsep"),
        ("SMA/MA kelas 11-12 (peminatan, Fase F)", [f"{CP} Fase F — Sejarah Dunia (peminatan) ({BSKAP})"], "id", "konsep"),
        ("perguruan tinggi S1 Ilmu Sejarah", ["Standar Kompetensi Lulusan Program Studi Ilmu Sejarah, Ditjen Diktiristek"], "id", "konsep"),
        ("pascasarjana S2/S3 Ilmu Sejarah", ["Standar Kompetensi Lulusan Program Magister/Doktor Ilmu Sejarah, Ditjen Diktiristek"], "id", "konsep"),
    ],
    "Seni Budaya": [
        ("SD-SMA kelas 1-12 (Fase A-F)", [f"{CP} Fase A-F — Seni Budaya, pengantar ({BSKAP})"], "id", "konsep"),
        ("SD-SMA kelas 1-12 (Fase A-F)", [f"{CP} Fase A-F — Seni Rupa ({BSKAP})"], "id", "konsep"),
        ("SD-SMA kelas 1-12 (Fase A-F)", [f"{CP} Fase A-F — Seni Musik ({BSKAP})"], "id", "konsep"),
        ("SD-SMA kelas 1-12 (Fase A-F)", [f"{CP} Fase A-F — Seni Tari dan Teater ({BSKAP})"], "id", "konsep"),
        ("SMA/SMK kelas 11-12 (industri kreatif)", ["Standar Kompetensi Desain Komunikasi Visual / Industri Kreatif, SMK"], "id", "konsep"),
    ],
    "Sosiologi": [
        ("SMA/MA kelas 10 (Fase E)", [f"{CP} Fase E — Sosiologi ({BSKAP})"], "id", "konsep"),
        ("SMA/MA kelas 11 (Fase F)", [f"{CP} Fase F — Sosiologi (Struktur & Dinamika Sosial) ({BSKAP})"], "id", "konsep"),
        ("SMA/MA kelas 11-12 (Fase F)", [f"{CP} Fase F — Sosiologi (Perubahan & Masalah Sosial) ({BSKAP})"], "id", "konsep"),
        ("SMA/MA kelas 12 (Fase F)", [f"{CP} Fase F — Sosiologi (Penelitian Sosial) ({BSKAP})"], "id", "konsep"),
        ("perguruan tinggi S1 Sosiologi", ["Standar Kompetensi Lulusan Program Studi Sosiologi, Ditjen Diktiristek"], "id", "konsep"),
        ("pascasarjana S2/S3 Sosiologi", ["Standar Kompetensi Lulusan Program Magister/Doktor Sosiologi, Ditjen Diktiristek"], "id", "konsep"),
    ],
    "Teknik Otomotif": [
        ("SMK kelas 10 (kejuruan)", ["Standar Kompetensi Dasar-Dasar Teknik Otomotif, SMK"], "id", "hitungan"),
        ("SMK kelas 11 (kejuruan)", ["Standar Kompetensi Pemeliharaan Mesin Kendaraan Ringan, SMK"], "id", "hitungan"),
        ("SMK kelas 11-12 (kejuruan)", ["Standar Kompetensi Sistem Kelistrikan & Pemindah Tenaga, SMK"], "id", "hitungan"),
        ("SMK kelas 12 (kejuruan)", ["Standar Kompetensi Sasis dan Teknologi Otomotif Lanjut, SMK"], "id", "hitungan"),
        ("perguruan tinggi S1/Diploma Teknik Otomotif", ["Standar Kompetensi Lulusan Program Studi Teknik Otomotif, Ditjen Diktiristek"], "id", "hitungan"),
    ],

    # ── Professional / exam-prep subjects: "Umum" throughout ──
    "Wawasan ASN & Kepegawaian": [
        ("umum/dewasa — CPNS/PPPK", ["Kisi-kisi Tes Karakteristik Pribadi (TKP), SKD CPNS/PPPK"], "id", "konsep"),
        ("umum/dewasa — CPNS/PPPK", ["Kisi-kisi Seleksi Kompetensi Bidang (SKB), sesuai formasi jabatan"], "id", "konsep"),
        ("perguruan tinggi S1 Administrasi Publik", ["Standar Kompetensi Lulusan Program Studi Administrasi Publik, Ditjen Diktiristek"], "id", "konsep"),
        ("umum/dewasa — CPNS/PPPK", ["Kisi-kisi Tes Wawasan Kebangsaan (TWK), SKD CPNS"], "id", "konsep"),
    ],
    # This subject's tahap rows sort (by order_index) as 4,3,2,1, not
    # 1,2,3,4 — order below matches that actual DB order, not the title.
    "Wawasan BUMN & Dunia Kerja": [
        ("umum/dewasa — asesmen karier", ["Kerangka Learning Agility untuk asesmen rekrutmen"], "id", "konsep"),  # Tahap 4
        ("umum/dewasa — rekrutmen BUMN & dunia kerja", ["Kisi-kisi Tes Kesiapan Seleksi Kerja BUMN/Swasta"], "id", "konsep"),  # Tahap 3
        ("umum/dewasa — rekrutmen BUMN", ["Materi Budaya Kerja dan Tata Kelola BUMN, Kementerian BUMN RI"], "id", "konsep"),  # Tahap 2
        ("umum/dewasa — rekrutmen BUMN", ["Core Values AKHLAK BUMN, Kementerian BUMN RI"], "id", "konsep"),  # Tahap 1
    ],
}


def main():
    # `json_agg` with no ORDER BY of its OWN does not reliably preserve
    # the subquery's ordering (Postgres is free to feed the aggregate
    # rows in whatever order the plan happens to produce, even when the
    # subquery itself has an ORDER BY) — learned this the hard way when
    # a dry run and the real run returned the same rows in different
    # order. The ORDER BY has to be on json_agg itself to be guaranteed.
    raw = psql(
        "select json_agg(row_to_json(x) order by x.subject, x.order_index) from ("
        "  select t.id as tahap_id, s.title as subject, t.title as tahap, t.order_index "
        "  from modules t join modules s on s.id = t.parent_id join modules r on r.id = s.parent_id "
        "  left join curriculum_standards cs on cs.tahap_folder_id = t.id "
        "  where r.parent_id is null and r.title = 'Semua Mata Pelajaran' and t.is_folder and cs.tahap_folder_id is null "
        ") x;"
    )
    missing = json.loads(raw)

    by_subject: dict[str, list[dict]] = {}
    for row in missing:
        by_subject.setdefault(row["subject"], []).append(row)

    inserted = 0
    unmatched_subjects = []
    for subject, rows in by_subject.items():
        rows.sort(key=lambda r: r["order_index"])
        mapping = SUBJECTS.get(subject)
        if not mapping:
            unmatched_subjects.append((subject, len(rows)))
            continue
        if len(mapping) != len(rows):
            print(f"!! {subject}: mapping has {len(mapping)} entries but {len(rows)} tahap are missing — check order/count", file=sys.stderr)
            continue
        for row, (jenjang, standar, bahasa, jenis_soal) in zip(rows, mapping):
            # Double backslashes first, then quotes, for the array element
            # boundary; the whole result is then embedded in a SQL
            # single-quoted literal, so any literal `'` (e.g. "Qur'an")
            # must ALSO be doubled for SQL's own escaping — a raw
            # apostrophe here would otherwise terminate the string early.
            standar_sql = "{" + ",".join('"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"' for s in standar) + "}"
            standar_sql = standar_sql.replace("'", "''")
            sql = (
                f"insert into curriculum_standards (tahap_folder_id, jenjang, standar, bahasa, jenis_soal, catatan) "
                f"values ('{row['tahap_id']}', $${jenjang}$$, '{standar_sql}', '{bahasa}', '{jenis_soal}', "
                f"'Diisi manual (skrip seed_all_curriculum_standards.py) — bukan hasil AI. Sesuaikan bila perlu.') "
                f"on conflict (tahap_folder_id) do nothing;"
            )
            if DRY_RUN:
                print(f"[dry-run] {subject} / {row['tahap']} -> {jenjang}")
            else:
                psql(sql)
            inserted += 1

    print(f"\n=== {inserted} standar {'akan diisi' if DRY_RUN else 'diisi'} ===")
    if unmatched_subjects:
        print("Belum ada pemetaan untuk subjek berikut (dilewati):")
        for subj, n in unmatched_subjects:
            print(f"  - {subj} ({n} tahap)")


if __name__ == "__main__":
    main()
