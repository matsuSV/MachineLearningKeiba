
class Place:
    """
    開催年度を受け取り、その年の全会場のレースIDを生成します
    """

    # 開催年度（4桁）: 1956(?) ~
    # 開催地域（2桁）: 01 ~ 10
    # 例）201901010101
    def __init__(self, target_year):
        self.year = target_year

    def generate_race_ids(self):
        """
        開催年度中の全レースID(例：201901010103)を生成します

        :return: レースIDの配列
        """
        # 01:札幌
        # 02:函館
        # 03:福島
        # 04:新潟
        # 05:東京
        # 06:中山
        # 07:中京
        # 08:京都
        # 09:阪神
        # 10:小倉
        return [self._zf2(self.year, venue, term, stage, race)  # レースID
                for venue in range(1, 11)  # 例）中山開催
                for term in range(1, 6)    # 例）(中山開催) 第1回
                for stage in range(1, 9)   # 例）(中山開催 第1回) 1日目
                for race in range(1, 13)]  # 例）(中山開催 第1回 1日目) 1レース

    @staticmethod
    def _zf2(*args):
        return ''.join(str(arg).zfill(2) for arg in args)
