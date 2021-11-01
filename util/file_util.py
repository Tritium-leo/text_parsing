import json
# import pandas as pd
import os
import shutil


def read_json(file_path) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def dump_json(content, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False)


def dump_excel(data, file_path):
    df = pd.DataFrame(data)
    print(df)
    # 保存到本地excel
    df.to_excel(file_path, index=False)


def dump_excel_sheet(sheets: dict, file_path):
    writer = pd.ExcelWriter(file_path)
    for sheet_name, data in sheets.items():
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name=sheet_name)
    writer.save()


def dump_csv(data, file_path):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)


def read_csv(file_path):
    df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
    return df.to_dict('records')


def path_util(dir_path: str, cover_path=False,del_path=False) -> str:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    elif cover_path:
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    if os.path.exists(dir_path) and del_path:
        shutil.rmtree(del_path)
    return dir_path
