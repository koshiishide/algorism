import numpy as np

# メニューの個数と予算を入力
N, W = map(int, input().split())

# 各メニューの料金と幸せさを入力
wv = [list(map(int, input().split())) for _ in range(N)]

"""
x[0],x[1]をそれぞれ金額、幸せさとする。
メイドさんオリジナルカクテル　　    750円	7
メイドさんの手作りパフェ	　　　  700円	6
メイドさんのお絵かきオムライス	　　900円	10
メイドさんと記念撮影（チェキ）	　　600円	10
メイドさんと記念撮影（デカチェキ）	1,200円	22
ドリンクセット（ドリンク+チェキ）	1,250円	17
デザートセット（ドリンク+デザート+チェキ）	1,850円	23
フードセット（ドリンク+フード+チェキ）	2,050円	27
お土産セット（ドリンク+お土産+チェキ）	1,750円	20
フルセット（ドリンク+デザート+フード+チェキ）	2,700円	33
プレミアムセット（ドリンク+デザート+フード+お土産+チェキ）	3,150円	3

メニューの個数をN , メニュー i の金額と幸せさを wi と vi , 予算を W
"""



# 価格あたりの幸せさ（コスパ）で降順ソート
wv = np.array(sorted(wv, key=lambda x: x[1] / x[0], reverse=True))#lambda式はxを引数に取り、x[1]/x[0]（幸せさ÷金額）を返す無名関数 つまり1円当たりの幸せさ


# 分枝操作をする関数
def rec(N, W, wv, acc, ans):
    # 分枝操作が終わったら0を返す
    if N <= 0 or W <= 0:
        return 0

    #整数計画問題を貪欲に解いた場合の値を計算
    #買える最大の累計金額のインデックス
    idx = np.searchsorted(acc[:, 0], W, side="right") - 1 #searchsorted(N行一列、予算W、右から探索せよ) つまり0~Nの価値の累計和の一次元リストを作って予算Wが右から探索してindexの場所を探す-1
    #5
    ans_ip = acc[idx, 1]#acc(3,1) → その予算で買える最大の幸せ値(49)

    # 線形計画問題を貪欲に解いた場合の値を計算
    if idx < N:#もし買える最大個数<メニューの個数なら
        ans_lp = ans_ip + (W - acc[idx, 0]) / wv[idx, 0] * wv[idx, 1]#ans_lp=その予算で買える最大の幸せ値 + (予算-累積金額)/wv[3,0]コスパ三番目の金額 * wv[3,1]コスパ三番目の幸せ
    else:#買える個数をオーバーしているなら(全部買える場合)
        ans_lp = ans_ip #その予算で買える最大の幸せ値

    # 線形計画問題の最適値が暫定値以下の場合は分枝操作を終了する
    if ans_lp <= ans:
        return ans
    # そうでない場合は暫定値を更新
    ans = max(ans, ans_ip)

    # 線形計画問題の解が整数計画問題の解と一致しない場合は分枝操作を再度行う
    if ans_lp != ans_ip:#線形計画!=整数計画
        #wv[0,3],wv[3+1:]
        new_wv = np.vstack([wv[:idx], wv[idx + 1:]])#最後の要素をコスパ一個下の物にする

        # 分枝後の累積和を事前計算
        nxt_acc = acc.copy()#nxt_accにaccをコピー
        nxt_acc[idx + 1:] -= wv[idx] #nxt(acc)の4つ目からした-=wv(3番目) 累計和で足し算するものを０にできる
        nxt_acc = np.vstack([nxt_acc[:idx], nxt_acc[idx + 1:]])#3番目削除

        # メニューidxを選ぶ場合
        if W - wv[idx, 0] >= 0:
            ans = max(ans, rec(
                N - 1, W - wv[idx, 0], new_wv, nxt_acc, ans - wv[idx, 1]) + wv[idx, 1])#再起するrec(#N-1 , 予算からidx差し引いたもの,new_wv,暫定値-idx(幸せ)) + idx(幸せ)
        # メニューidxを選ばない場合
        if W >= 0:
            ans = max(ans, rec(N - 1, W, new_wv, nxt_acc, ans))#rec(単純にidx入れなかった)

    return ans


acc = np.vstack([np.array([0, 0]), wv]).cumsum(axis=0)