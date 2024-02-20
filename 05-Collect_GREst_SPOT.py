import json
import pandas as pd
import os
import numpy as np

dir = "prokkaSPOT/"
file_FL = pd.read_csv("data/SPOT_opt_genomes_FL.csv",sep=',')
file_PA = pd.read_csv("data/SPOT_opt_genomes_PA.csv",sep=',')

file = pd.concat([file_FL, file_PA], ignore_index=True)


data_df = pd.DataFrame()


for genomeid in file.iloc[:,0].unique():
    est_file = dir + str(genomeid) + "/" + str(genomeid) + "_growth_est.json"
    if os.path.isfile(est_file):
        with open(est_file) as f:
            data = json.load(f)
            data['genomeid'] = genomeid
            data['OGT_FL'] = np.nan
            data['d_FL'] = np.nan
            data['LowerCI_FL'] = np.nan
            data['UpperCI_FL'] = np.nan
            data['OGT_PA'] = np.nan
            data['d_PA'] = np.nan
            data['LowerCI_PA'] = np.nan
            data['UpperCI_PA'] = np.nan
            # print(data["CUBHE"])

    est_file_FL = dir + str(genomeid) + "/" + str(genomeid) + "_growth_est_tempopt_FL.json"
    if os.path.isfile(est_file_FL):
        with open(est_file_FL) as f:
            data_FL = json.load(f)
            data['OGT_FL'] = data_FL['OGT']
            data['d_FL'] = data_FL['d']
            data['LowerCI_FL'] = data_FL['LowerCI']
            data['UpperCI_FL'] = data_FL['UpperCI']

    est_file_PA = dir + str(genomeid) + "/" + str(genomeid) + "_growth_est_tempopt_PA.json"
    if os.path.isfile(est_file_PA):
        with open(est_file_PA) as f:
            data_PA = json.load(f)
            data['OGT_PA'] = data_PA['OGT']
            data['d_PA'] = data_PA['d']
            data['LowerCI_PA'] = data_PA['LowerCI']
            data['UpperCI_PA'] = data_PA['UpperCI']
    data_df = pd.concat([data_df, pd.DataFrame(data, index=[0])], ignore_index=True)

data_df.to_csv("data/SPOT_GRest.tsv", sep='\t', index=False)
