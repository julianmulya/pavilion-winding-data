# Studi pengaruh jumlah anchor dan shift pada pavilion CFRP

## Pertanyaan dan ruang lingkup
Bagaimana anchor dan shift mengubah visual openness, kebutuhan material winding, dan respons struktur pada jumlah panel yang sama?

Dataset: 500 baseline native Karamba / 4.500 kasus. Jarak boundary 1,0 m; bentuk loft asal tetap; N10–14, shift 5–7 (9 pasangan tersedia). Tidak ada Analyze baru atau reinforcement dalam studi ini. Ini studi ulang dataset, bukan eksperimen faktorial lengkap atau bukti kapasitas aman.

## Variabel dan metode
Anchor N adalah jumlah tersedia pada masing-masing boundary A dan B. Shift mengikuti persis generator web: indeks berikut = (indeks + shift + 1) mod N, berganti A/B tiap transfer. Satu siklus berhenti ketika indeks dan layer kembali ke awal. Jumlah transfer/anchor yang dikunjungi L = lcm(2, N/gcd(N,shift+1)); tersedia 2N anchor per panel. Satu orbit saja digunakan, tidak otomatis memulai orbit lain yang belum dikunjungi.

Semua 500 hasil diikat ke hash review native. Perhitungan geometri TypeScript yang sudah ada dicocokkan terhadap koordinat A/B, urutan sleeve contact, panjang dan massa native sebelum openness dihitung. Openness: proyeksi prisma ribbon ke bidang Newell polygon B, union area overlap, rata-rata berbobot luas seluruh panel. Basis 128/256/512 scanlines; hasil 512. Local wraps dan hardware tidak masuk footprint; massa winding memasukkan transfer + satu putaran analitik per sleeve yang dikunjungi, tanpa waste, boundary, pin/bolt atau fondasi.

Efisiensi material disajikan sebagai massa winding (kg), panjang (m), dan kg/m² luas proyeksi panel. Massa kecil tidak otomatis efisien: harus dibaca bersama keterbukaan, tegangan, deformasi dan cakupan orbit. Frontier Pareto hanya membandingkan konfigurasi dengan P yang sama pada tiga objektif: openness maksimum, massa winding minimum, tegangan shell minimum; tidak merupakan penilaian keselamatan.

## Kontrol FE
Boundary memakai ekuivalen beam CFRP D10, sleeve/link lokal aluminium OD12/ID6,6; bukan rangka aluminium kontinu. Ribbon lebar20 mm, tebal ekuivalen0,981747704 mm, densitas1620 kg/m³. Mesh8 segitiga per transfer; InitialStrain OFF. Kontak perfect-bonded/shared DOF; tidak ada slip, kapasitas baut, pretension atau contact lokal. Tumpuan translasiXYZ terkunci di node sepanjang seluruh tepiZ0, rotasi bebas.

Sembilan kasus: G; lateral sendiri ±X/±Y dengan total1 kN per arah; G ditambah masing-masing lateral. Ini lateral konseptual, bukan angin berbasis lokasi. Metrik envelope adalah maksimum tiap kategori dari sembilan kasus; maksimum masing-masing kategori tidak harus berada di kasus atau elemen yang sama.

## Perbandingan terkendali pada 39 panel
| Pasangan | Dikunjungi/tersedia | Openness % | Massa winding kg | Shell MPa | Boundary MPa | Link Al MPa | Deformasi mm |
|---|---:|---:|---:|---:|---:|---:|---:|
|N10/S5|10/20|84.042|25.976|17.121|76.744|11.432|29.890|
|N11/S5|22/22|72.923|58.272|9.767|48.515|6.812|14.693|
|N12/S5|2/24|93.343|5.672|64.589|1127.196|130.135|1138.028|
|N12/S6|12/24|81.762|31.140|20.052|87.283|16.216|21.713|
|N13/S5|26/26|69.941|68.927|8.488|40.003|6.219|13.783|
|N13/S6|26/26|69.941|68.927|8.488|40.003|6.219|13.783|
|N14/S5|14/28|79.962|36.808|13.508|54.133|12.763|13.197|
|N14/S6|2/28|93.343|5.672|65.875|751.953|136.722|1132.699|
|N14/S7|14/28|79.962|36.808|13.508|54.133|12.763|13.197|

## Analisis pasangan lintas jumlah panel
Setiap efek dihitung hanya pada P yang ada pada kedua pasangan. Delta adalah B terhadap A. Openness menggunakan poin persentase, metrik lain persen relatif. Median adalah ringkasan pasangan, bukan efek kausal murni atau rata-rata seluruh500 yang mencampur P.

- N10_S05 → N11_S05, 64 pasangan P: Δ openness -13.248 pp; massa +123.72%; shell -40.73%; boundary -51.42%; link -36.07%; u -51.10%.
- N10_S05 → N12_S05, 62 pasangan P: Δ openness +11.789 pp; massa -78.80%; shell +171.75%; boundary +635.16%; link +375.80%; u +4623.37%.
- N10_S05 → N13_S05, 60 pasangan P: Δ openness -16.789 pp; massa +164.71%; shell -48.90%; boundary -54.54%; link -46.35%; u -54.52%.
- N10_S05 → N14_S05, 64 pasangan P: Δ openness -5.004 pp; massa +41.50%; shell -20.86%; boundary -43.88%; link -6.46%; u -36.63%.
- N11_S05 → N12_S05, 63 pasangan P: Δ openness +24.978 pp; massa -90.52%; shell +404.52%; boundary +1374.11%; link +719.52%; u +10449.98%.
- N11_S05 → N13_S05, 61 pasangan P: Δ openness -3.510 pp; massa +18.30%; shell -13.73%; boundary -4.87%; link -16.74%; u -5.70%.
- N11_S05 → N14_S05, 65 pasangan P: Δ openness +8.230 pp; massa -36.74%; shell +51.43%; boundary +20.48%; link +37.26%; u +39.33%.
- N12_S05 → N12_S06, 63 pasangan P: Δ openness -14.627 pp; massa +465.70%; shell -57.44%; boundary -88.53%; link -73.25%; u -97.98%.
- N12_S05 → N13_S05, 59 pasangan P: Δ openness -28.565 pp; massa +1147.82%; shell -83.04%; boundary -93.44%; link -90.97%; u -99.06%.
- N12_S05 → N14_S05, 63 pasangan P: Δ openness -16.749 pp; massa +567.67%; shell -72.46%; boundary -91.71%; link -79.45%; u -98.64%.
- N12_S06 → N13_S06, 64 pasangan P: Δ openness -13.841 pp; massa +120.70%; shell -56.40%; boundary -41.80%; link -62.29%; u -57.65%.
- N12_S06 → N14_S06, 33 pasangan P: Δ openness +13.198 pp; massa -82.23%; shell +166.31%; boundary +827.73%; link +433.33%; u +5136.60%.
- N13_S05 → N13_S06, 60 pasangan P: Δ openness +0.000 pp; massa +0.00%; shell -0.00%; boundary +0.00%; link +0.00%; u +0.00%.
- N13_S05 → N14_S05, 61 pasangan P: Δ openness +11.728 pp; massa -46.52%; shell +66.26%; boundary +27.94%; link +72.33%; u +56.55%.
- N13_S06 → N14_S06, 32 pasangan P: Δ openness +26.304 pp; massa -91.96%; shell +548.06%; boundary +1661.34%; link +1340.68%; u +9350.05%.
- N14_S05 → N14_S06, 33 pasangan P: Δ openness +15.201 pp; massa -84.96%; shell +321.80%; boundary +1278.48%; link +715.42%; u +8148.29%.
- N14_S05 → N14_S07, 20 pasangan P: Δ openness +0.000 pp; massa +0.00%; shell -0.00%; boundary -0.00%; link -0.00%; u -0.00%.
- N14_S06 → N14_S07, 19 pasangan P: Δ openness -14.275 pp; massa +555.12%; shell -78.17%; boundary -93.04%; link -90.84%; u -98.79%.

## Temuan dan interpretasi
1. Pengaruh anchor dan shift tidak monoton. Kombinasi N dan step menentukan orbit aktif. N12/S5 dan N14/S6 hanya mengunjungi dua anchor, mengulang segmen yang sama bolak-balik. Keterbukaan besar dan massa rendah pada orbit ini berasal dari winding yang sangat terbatas, bukan bukti rancangan paling efisien. Pada P39 deformasinya melampaui1.100 mm; respons linear ini memerlukan verifikasi nonlinear sebelum interpretasi fisik lanjut.
2. N13/S5 dan N13/S6 menghasilkan jejak winding geometris sama dengan arah urutan berlawanan. Massa, openness dan respons native nyaris identik. N14/S5 dan N14/S7 juga merupakan pasangan balik arah. Nilai shift berbeda tidak selalu berarti geometri winding berbeda.
3. Pada P39 N13/S5–S6 memberi tegangan winding terendah dari9 pasangan, sedangkan N14/S5–S7 memberi deformasi terendah. N11/S5 adalah alternatif lebih ringan dengan semua22 anchor aktif, dengan openness lebih tinggi dan tegangan/deformasi lebih tinggi daripada N13. Tidak ada satu pemenang untuk seluruh objektif.
4. Jumlah node tumpuan dan segmen boundary berubah menurut N meski aturan tumpuannya sama. N12/S5 dan N14/S6 bahkan memiliki winding, massa dan openness sama pada P yang sama, tetapi FE boundary berbeda karena diskretisasi. Perbedaan tegangan ini tidak boleh langsung disebut efek penguatan winding. Perlu studi konvergensi mesh dan tumpuan sebelum menyimpulkan efek anchor secara kausal.

## Batas dan tahap lanjut
- Dataset berurutan hanya mencakup9 keluarga dari domainweb yang lebih besar. Beberapa P hilang/HOLD dan rentangP antar keluarga berbeda; jangan gunakan rerata pooled500 untuk pemeringkatan.
- 14 catatan HOLD tetap disertakan (crash/proses belum lengkap atau pemeriksaan residual). HOLD bukan otomatis gagal kapasitas, bukan nilai0, dan tidak dimasukkan dalam hasil500 reviewed.
- Tegangan winding adalah maksimum absolut principal shell; boundary/link maksimum absolut normal beam. Ketiganya dilaporkan terpisah dan tidak dijumlahkan. Tanpa allowable CFRP, failure criterion, buckling, nonlinearity dan sambungan nyata, tidak ada klaim lolos keselamatan.
- Kandidat lanjutan yang masuk akal adalah orbit penuh (misalnyaN11/S5 danN13/S5 atauS6), kemudian kaji batas openness, massa, deformasi dan tegangan proyek. Untuk mengisolasi efekN/S, samakan diskretisasi boundary dan tumpuan sebelum Analyze baru; studi ini tidak mengubah kontrak lama.

P lengkap9 keluarga: 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 48, 50, 51, 54, 55.
Maksimum selisih openness512–256: 0.047033 pp (pavilion), 0.589955 pp (panel). Ini pemeriksaan resolusi, bukan galat eksak.
Residual gaya maksimum hasil reviewed: 6.836388e-08 kN.

## Jejak data
Sumber native: NG09_PUBLIC_500_20261018 dan NG09_FULL_BATCH_H100_20261018. Visual openness: GH_NEW_PROJECTED_OPENNESS_V1. Detail hash dan galat kecocokan per konfigurasi ada padaidentity-checks.json. Unduhanconfigurations.csv, native-cases.csv danpaired-effects.csv menyertakan seluruh500 baseline dan4.500 kasus. Data historis tidak diubah.
