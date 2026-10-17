# Studi jarak boundary — native Karamba

N29, shift14, 55panel; baseline tanpa reinforcement. G, empat lateral 1kN dan empat kombinasi G+lateral. InitialStrain OFF.

| Gap m | CFRP winding kg | Panjang m | Shell MPa | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|---:|---:|
| 0.2 | 155.590 | 4891.450 | 11.3046 | 53.6752 | 6.3621 | 9.7360 |
| 0.4 | 161.735 | 5084.634 | 9.9181 | 32.0583 | 5.6246 | 10.7602 |
| 0.6 | 170.112 | 5347.976 | 7.8753 | 26.3717 | 5.4058 | 11.1735 |

Jumlah beam boundary dapat berubah mengikuti pembagian garis hasil offset, dengan aturan dan toleransi yang sama. Mesh shell tetap 25.520 segitiga pada seluruh gap. Koordinat tumpuan B mengikuti offset; kesamaan berlaku pada aturan tumpuan, bukan koordinat B.

## Kesetaraan input

- configuration_except_gap: True
- main_loft_unchanged: True
- boundary_A_identical: True
- lateral_locations_identical: True
- lateral_total_1kN: True
- materials_and_sections_fixed: True
- same_shell_mesh_rule_and_counts: True
- same_ground_support_rule: True
- initial_strain_OFF: True
- native_displacement_superposition: True
- native_analysis_and_reactions: True

## Kesimpulan

Pada tiga jarak yang diuji, maksimum shell terendah ada pada gap 0.6 m (7.875 MPa), sedangkan tertinggi pada 0.2 m (11.305 MPa).
Pada lateral saja dengan gaya total yang sama, maksimum perpindahan turun 3.943 -> 2.191 -> 1.720 mm untuk gap 0,2 -> 0,4 -> 0,6 m; maksimum shell lateral juga turun 10.296 -> 7.802 -> 6.118 MPa. Respons lateral membaik pada rentang uji ini.
Pada gravitasi saja, perpindahan maksimum justru naik 8.383 -> 10.241 -> 10.863 mm. Karena geometri dan berat sendiri berubah bersama gap, tren gravitasi dan lateral perlu dibaca terpisah.
Perpindahan maksimum terendah ada pada gap 0.2 m (9.736 mm). Penilaian tegangan dan kekakuan harus dibaca bersama, bukan hanya satu angka shell.
Gap mengubah kedalaman geometri A/B, panjang dan arah winding, serta berat sendiri. Koordinat tumpuan B mengikuti offset dengan aturan Z=0 yang sama. Ini menilai usulan aktual; massa tidak disamakan antar gap.
Kesimpulan hanya berlaku untuk N29, shift 14, 55 panel dan beban konseptual yang diuji. Tiga titik uji belum membuktikan gap optimum atau kapasitas aman. Shell dan beam tetap memiliki definisi tegangan berbeda.
Jumlah node tumpuan adalah 141 / 141 / 140 untuk gap 0,2 / 0,4 / 0,6 m. Semua memakai aturan dukungan garis Z=0 yang sama; jumlah node serta posisi pada boundary B mengikuti offset. Ini bukan uji dengan koordinat tumpuan B atau jumlah beam yang dipaksakan identik.

## H020

| Kasus | Shell MPa | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|
| G | 4.6294 | 18.6390 | 3.0151 | 8.3833 |
| G_X_POS | 7.0556 | 22.3524 | 3.4707 | 8.8303 |
| G_X_NEG | 7.5621 | 28.4962 | 4.1784 | 8.4564 |
| G_Y_POS | 11.3046 | 53.0651 | 6.3372 | 9.5414 |
| G_Y_NEG | 9.8857 | 53.6752 | 6.3621 | 9.7360 |
| L_X_POS | 6.6362 | 18.2182 | 3.4342 | 2.1831 |
| L_X_NEG | 6.6362 | 18.2182 | 3.4342 | 2.1831 |
| L_Y_POS | 10.2964 | 53.0493 | 5.7073 | 3.9435 |
| L_Y_NEG | 10.2964 | 53.0493 | 5.7073 | 3.9435 |

shell hotspot G_Y_POS: {"shell_id":"NG_P007_F0","coordinate_m":[0.476369920806035,1.007814738020973,0.2846795063628457],"component":"s2","signed_value_MPa":-11.304579710909028,"element_index":9593,"face_index":237,"value_MPa":11.304579710909028,"surface":1}

boundary hotspot G_Y_NEG: {"coordinate_m":[3.407754313200652,7.19879296175319,0],"original_id":"NG_EDGE_P053_B_S038","normal_stress_extreme_index":1,"signed_value_MPa":53.67524029067663,"beam_id":"NG_EDGE_P053_B_S038","element_index":6189,"value_MPa":53.67524029067663,"station":1}

aluminium_link hotspot G_Y_NEG: {"coordinate_m":[3.370882601278691,7.183018797796183,0.024913166031118445],"original_id":"NG_LINK_P053_V045","normal_stress_extreme_index":1,"signed_value_MPa":6.362149607845111,"beam_id":"NG_LINK_P053_V045","element_index":9457,"value_MPa":6.362149607845111,"station":0}

displacement hotspot G_Y_NEG: {"translation_mm":[-2.1490817900238093,-1.425610762165038,-9.38817487532224],"coordinate_m":[-0.08509088781616793,5.880298193059753,3.1256261186856467],"node_index":3247,"value_mm":9.735951215728461}

## H040

| Kasus | Shell MPa | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|
| G | 4.3001 | 19.4248 | 2.9997 | 10.2410 |
| G_X_POS | 6.8658 | 20.0754 | 4.1872 | 10.5914 |
| G_X_NEG | 5.6548 | 25.8542 | 3.6808 | 9.9113 |
| G_Y_POS | 9.9181 | 32.0583 | 5.3336 | 10.7602 |
| G_Y_NEG | 7.0625 | 24.5007 | 5.6246 | 9.7947 |
| L_X_POS | 6.2483 | 17.3557 | 3.1835 | 0.8909 |
| L_X_NEG | 6.2483 | 17.3557 | 3.1835 | 0.8909 |
| L_Y_POS | 7.8023 | 24.8272 | 3.8230 | 2.1913 |
| L_Y_NEG | 7.8023 | 24.8272 | 3.8230 | 2.1913 |

shell hotspot G_Y_POS: {"shell_id":"NG_P053_F0","coordinate_m":[3.130493900908084,7.096185334206858,0.30726744257862476],"component":"s2","signed_value_MPa":-9.918051669930632,"element_index":9636,"face_index":355,"value_MPa":9.918051669930632,"surface":1}

boundary hotspot G_Y_POS: {"coordinate_m":[2.084472496043738,5.849126469764234,1.5374451507097562],"original_id":"NG_EDGE_P047_A_S047","normal_stress_extreme_index":0,"signed_value_MPa":-32.058282877865686,"beam_id":"NG_EDGE_P047_A_S047","element_index":5471,"value_MPa":32.058282877865686,"station":0}

aluminium_link hotspot G_Y_NEG: {"coordinate_m":[3.459397574111842,7.007848983901629,0.030121365073569297],"original_id":"NG_LINK_P053_V018","normal_stress_extreme_index":0,"signed_value_MPa":-5.624566946268031,"beam_id":"NG_LINK_P053_V018","element_index":9427,"value_MPa":5.624566946268031,"station":0}

displacement hotspot G_Y_POS: {"translation_mm":[1.0057516126303254,4.061551829840284,-9.91332876414993],"coordinate_m":[8.94523767904586,3.214634942849409,3.941626189221102],"node_index":17915,"value_mm":10.760196408937425}

## H060

| Kasus | Shell MPa | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|
| G | 4.7138 | 15.7841 | 2.5802 | 10.8635 |
| G_X_POS | 6.5852 | 17.5379 | 4.4287 | 11.1735 |
| G_X_NEG | 5.1519 | 24.2938 | 3.5307 | 10.5674 |
| G_Y_POS | 7.8753 | 26.3717 | 5.4058 | 11.0513 |
| G_Y_NEG | 5.7516 | 25.6241 | 4.8300 | 10.7145 |
| L_X_POS | 5.6803 | 17.4624 | 3.2276 | 0.8297 |
| L_X_NEG | 5.6803 | 17.4624 | 3.2276 | 0.8297 |
| L_Y_POS | 6.1180 | 19.0249 | 3.1348 | 1.7199 |
| L_Y_NEG | 6.1180 | 19.0249 | 3.1348 | 1.7199 |

shell hotspot G_Y_POS: {"element_index":9637,"shell_id":"NG_P053_F0","face_index":343,"surface":-1,"component":"s2","coordinate_m":[2.5744615255319743,6.452742334156611,0.9940845598799672],"value_MPa":7.875342813312346,"signed_value_MPa":-7.875342813312346}

boundary hotspot G_Y_POS: {"beam_id":"NG_EDGE_P047_A_S002","original_id":"NG_EDGE_P047_A_S002","element_index":5427,"station":1,"coordinate_m":[3.5278661984196296,6.391959984831006,1.1347296654587558],"normal_stress_extreme_index":0,"value_MPa":26.371712297710697,"signed_value_MPa":-26.371712297710697}

aluminium_link hotspot G_Y_POS: {"beam_id":"NG_LINK_P052_V032","original_id":"NG_LINK_P052_V032","element_index":9384,"station":0,"coordinate_m":[5.291740806291751,6.138674540483968,1.2344097098068763],"normal_stress_extreme_index":0,"value_MPa":5.405813748930623,"signed_value_MPa":-5.405813748930623}

displacement hotspot G_X_POS: {"value_mm":11.173470824059534,"coordinate_m":[8.943314093463027,3.2364983373733414,4.0371790278847],"node_index":17913,"translation_mm":[2.303591785907011,3.318167699646911,-10.417757832519976]}

## Riwayat yang dikecualikan

Input H040 V1 menggunakan total lateral 91/62kN. Pemeriksaan reaksi menghentikan ekspor; hasil tidak dipakai untuk perbandingan. Salinan dan log asli dipertahankan. Input V2 diaudit native sebelum Analyze dan total lateral 1kN terverifikasi pada semua kasus.

Tidak ada PASS keamanan struktur atau pemeriksaan kapasitas kontak baut, buckling, dan konvergensi mesh.