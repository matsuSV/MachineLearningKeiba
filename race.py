import pandas as pd
import time
from file import write_dict, read, write, read_dict


class Race:
    def __init__(self, race_id_list):
        self.race_id_list = race_id_list
        self.downloaded_ids = read()

    def scrape_race_results(self):
        for race_id in self.race_id_list:
            if race_id not in self.downloaded_ids:
                url = f'https://db.netkeiba.com/race/{race_id}'
                try:
                    race_result = pd.read_html(url)[0]
                except IndexError:
                    continue
                write(race_id)  # レース情報を取得できたら取得済みレースIDとしてファイル保持する（何回も取得させないため）
                write_dict({race_id: race_result})
                time.sleep(1)   # スクレイピング時の対象サイトへの負荷軽減

    @staticmethod
    def get_all_races():
        all_races = read_dict()

        for k, v in all_races.items():
            v.index = [k] * len(v)

        results = pd.concat([v for v in all_races.values()], sort=False)
        results.to_pickle('df.pickle')
        return pd.read_pickle('df.pickle')
