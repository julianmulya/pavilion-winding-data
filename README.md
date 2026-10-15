# Pavilion winding data

Versioned public geometry and native conceptual Karamba datasets for Pavilion Winding Lab. The application source remains private. No credentials, environment files, GH source files or desktop command history are included.

Pin a Git commit when serving these files. DATA_MANIFEST.json lists every file, size and SHA256. Git newline normalization is disabled to preserve exported bytes. Each native field is tied to its own model, loadcase and RunID; missing results never substitute another field.

BND14 retains the BND12 M065/M070 additions and adds two passes on M058 S039. Only G+Y was solved. Its native winding maximum is 9.2329048973926 MPa versus 9.859966943264288 MPa for BND12 in the same case. Four remaining cases are paused before Analyze at the user's request; their fields and metrics are null. No five-case envelope or whole-loadset qualification is claimed for BND14. InitialStrain is OFF. The viewer snapshot is study-v5; all previous snapshots and original statuses remain byte-identical. The historical proposal PNG is labelled as pre-FE geometry.

BND13 already completed G+X and G on the same BND12 candidate; together with the preserved BND12 cases it has a five-case gravity/lateral loadset. Those results remain in study-v4 and study-v5.

Native shell principal stresses, CFRP boundary normal stresses and aluminium-link normal stresses remain separate. These conceptual results do not establish physical material strength, local bolt-contact capacity, design wind loads or structural safety.

Vercel hosts the frontend and proxies dataset URLs to a pinned public GitHub commit. Moving storage does not eliminate decode/render RAM or proxy traffic. The native comparison viewer releases the prior pair when selection changes.
