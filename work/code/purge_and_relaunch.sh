#!/bin/bash
# Purge stale MSSBOA/SBOA-EGS rows from paper A results and relaunch the full pipeline.
set -e
cd /home/user/xixi/work/code
python3 - <<'EOF'
import csv, os
import numpy as np
STALE = {'MSSBOA', 'SBOA-EGS'}
for dim in (10, 30):
    path = f'/home/user/xixi/work/results/A_cec2017_{dim}.csv'
    if not os.path.exists(path):
        continue
    rows = []
    with open(path) as fh:
        rd = csv.reader(fh)
        header = next(rd)
        for r in rd:
            if r and r[1] not in STALE:
                rows.append(r)
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f'{dim}D kept {len(rows)}')
    npz = f'/home/user/xixi/work/results/curves_A_cec2017_{dim}.npz'
    if os.path.exists(npz):
        z = np.load(npz)
        keep = {k: z[k] for k in z.files if k.split('|')[1] not in STALE}
        np.savez_compressed(npz, **keep)
        print(f'{dim}D curves kept {len(keep)}')
EOF
rm -f /home/user/xixi/work/results/PIPELINE_DONE
nohup bash -c 'cd /home/user/xixi/work/code && python3 run_cec.py --paper A --procs 4 > ../results/logA.txt 2>&1; python3 run_cec.py --paper B --procs 4 > ../results/logB.txt 2>&1; python3 run_apps.py > ../results/logApps.txt 2>&1; touch ../results/PIPELINE_DONE' > /dev/null 2>&1 &
disown
echo "pipeline relaunched"
