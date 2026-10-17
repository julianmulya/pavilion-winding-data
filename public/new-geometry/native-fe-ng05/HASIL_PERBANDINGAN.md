# Perbandingan reinforcement pavilion NG05

Anchor 25; shift 6; gap 0,4m; 36 panel. G, empat lateral 1kN, dan empat kombinasi. InitialStrain OFF.

| Kandidat | Tambahan CFRP kg | Shell MPa | Penurunan shell | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 0.0000 | 7.0963 | 0.000% | 23.8021 | 5.7281 | 5.2003 |
| Winding ulang | 0.3010 | 6.7154 | 5.367% | 23.7430 | 7.9167 | 5.2320 |
| Anchor baru | 0.5052 | 7.0366 | 0.842% | 23.7882 | 5.4143 | 5.0866 |

## Input dan geometri

Lokasi dipilih sebelum solve kandidat dari hotspot native baseline pada G (P024), G-X (P033), G-Y (P034). Winding ulang menambah satu pass pada dua transfer paling tinggi di setiap panel tersebut. Shell F1 berbagi node dengan ribbon asli sebagai lapisan terikat sempurna.

Anchor baru menggunakan node tengah jalur kritis dekat hotspot; bukan tepat koordinat centroid tegangan. Winding segitiga tertutup menghubungkan node itu ke dua kontak anchor boundary A dan B dengan luas segitiga terbesar dalam panel. Sambungan berbagi DOF pada titik tersebut, tanpa support baru. Ini model global ekuivalen; kekuatan ikatan, slip dan kontak baut belum dinilai.

Seluruh node dan muka shell asli serta koordinat tumpuan diverifikasi sama. Penampang boundary CFRP dan link aluminium diteruskan. Perbedaan hanya shell tambahan dan berat sendiri tambahan termasuk lilitan lokal.

Kedua kandidat memakai jumlah material berbeda. Perbandingan ini menilai dua usulan aktual beserta kebutuhan materialnya; belum merupakan uji topologi dengan anggaran CFRP yang identik. Massa hardware anchor virtual tidak dimodelkan.

## Review per kasus

### REPEAT

| Kasus | Shell MPa | Perubahan shell % turun | u mm | Perubahan u % turun |
|---|---:|---:|---:|---:|
| G | 2.0575 | 1.108 | 2.7804 | -13.164 |
| G_X_POS | 3.2227 | 18.558 | 2.9332 | -11.887 |
| G_X_NEG | 4.3274 | 3.896 | 4.3362 | -10.351 |
| G_Y_POS | 6.2316 | 3.617 | 3.3141 | 0.575 |
| G_Y_NEG | 6.7154 | 5.367 | 5.2320 | -0.610 |
| L_X_POS | 3.3121 | 21.698 | 1.9574 | 1.881 |
| L_X_NEG | 3.3121 | 21.698 | 1.9574 | 1.881 |
| L_Y_POS | 6.4735 | 3.096 | 3.2252 | 4.492 |
| L_Y_NEG | 6.4735 | 3.096 | 3.2252 | 4.492 |

Nilai negatif berarti kenaikan.

shell maksimum: G_Y_NEG; {"shell_id":"NG_P033_F0","coordinate_m":[3.718420518151975,6.8145766354495345,0.5344252769835484],"component":"s2","signed_value_MPa":-6.715412143064878,"element_index":5414,"face_index":213,"value_MPa":6.715412143064878,"surface":-1}
boundary maksimum: G_Y_NEG; {"coordinate_m":[6.794609056073185,6.257267842067581,1.6760538079641243],"original_id":"NG_EDGE_P032_A_S036","normal_stress_extreme_index":0,"signed_value_MPa":-23.742994143480594,"beam_id":"NG_EDGE_P032_A_S036","element_index":3169,"value_MPa":23.742994143480594,"station":1}
link maksimum: G_Y_POS; {"coordinate_m":[3.455598291429081,6.212022219125815,1.385054252456386],"original_id":"NG_LINK_P034_V026","normal_stress_extreme_index":0,"signed_value_MPa":-7.916699743682334,"beam_id":"NG_LINK_P034_V026","element_index":5256,"value_MPa":7.916699743682334,"station":0}
displacement maksimum: G_Y_NEG; {"translation_mm":[-0.09058552675977379,-4.115401427605923,-3.229345996653919],"coordinate_m":[3.819994091551346,6.7904190441763435,0.5937697313587234],"node_index":15013,"value_mm":5.231960456091379}

Residual gaya maksimum: 7.428206101837855e-11 kN.

### NEW_ANCHOR

| Kasus | Shell MPa | Perubahan shell % turun | u mm | Perubahan u % turun |
|---|---:|---:|---:|---:|
| G | 2.0044 | 3.661 | 2.9620 | -20.553 |
| G_X_POS | 3.7787 | 4.505 | 2.5009 | 4.606 |
| G_X_NEG | 4.4912 | 0.260 | 3.9768 | -1.204 |
| G_Y_POS | 6.0885 | 5.832 | 3.3218 | 0.342 |
| G_Y_NEG | 7.0366 | 0.842 | 5.0866 | 2.186 |
| L_X_POS | 4.1202 | 2.595 | 1.7145 | 14.059 |
| L_X_NEG | 4.1202 | 2.595 | 1.7145 | 14.059 |
| L_Y_POS | 6.2387 | 6.610 | 2.8241 | 16.370 |
| L_Y_NEG | 6.2387 | 6.610 | 2.8241 | 16.370 |

Nilai negatif berarti kenaikan.

shell maksimum: G_Y_NEG; {"shell_id":"NG_P034_F0","coordinate_m":[2.6749715568003167,6.865243194899532,0.6272116236139045],"component":"s2","signed_value_MPa":-7.036561862301513,"element_index":5416,"face_index":130,"value_MPa":7.036561862301513,"surface":1}
boundary maksimum: G_Y_NEG; {"coordinate_m":[6.794609056073185,6.257267842067581,1.6760538079641243],"original_id":"NG_EDGE_P032_A_S036","normal_stress_extreme_index":0,"signed_value_MPa":-23.78820778003905,"beam_id":"NG_EDGE_P032_A_S036","element_index":3169,"value_MPa":23.78820778003905,"station":1}
link maksimum: G_Y_NEG; {"coordinate_m":[2.277505019158033,6.803167914865681,0.9124906551320047],"original_id":"NG_LINK_P034_V017","normal_stress_extreme_index":1,"signed_value_MPa":5.414321175331029,"beam_id":"NG_LINK_P034_V017","element_index":5247,"value_MPa":5.414321175331029,"station":0}
displacement maksimum: G_Y_NEG; {"translation_mm":[-0.08670433541432092,-4.004704799090658,-3.134953254634083],"coordinate_m":[3.819994091551346,6.7904190441763435,0.5937697313587234],"node_index":15013,"value_mm":5.086561714791261}

Residual gaya maksimum: 6.772509226526968e-11 kN.

## Keputusan

Angka merupakan native Karamba. Penurunan envelope shell dilaporkan sebagai hasil numerik. Peningkatan pada kategori/kasus lain tetap ditampilkan. Tidak ditetapkan PASS keamanan struktur; tidak ada satu maksimum sistem yang menggabungkan tegangan utama shell dengan tegangan normal beam.