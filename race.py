import pandas as pd
import time


class Race:
    def __init__(self, race_id_list):
        self.race_id_list = race_id_list

    def scrape_race_results(self):
        race_results = {}
        for race_id in self.race_id_list:
            try:
                url = f'https://db.netkeiba.com/race/{race_id}'
                race_results[race_id] = pd.read_html(url)[0]
                time.sleep(1)  # スクレイピング時の対象サイトへの負荷軽減
            except:
                break
        return race_results
