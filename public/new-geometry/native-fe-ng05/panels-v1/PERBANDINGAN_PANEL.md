# Perbandingan per panel NG05

Maksimum tiap panel dari sembilan kasus native Karamba. Kolom dapat dikendalikan kasus yang berbeda; bukan penjumlahan maksimum. Shell mencakup winding asli dan tambahan. Tidak ada solve baru.

| Panel | Baseline MPa | Ulang MPa | Turun % | Anchor MPa | Turun % |
|---|---:|---:|---:|---:|---:|
| P001 | 2.2624 | 2.2413 | 0.935 | 2.2466 | 0.701 |
| P002 | 3.0350 | 3.0221 | 0.426 | 3.0437 | -0.287 |
| P003 | 3.7716 | 3.7438 | 0.737 | 3.7639 | 0.204 |
| P004 | 2.9448 | 2.9056 | 1.330 | 2.9320 | 0.435 |
| P005 | 5.1336 | 5.0866 | 0.915 | 5.1071 | 0.515 |
| P006 | 5.7819 | 5.6672 | 1.985 | 5.7067 | 1.301 |
| P007 | 4.4045 | 4.3686 | 0.813 | 4.3804 | 0.547 |
| P008 | 3.2199 | 3.1830 | 1.146 | 3.2073 | 0.391 |
| P009 | 2.1685 | 2.1648 | 0.169 | 2.1600 | 0.392 |
| P010 | 2.2291 | 2.1825 | 2.090 | 2.2091 | 0.897 |
| P011 | 3.5100 | 3.4480 | 1.765 | 3.4889 | 0.600 |
| P012 | 2.7897 | 2.7253 | 2.310 | 2.7490 | 1.459 |
| P013 | 1.9311 | 1.9160 | 0.784 | 1.9296 | 0.079 |
| P014 | 2.2197 | 2.2233 | -0.164 | 2.2329 | -0.596 |
| P015 | 3.0061 | 2.9945 | 0.385 | 3.0037 | 0.078 |
| P016 | 1.7371 | 1.7361 | 0.055 | 1.7287 | 0.480 |
| P017 | 3.4334 | 3.3331 | 2.922 | 3.4047 | 0.837 |
| P018 | 2.4187 | 2.4168 | 0.078 | 2.3953 | 0.967 |
| P019 | 2.0663 | 2.0642 | 0.102 | 2.0739 | -0.368 |
| P020 | 2.1467 | 2.1551 | -0.395 | 2.1385 | 0.381 |
| P021 | 1.6109 | 1.6193 | -0.521 | 1.6084 | 0.157 |
| P022 | 2.9999 | 2.9012 | 3.290 | 2.9935 | 0.211 |
| P023 | 2.3053 | 2.1926 | 4.887 | 2.2550 | 2.181 |
| P024 | 2.5733 | 2.5859 | -0.489 | 2.5298 | 1.689 |
| P025 | 2.0492 | 2.0524 | -0.157 | 2.0554 | -0.300 |
| P026 | 3.5344 | 3.5133 | 0.596 | 3.5342 | 0.005 |
| P027 | 2.4179 | 2.5699 | -6.288 | 2.4039 | 0.578 |
| P028 | 2.9692 | 2.8423 | 4.274 | 2.9656 | 0.122 |
| P029 | 2.4369 | 2.5566 | -4.912 | 2.5217 | -3.481 |
| P030 | 1.8174 | 1.8994 | -4.512 | 1.8128 | 0.251 |
| P031 | 4.1093 | 4.0963 | 0.316 | 4.0986 | 0.261 |
| P032 | 3.2139 | 3.2052 | 0.270 | 3.1999 | 0.435 |
| P033 | 6.9278 | 6.7154 | 3.066 | 6.4571 | 6.794 |
| P034 | 7.0963 | 4.7275 | 33.380 | 7.0366 | 0.842 |
| P035 | 2.9745 | 2.9309 | 1.464 | 2.9941 | -0.659 |
| P036 | 2.0158 | 2.0123 | 0.173 | 2.0209 | -0.254 |

## Sebaran perubahan

Batas deskriptif hampir sama: +/-0,1%. Ini bukan toleransi penerimaan hasil atau penilaian keamanan.
- REPEAT shell: 26 turun; 8 naik; 2 hampir sama.
- REPEAT original_shell: 26 turun; 8 naik; 2 hampir sama.
- REPEAT boundary: 27 turun; 8 naik; 1 hampir sama.
- REPEAT link: 24 turun; 8 naik; 4 hampir sama.
- REPEAT displacement: 28 turun; 5 naik; 3 hampir sama.
- REPEAT original_displacement: 28 turun; 5 naik; 3 hampir sama.
- NEW_ANCHOR shell: 26 turun; 7 naik; 3 hampir sama.
- NEW_ANCHOR original_shell: 26 turun; 7 naik; 3 hampir sama.
- NEW_ANCHOR boundary: 29 turun; 4 naik; 3 hampir sama.
- NEW_ANCHOR link: 24 turun; 8 naik; 4 hampir sama.
- NEW_ANCHOR displacement: 27 turun; 8 naik; 1 hampir sama.
- NEW_ANCHOR original_displacement: 28 turun; 7 naik; 1 hampir sama.

Nilai negatif berarti kenaikan. Panel yang menerima reinforcement langsung: P024, P033, P034. Perubahan panel lain menunjukkan redistribusi respons dalam model, bukan bukti arah transfer gaya tanpa pemeriksaan gaya elemen.

Detail nilai dan kasus pengendali per panel tersedia di panel-comparison.json. Tambahan massa kedua kandidat berbeda.

## Kesimpulan

- P034: winding ulang menurunkan maksimum shell sembilan kasus 33,38%, tetapi P033 menjadi hotspot global dan maksimum link P034 naik 38,21%.
- P033: anchor baru menurunkan shell 6,79%; winding ulang 3,07%.
- P024: winding ulang menaikkan maksimum shell 0,49%, sedangkan anchor baru menurunkannya 1,69%. Pemilihan hanya dari hotspot G belum menjamin hasil baik pada kasus lain.
- P027 dan P029 memperlihatkan kenaikan shell pada winding ulang 6,29% dan 4,91%. Ini menunjukkan perlunya memantau panel di luar tiga target.
- P032 tetap mengendalikan maksimum boundary: 23,802 MPa baseline, 23,743 MPa winding ulang, dan 23,788 MPa anchor baru. Perbaikan winding belum banyak mengubah konsentrasi boundary tersebut.
- Kedua kandidat memperbaiki maksimum shell 26 dari 36 panel (>0,1%), tetapi jumlah panel yang membaik tidak menggantikan penilaian nilai maksimum dan kategori lain.
- Gravitasi saja pada anchor baru: maksimum semua node 2,962 mm terjadi di ribbon tambahan; maksimum pada node asli yang sama justru turun dari 2,457 menjadi 2,311 mm.

Belum ada pemenang pada semua ukuran atau PASS keamanan. Perbandingan material tidak identik; angka merupakan hasil model global dengan ikatan sempurna.
