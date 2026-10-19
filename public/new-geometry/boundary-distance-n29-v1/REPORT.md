# Studi jarak boundary — native Karamba

N29, shift14, 55panel; baseline tanpa reinforcement. G, empat lateral 1kN dan empat kombinasi G+lateral. InitialStrain OFF.

| Gap m | CFRP winding kg | Panjang m | Shell MPa | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|---:|---:|
| 0.1 | 153.443 | 4823.932 | 13.0213 | 107.4893 | 7.7042 | 12.2781 |
| 0.2 | 155.590 | 4891.450 | 11.3046 | 53.6752 | 6.3621 | 9.7360 |
| 0.3 | 158.368 | 4978.787 | 11.8719 | 36.8206 | 6.1913 | 10.5083 |
| 0.4 | 161.735 | 5084.634 | 9.9181 | 32.0583 | 5.6246 | 10.7602 |
| 0.5 | 165.666 | 5208.198 | 7.2363 | 28.5488 | 5.3648 | 10.8768 |
| 0.6 | 170.112 | 5347.976 | 7.8753 | 26.3717 | 5.4058 | 11.1735 |
| 0.7 | 175.031 | 5502.633 | 7.2464 | 26.0175 | 5.3957 | 11.2893 |
| 0.8 | 180.376 | 5670.662 | 6.3444 | 25.4736 | 5.3619 | 11.2688 |
| 0.9 | 186.110 | 5850.916 | 6.3023 | 25.3552 | 5.3669 | 11.4084 |
| 1.0 | 192.200 | 6042.384 | 6.1909 | 24.9547 | 5.4013 | 11.5489 |

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

Dari 10 jarak yang telah ditinjau, maksimum shell terendah ada pada 1.0 m (6.1909 MPa).
Maksimum perpindahan terendah ada pada 0.2 m (9.7360 mm).
Kandidat Pareto untuk shell, perpindahan, dan massa winding: [0.1, 0.2, 0.4, 0.5, 0.8, 0.9, 1.0] m. Tidak ada bobot atau ambang kinerja yang diasumsikan untuk memilih satu kompromi.
Pilihan hanya berlaku untuk N29/shift14/55 panel, sembilan kasus konseptual. Posisi dan jumlah node tumpuan B mengikuti gap; berat sendiri aktual berubah. Shell dan beam dilaporkan terpisah. Tidak ada penilaian kapasitas aman.

## H010

| Kasus | Shell MPa | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|
| G | 5.5362 | 23.0850 | 2.8288 | 7.7718 |
| G_X_POS | 7.0968 | 31.7373 | 3.1650 | 8.6337 |
| G_X_NEG | 9.6023 | 38.8482 | 5.1390 | 8.7661 |
| G_Y_POS | 13.0213 | 74.9504 | 6.1222 | 11.0273 |
| G_Y_NEG | 12.7266 | 107.4893 | 7.7042 | 12.2781 |
| L_X_POS | 6.8876 | 24.9953 | 3.4586 | 3.8735 |
| L_X_NEG | 6.8876 | 24.9953 | 3.4586 | 3.8735 |
| L_Y_POS | 11.6683 | 91.0492 | 6.3692 | 8.8993 |
| L_Y_NEG | 11.6683 | 91.0492 | 6.3692 | 8.8993 |

shell hotspot G_Y_POS: {"element_index":9594,"shell_id":"NG_P007_F0","face_index":237,"surface":1,"component":"s2","coordinate_m":[0.4972121785711128,1.069491962417919,0.2846685004402129],"value_MPa":13.021301735801497,"signed_value_MPa":-13.021301735801497}

boundary hotspot G_Y_NEG: {"beam_id":"NG_EDGE_P053_B_S039","original_id":"NG_EDGE_P053_B_S039","element_index":6190,"station":1,"coordinate_m":[3.4332902708524737,7.111901844611944,0],"normal_stress_extreme_index":1,"value_MPa":107.48927576348915,"signed_value_MPa":107.48927576348915}

aluminium_link hotspot G_Y_NEG: {"beam_id":"NG_LINK_P053_V045","original_id":"NG_LINK_P053_V045","element_index":9458,"station":0,"coordinate_m":[3.3471823676897596,7.078711104922362,0.05208577498085315],"normal_stress_extreme_index":1,"value_MPa":7.704242210014769,"signed_value_MPa":7.704242210014769}

displacement hotspot G_Y_NEG: {"value_mm":12.278099661748005,"coordinate_m":[2.0680493738651826,6.586709352076314,0.82521702825103],"node_index":27802,"translation_mm":[-0.4598419373323516,-9.974544464740436,-7.144840055410816]}

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

## H030

| Kasus | Shell MPa | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|
| G | 4.5139 | 26.7819 | 3.0587 | 9.6485 |
| G_X_POS | 6.5082 | 25.8941 | 3.9241 | 10.0446 |
| G_X_NEG | 6.4016 | 27.6738 | 3.6744 | 9.2843 |
| G_Y_POS | 11.8719 | 36.8206 | 6.1913 | 10.5083 |
| G_Y_NEG | 8.3400 | 29.4901 | 5.7153 | 8.8862 |
| L_X_POS | 6.3815 | 16.3089 | 3.1140 | 1.2438 |
| L_X_NEG | 6.3815 | 16.3089 | 3.1140 | 1.2438 |
| L_Y_POS | 10.1026 | 28.5278 | 5.1160 | 2.6712 |
| L_Y_NEG | 10.1026 | 28.5278 | 5.1160 | 2.6712 |

shell hotspot G_Y_POS: {"element_index":9639,"shell_id":"NG_P053_F0","face_index":353,"surface":1,"component":"s2","coordinate_m":[3.159283959872681,7.041023458842578,0.2700865291342666],"value_MPa":11.871935006884478,"signed_value_MPa":-11.871935006884478}

boundary hotspot G_Y_POS: {"beam_id":"NG_EDGE_P047_A_S047","original_id":"NG_EDGE_P047_A_S047","element_index":5474,"station":0,"coordinate_m":[2.084472496043738,5.849126469764234,1.5374451507097562],"normal_stress_extreme_index":0,"value_MPa":36.820617491625875,"signed_value_MPa":-36.820617491625875}

aluminium_link hotspot G_Y_POS: {"beam_id":"NG_LINK_P052_V019","original_id":"NG_LINK_P052_V019","element_index":9373,"station":0,"coordinate_m":[3.389510426781202,6.666092126422293,1.2172498879389442],"normal_stress_extreme_index":1,"value_MPa":6.191308290284915,"signed_value_MPa":6.191308290284915}

displacement hotspot G_Y_POS: {"value_mm":10.508301337786063,"coordinate_m":[8.945446632811851,3.212824975456238,3.8969707408319705],"node_index":17915,"translation_mm":[0.5795908511948624,4.053224556309025,-9.677801514138483]}

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

## H050

| Kasus | Shell MPa | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|
| G | 4.5206 | 16.8417 | 2.7919 | 10.5545 |
| G_X_POS | 6.8267 | 17.5550 | 4.3561 | 10.8768 |
| G_X_NEG | 5.2087 | 25.2702 | 3.5880 | 10.2485 |
| G_Y_POS | 7.2363 | 28.5488 | 5.3648 | 10.8740 |
| G_Y_NEG | 5.9189 | 25.3990 | 5.2638 | 10.2901 |
| L_X_POS | 5.9560 | 17.7077 | 3.2097 | 0.8116 |
| L_X_NEG | 5.9560 | 17.7077 | 3.2097 | 0.8116 |
| L_Y_POS | 5.6379 | 20.4932 | 3.2152 | 1.7995 |
| L_Y_NEG | 5.6379 | 20.4932 | 3.2152 | 1.7995 |

shell hotspot G_Y_POS: {"element_index":9636,"shell_id":"NG_P053_F0","face_index":355,"surface":1,"component":"s2","coordinate_m":[3.1095911680561272,7.149683813345701,0.34865569396714763],"value_MPa":7.236348676972569,"signed_value_MPa":-7.236348676972569}

boundary hotspot G_Y_POS: {"beam_id":"NG_EDGE_P047_A_S047","original_id":"NG_EDGE_P047_A_S047","element_index":5471,"station":0,"coordinate_m":[2.084472496043738,5.849126469764234,1.5374451507097562],"normal_stress_extreme_index":0,"value_MPa":28.548767863713586,"signed_value_MPa":-28.548767863713586}

aluminium_link hotspot G_Y_POS: {"beam_id":"NG_LINK_P052_V032","original_id":"NG_LINK_P052_V032","element_index":9383,"station":0,"coordinate_m":[5.291740806291751,6.138674540483968,1.2344097098068763],"normal_stress_extreme_index":0,"value_MPa":5.364816142992628,"signed_value_MPa":-5.364816142992628}

displacement hotspot G_X_POS: {"value_mm":10.876777063650103,"coordinate_m":[8.943613251998247,3.2351753501731997,3.9924793574191892],"node_index":17913,"translation_mm":[1.8012653678847443,3.136664684000212,-10.257731573157384]}

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

## H070

| Kasus | Shell MPa | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|
| G | 4.7896 | 13.0908 | 2.5367 | 11.0085 |
| G_X_POS | 6.3947 | 17.3929 | 4.4819 | 11.2893 |
| G_X_NEG | 5.0538 | 23.1841 | 3.5635 | 10.7402 |
| G_Y_POS | 7.2464 | 26.0175 | 5.3957 | 11.0959 |
| G_Y_NEG | 5.8064 | 25.5068 | 4.6019 | 10.9529 |
| L_X_POS | 5.4814 | 17.0422 | 3.2817 | 0.8626 |
| L_X_NEG | 5.4814 | 17.0422 | 3.2817 | 0.8626 |
| L_Y_POS | 5.5547 | 17.3355 | 3.0387 | 1.8041 |
| L_Y_NEG | 5.5547 | 17.3355 | 3.0387 | 1.8041 |

shell hotspot G_Y_POS: {"element_index":9639,"shell_id":"NG_P053_F0","face_index":343,"surface":-1,"component":"s2","coordinate_m":[2.5701694935442405,6.480548104732416,0.9981746491691069],"value_MPa":7.246409836091513,"signed_value_MPa":-7.246409836091513}

boundary hotspot G_Y_POS: {"beam_id":"NG_EDGE_P047_A_S002","original_id":"NG_EDGE_P047_A_S002","element_index":5428,"station":1,"coordinate_m":[3.5278661984196296,6.391959984831006,1.1347296654587558],"normal_stress_extreme_index":0,"value_MPa":26.01746048225006,"signed_value_MPa":-26.01746048225006}

aluminium_link hotspot G_Y_POS: {"beam_id":"NG_LINK_P052_V032","original_id":"NG_LINK_P052_V032","element_index":9386,"station":0,"coordinate_m":[5.291740806291751,6.138674540483968,1.2344097098068763],"normal_stress_extreme_index":0,"value_MPa":5.3956801569342545,"signed_value_MPa":-5.3956801569342545}

displacement hotspot G_X_POS: {"value_mm":11.289320665937279,"coordinate_m":[8.943111904711007,3.2379857890519066,4.081572333289213],"node_index":17913,"translation_mm":[2.780598130784818,3.4419385192906264,-10.386052876952721]}

## H080

| Kasus | Shell MPa | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|
| G | 4.7809 | 13.8378 | 2.6422 | 11.0103 |
| G_X_POS | 6.2357 | 17.3866 | 4.5105 | 11.2688 |
| G_X_NEG | 5.0365 | 22.0186 | 3.6379 | 10.7636 |
| G_Y_POS | 6.3444 | 25.1856 | 5.3619 | 11.0131 |
| G_Y_NEG | 5.7864 | 25.4736 | 4.6060 | 11.0356 |
| L_X_POS | 5.3383 | 16.5289 | 3.3459 | 0.9054 |
| L_X_NEG | 5.3383 | 16.5289 | 3.3459 | 0.9054 |
| L_Y_POS | 4.3056 | 17.1016 | 2.9396 | 1.8807 |
| L_Y_NEG | 4.3056 | 17.1016 | 2.9396 | 1.8807 |

shell hotspot G_Y_POS: {"element_index":9616,"shell_id":"NG_P029_F0","face_index":64,"surface":-1,"component":"s2","coordinate_m":[9.24954035415387,3.2978649257519614,4.232011189008838],"value_MPa":6.344449110008657,"signed_value_MPa":-6.344449110008657}

boundary hotspot G_Y_NEG: {"beam_id":"NG_EDGE_P051_A_S032","original_id":"NG_EDGE_P051_A_S032","element_index":5919,"station":0,"coordinate_m":[5.496752628394511,6.687960395081754,0],"normal_stress_extreme_index":0,"value_MPa":25.47361338590626,"signed_value_MPa":-25.47361338590626}

aluminium_link hotspot G_Y_POS: {"beam_id":"NG_LINK_P052_V032","original_id":"NG_LINK_P052_V032","element_index":9387,"station":0,"coordinate_m":[5.291740806291751,6.138674540483968,1.2344097098068763],"normal_stress_extreme_index":0,"value_MPa":5.361886910992014,"signed_value_MPa":-5.361886910992014}

displacement hotspot G_X_POS: {"value_mm":11.268838984826093,"coordinate_m":[8.943002090802707,3.2395262457032667,4.125912105031847],"node_index":17913,"translation_mm":[3.216302562361881,3.5255796916046793,-10.208448350823225]}

## H090

| Kasus | Shell MPa | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|
| G | 4.7578 | 14.9145 | 2.7786 | 11.1280 |
| G_X_POS | 6.0443 | 17.1542 | 4.4997 | 11.4084 |
| G_X_NEG | 4.9802 | 21.5927 | 3.7520 | 10.8590 |
| G_Y_POS | 6.3023 | 24.6723 | 5.3669 | 11.1138 |
| G_Y_NEG | 5.7061 | 25.3552 | 4.5477 | 11.1755 |
| L_X_POS | 5.2024 | 15.8900 | 3.3914 | 0.9467 |
| L_X_NEG | 5.2024 | 15.8900 | 3.3914 | 0.9467 |
| L_Y_POS | 3.8479 | 17.0502 | 2.8252 | 1.9630 |
| L_Y_NEG | 3.8479 | 17.0502 | 2.8252 | 1.9630 |

shell hotspot G_Y_POS: {"element_index":9615,"shell_id":"NG_P029_F0","face_index":64,"surface":-1,"component":"s2","coordinate_m":[9.24974518485559,3.299828138972971,4.291115504493572],"value_MPa":6.302330016017833,"signed_value_MPa":-6.302330016017833}

boundary hotspot G_Y_NEG: {"beam_id":"NG_EDGE_P051_A_S032","original_id":"NG_EDGE_P051_A_S032","element_index":5919,"station":0,"coordinate_m":[5.496752628394511,6.687960395081754,0],"normal_stress_extreme_index":0,"value_MPa":25.355204210931266,"signed_value_MPa":-25.355204210931266}

aluminium_link hotspot G_Y_POS: {"beam_id":"NG_LINK_P052_V032","original_id":"NG_LINK_P052_V032","element_index":9386,"station":0,"coordinate_m":[5.291740806291751,6.138674540483968,1.2344097098068763],"normal_stress_extreme_index":0,"value_MPa":5.366913032715172,"signed_value_MPa":-5.366913032715172}

displacement hotspot G_X_POS: {"value_mm":11.40841452856736,"coordinate_m":[8.942900554308542,3.240966454519088,4.170252901964504],"node_index":17913,"translation_mm":[3.6813764639217945,3.654500451841223,-10.160906250625567]}

## H100

| Kasus | Shell MPa | Boundary MPa | Link Al MPa | u mm |
|---|---:|---:|---:|---:|
| G | 4.6822 | 15.7722 | 2.9558 | 11.2353 |
| G_X_POS | 5.9056 | 17.6321 | 4.5185 | 11.5489 |
| G_X_NEG | 5.1384 | 22.5234 | 4.0567 | 10.9330 |
| G_Y_POS | 6.1909 | 24.5367 | 5.4013 | 11.2333 |
| G_Y_NEG | 5.5794 | 24.9547 | 4.3364 | 11.2959 |
| L_X_POS | 5.0424 | 14.9664 | 3.4250 | 0.9904 |
| L_X_NEG | 5.0424 | 14.9664 | 3.4250 | 0.9904 |
| L_Y_POS | 3.5677 | 16.8898 | 2.7183 | 2.0887 |
| L_Y_NEG | 3.5677 | 16.8898 | 2.7183 | 2.0887 |

shell hotspot G_Y_POS: {"element_index":9614,"shell_id":"NG_P029_F0","face_index":64,"surface":-1,"component":"s2","coordinate_m":[9.250060591739393,3.3017724325611666,4.350110420568591],"value_MPa":6.190928491274523,"signed_value_MPa":-6.190928491274523}

boundary hotspot G_Y_NEG: {"beam_id":"NG_EDGE_P051_A_S032","original_id":"NG_EDGE_P051_A_S032","element_index":5918,"station":0,"coordinate_m":[5.496752628394511,6.687960395081754,0],"normal_stress_extreme_index":0,"value_MPa":24.954684917831038,"signed_value_MPa":-24.954684917831038}

aluminium_link hotspot G_Y_POS: {"beam_id":"NG_LINK_P052_V032","original_id":"NG_LINK_P052_V032","element_index":9385,"station":0,"coordinate_m":[5.291740806291751,6.138674540483968,1.2344097098068763],"normal_stress_extreme_index":0,"value_MPa":5.401271170413058,"signed_value_MPa":-5.401271170413058}

displacement hotspot G_X_POS: {"value_mm":11.548859026034515,"coordinate_m":[8.942882285347592,3.2423883109462115,4.214510249848431],"node_index":17913,"translation_mm":[4.135997052947151,3.7748606127322666,-10.100500014141574]}

## Riwayat yang dikecualikan

Input H040 V1 menggunakan total lateral 91/62kN. Pemeriksaan reaksi menghentikan ekspor; hasil tidak dipakai untuk perbandingan. Salinan dan log asli dipertahankan. Input V2 diaudit native sebelum Analyze dan total lateral 1kN terverifikasi pada semua kasus.

Tidak ada PASS keamanan struktur atau pemeriksaan kapasitas kontak baut, buckling, dan konvergensi mesh.