from race import Race
from place import Place

i_place = Place("2019")
i_race = Race(i_place.make_race_id_list())
test = i_race.scrape_race_results()


print(test)
