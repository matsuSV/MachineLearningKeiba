# from unittest.mock import patch
import apps.race as apps_race


def test_init():
    """
    期待動作：
    　 Raceクラスを初期化したインスタンス内のメンバ変数が以下の状態となっていること
    　　　race_id_list：コンストラクタへ渡された引数の値
    　　　downloaded_ids：既に取得しているレースID
    　　　pd_all_races：空のデータフレーム
    """
    # read()関数をモックする
    # with patch('apps.file.read', return_value=['20190101010101', '20190101010102', '20190101010103']):
    race = apps_race.Race(['201901010101'])
    assert race.race_id_list == ['201901010101']
    # assert race.downloaded_ids == ['20190101010101', '20190101010102', '20190101010103']


def test__scrape():
    """

    :return:
    """
    # exists race page
    df = apps_race.Race._scrape('201901010101')
    print(df)



    # nothing
