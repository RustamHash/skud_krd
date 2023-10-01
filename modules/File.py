import pandas as pd
from pathlib import Path

path_file_users = r"D:\Общая\Книга1.xlsx"
PATH_SKUD = r"D:\Общая\skud"


def get_path_save(__date):
    __file_name = f"{__date}.xlsx"
    __file = Path(PATH_SKUD, __file_name)
    return __file

def users_load():
    __df_users = pd.read_excel(path_file_users)
    return __df_users


def __read_files(__file_names):
    df = pd.DataFrame()
    for __file_name in __file_names:
        _df = pd.read_csv(__file_name, sep="\t", encoding='cp1251', header=None)
        df = pd.concat([df, _df], axis=0)
    return df


def __path_join(start_date_path, end_date_path):
    __start_path = Path(PATH_SKUD, start_date_path)
    __end_path = Path(PATH_SKUD, end_date_path)
    __l = [__start_path, __end_path]
    return __l


def __get_files_folders(__list_path):
    __files = []
    for __path in __list_path:
        _l = [str(f.absolute()) for f in __path.glob("**/*")]
        __files += _l
    if len(__files) < 1:
        return False
    return __files


def data_load(start_date_path, end_date_path):
    __list_path = __path_join(start_date_path, end_date_path)
    __files = __get_files_folders(__list_path=__list_path)
    if not __files:
        return False
    __df = __read_files(__files)
    return __df
