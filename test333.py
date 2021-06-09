import numpy as np

N=11
W=5000

wv=[[7,750],[6,700],[10,900],[10,600],[22,1200],[17,1250],[23,1850],[27,2050],
    [20,1750],[33,2700],[36,3150]]

# 価格あたりの幸せさ（コスパ）で降順ソート
wv = np.array(sorted(wv, key=lambda x: x[1] / x[0], reverse=True))


acc = np.vstack([np.array([0, 0]), wv]).cumsum(axis=0)
