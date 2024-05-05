import pandas as pd
import time
import apps.file as file


class Race:
    """
    レースIDを受け取り、そのレース結果をWebサイトから取得します
    """

    def __init__(self, race_id_list):
        self.race_id_list = race_id_list

    def get_results(self) -> pd.DataFrame:
        """
        サイトからレース結果情報を取得してローカルファイルへ保持する
        """
        downloaded_ids = file.read()
        for race_id in self.race_id_list:
            if race_id not in downloaded_ids:
                result = self._scrape(race_id)
                if not result.empty:
                    classified = self._classify(race_id, result)
                    all_races = self._get_latest_races(classified)
                    self._save(race_id, all_races)

        return file.to_pickle(self._create_df())  # pickle関数を使ってみたかった

    @staticmethod
    def _scrape(race_id):
        """
        レースIDを元にネット競馬サイトからレース結果のTable要素をDataFrameとして取得する
        スクレイピング時の対象サイトへの負荷軽減を考慮している
        """
        time.sleep(0.25)
        try:
            return pd.read_html(f'https://db.netkeiba.com/race/{race_id}')[0]
        except IndexError:
            return pd.DataFrame()

    @staticmethod
    def _classify(race_id, result):
        """
        レース結果のインデックスをレースIDへ差し替える
        (後続処理をし易くするため)

        :param race_id: 生成したレースID
        :param result : サイトからスクレイピングした結果
        """
        result.index = [race_id] * len(result)
        return {race_id: result}

    @staticmethod
    def _get_latest_races(race):
        """
        現状取得できる全レース結果を返却する

        :param race: キーにレースID、値にインデックスをレースIDにしたデータフレームとなっているdict型の値
        :return: 既に取得済みのレース結果を合わせたdict型の値
        """
        race.update(file.read_all_races())
        return race

    @staticmethod
    def _save(race_id, all_races):
        """
        レースIDのみとレースID＆レース結果でファイルを分けて保持する
        レースIDのみを保持しているファイルを参照することで取得済みのレース結果は再取得させない意図
        """
        file.write(race_id)
        file.write_races(all_races)

    @staticmethod
    def _create_df():
        """
        取得したレース結果を解析用に１つのDataFrameとして取得する
        """
        return pd.concat(list(file.read_all_races().values()), sort=False)
