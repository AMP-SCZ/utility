from pathlib import Path
import re
from typing import Union
import sys
import os


'''
Following lines are required in ~/.ssh/config to use the shrotcuts
for the server address, within the corresponding firewall or connected to VPN.

Host prescient
    HostName IP.ADDRESS.FOR.PRESCIENT
    User YOUR-USER-ID
    ProxyCommand ssh RELAY.SERVER.IP.ADDRESS -W %h:%p
    ForwardX11 yes
    ForwardX11Trusted yes
    ForwardAgent yes

Host pronet
    HostName IP.ADDRESS.FOR.PRONT
    User YOUR-USER-ID
    ProxyCommand none
    ForwardX11 yes
    ForwardX11Trusted yes
    ForwardAgent yes
'''

config_dict = {
    'bwh_data_root': '/data/predict1/data_from_nda',
    'prescient_s3_root': '/prescient-test/PHOENIX_ROOT_PRESCIENT',
    'pronet_s3_root': '/prod-ampscz-pronet/PHOENIX_ROOT_PRONET',
    'presc_agg_root': '/mnt/prescient/Prescient_production/PHOENIX',
    'pro_agg_root': '/mnt/ProNET/Lochness/PHOENIX',
    'prescient_server': 'prescient',
    'pronet_server': 'pronet'
    }


def get_s3_path(data_path: Union[Path, str],
                bwh_data_root: str = config_dict['bwh_data_root'],
                prescient_s3_root: str = config_dict['prescient_s3_root'],
                pronet_s3_root: str = config_dict['pronet_s3_root']) -> str:
    '''Return s3 path of a data path on DPACC'''
    data_path = Path(data_path)
    bwh_data_root = Path(bwh_data_root)

    # get network
    network = data_path.relative_to(bwh_data_root).parts[0]

    # get s3 root according to network
    if network == 'Prescient':
        s3_phx_root = Path(prescient_s3_root)
    elif network == 'Pronet':
        s3_phx_root = Path(pronet_s3_root)
    else:
        print(f'No network detected in {data_path}')

    # make relative paths from the PHOENIX path
    local_phoenix_root = data_path.relative_to(
            bwh_data_root / network / 'PHOENIX')

    # get full s3 path
    s3_data_path = 's3:/' + str(s3_phx_root / local_phoenix_root)

    return s3_data_path


def get_agg_server_path(data_path: Union[Path, str],
                        bwh_data_root: str = config_dict['bwh_data_root'],
                        presc_phx_root: str = config_dict['presc_agg_root'],
                        pro_phx_root: str = config_dict['pro_agg_root']) \
                                -> str:
    '''Return s3 path of a data path on DPACC'''
    data_path = Path(data_path)
    bwh_data_root = Path(bwh_data_root)

    # get network
    network = data_path.relative_to(bwh_data_root).parts[0]

    if network == 'Prescient':
        agg_phx_root = Path(presc_phx_root)
    elif network == 'Pronet':
        agg_phx_root = Path(pro_phx_root)
    else:
        print(f'No network detected in {data_path}')

    # make relative paths from the PHOENIX path
    local_phoenix_root = data_path.relative_to(
            bwh_data_root / network / 'PHOENIX')
    agg_data_path = str(agg_phx_root / local_phoenix_root)

    return agg_data_path


def remove_data(data_path: Union[Path, str],
                prescient_server: str = config_dict['prescient_server'],
                pronet_server: str = config_dict['pronet_server'],
                print_only=True) -> None:
    '''Remove data from s3 and data aggregation server'''

    if Path(data_path).is_dir():
        folder = True
    else:
        folder = False

    s3_path = get_s3_path(data_path)
    rm_command = 'rm --recursive' if folder else 'rm'
    s3_command = f'aws s3 {rm_command} {s3_path} --profile dpacc'

    agg_path = get_agg_server_path(data_path)
    rm_command = 'rm -rf' if folder else 'rm'
    if 'prescient' in s3_command.lower():
        agg_command = f"ssh {prescient_server} '{rm_command} {agg_path}'"
    elif 'pronet' in s3_command.lower():
        agg_command = f"ssh {pronet_server} '{rm_command} {agg_path}'"
    else:
        print('No network detected, please check your data path')
        return

    if print_only:
        print(f'{rm_command} {data_path}')
        print(s3_command)
        print(agg_command)
        return

    os.popen(f'{rm_command} {data_path}').read()
    os.popen(s3_command).read()
    os.popen(agg_command).read()


def test_get_path():
    test_path = '/data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED' \
            '/PrescientME/raw/ME00001/mri/ME00001_MR_1900_01_01_1.ZIP'
    s3_path = get_s3_path(test_path)
    agg_path = get_agg_server_path(test_path)

    assert s3_path == 's3://prescient-test/PHOENIX_ROOT_PRESCIENT/' \
        'PROTECTED/PrescientME/raw/ME00001/mri/ME00001_MR_1900_01_01_1.ZIP'

    assert agg_path == '/mnt/prescient/Prescient_production/PHOENIX/' \
            'PROTECTED/PrescientME/raw/ME00001/mri/ME00001_MR_1900_01_01_1.ZIP'
            
    remove_data(test_path)


    test_path = '/data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED' \
            '/PronetYA/raw/YE00001/mri/YE00001_MR_1900_01_01_1.zip'
    s3_path = get_s3_path(test_path)
    agg_path = get_agg_server_path(test_path)

    assert s3_path == 's3://prod-ampscz-pronet/PHOENIX_ROOT_PRONET/' \
        'PROTECTED/PronetYA/raw/YE00001/mri/YE00001_MR_1900_01_01_1.zip'

    assert agg_path == '/mnt/ProNET/Lochness/PHOENIX/' \
            'PROTECTED/PronetYA/raw/YE00001/mri/YE00001_MR_1900_01_01_1.zip'
    remove_data(test_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide file local PHOENIX file path to delete')

    for local_path in sys.argv[1:]:
        if Path(local_path).is_file() or Path(local_path).is_dir():
            remove_data(local_path, print_only=False)
        else:
            print(f'{local_path} does not exist')
