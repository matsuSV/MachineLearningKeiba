from unittest.mock import patch
from apps.race import Race


def test_init():
    # read()関数をモックする
    with patch('apps.file.read', return_value=['20190101010101', '20190101010102', '20190101010103']):
        race = Race(['201901010101'])
        assert race.race_id_list == ['201901010101']
        assert race.downloaded_ids == ['20190101010101', '20190101010102', '20190101010103']
        assert race.all_races.empty
