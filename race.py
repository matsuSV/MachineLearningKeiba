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

    @staticmethod
    def pre_processing(results):
        df = results.copy()

        # 着順に数字以外の文字列が含まれているものを取り除く
        df = df[~(df['着 順'].astype(str).str.contains("\\D"))]
        df['着 順'] = df['着 順'].astype(int)

        # 年齢を性と年齢に分ける
        df['性'] = df['性齢'].map(lambda x: str(x)[0])
        df['年齢'] = df['性齢'].map(lambda x: str(x)[1]).astype(int)

        # 馬体重が現体重(±増減値)という表記なので体重と体重変化に分ける
        df['体重'] = df['馬体重'].str.split("(", expand=True)[0].astype(int)
        df['体重変化'] = df['馬体重'].str.split("(", expand=True)[1].str[:-1].astype(int)

        # データをint, floatへ変換する
        df['単勝'] = df['単勝'].astype(float)

        # 不要な列を削除する
        df.drop(['タイム', '着差', '調教師', '性齢', '馬体重'], axis=1, inplace=True)

        return df
