import json
import pandas as pd
import os
dir = "prokkaSPOT/"
file = pd.read_csv("data/SPOT_opt_genomes_FL.csv",sep=',')
data_df = pd.DataFrame()
data_temp_df = pd.DataFrame()

for genomeid in file.iloc[:,0].unique():
    est_file = dir + str(genomeid) + "/" + str(genomeid) + "_growth_est.json"
    if os.path.isfile(est_file):
        with open(est_file) as f:
            data = json.load(f)
            data['genomeid'] = genomeid
            data_df = pd.concat([data_df, pd.DataFrame(data, index=[0])], ignore_index=True)
            # print(data["CUBHE"])

    est_temp_file = dir + str(genomeid) + "/" + str(genomeid) + "_growth_est_tempopt.json"
    if os.path.isfile(est_temp_file):
        with open(est_temp_file) as f:
            data = json.load(f)
            data['genomeid'] = genomeid
            data_temp_df = pd.concat([data_df, pd.DataFrame(data, index=[0])], ignore_index=True)

data_df.to_csv("data/SPOT_EstG_genome_sameT.tsv", sep='\t', index=False)
data_temp_df.to_csv("data/SPOT_EstG_genome_variableT.tsv", sep='\t', index=False)
