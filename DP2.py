import sys
input = sys.stdin.readline

# dpテーブルから特定の重さのindexを逆引きするため二分探索ライブラリをimport
import bisect

N=2
W=10
wv=[[3,8],[7,5]]

# 品物を全て選んだ場合の価値の合計を計算
V = sum(x[1] for x in wv) #13

# 最小化問題なのでdpテーブルをINFで初期化
# 1 << 60は2**60, pow(2, 60)と同義
INF = 1 << 60

# i行目への遷移はi-1行目のみから行われるため、工夫するとdpテーブルは1行で済む
dp = [INF] * (V + 1) #14個作成
dp[0] = 0

# 価値jを達成するための最小の重さ = min(dp[j], dp[max(0, j - v)] + w)
#indexが価値中身が重さ
for w, v in wv:#[w=3,v=8]
    dp_tmp = dp[:]
    for j in range(1, V + 1):#14未満 1~13
        # j - vが負の場合は0からの遷移としてよい
        idx_prev = max(0, j - v)#0,1~13 - 8 つまり価値なしかj-vの価値
        dp_tmp[j] = min(dp[j], dp[idx_prev] + w)#INF,8までは0+
    dp = dp_tmp

# 重さWで達成できる最大価値を求める
print(bisect.bisect_right(dp, W) - 1)