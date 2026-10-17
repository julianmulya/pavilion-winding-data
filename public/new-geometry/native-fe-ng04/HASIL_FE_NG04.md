# Hasil native Karamba NG04

Anchor 25, shift 6, gap 0,4 m, 36 panel. G = gravitasi; L = lateral konseptual total 1 kN. G_X/Y = gravitasi ditambah lateral. Input struktur mengikuti NG03; InitialStrain OFF.

| Kasus | Shell MPa | Boundary CFRP MPa | Link Al MPa | Perpindahan mm |
|---|---:|---:|---:|---:|
| G | 2.081 | 10.583 | 1.671 | 2.457 |
| G_X_POS | 3.957 | 12.511 | 2.943 | 2.622 |
| G_X_NEG | 4.503 | 14.988 | 2.704 | 3.929 |
| G_Y_POS | 6.466 | 17.089 | 5.499 | 3.333 |
| G_Y_NEG | 7.096 | 23.802 | 5.728 | 5.200 |
| L_X_POS | 4.230 | 6.548 | 2.367 | 1.995 |
| L_X_NEG | 4.230 | 6.548 | 2.367 | 1.995 |
| L_Y_POS | 6.680 | 16.776 | 5.493 | 3.377 |
| L_Y_NEG | 6.680 | 16.776 | 5.493 | 3.377 |

Analyze sembilan kasus selesai tanpa error/warning. Residual gaya maksimum 9.928211627600238e-11 kN.

Seluruh kasus G dan G+lateral cocok dengan run NG03: selisih maksimum angka pembanding 0. Pemeriksaan superposisi vektor perpindahan pada semua node: kesalahan maksimum 1.5349892580965308e-12 m. Maksimum tegangan pada lokasi berbeda tidak dijumlahkan.

Boundary tetap CFRP ekuivalen D10 dengan link sleeve aluminium lokal. Model sambungan terikat sempurna. Hasil berupa analisis global konseptual, belum penilaian kapasitas atau angin desain.

Hotspot setiap kategori dan kasus tersedia dalam REVIEW_COMPLETE.json serta raw output native terpisah.