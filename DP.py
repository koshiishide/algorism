N,W=2,10
wv=[[3,8],[7,5]]

# 最大化問題なのでdpテーブルを0で初期化
# dp[i][j]は、重量の合計j以下という制約下でi番目までの品物から任意の品物を選んだ場合の価値の最大値
dp = [[0] * (W + 1) for _ in range(N + 1)]

# 品物i+1を選ばない場合で仮更新してから、ナップサックにi+1個目を詰め込める場合は再更新
for i, (w, v) in enumerate(wv):
    for j in range(W + 1):
        dp[i + 1][j] = dp[i][j]
        if j - w >= 0:
            dp[i + 1][j] = max(dp[i + 1][j], dp[i][j - w] + v)

print(dp[-1][-1])