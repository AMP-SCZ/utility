from pathlib import Path
import sys
test_dir = Path(__file__).parent
code_dir = test_dir.parent
sys.path.append(str(code_dir))
from subject_files_status_for_dpdash import check_upenn_cnb
import json
import os
import shutil


def create_fake_upenn_json(fake_json: Path, item_nums: int = 2):
    '''Create fake json'''

    fake_json.parent.mkdir(exist_ok=True, parents=True)

    if item_nums == 2:
        fake_dict_list = [
                {"session_battery": "SPLLT-A"},
                {"session_battery": "ProNET_NOSPLLT"}
                ]
    elif item_nums == 1:
        fake_dict_list = [
                {"session_battery": "ProNET_NOSPLLT"}
                ]
    elif item_nums == 3:
        fake_dict_list = [
                ]
    else:
        return fake_json

    with open(fake_json, 'w') as fp:
        json.dump(fake_dict_list, fp)
    return fake_json


def test_check_upenn_cnb():
    subject = 'YA00000'
    phoenix_fake = test_dir / 'test_PHOENIX'
    site = subject[:2]
    subject_raw_path = phoenix_fake / 'PROTECTED' / ('Pronet' + site) / \
            'raw' / subject
    fake_json = subject_raw_path / 'surveys' / f'{subject}.UPENN.json'

    create_fake_upenn_json(fake_json, item_nums=1)
    assert check_upenn_cnb(subject_raw_path) == 0

    create_fake_upenn_json(fake_json, item_nums=2)
    assert check_upenn_cnb(subject_raw_path) == 1

    create_fake_upenn_json(fake_json, item_nums=3)
    assert check_upenn_cnb(subject_raw_path) == 0

    os.remove(fake_json)
    assert check_upenn_cnb(subject_raw_path) == 0

    shutil.rmtree(phoenix_fake)
    
