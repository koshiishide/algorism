import sys
input = sys.stdin.readline

# 最大再帰数の引き上げ
sys.setrecursionlimit(10**7)

import numpy as np

# メニューの個数と予算を入力
N, W = map(int, input().split())

# 各メニューの料金と幸せさを入力
wv = [list(map(int, input().split())) for _ in range(N)]

# 価格あたりの幸せさ（コスパ）で降順ソート
wv = np.array(sorted(wv, key=lambda x: x[1] / x[0], reverse=True))

acc_arg = np.vstack([np.array([0, 0]), wv]).cumsum(axis=0)


# 分枝操作をする関数
def rec(N, W, wv, acc, ans):
    # 分枝操作が終わったら0を返す
    if N <= 0 or W <= 0:
        return 0

    # 整数計画問題を貪欲に解いた場合の値を計算
    idx = np.searchsorted(acc[:, 0], W, side="right") - 1
    ans_ip = acc[idx, 1]

    # 線形計画問題を貪欲に解いた場合の値を計算
    if idx < N:
        ans_lp = ans_ip + (W - acc[idx, 0]) / wv[idx, 0] * wv[idx, 1]
    else:
        ans_lp = ans_ip

    # 線形計画問題の最適値が暫定値以下の場合は分枝操作を終了する
    if ans_lp <= ans:
        return ans
    # そうでない場合は暫定値を更新
    ans = max(ans, ans_ip)

    # 線形計画問題の解が整数計画問題の解と一致しない場合は分枝操作を再度行う
    if ans_lp != ans_ip:
        new_wv = np.vstack([wv[:idx], wv[idx + 1:]])

        # 分枝後の累積和を事前計算
        nxt_acc = acc.copy()
        nxt_acc[idx + 1:] -= wv[idx]
        nxt_acc = np.vstack([nxt_acc[:idx], nxt_acc[idx + 1:]])

        # メニューidxを選ぶ場合
        if W - wv[idx, 0] >= 0:
            ans = max(ans, rec(
                N - 1, W - wv[idx, 0], new_wv, nxt_acc, ans - wv[idx, 1]) + wv[idx, 1])

        # メニューidxを選ばない場合
        if W >= 0:
            ans = max(ans, rec(N - 1, W, new_wv, nxt_acc, ans))

    return ans




print(rec(N, W, wv, acc_arg, 0))