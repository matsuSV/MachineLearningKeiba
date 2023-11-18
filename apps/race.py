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

        :param race:
        :return:
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

    @staticmethod
    def pre_processing(results):
        """
        解析しやすいように各情報を整形します

        :param results:
        :return:
        """
        df = results.copy()
        print(df)

        # 着順は数字であるものを対象とする（取消などは対象外とする）
        df = df[df['着 順'].astype(str).str.isnumeric()]
        df['着 順'] = df['着 順'].astype(int)

        # 年齢を性と年齢に分ける
        df['性'] = df['性齢'].map(lambda x: str(x)[0])
        df['年齢'] = df['性齢'].map(lambda x: str(x)[1]).astype(int)

        # 馬体重が現体重(±増減値)という表記なので体重と体重変化に分ける
        # df['体重'] = df['馬体重'].str.split("(", expand=True)[0].astype(int)
        # df['体重変化'] = df['馬体重'].str.split("(", expand=True)[1].str[:-1].astype(int)

        '''
        正規表現：
        (\\d+)     : 1つ以上の数字をキャプチャします。
        \\(        : 左括弧 ( にマッチします。
        ([-+]?\\d+): 符号（+ または -）を含む1つ以上の数字をキャプチャします。
        \\)        : 右括弧 ) にマッチします。
        '''
        df[['体重', '体重変化']] = df['馬体重'].str.extract(r'(\d+)\(([-+]?\d+)\)').astype(int)

        # データをint, floatへ変換する
        df['単勝'] = df['単勝'].astype(float)

        # 不要な列を削除する
        df.drop(['タイム', '着差', '調教師', '性齢', '馬体重'], axis=1, inplace=True)

        return df

    @staticmethod
    def clip_out_of_returns(results):
        """
        分析用で4着以下を4着として扱う
        """
        df = results.copy()
        df['rank'] = df['着 順'].map(lambda x: x if x < 4 else 4)

        return df

    @staticmethod
    def get_dummies(results):
        """
        データフレームをダミー変数化する
        """
        df = results.copy()
        df.drop(['着 順', '馬名'], axis=1, inplace=True)

        return pd.get_dummies(df)
