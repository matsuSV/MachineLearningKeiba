import pandas as pd
import time
from file import write_dict, read, write, read_dict


class Race:
    def __init__(self, race_id_list):
        self.race_id_list = race_id_list
        self.downloaded_ids = read()
        self.all_races = pd.DataFrame(index=[], columns=[])

    def get_results(self) -> pd.DataFrame:
        self._scrape()
        self._make_df()
        return self.all_races

    def _scrape(self):
        for id in self.race_id_list:
            if id not in self.downloaded_ids:
                url = f'https://db.netkeiba.com/race/{id}'
                try:
                    result = pd.read_html(url)[0]
                except IndexError:
                    continue

                # TODO
                # トランザクション処理できるか？
                # レース情報を取得できたら取得済みレースIDとしてファイル保持する（何回も取得させないため）
                result.index = [id] * len(result)
                content = {id: result}
                content.update(read_dict())

                write(id)
                write_dict(content)
                time.sleep(0.5)  # スクレイピング時の対象サイトへの負荷軽減

    def _make_df(self):
        all_races = read_dict()

        # 各レースのDataFrameを繋げて1つのDataFrameとする
        results = pd.concat(list(all_races.values()), sort=False)

        # ファイルに出力して永続化（pickle系のメソッドを使ってみたかっただけ）
        results.to_pickle('df.pickle')
        self.all_races = pd.read_pickle('df.pickle')

    # def pre_processing():
