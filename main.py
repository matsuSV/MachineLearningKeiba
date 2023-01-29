from race import Race
from place import Place
from file import read_dict


# レースidを生成する
i_place = Place("2019")
race_ids = i_place.make_race_id_list()
print(race_ids)

# レース結果を取得する
test_race_id = ['201901010101', '201901010102', '201901010103']  # 実装確認用
i_race = Race(test_race_id)
i_race.scrape_race_results()
test = read_dict()
print(test)
