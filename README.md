# Pavilion winding data

Versioned public geometry and native conceptual Karamba datasets for Pavilion Winding Lab. The application source repository remains private; no credentials, environment files, private GH sources or desktop command history are included.

Pin a Git commit when serving these files. `DATA_MANIFEST.json` lists every file, size and SHA256. Git newline normalization is disabled so the exact exported bytes are retained. Each native field is tied to its own model, loadcase and RunID; missing results never substitute another field.

BND13 completes G+X and G on the same BND12 M065+M070 candidate. Together with its three preserved BND12 cases, the conceptual gravity/lateral loadset is G, G+X, G-X, G+Y and G-Y. InitialStrain remains OFF. No new reinforcement variant was added. BND12's original three-case snapshot remains unchanged in study-v3; the completed loadset is in study-v4. Historical increases and failed cases remain available.

Native shell principal stresses and beam normal stresses are reported separately. These conceptual results do not establish physical material strength, local bolt-contact capacity, design wind loads or structural safety.

Vercel hosts the frontend and proxies dataset URLs to a pinned public GitHub commit. Moving file storage does not eliminate decode/render RAM for selected fields or proxy traffic. The native comparison viewer releases the prior pair when model/load selection changes.
