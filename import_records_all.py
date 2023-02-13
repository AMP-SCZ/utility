#!/usr/bin/env python

import pandas as pd

import socket
from urllib3.connection import HTTPConnection

HTTPConnection.default_socket_options = (
    HTTPConnection.default_socket_options + [
        (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
        (socket.SOL_TCP, socket.TCP_KEEPIDLE, 60),
        (socket.SOL_TCP, socket.TCP_KEEPINTVL, 10),
        (socket.SOL_TCP, socket.TCP_KEEPCNT, 6)
    ]
)

"""
# from tcp man page
TCP_KEEPCNT (since Linux 2.4)
      The maximum number of keepalive probes TCP should send before dropping the connection.  This option should  not
      be used in code intended to be portable.

TCP_KEEPIDLE (since Linux 2.4)
      The  time  (in  seconds) the connection needs to remain idle before TCP starts sending keepalive probes, if the
      socket option SO_KEEPALIVE has been set on this socket.  This option should not be used in code intended to  be
      portable.

TCP_KEEPINTVL (since Linux 2.4)
      The  time (in seconds) between individual keepalive probes.  This option should not be used in code intended to
      be portable.

"""

import requests
import sys
import json
from copy import deepcopy
from tempfile import NamedTemporaryFile
from os import remove, stat, getcwd, chdir, stat
from os.path import isfile, abspath, basename, dirname, join as pjoin
from numpy import save, load
from hashlib import md5
from glob import glob


if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage: {abspath(__file__)} CA00007.json forms-dir API_TOKEN /path/to/date_offset.csv 1
forms-dir is the directory with *_DataDictionary_*.csv and *_InstrumentDesignations_*.csv files
optional: date_offset.csv is the file with 1/0 upload bit
optional: 1 is for force re-upload''')
    exit(0)


if sys.argv[-1]=='1':
    pass
else:
    subject=basename(sys.argv[1]).split('.')[0]
    
    hashfile=abspath(sys.argv[4])
    if isfile(hashfile):

        dfshift=pd.read_csv(hashfile)
        dfshift.set_index('subject',inplace=True)

        # skip unchanged JSONs
        if subject in dfshift.index and dfshift.loc[subject,'upload']==0:
            print(sys.argv[1], 'has not been modified, skipping')
            exit()
         # if a subject is not in dfshift.index, that got downloaded after date_offset.csv was created
         # that is a new one and we let it upload
    
    else:
        print('Could not find {}, so force uploading {}'.format(hashfile,sys.argv[1]))


dirbak= getcwd()
chdir(sys.argv[2])
dfdict= pd.read_csv(glob('*_DataDictionary_*')[0], on_bad_lines='skip', engine='python')
dfevent= pd.read_csv(glob('*_InstrumentDesignations_*')[0], on_bad_lines='skip', engine='python')
chdir(dirbak)


forms_group= dfdict.groupby('Form Name')
events_group= dfevent.groupby('unique_event_name')


with open(sys.argv[1]) as f:
    data= json.load(f)


for visit in data:
    data2= []
    
    redcap_event_name= visit['redcap_event_name']
    
    
    print(redcap_event_name)

    for form in events_group.get_group(redcap_event_name)['form']:
        data2= []
        data1={
            'chric_record_id': data[0]['chric_record_id'],
            'redcap_event_name': redcap_event_name
        }

        empty=True
        data_form={}
        for v in forms_group.get_group(form)['Variable / Field Name']:
            # try/except block for bypassing nonexistent vars in JSON
            # also for bypassing empty forms
            try:
                if visit[v]:
                    # leave checkbox variables out of consideration
                    # to decide whether a form is empty
                    if '___' not in v:
                        empty=False
                    data_form[v]= visit[v]
            except:
                pass
        
        
        completion= f'{form}_complete'
        # bypass empty forms
        # essential for showing blank circles in REDCap record status dashboard
        if empty:
            continue
        # calculated fields may still pose a form as non-empty
        # see how REDCap circles are colored
        # https://user-images.githubusercontent.com/35086881/168111407-d99c0a49-d33c-4cd9-9530-79f0debd9690.png

        '''
        REDCap policy
        value  color  meaning
        ''     Blank  Incomplete (no data saved)
        0      Red    Incomplete
        1      Yellow Unverified
        2      Green  Complete
        '''
        
        print('\t',form)

        data1.update(data_form)
        data1[completion]= visit[completion]
        
        
        data2.append(data1)


        # save it as text and load it back to avoid REDCap import error
        fw= NamedTemporaryFile('w', delete=False)
        json.dump(data2,fw)
        fw.close()

        with open(fw.name) as f:
            data2= f.read()

        remove(fw.name)


        fields = {
            'token': sys.argv[3],
            'content': 'record',
            'action': 'import',
            'format': 'json',
            'type': 'flat',
            'data': data2,
            'overwriteBehavior': 'normal',
            'returnContent': 'count',
            'returnFormat': 'json'
        }
        
        try:
            r = requests.post('https://redcap.partners.org/redcap/api/', data= fields)
        except requests.exceptions.ConnectionError:
            print('Failed due to ConnectionResetError')

        print('\t HTTP Status: ' + str(r.status_code))
        print('\t',r.json())

        print('')

