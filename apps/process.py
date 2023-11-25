

class Process:
    """
    解析しやすいように各情報を整形します
    """

    def __init__(self, df):
        self.df = df.copy()

    def allow_only_numbers(self):
        """
        着順は数字であるものを対象とする（取消や中止などは対象外とする）
        """
        self.df = self.df[self.df['着 順'].astype(str).str.isnumeric()]
        self.df['着 順'] = self.df['着 順'].astype(int)


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
