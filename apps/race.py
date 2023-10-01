import pandas as pd
import time
import apps.file as file


class Race:
    """
    レースIDを受け取り、そのレース結果をWebサイトから取得します
    """

    def __init__(self, race_id_list):
        self.race_id_list = race_id_list
        self.downloaded_ids = file.read()
        self.all_races = pd.DataFrame(index=[], columns=[])

    def get_results(self) -> pd.DataFrame:
        self._scrape()
        self._concat_df()
        return self.all_races

    def _scrape(self):
        """
        レースIDを元にネット競馬サイトのHTMLページにあるレース結果のTable要素をDataFrameとして取得します
        """
        for race_id in self.race_id_list:
            if race_id not in self.downloaded_ids:
                try:
                    result = pd.read_html(f'https://db.netkeiba.com/race/{race_id}')[0]
                except IndexError:
                    continue

                self._save_df(result)

    @staticmethod
    def _save_df(result):
        """
        レース結果をIDとデータのKey＆Valueにしてローカルファイルへ保持します

        :param result: サイトからスクレイピングした結果
        """
        # TODO
        # トランザクション処理できるか？
        # レース情報を取得できたら取得済みレースIDとしてファイル保持する（何回も取得させないため）
        result.index = [id] * len(result)
        content = {id: result}
        content.update(read_all_races())

        # レースIDのみとレースID＆レース結果で分けて保持して、レースIDのみファイルを参照することで既に取得済みのレース結果を再取得させない
        write(id)
        write_races(content)
        time.sleep(0.5)  # スクレイピング時の対象サイトへの負荷軽減

    def _concat_df(self):
        """
        取得したレース結果を解析用に１つのDataFrameとします
        pickleとしてローカルファイルへ保持します（趣味で）
        """
        # 各レースのDataFrameを繋げて1つのDataFrameとする
        results = pd.concat(list(read_all_races().values()), sort=False)

        # ファイルに出力して永続化（pickle系のメソッドを使ってみたかっただけ）
        self.all_races = to_pickle(results)

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
