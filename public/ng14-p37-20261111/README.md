# NG14 P37 FE results (web dataset)

This folder contains the web-ready, case-level FE metrics for the P37 study.

- 37 panels; 1.0 m boundary offset
- 421 valid anchor/shift configurations
- 3 methods: BASELINE, REPEAT, AB_SHIFT
- 3,786 FE case-result rows and 1 AB_SHIFT model held before Analyze
- Cases: G, L_X_NEG and G_X_NEG
- Units: MPa, mm, kg, m

The result table is gzip-compressed and base64-encoded across the ordered files in `parts/` so it can be transported through GitHub's text-file interface. The manifest records the gzip and decompressed CSV SHA-256 values. Use the Pavilion website to view, filter, and download the reconstructed CSV:

https://pavilion-winding-lab.vercel.app/p37-study.html

The single HOLD is retained with a short explanation. Its original local traceback and absolute file paths are excluded from the public data.

This web publication is the complete case-metrics table, not the 33.8 GB raw research archive. Raw Karamba contours, GH inputs, run logs and other evidence remain in the local research archive. The FE outputs are conceptual model results under the stated assumptions. They do not establish material capacity or structural safety.
