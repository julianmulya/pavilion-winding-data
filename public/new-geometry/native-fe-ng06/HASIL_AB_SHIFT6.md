# Winding A/B shift 6 — hasil native Karamba

25 anchor per sisi, shift 6, gap 0,4 m, 36 panel. Tambahan hanya pada P024/P033/P034. Geometri awal, boundary, material, tumpuan dan lokasi lateral tetap. InitialStrain OFF.

| Kandidat | CFRP tambahan kg | Shell MPa | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|---:|
| Baseline | 0.0000 | 7.0963 | 23.8021 | 5.7281 | 5.2003 |
| Winding ulang | 0.3010 | 6.7154 | 23.7430 | 7.9167 | 5.2320 |
| Anchor baru | 0.5052 | 7.0366 | 23.7882 | 5.4143 | 5.0866 |
| Winding A/B shift 6 | 6.8369 | 6.3222 | 23.1427 | 5.3252 | 5.5123 |

Seluruh angka maksimum adalah envelope sembilan kasus. Tegangan utama shell dan tegangan normal beam dilaporkan terpisah; bukan satu metrik maksimum sistem.

A/B mengikuti anchor asli yang tidak sepenuhnya koplanar (audit native maksimum penyimpangan 36,8–84,2 mm). Tidak ada proyeksi atau perubahan geometri. Siklus tiap sisi: i -> (i+6) modulo 25; satu lingkaran lokal per kunjungan anchor. FE memakai bentang lurus shell dan berat lilitan lokal nodal; kontak baut tidak dinilai.

Tambahan 150 bentang, 150 lilitan, 214,937 m CFRP atau 6,8369 kg. Anggaran material berbeda dari dua kandidat terdahulu; hasil bukan uji topologi bermassa sama.

## Pemeriksaan native

Satu Analyze menyelesaikan sembilan kasus, tanpa error/warning. Residual gaya maksimum 7.16941331256686e-11 kN. Mapping muka shell dan probe tegangan beam tervalidasi. Output mentah tiap kasus disimpan terpisah.

## Interpretasi

Envelope shell turun 10.908%, boundary dan link Al juga turun, tetapi perpindahan maksimum naik 6.001%. Karena itu kandidat belum unggul pada seluruh indikator. Tambahan massa juga jauh lebih besar. Tidak ada PASS keamanan struktur.