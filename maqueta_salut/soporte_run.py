import sys, json, verif_foto as VF
from collections import defaultdict
for nm in sys.argv[1:]:
    cam = json.load(open(f"cam_{nm}_verif.json"))
    res = VF.soporte(nm, cam["foto"], cam["cam"])
    z = defaultdict(lambda: [0, 0])
    for k, zona, tot, sop, fr in res: z[zona][0] += tot; z[zona][1] += sop
    print(nm, "calibración rms", round(cam["rms"], 1))
    for zona, (t, s) in sorted(z.items()): print(f"   {zona:22s} {s:4d}/{t:4d} = {s / t:4.0%}")
    print("   peores líneas:", sorted([(round(fr, 2), k) for k, zona, tot, sop, fr in res if tot >= 6])[:12])
