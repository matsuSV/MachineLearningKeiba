import apps.race as apps_race
import pandas as pd
from pandas.util.testing import assert_frame_equal
from unittest.mock import patch


def test__init__():
    """
    期待動作：
    　 Raceクラスを初期化したインスタンス内のメンバ変数が以下の状態となっていること
    　　　race_id_list：コンストラクタへ渡された引数の値
    """
    race = apps_race.Race(['201901010101'])
    assert race.race_id_list == ['201901010101']


def test_get_results():
    # file関連の関数をモックする
    with patch('apps.file.read', return_value=['20190101010101', '20190101010102', '20190101010103']):
        with patch('apps.file.to_pickle', return_value=pd.DataFrame()):
            race = apps_race.Race(['201901010101'])
            actual_df = race.get_results()
            expected_df = pd.DataFrame()
            assert_frame_equal(actual_df, expected_df)


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


def test__classify():
    race = apps_race.Race(['201901010101'])
    test_scraped = pd.read_csv('csv/test__scrape.csv')
    test_scraped.index = ['201901010101'] * len(test_scraped)

    actual_result = race._classify('201901010101', test_scraped)
    # ↓の比較で出来ていると思う( ´∀｀ )
    assert all((k, v) in actual_result.items() for (k, v) in {'201901010101': test_scraped}.items())
