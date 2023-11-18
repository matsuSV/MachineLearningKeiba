import apps.place as place


def test_init():
    """
    期待動作：
    　 Placeクラスを初期化したインスタンス内のメンバ変数が以下の状態となっていること
    　　　year：コンストラクタへ渡された引数の値
    """
    asserted_place = place.Place("2019")
    assert asserted_place.year == "2019"


def test_generate_race_ids():
    """
    期待動作：
    　 対象年度に開催される全場のレースIDが生成できること
    　　　len(race_ids)：全場のレースID数
         race_ids[0] : 札幌開催の第1回の1日目の1レース
         race_ids[4799] : 小倉開催の第5回（最終回）の8日目（最終日）の12レース（最終走）
    """
    test_place = place.Place("2019")
    race_ids = test_place.generate_race_ids()
    assert len(race_ids) == 4800
    assert race_ids[0] == "201901010101"
    assert race_ids[4799] == "201910050812"


def test__zf2():
    """
    期待動作：
    　 引数として渡した値を最小2桁の左側0埋めを行い連結した文字列を生成すること
    """
    test_place = place.Place("2019")
    actual_result = test_place._zf2("2019", "1", "2", "3", "40")
    assert actual_result == "201901020340"
