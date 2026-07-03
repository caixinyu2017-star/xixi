"""Application experiments.

Paper A: cardinality-constrained mean-variance portfolio selection (OR-Library).
Paper B: customer segmentation clustering (Mall Customers, Wholesale Customers).
"""
import csv, os, sys, time
import numpy as np
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
os.makedirs(RESULTS, exist_ok=True)

RUNS = 30
POP = 30
FES = 20000

ALGOS_A = ['MSSBOA', 'SBOA', 'GWO', 'WOA', 'SCA', 'PSO', 'HHO', 'DBO', 'COA', 'RIME']
ALGOS_B = ['MSBKA', 'BKA', 'SSA', 'COA', 'GWO', 'SCA', 'PSO', 'DE', 'HHO', 'RIME']


def all_algos():
    from algos_classic import ALGOS as C
    from algos_sboa import sboa, mssboa
    from algos_bka import bka, msbka
    d = dict(C)
    d.update({'SBOA': sboa, 'MSSBOA': mssboa, 'BKA': bka, 'MSBKA': msbka})
    return d


def port_task(args):
    algo_name, ds, run = args
    import zlib
    from applications import portfolio_problem, decode_portfolio, load_port
    algos = all_algos()
    prob, mu, cov = portfolio_problem(ds, lam=0.5, K=10, eps=0.01)
    seed = 31 + run * 7717 + ds * 131 + (zlib.crc32(algo_name.encode()) % 997) * 13
    rng = np.random.default_rng(seed)
    bf, bx, curve = algos[algo_name](prob, FES, POP, rng)
    w = decode_portfolio(bx, mu, cov)
    risk = float(w @ cov @ w)
    ret = float(w @ mu)
    return ('port', ds, algo_name, run, bf, risk, ret, curve)


def frontier_task(args):
    algo_name, lam_idx, run = args
    import zlib
    from applications import portfolio_problem, decode_portfolio
    lam = lam_idx / 20.0
    algos = all_algos()
    prob, mu, cov = portfolio_problem(1, lam=lam, K=10, eps=0.01)
    seed = 97 + run * 4013 + lam_idx * 211 + (zlib.crc32(algo_name.encode()) % 997)
    rng = np.random.default_rng(seed)
    bf, bx, _ = algos[algo_name](prob, 10000, POP, rng)
    w = decode_portfolio(bx, mu, cov)
    return ('frontier', algo_name, lam, run, bf, float(w @ cov @ w), float(w @ mu))


def clust_task(args):
    algo_name, ds, run = args
    import zlib
    from applications import load_mall, load_wholesale, clustering_problem, sse
    algos = all_algos()
    if ds == 'mall':
        X, K = load_mall(), 5
    else:
        X, K = load_wholesale(), 3
    prob = clustering_problem(X, K, ds)
    seed = 53 + run * 6089 + (zlib.crc32((algo_name + ds).encode()) % 997) * 17
    rng = np.random.default_rng(seed)
    bf, bx, curve = algos[algo_name](prob, FES, POP, rng)
    centers = bx.reshape(K, -1)
    d2 = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
    labels = d2.argmin(axis=1)
    from sklearn.metrics import silhouette_score
    try:
        sil = float(silhouette_score(X, labels)) if len(set(labels)) > 1 else -1.0
    except Exception:
        sil = -1.0
    return ('clust', ds, algo_name, run, bf, sil, curve)


def main():
    t0 = time.time()
    tasks_port = [(a, ds, r) for a in ALGOS_A for ds in range(1, 6) for r in range(RUNS)]
    tasks_frontier = [(a, li, r) for a in ['MSSBOA', 'SBOA'] for li in range(21) for r in range(5)]
    tasks_clust = [(a, ds, r) for a in ALGOS_B for ds in ('mall', 'wholesale') for r in range(RUNS)]

    with Pool(4) as pool:
        with open(f'{RESULTS}/apps_portfolio.csv', 'w', newline='') as fh:
            wr = csv.writer(fh)
            wr.writerow(['dataset', 'algo', 'run', 'objective', 'risk', 'return'])
            curves = {}
            for res in pool.imap_unordered(port_task, tasks_port, chunksize=4):
                _, ds, alg, run, bf, risk, ret, curve = res
                wr.writerow([ds, alg, run, f'{bf:.10e}', f'{risk:.10e}', f'{ret:.10e}'])
                curves[f'port{ds}|{alg}|{run}'] = curve.astype(np.float32)
            np.savez_compressed(f'{RESULTS}/curves_portfolio.npz', **curves)
        print(f'portfolio done {time.time()-t0:.0f}s', flush=True)

        with open(f'{RESULTS}/apps_frontier.csv', 'w', newline='') as fh:
            wr = csv.writer(fh)
            wr.writerow(['algo', 'lam', 'run', 'objective', 'risk', 'return'])
            for res in pool.imap_unordered(frontier_task, tasks_frontier, chunksize=4):
                _, alg, lam, run, bf, risk, ret = res
                wr.writerow([alg, f'{lam:.2f}', run, f'{bf:.10e}', f'{risk:.10e}', f'{ret:.10e}'])
        print(f'frontier done {time.time()-t0:.0f}s', flush=True)

        with open(f'{RESULTS}/apps_clustering.csv', 'w', newline='') as fh:
            wr = csv.writer(fh)
            wr.writerow(['dataset', 'algo', 'run', 'sse', 'silhouette'])
            curves = {}
            for res in pool.imap_unordered(clust_task, tasks_clust, chunksize=4):
                _, ds, alg, run, bf, sil, curve = res
                wr.writerow([ds, alg, run, f'{bf:.10e}', f'{sil:.6f}'])
                curves[f'{ds}|{alg}|{run}'] = curve.astype(np.float32)
            np.savez_compressed(f'{RESULTS}/curves_clustering.npz', **curves)
        print(f'clustering done {time.time()-t0:.0f}s', flush=True)

    # K-means baselines for clustering (single random init per run, plus kmeans++ reference)
    from applications import load_mall, load_wholesale
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    with open(f'{RESULTS}/apps_kmeans.csv', 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['dataset', 'method', 'run', 'sse', 'silhouette'])
        for ds, X, K in (('mall', load_mall(), 5), ('wholesale', load_wholesale(), 3)):
            for run in range(RUNS):
                km = KMeans(n_clusters=K, init='random', n_init=1, random_state=run).fit(X)
                sil = silhouette_score(X, km.labels_)
                wr.writerow([ds, 'KMeans', run, f'{km.inertia_:.10e}', f'{sil:.6f}'])
                kmpp = KMeans(n_clusters=K, init='k-means++', n_init=1, random_state=run).fit(X)
                sil2 = silhouette_score(X, kmpp.labels_)
                wr.writerow([ds, 'KMeans++', run, f'{kmpp.inertia_:.10e}', f'{sil2:.6f}'])
    print(f'kmeans baselines done {time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
