
class Place:
    """
    開催年度を受け取り、その年の全会場のレースIDを生成します
    """

    # 開催年度（4桁）: 1956(?) ~
    # 開催地域（2桁）: 01 ~ 10
    # 例）201901010101
    def __init__(self, target_year):
        self.year = target_year

    def make_race_id_list(self):
        """
        開催年度中のレースIDを生成します

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
        race_id_list = []
        for venue in range(1, 11, 1):  # 例）中山開催
            for term in range(1, 6, 1):  # 例）第1回(中山開催)
                for round in range(1, 9, 1):  # 例）(第1回中山開催)1日目
                    for race in range(1, 13, 1):  # 例）(第1回中山開催1日目)1レース
                        race_id = self.year + str(venue).zfill(2) + str(term).zfill(2) + str(round).zfill(2) + str(race).zfill(2)
                        race_id_list.append(race_id)
        return race_id_list
