"""Multi-object tracking metrics: MOTA, MOTP, IDF1 (Light db03 tracking asset).

CLEAR-MOT (Bernardin & Stiefelhagen 2008) + IDF1 (Ristani 2016).
Greedy per-frame matching by IoU >= threshold with identity continuity.
Self-test: a hand-constructed scenario with known TP/FP/FN/IDSW counts.
Run:  python tracking_metrics.py
"""
import numpy as np


def iou(b1, b2):
    """boxes xywh."""
    x1, y1, w1, h1 = b1; x2, y2, w2, h2 = b2
    xa, ya = max(x1, x2), max(y1, y2)
    xb, yb = min(x1 + w1, x2 + w2), min(y1 + h1, y2 + h2)
    inter = max(0, xb - xa) * max(0, yb - ya)
    union = w1 * h1 + w2 * h2 - inter
    return inter / union if union > 0 else 0.0


def clear_mot(gt, pred, iou_thr=0.5):
    """gt, pred: list over frames of dict {id: box_xywh}.
    Returns dict with MOTA, MOTP, num_fp, num_fn, num_idsw, num_gt."""
    fp = fn = idsw = matches = 0
    dist_sum = 0.0
    num_gt = 0
    prev_map = {}  # gt_id -> pred_id from last frame
    for gframe, pframe in zip(gt, pred):
        num_gt += len(gframe)
        gids = list(gframe); pids = list(pframe)
        # build candidate matches by IoU
        pairs = []
        for gi in gids:
            for pi in pids:
                v = iou(gframe[gi], pframe[pi])
                if v >= iou_thr:
                    pairs.append((v, gi, pi))
        pairs.sort(reverse=True)
        gmatched, pmatched = {}, set()
        # CLEAR-MOT continuity: first PRESERVE last-frame correspondences that are
        # still valid (gt_id was matched to prev_pi, prev_pi present, IoU>=thr),
        # even if another hypothesis has higher IoU this frame. Only then greedily
        # match the remainder. This is the step Bernardin & Stiefelhagen (2008)
        # require; pure greedy would create false ID switches on duplicate detections.
        for gi in gids:
            prev_pi = prev_map.get(gi)
            if prev_pi is not None and prev_pi in pframe and prev_pi not in pmatched:
                if iou(gframe[gi], pframe[prev_pi]) >= iou_thr:
                    gmatched[gi] = prev_pi; pmatched.add(prev_pi)
                    matches += 1; dist_sum += iou(gframe[gi], pframe[prev_pi])
        for v, gi, pi in pairs:
            if gi in gmatched or pi in pmatched:
                continue
            gmatched[gi] = pi; pmatched.add(pi)
            matches += 1; dist_sum += v
            if gi in prev_map and prev_map[gi] != pi:
                idsw += 1
        fp += len(pids) - len(pmatched)
        fn += len(gids) - len(gmatched)
        for gi, pi in gmatched.items():
            prev_map[gi] = pi
    mota = 1.0 - (fp + fn + idsw) / num_gt if num_gt else 0.0
    motp = dist_sum / matches if matches else 0.0
    return dict(MOTA=mota, MOTP=motp, num_fp=fp, num_fn=fn, num_idsw=idsw,
                num_gt=num_gt, num_matches=matches)


def idf1(gt, pred, iou_thr=0.5):
    """Global identity matching → IDF1 = 2*IDTP / (2*IDTP + IDFP + IDFN)."""
    from scipy.optimize import linear_sum_assignment
    gids = sorted({i for f in gt for i in f})
    pids = sorted({i for f in pred for i in f})
    gi_idx = {g: k for k, g in enumerate(gids)}
    pi_idx = {p: k for k, p in enumerate(pids)}
    overlap = np.zeros((len(gids), len(pids)))
    gcount = np.zeros(len(gids)); pcount = np.zeros(len(pids))
    for gframe, pframe in zip(gt, pred):
        for g in gframe: gcount[gi_idx[g]] += 1
        for p in pframe: pcount[pi_idx[p]] += 1
        for g in gframe:
            for p in pframe:
                if iou(gframe[g], pframe[p]) >= iou_thr:
                    overlap[gi_idx[g], pi_idx[p]] += 1
    # maximize matched identity-frames via Hungarian on -overlap
    r, c = linear_sum_assignment(-overlap)
    idtp = sum(overlap[i, j] for i, j in zip(r, c))
    idfn = gcount.sum() - idtp
    idfp = pcount.sum() - idtp
    return 2 * idtp / (2 * idtp + idfp + idfn) if (2 * idtp + idfp + idfn) else 0.0


if __name__ == '__main__':
    ok = True
    B = lambda x: (x, 0, 10, 10)  # box at varying x, size 10x10

    # Scenario: 3 frames, gt has goats A,B every frame.
    # pred: frame0 perfect; frame1 perfect; frame2 pred swaps A<->B ids AND misses B once.
    gt = [
        {'A': B(0),  'B': B(50)},
        {'A': B(2),  'B': B(52)},
        {'A': B(4),  'B': B(54)},
    ]
    pred = [
        {1: B(0),  2: B(50)},          # 1->A, 2->B
        {1: B(2),  2: B(52)},          # same
        {2: B(4),  1: B(54)},          # frame2: id 1 now on B's pos, id 2 on A's pos -> 2 idsw
    ]
    r = clear_mot(gt, pred, 0.5)
    # num_gt=6, all boxes overlap so 6 matches, 0 fp, 0 fn.
    # frame2: gtA matched to pred2 (was 1)->switch; gtB matched to pred1 (was 2)->switch => 2 idsw
    print(f"clear_mot: {r}")
    assert r['num_gt'] == 6, r
    assert r['num_fp'] == 0 and r['num_fn'] == 0, r
    assert r['num_idsw'] == 2, r
    # MOTA = 1 - (0+0+2)/6 = 0.6667
    assert abs(r['MOTA'] - (1 - 2/6)) < 1e-9, r['MOTA']
    print(f"  MOTA={r['MOTA']:.4f} (expect 0.6667), idsw={r['num_idsw']} (expect 2)  OK")

    # IDF1: global identity matching is swap-invariant within consistent runs.
    # gtA appears 3x, gtB 3x; pred id1 overlaps A(frame0,1)+B(frame2), pred id2 overlaps B(0,1)+A(2).
    # Hungarian picks A<->1 (2) + B<->2 (2) = IDTP 4; or A<->2(1)+B<->1(1). Max=4.
    f = idf1(gt, pred, 0.5)
    # IDTP=4, IDFP = 6-4=2, IDFN=6-4=2 -> IDF1 = 8/(8+2+2)=0.6667
    print(f"  IDF1={f:.4f} (expect 0.6667)")
    assert abs(f - 2*4/(2*4+2+2)) < 1e-9, f

    # Sanity: perfect tracking -> MOTA=1, IDF1=1
    rp = clear_mot(gt, gt, 0.5); fp_ = idf1(gt, gt, 0.5)
    assert abs(rp['MOTA'] - 1) < 1e-9 and abs(fp_ - 1) < 1e-9
    print(f"  perfect: MOTA={rp['MOTA']:.4f} IDF1={fp_:.4f}  OK")

    # ADVERSARIAL-GATE reproduction: duplicate-detection / continuity conflict.
    # gtA present both frames. frame0: pred 1 on A. frame1: pred 1 still valid
    # (IoU 0.538>=0.5) BUT pred 2 has higher IoU (0.818). CLEAR-MOT must KEEP A<->1
    # by continuity => idsw=0, fp=1, MOTA=1-1/2=0.5. Pure greedy wrongly gives idsw=1, MOTA=0.
    gt2 = [{'A': (0, 0, 10, 10)}, {'A': (0, 0, 10, 10)}]
    pr2 = [{1: (3, 0, 10, 10)}, {1: (3, 0, 10, 10), 2: (1, 0, 10, 10)}]
    r2 = clear_mot(gt2, pr2, 0.5)
    print(f"  continuity-conflict: MOTA={r2['MOTA']:.4f} idsw={r2['num_idsw']} fp={r2['num_fp']} "
          f"(expect MOTA=0.5 idsw=0 fp=1)")
    assert r2['num_idsw'] == 0, r2
    assert r2['num_fp'] == 1, r2
    assert abs(r2['MOTA'] - 0.5) < 1e-9, r2
    print("  continuity preserved (matches CLEAR-MOT / motmetrics)  OK")

    print("ALL PASS" if ok else "FAIL")
