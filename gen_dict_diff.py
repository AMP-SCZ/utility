#!/usr/bin/env python

import sys
from os.path import abspath, dirname, join as pjoin
from os import getcwd, chdir
SCIRPTDIR=dirname(abspath(__file__))

# ground truth dictionary
df1=pd.read_csv(sys.argv[1])
# network's dictionary
df2=pd.read_csv(sys.argv[2])
# network name
network=sys.argv[3]

datestamp=datetime.now().strftime('%Y%m%d')
suffix=f'{network}_{datestamp}'

# when downloaded through GUI
var_header='Variable / Field Name'
form_header='Form Name'
branch_header='Branching Logic (Show field only if...)'
calc_header='Choices, Calculations, OR Slider Labels'

# when downloaded through API
var_header='field_name'
form_header='form_name'
branch_header='branching_logic'
calc_header='select_choices_or_calculations'

ground_groups=df1.groupby(form_header)
target_groups=df2.groupby(form_header)


nonexistent_vars=[]
df_branch=pd.DataFrame(columns=[var_header,'AMP-SCZ logic','Network logic'])
df_branch.set_index(var_header, inplace=True)
df_calc=pd.DataFrame(columns=[var_header,'AMP-SCZ calculation','Network calculation'])
df_calc.set_index(var_header, inplace=True)

for form in ground_groups.groups.keys():
    if form not in target_groups.groups.keys():
        continue
        
    if '_consent_' in form and 'informed_consent_run_sheet' not in form:
        continue
    
    print(form)
    
    dfg= ground_groups.get_group(form)    
    dft= target_groups.get_group(form)
    
    dfg.set_index(var_header, inplace=True)
    dft.set_index(var_header, inplace=True)
    
    for v,row in dfg.iterrows():
        try:
            dft.loc[v]
        except KeyError:
            nonexistent_vars.append(v)
            continue
            
        
        # compare branching logic
        if not pd.isna(row[branch_header]) and row[branch_header]!=dft.loc[v,branch_header]:
            df_branch.loc[v]= [row[branch_header], dft.loc[v,branch_header]]
        
        # compare calculation
        if not pd.isna(row[calc_header]) and row[calc_header]!=dft.loc[v,calc_header]:
            df_calc.loc[v]= [row[calc_header], dft.loc[v,calc_header]]
    


df_var=pd.DataFrame(data={var_header:nonexistent_vars})

dir_bak=getcwd()
chdir(pjoin(SCRIPTDIR,'dict_diff'))
df_var.to_csv(f'ampscz_vars_absent_in_{suffix}.csv', index=False)
df_branch.to_csv(f'branch_logic_diff_ampscz_{suffix}.csv')
df_calc.to_csv(f'calc_diff_ampscz_{suffix}.csv')
chdir(dir_bak)


