from race import Race
from place import Place


# レースidを生成する
place = Place("2019")
race_ids = place.make_race_id_list()

# レース結果を取得する
test_race_id = ['201901010101', '201901010102', '201901010103']  # 実装確認用
race = Race(test_race_id)
result = race.get_results()

print(result)
print(result['着 順'].astype(str).value_counts())

# 着順が数字のものだけを残す
result2 = result[~(result['着 順'].astype(str).str.contains("\\D"))]
print(result2['性齢'].map(lambda x: str(x)[1]).value_counts())

result2['性'] = result2['性齢'].map(lambda x: str(x)[0])
print(result2)

result2['年齢'] = result2['性齢'].map(lambda x: str(x)[1])
print(result2)

# 馬体重が現体重(±増減値)という表記なので分割する
result2['体重'] = result2['馬体重'].str.split("(", expand=True)[0].astype(int)
result2['体重変化'] = result2['馬体重'].str.split("(", expand=True)[1].str[:-1].astype(int)
print(result2)

# 不要な列を削除する
result2.drop(['タイム', '着差', '調教師', '性齢', '馬体重'], axis=1, inplace=True)
print(result2)

result2['着 順'] = result2['着 順'].astype(int)
result2['年齢'] = result2['年齢'].astype(int)
print(result2.info())
