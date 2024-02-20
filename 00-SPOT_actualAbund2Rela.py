import pandas as pd
from time import sleep
from tqdm import tqdm

# read SPOT_combine_16S_18SwMetazoa_ASV_Jan2001_Aug2018_QC.csv
spot_actual_abund = pd.read_csv("data/SPOT_Prokaryotic16S_ASV_Table.csv", sep=',')
old_relative_abund = pd.read_csv("data/SPOT_FreeLivingProkaroytes_ASV_2005_2018_5depths.csv", sep=',')

spot_actual_abund.columns.values.__len__()
old_relative_abund.columns.values.__len__()


FL_df = pd.DataFrame({'OTU_ID':spot_actual_abund.index})
PA_df = pd.DataFrame({'OTU_ID':spot_actual_abund.index})

new_col_names = spot_actual_abund.columns.values

for i in tqdm(range(1,len(new_col_names))):
    dt, depth, env, date = new_col_names[i].split('_')
    year, month, day = date.split('.')
    # string to int
    year = int(year)
    month = int(month)
    day = int(day)
    if env == 'FL':
        FL_colname = str(year) + '_'  + str(month) + '_' + str(day) + '_' + depth + '_' + 'FL'
        relative_abund = spot_actual_abund.iloc[:,i].values / spot_actual_abund.iloc[:,i].values.sum()
        FL_df[FL_colname] = relative_abund
    elif env == 'PA':
        PA_colname = str(year) + '_'  + str(month) + '_' + str(day) + '_' + depth + '_' + 'PA'
        relative_abund = spot_actual_abund.iloc[:,i].values / spot_actual_abund.iloc[:,i].values.sum()
        PA_df[PA_colname] = relative_abund
    else:
        print('error')

    sleep(0.1)

FL_df.to_csv('data/SPOT_Prokaryotic16S_ASV_Table_FL.csv', index=False)
PA_df.to_csv('data/SPOT_Prokaryotic16S_ASV_Table_PA.csv', index=False)