# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

path = Path(r"C:\WORK\MMO\lab2\LR02_podgotovka_dannyh.ipynb")
nb = json.loads(path.read_text(encoding="utf-8"))

found = False
for i, c in enumerate(nb["cells"]):
    if c.get("cell_type") != "code":
        continue
    src = "".join(c.get("source", []))[:80].replace("\n", " ")
    for o in c.get("outputs", []):
        if o.get("output_type") == "error":
            found = True
            print("=" * 70)
            print(f"CELL {i}: {o.get('ename')}: {o.get('evalue')}")
            print("SRC:", src)
            for line in o.get("traceback", []):
                clean = re.sub(r"\x1b\[[0-9;]*m", "", line)
                print(clean)
        elif o.get("output_type") == "stream":
            text = "".join(o.get("text", []))
            if "Error" in text or "Traceback" in text or "error" in text.lower():
                found = True
                print("=" * 70)
                print(f"CELL {i} STREAM")
                print("SRC:", src)
                print(text[:3000])

if not found:
    print("NO ERRORS IN SAVED NOTEBOOK OUTPUTS")
    print("code cells:", sum(1 for c in nb["cells"] if c.get("cell_type") == "code"))
    for i, c in enumerate(nb["cells"]):
        if c.get("cell_type") != "code":
            continue
        outs = c.get("outputs", [])
        types = [o.get("output_type") for o in outs]
        print(f"cell {i}: execution_count={c.get('execution_count')} outputs={types}")
