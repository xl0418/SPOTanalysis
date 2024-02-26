import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime

# read the data
spot_fl = pd.read_csv("data/SPOT_mean_d_meta_FL.csv", sep=',')

unique_sample = spot_fl['sample'].unique()
plot_df = pd.DataFrame()
for sampleid in unique_sample:
    sample_df = spot_fl[spot_fl['sample'] == sampleid]
    mean_maxg_vt = np.dot(np.log(2) / sample_df['mean_d_vT'], sample_df['relative_a']/ sample_df['relative_a'].sum())
    mean_maxg_st = np.dot(np.log(2) / sample_df['mean_d_sT'], sample_df['relative_a']/ sample_df['relative_a'].sum())
    depth = sample_df['depth'].mean()
    depth_cat = sampleid.split('_')[3]
    sampleid_date = '_'.join(sampleid.split('_')[0:3])
    data_sample = datetime.strptime(sampleid_date, '%Y_%m_%d').strftime('%m/%d/%Y')
    plot_df = pd.concat([plot_df, pd.DataFrame({'sample':sampleid,
                                                'mean_maxg_vt':mean_maxg_vt,
                                                'mean_maxg_st':mean_maxg_st,
                                                'date': data_sample,
                                                'depth': depth,
                                                'depth_cat': depth_cat}, index=[0])], ignore_index=True)

plot_df['log_mean_maxg_vt'] = np.log(plot_df['mean_maxg_vt'])
plot_df['log_mean_maxg_st'] = np.log(plot_df['mean_maxg_st'])


### plot plot_df with seaborn along depth in time with scatters colored by mean_maxg_vt
sns.set(style="white")
fig, ax = plt.subplots(figsize=(20, 10))
ax = sns.scatterplot(x="date", y="depth", data=plot_df, hue="log_mean_maxg_st", palette="viridis", s=100)
plt.xticks(rotation=90)
# reverse y axis
plt.gca().invert_yaxis()
plt.show()


### plot boxplot along depth
sns.set(style="white")
fig, ax = plt.subplots(figsize=(10, 10))
ax = sns.boxplot(x="depth_cat", y="mean_maxg_vt", data=plot_df)
plt.show()

plot_df.depth.unique()