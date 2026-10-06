"""Menambahkan jalur turunan UTBK/UM-PTN ke rencana SMA setelah dibangkitkan ulang."""
import json
U="Persiapan Ujian Masuk Perguruan Tinggi"
spec={"fisika":("Fisika","Materi Mata Pelajaran — Saintek"),"kimia":("Kimia","Materi Mata Pelajaran — Saintek"),"biologi":("Biologi","Materi Mata Pelajaran — Saintek"),
 "ekonomi":("Ekonomi","Materi Mata Pelajaran — Soshum"),"geografi":("Geografi","Materi Mata Pelajaran — Soshum"),"sejarah":("Sejarah","Materi Mata Pelajaran — Soshum"),"sosiologi":("Sosiologi","Materi Mata Pelajaran — Soshum"),"akuntansi":("Akuntansi","Materi Mata Pelajaran — Soshum"),
 "bahasa_indonesia":("Bahasa Indonesia",None),"penalaran":("Penalaran & Logika",None)}
for f,(m,grp) in spec.items():
    p=json.load(open(f"{f}.json"))
    p["tka"]=[e for e in p.get("tka",[]) if e.get("root")!=U]
    if grp: p["tka"].append({"root":U,"via":[grp],"bundle":m,"kelas":[10,11,12]})
    p["tka"].append({"root":U,"via":["Ujian Mandiri PTN"],"bundle":m,"kelas":[10,11,12]})
    json.dump(p,open(f"{f}.json","w"),ensure_ascii=False,indent=1)
