import apps.race as apps_race
import apps.process as apps_process
import pandas as pd
from pandas.util.testing import assert_frame_equal
from unittest.mock import patch


def test__init__():
    """
    期待動作：
    　 Processクラスを初期化したインスタンス内のメンバ変数が以下の状態となっていること
    　　　df：コンストラクタへ渡された引数の値
    """
    test_201901010101 = pd.read_csv('csv/test__scrape.csv')
    test_201901010102 = pd.read_csv('csv/test__scrape.csv')
    test_201901010101.index = ['201901010101'] * len(test_201901010101)
    test_201901010102.index = ['201901010102'] * len(test_201901010102)

    with patch('apps.file.read_all_races',
               return_value={'201901010101': test_201901010101, '201901010102': test_201901010102}):
        df = apps_race.Race._create_df()
        process = apps_process.Process(df)
        assert_frame_equal(process.df, df)


def test_allow_only_numbers():
    """
    期待動作：
    　 データフレームの「着順」列が数字のみであること
    """
    test_201901010101 = pd.read_csv('csv/test__scrape.csv')
    test_201901010102 = pd.read_csv('csv/test__scrape.csv')
    test_201901010101.index = ['201901010101'] * len(test_201901010101)
    test_201901010102.index = ['201901010102'] * len(test_201901010102)

    with patch('apps.file.read_all_races',
               return_value={'201901010101': test_201901010101, '201901010102': test_201901010102}):
        df = apps_race.Race._create_df()
        process = apps_process.Process(df)
        process.allow_only_numbers()
        assert process.df['着 順'].astype(str).str.isnumeric().all(), "着順列に数字以外のデータが含まれています"
