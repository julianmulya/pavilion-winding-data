# Hasil FE Karamba NG03

Konfigurasi: 25 anchor per boundary, shift 6, gap 0,4 m, 36 panel. Bentuk sisi terbuka tetap \_/; P033 memiliki alas A+B datar Z=0.

## Hasil native

| Beban | Shell winding maks. | Boundary CFRP maks. | Link Al maks. | Perpindahan maks. |
|---|---:|---:|---:|---:|
| G | 2.081 MPa | 10.583 MPa | 1.671 MPa | 2.457 mm |
| G_X_POS | 3.957 MPa | 12.511 MPa | 2.943 MPa | 2.622 mm |
| G_X_NEG | 4.503 MPa | 14.988 MPa | 2.704 MPa | 3.929 mm |
| G_Y_POS | 6.466 MPa | 17.089 MPa | 5.499 MPa | 3.333 mm |
| G_Y_NEG | 7.096 MPa | 23.802 MPa | 5.728 MPa | 5.200 mm |

Analyze native selesai tanpa error/warning. Lima kasus diselesaikan pada satu pemanggilan Analyze. InitialStrain OFF. Residual gaya maksimum 9.928e-11 kN.

## Model dan batas interpretasi

Material, penampang, mesh, toleransi, sambungan ekuivalen dan definisi pembebanan meneruskan model global konseptual sebelumnya. Boundary permanen pada template FE adalah tepi CFRP ekuivalen D10 mm dengan sleeve aluminium lokal; tidak ada rangka aluminium kontinu yang ditambahkan. Sambungan antar panel mengikat seluruh DOF yang berimpit; kontak baut dan slip tidak dinilai. Semua translasi XYZ pada 101 node garis tumpuan Z=0 ditahan, rotasi bebas.

Gaya lateral total 1 kN pada 62 simpul atas untuk masing-masing arah merupakan beban konseptual, bukan tekanan angin desain. Native shell terdiri atas 14.400 segitiga; boundary memiliki 3.581 beam milik panel dan 1.800 link aluminium lokal.

## Hotspot dan review

G-Y mengendalikan seluruh maksimum yang dilaporkan: shell P034 = 7,096 MPa di [2,674972; 6,865243; 0,627212] m; boundary P032 A S036 = 23,802 MPa di [6,794609; 6,257268; 1,676054] m; link Al P034 V017 = 5,728 MPa. Perpindahan terbesar 5,200 mm di [3,819994; 6,790419; 0,593770] m.

Hotspot shell berubah dari P024 pada gravitasi ke P033/P034 pada pembebanan lateral. Secara interpretatif, konsentrasinya berada di area kaki sisi terbuka dan panel di sekitarnya. Pernyataan ini merupakan pembacaan lokasi hasil, bukan hasil analisis kontak sambungan.

Tegangan shell adalah maksimum absolut tegangan utama pada kedua muka. Tegangan beam adalah maksimum absolut tegangan normal ekstrem pada 17 stasiun tiap elemen. Keduanya tidak digabung sebagai satu metrik maksimum sistem.

Hasil ini menjadi baseline numerik untuk konfigurasi baru. Belum ada pasangan baseline–reinforcement yang setara, pemeriksaan kapasitas komposit, buckling, atau konvergensi mesh; tidak ditetapkan PASS keamanan atau klaim keberhasilan reinforcement.

## Provenance

Seluruh angka FE berasal dari output native Karamba pada GH. Viewer hanya menampilkan geometri, nilai tegangan dan perpindahan tersimpan. Raw data dan GH hasil disimpan terpisah dengan RunID baru. Tidak ada hasil lama ditimpa.