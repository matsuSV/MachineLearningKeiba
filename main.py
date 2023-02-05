import pandas as pd

from race import Race
from place import Place
from file import read_dict


# レースidを生成する
i_place = Place("2019")
race_ids = i_place.make_race_id_list()

# レース結果を取得する
test_race_id = ['201901010101', '201901010102', '201901010103']  # 実装確認用
i_race = Race(test_race_id)
i_race.scrape_race_results()
result = i_race.get_all_races()

print(result)
print(result['着 順'].astype(str).value_counts())

result2 = result[~(result['着 順'].astype(str).str.contains("\D"))]
print(result2['性齢'].map(lambda x: str(x)[1]).value_counts())

result2['性'] = result2['性齢'].map(lambda x: str(x)[0])
print(result2)

result2['年齢'] = result2['性齢'].map(lambda x: str(x)[1])
print(result2)
