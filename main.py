from race import Race
from place import Place


# レースidを生成する
place = Place("2019")
race_ids = place.make_race_id_list()

# レース結果を取得する
race = Race(['201901010101', '201901010102', '201901010103'])  # 実装確認用
result = race.get_results()

# レース結果を整形する
test = race.pre_processing(result)
print(test)
print(test.info())
