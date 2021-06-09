import numpy as np

N=11
W=5000

wv=[[750, 7], [700, 6], [900, 10], [600, 10], [1200, 22], [1250, 17], [1850, 23], [2050, 27], [1750, 20], [2700, 33], [3150, 36]]

wv = np.array(sorted(wv, key=lambda x: x[1] / x[0], reverse=True))
acc = np.vstack([np.array([0, 0]), wv]).cumsum(axis=0)

# 価格あたりの幸せさ（コスパ）で降順ソート


idx = np.searchsorted(acc[:, 0], W, side="right")-1
ans_ip = acc[idx, 1]
new_wv = np.vstack([wv[:idx], wv[idx + 1:]])
nxt_acc = acc.copy()#nxt_accにaccをコピー

nxt_acc[idx + 1:] -= wv[idx]
#nxt_acc = np.vstack([nxt_acc[:idx], nxt_acc[idx + 1:]])
 
