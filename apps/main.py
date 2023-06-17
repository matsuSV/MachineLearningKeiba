import pandas as pd

from race import Race
from place import Place

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler

# レースidを生成する
place = Place("2019")
race_ids = place.make_race_id_list()

# レース結果を取得する
race = Race(['201901010101', '201901010102', '201901010103'])  # 実装確認用
result = race.get_results()

# レース結果を整形する
test = race.pre_processing(result)
print(test)

# 1,2,3着と4着以下に分類されていること
cliped = race.clip_out_of_returns(result)
# print(cliped['rank'].value_counts())

droped = race.get_dummies(cliped)

# 分析
# 説明変数
X = droped.drop(['rank'], axis=1)

# 目的変数
y = droped['rank']

# オプションのstratifyは均等に散らばるようにする命令
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=0)

# max_iter=10000にしないとエラー
model = LogisticRegression(max_iter=10000)
model.fit(X_train, y_train)

# 訓練データ（左）、テストデータ（右）
print(model.score(X_train, y_train), model.score(X_test, y_test))

# ほとんどのデータが4なので4と予測してしまう→不均衡データと呼ばれる→なのでアンダーサンプリングを行う
print(model.predict(X_test))
print(y_train.value_counts())

# データをn:nにしてください
rank_1 = y_train.value_counts()[1]
rank_2 = y_train.value_counts()[2]
rank_3 = y_train.value_counts()[3]
rus = RandomUnderSampler(sampling_strategy={1: rank_1, 2: rank_2, 3: rank_3, 4: rank_1}, random_state=71)
X_train_rus, y_train_rus = rus.fit_resample(X_train, y_train)
print(pd.Series(y_train_rus).value_counts())

# 実際に予測をしてみる
model = LogisticRegression(max_iter=10000)
model.fit(X_train_rus, y_train_rus)
print(model.score(X_train, y_train), model.score(X_test, y_test))

y_pred = model.predict(X_test)
pred_df = pd.DataFrame({'pred': y_pred, 'actual': y_test})
print(pred_df)

# 1着に来ると予測された馬を見てみる
print(pred_df[pred_df['pred']==1]['actual'].value_counts())
print(len(pred_df[pred_df['pred']==1]))
print("--------------------------------------------------------------------------")
# 4着以下になると予測されたもの(だけど実際は～だったよ、って感じ)
print(pred_df[pred_df['pred']==4]['actual'].value_counts())

# ロジスティックス回帰のいいところとして、この予測がどういう仕組みで行えたかということが分かりやすい
# print(model.coef_)  # 回帰変数全体を見ることができる

# このままだと見づらいのでこうする
coefs = pd.Series(model.coef_[0], index=X.columns).sort_values()
print(coefs)

print(cliped.columns)
print(droped.columns)
jockey_iwata = cliped[cliped['騎手']=='岩田康誠']
print(jockey_iwata)
print(jockey_iwata['rank'].value_counts())
print(X.columns)
print(coefs[['枠 番', '馬 番', '斤量', '単勝', '人 気']])

# 過去のデータを使って未来のデータを予測したい！