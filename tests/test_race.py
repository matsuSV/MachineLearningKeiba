# from unittest.mock import patch
import apps.race as apps_race
import pandas as pd
from pandas.util.testing import assert_frame_equal


def test_init():
    """
    期待動作：
    　 Raceクラスを初期化したインスタンス内のメンバ変数が以下の状態となっていること
    　　　race_id_list：コンストラクタへ渡された引数の値
    """
    # read()関数をモックする(リファクタリングして使わなくなった、けど参考として残している)
    # with patch('apps.file.read', return_value=['20190101010101', '20190101010102', '20190101010103']):
    race = apps_race.Race(['201901010101'])
    assert race.race_id_list == ['201901010101']


def test__scrape():
    """
    期待動作：
    　 １．存在するレースIDの場合、レース情報がDataFrameで取得できること
       2. 存在しないレースIDの場合、空のDataFrameが取得できること
    """
    # 1. exists race page
    actual_df = apps_race.Race._scrape('201901010101')
    expected_df = pd.read_csv('csv/test__scrape.csv')
    assert_frame_equal(actual_df, expected_df)

    # 2. nothing
    actual_df = apps_race.Race._scrape('101901010101')
    expected_df = pd.DataFrame()
    assert_frame_equal(actual_df, expected_df)
