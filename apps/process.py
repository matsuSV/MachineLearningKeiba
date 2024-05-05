import pandas as pd


class Process:
    """
    解析しやすいように各情報を整形します
    """

    def __init__(self, df):
        self.df = df.copy()

    def allow_only_numbers_order_of_finish(self):
        """
        着順は数字であるものを対象とする（取消や中止などは対象外とする）
        """
        self.df = self.df[self.df['着 順'].astype(str).str.isnumeric()]
        self.df['着 順'] = self.df['着 順'].astype(int)

    def parse_gender_and_age(self):
        """
        年齢を性と年齢に分ける
        """
        self.df['性'] = self.df['性齢'].map(lambda x: str(x)[0])
        self.df['年齢'] = self.df['性齢'].map(lambda x: str(x)[1]).astype(int)

    def parse_weight_and_change(self):
        """
        正規表現：
        (\\d+)     : 1つ以上の数字をキャプチャします。
        \\(        : 左括弧 ( にマッチします。
        ([-+]?\\d+): 符号（+ または -）を含む1つ以上の数字をキャプチャします。
        \\)        : 右括弧 ) にマッチします。
        """
        # 馬体重が現体重(±増減値)という表記なので体重と体重変化に分ける
        # df['体重'] = df['馬体重'].str.split("(", expand=True)[0].astype(int)
        # df['体重変化'] = df['馬体重'].str.split("(", expand=True)[1].str[:-1].astype(int)
        self.df[['体重', '体重変化']] = self.df['馬体重'].str.extract(r'(\d+)\(([-+]?\d+)\)').astype(int)

    def convert_data_type(self):
        """
        単勝カラムのデータ型をfloatへ変換する
        """
        self.df['単勝'] = self.df['単勝'].astype(float)

    def delete_columns(self):
        """
        分析に不要な列は削除する
        """
        self.df.drop(['タイム', '着差', '調教師', '性齢', '馬体重'], axis=1, inplace=True)

    def clip_out_of_returns(self):
        """
        分析用で4着以下を4着として扱う
        """
        self.df['rank'] = self.df['着 順'].map(lambda x: x if x < 4 else 4)

    @staticmethod
    def get_dummies(results):
        """
        データフレームをダミー変数化する
        """
        df = results.copy()
        df.drop(['着 順', '馬名'], axis=1, inplace=True)

        return pd.get_dummies(df)

    def pre_processing(self):
        """
        解析しやすいように各情報を整形します

        :return: 加工したデータフレーム
        """
        self.allow_only_numbers_order_of_finish()
        self.parse_gender_and_age()
        self.parse_weight_and_change()
        self.convert_data_type()
        self.delete_columns()
        self.clip_out_of_returns()

        return self.df
