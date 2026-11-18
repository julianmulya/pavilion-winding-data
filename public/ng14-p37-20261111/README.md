# NG14 P37 FE results (web dataset)

This directory contains the public, web-ready case-level FE table for the P37 study.

- 37 panels; boundary offset fixed at 1.0 m
- 421 anchor/shift configurations
- 3 methods: BASELINE, REPEAT (winding ulang), AB_SHIFT (planar A/B)
- 3,786 FE case-result rows; 1 model is HOLD and has no Analyze output
- Cases: G, L_X_NEG, G_X_NEG
- Units: MPa, mm, kg, m

## Shift and ratio convention

The Grasshopper/FE source stores the shift index one lower than the shift-list value shown in the generator. In this publication, `shift` and the displayed configuration ID use the generator's shift-list value:

- `shift list = source_shift_index + 1`
- `ratio = shift list / anchors`
- The CSV keeps `source_configuration` and `source_shift_index` so the original FE IDs and values can be audited.

The CSV has been gzip-compressed and base64-encoded across the ordered text files in `parts/` for GitHub's text-file transport. `manifest.json` contains the CSV/gzip SHA-256 values and publication metadata. Use the interactive study page to view, filter, and download the reconstructed CSV:

https://pavilion-p37-study.vercel.app/

The HOLD record is retained with a concise explanation. Its original local traceback and absolute file paths are excluded. This web publication includes the case-level results table; the 33.8 GB raw research archive (native contours, GH inputs, full run evidence) remains local and is not uploaded here.

FE values are results from the stated Karamba model assumptions. They are not a material-strength test or certification of structural safety.
