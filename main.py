from race import Race
from place import Place

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

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
#print(cliped['rank'].value_counts())

droped = race.get_dummies(cliped)

## 分析
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