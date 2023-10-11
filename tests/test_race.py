from unittest.mock import patch
import apps.race as race


def test_init():
    """
    期待動作：
    　 Raceクラスを初期化したインスタンス内のメンバ変数が以下の状態となっていること
    　　　race_id_list：コンストラクタへ渡された引数の値
    　　　downloaded_ids：既に取得しているレースID
    　　　all_races：空のデータフレーム
    """
    # read()関数をモックする
    with patch('apps.file.read', return_value=['20190101010101', '20190101010102', '20190101010103']):
        asserted_race = race.Race(['201901010101'])
        assert asserted_race.race_id_list == ['201901010101']
        assert asserted_race.downloaded_ids == ['20190101010101', '20190101010102', '20190101010103']
        assert asserted_race.all_races.empty
