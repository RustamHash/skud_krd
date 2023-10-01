import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as tmd

from modules import File


START_TIME = tmd(hours=12)
END_TIME = tmd(days=1, hours=12)
__df_users = File.users_load()
USERS_LIST = __df_users['ФИО'].tolist()


def parse_data(__df_data, start_date, end_date):
    _l = []
    date_format = "%Y-%m-%d"
    start_date = dt.strptime(start_date, date_format)
    end_date = dt.strptime(end_date, date_format)
    _list_date = pd.date_range(start=start_date, end=end_date)
    _dict_date = {}
    for ind in _list_date:
        _ = {"start": (ind + START_TIME), "end": (ind + END_TIME)}
        _dict_date[ind] = _
    __df_data['date'] = pd.to_datetime(__df_data[0], format="%Y-%m-%d", exact=False).copy()
    __df_data[0] = pd.to_datetime(__df_data[0])
    __df_data = __df_data[__df_data[1].isin(USERS_LIST)].copy()

    for k, v in _dict_date.items():
        _df_new = __df_data[(__df_data[0] >= v['start']) & (__df_data[0] <= v['end'])].copy()
        _df_new['date'] = k
        for user in USERS_LIST:
            _df_user_in = _df_new[(_df_new[1] == user) & (_df_new[2] == 'Вход')].copy()
            _df_user_out = _df_new[(_df_new[1] == user) & (_df_new[2] == 'Выход')].copy()
            _d = {'Дата': k, 'ФИО': user, 'Вход': _df_user_in[0].min(), 'Выход': _df_user_out[0].max()}
            _l.append(_d)
    # noinspection PyTypeChecker
    _df = pd.DataFrame.from_dict( _l, orient='columns')
    _df['Общее'] = _df['Выход'] - _df['Вход']
    _df['Дата'] = pd.to_datetime(_df['Дата'], format="%Y-%m-%d")
    __file_save = File.get_path_save(start_date.date())
    _df.to_excel(__file_save, index=False)
    return _df
