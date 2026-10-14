# Pavilion winding data

Versioned datasets for the public Pavilion Winding Lab website. The application source repository remains private.

This snapshot contains the web-exported geometry, native Karamba results, result contracts and checks. It preserves the existing bytes and historical statuses. It does not include credentials, environment files, private GH sources, or desktop command history.

Use a pinned Git commit when serving these files. `DATA_MANIFEST.json` lists every file, byte size and SHA256. Native records remain bound to their own model, loadcase and RunID; missing cases have no result substitute.

BND12 has three actual native conceptual cases (G+Y, G-Y, G-X), with InitialStrain OFF. Its G and G+X cases have not been run. Conceptual stress results do not establish physical strength, bolt contact capacity, design wind loads or structural safety. Historical non-improving and failed cases remain available.

The Vercel frontend may proxy the public dataset paths to this immutable commit. Moving file storage does not eliminate the RAM needed to decode and render the selected fields in the browser.
