import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import griddata
from datetime import date


def f_Interp(xaxis, yaxis, d, orgname, save_name, todepth = 900):
    # data coordinates and values
    x = xaxis
    y = yaxis
    z = d
    # target grid to interpolate to
    xi = np.arange(np.min(x),np.max(x),1)
    yi = np.arange(np.min(y),np.max(y),1)
    xi,yi = np.meshgrid(xi,yi)
    # interpolate
    zi = griddata((x,y),z,(xi,yi),method='linear') #also: nearest, cubic
    # plot
    fig = plt.figure(figsize = (14,7))
    #fig = plt.figure(figsize = (5,2.2))
    ax = fig.add_subplot(111)
    im0 = plt.contourf(xi[:todepth,:],yi[:todepth,:],zi[:todepth,:], cmap = 'viridis')
    plt.ylim([-5,todepth])
    # plt.xlim(-70,60)
    cbar = plt.colorbar()
    #cbar.ax.locator_params(nbins = 5)
    cbar.ax.tick_params(labelsize=16)
    cbar.ax.set_title('H', fontsize = 18)
    plt.title(orgname, fontsize = 18, loc = 'left')
    #plt.clim(0,3)
    #May 2023:
    #plt.plot(x,y,‘k.’, markersize = 3)
    plt.scatter(np.array(x),np.array(y),color='#1a1a1a', s = 15)
    plt.xlabel('Time',fontsize=16)
    plt.ylabel('Depth (m)',fontsize=16)
    plt.xticks(fontsize = 13)
    plt.yticks(fontsize = 13)
    # set x label to date for 10 ticks
    xticks = np.linspace(x.min(), x.max(), 10)
    xticks = np.round(xticks, 0)
    xticks = xticks.astype(int)
    # convert to date
    xlabel = []
    for eachtick in xticks:
        d = date(2005, 1, 19) + pd.Timedelta(days=eachtick)
        xlabel.append(d.strftime('%Y-%m-%d'))
    plt.gca().set_xticks(xticks)
    plt.gca().set_xticklabels(xlabel)
    # rotate x labels
    plt.xticks(rotation=45)
    # plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(save_name, dpi = 1000)
    print('Plotted and Saved: ' + orgname)




# read the data
full_data = pd.read_csv('data/SPOT_FreeLivingProkaroytes_ASV_2005_2018_5depths.csv')
geo_meta = pd.read_csv('data/SPOT_CTD_Nutrients_BP_5Depths.csv')
geo_meta = geo_meta.iloc[2:,:]
geo_meta.insert(geo_meta.shape[1], 'sample', np.nan)

for ii in range(geo_meta.shape[0]):
    sample1, sample2, sample3 = geo_meta.iloc[ii, 0].split('/')
    depthbin = geo_meta.iloc[ii, 1]
    sample = '20' + sample3 + '_' + sample1 + '_' + sample2 + '_' + depthbin + '_' + 'FL'
    # add sample column
    geo_meta['sample'].iloc[ii] = sample
    if sample not in full_data.columns:
        print(sample)

print("The number of samples is: ", full_data.shape[1]-1)
print("The number of ASVs is: ", full_data.index.unique().shape)

sample_richness_shannon = pd.DataFrame(columns=['sample', 'richness', 'shannon', 'temp', 'Depth', 'Date', 'Days'])

samples_in_full_data = full_data.columns[:-1]

# read est for asv
est_asv = pd.read_csv('data/SPOT_1hits_FL.csv', sep=',')

for sample in samples_in_full_data:
    date1, date2, date3, depth, type = sample.split('_')
    date_sample = date1 + '_' + date2 + '_' + date3

    d0 = date(2005, 1, 19)
    d1 = date(int(date1), int(date2), int(date3))
    delta = d1 - d0
    # print(delta.days)
    # replace DCM with 100m
    if depth == 'DCM':
        depth = '100m'
    # remove the 'm' in depth and convert to int
    depth = depth.replace('m', '')
    depth = int(depth)

    sample_data = full_data[sample]
    relative_abund_asv = sample_data.values / sum(sample_data.values)
    relative_abund_asv = relative_abund_asv[relative_abund_asv>0]

    # calculate the weighted mean d
    asv_d_df = est_asv[est_asv['sample']==sample]
    abund_weighted_d = np.dot(asv_d_df['maxg'].values, asv_d_df['relative_a'].values / sum(asv_d_df['relative_a'].values))

    sample_richness_shannon = pd.concat([sample_richness_shannon,
                                         pd.DataFrame({'sample':sample,
                                                       'richness':sum(sample_data > 0),
                                                       'shannon':-np.sum(relative_abund_asv *np.log(relative_abund_asv)),
                                                       'temp':geo_meta[geo_meta['sample'] == sample]['CTDTemp'].values,
                                                       'Depth':depth,
                                                       'Date': date_sample,
                                                       'Days': delta.days,
                                                       'mean_maxg': np.log(2) / abund_weighted_d})], ignore_index=True)

# plot the heatmap of the richness and shannon index in depth with the Date on x axis
plt.figure(figsize=(10, 6))
ax = sns.scatterplot(y='Depth', x='Date', s = 80, data=sample_richness_shannon, hue='richness', palette='RdBu_r')
plt.gca().invert_yaxis()
# vertical x labels
plt.xticks(rotation=90)
plt.title('Richness')

norm = plt.Normalize(sample_richness_shannon['richness'].min(), sample_richness_shannon['richness'].max())
sm = plt.cm.ScalarMappable(cmap="RdBu_r", norm=norm)
sm.set_array([])
# Remove the legend and add a colorbar
ax.get_legend().remove()
cbar = plt.colorbar(
    sm,
    ax=plt.gca()
)



# interpolation

f_Interp(sample_richness_shannon['Days'].values,
         sample_richness_shannon['Depth'].values,
         sample_richness_shannon['richness'].values,
         'Richness',
         'SPOT_richness.png')

f_Interp(sample_richness_shannon['Days'].values,
         sample_richness_shannon['Depth'].values,
         sample_richness_shannon['shannon'].values,
         'Shannon',
         'SPOT_shannon.png')

f_Interp(sample_richness_shannon['Days'].values,
         sample_richness_shannon['Depth'].values,
         sample_richness_shannon['mean_maxg'].values,
         'Shannon',
         'SPOT_meanmaxg.png')















sample_richness_shannon['Lon'].unique()

# plot the heatmap of the richness and shannon index in depth with the Lat on x axis
plt.figure(figsize=(10, 6))
ax = sns.scatterplot(y='Depth', x='Lat', s = 80, data=sample_richness_shannon, hue='richness', palette='RdBu_r')
plt.gca().invert_yaxis()
plt.title('Richness')

norm = plt.Normalize(sample_richness_shannon['richness'].min(), sample_richness_shannon['richness'].max())
sm = plt.cm.ScalarMappable(cmap="RdBu_r", norm=norm)
sm.set_array([])
# Remove the legend and add a colorbar
ax.get_legend().remove()
cbar = plt.colorbar(
    sm,
    ax=plt.gca()
)

# save
plt.savefig('figures/P16NS_richness.png', dpi=300)



plt.figure(figsize=(10, 6))
ax = sns.scatterplot(y='Depth', x='Lat', s = 80, data=sample_richness_shannon, hue='shannon', palette='RdBu_r')
plt.gca().invert_yaxis()
plt.title('shannon')

norm = plt.Normalize(sample_richness_shannon['shannon'].min(), sample_richness_shannon['shannon'].max())
sm = plt.cm.ScalarMappable(cmap="RdBu_r", norm=norm)
sm.set_array([])
# Remove the legend and add a colorbar
ax.get_legend().remove()
cbar = plt.colorbar(
    sm,
    ax=plt.gca()
)

# save
plt.savefig('figures/P16NS_shannon.png', dpi=300)


# Check ASV numbers
asv_raw = pd.read_csv('data/221117-1910.P16N-S.16S.dna-sequences.fasta', sep='\t', header=None)

asvs = []
for each_asv in asv_raw[0]:
    if each_asv[0] == '>':
        asvs.append(each_asv.split('>')[1])
asvs_df = pd.DataFrame({'asvid':asvs})

print("The number of ASVs in the raw asv file is: ", asvs_df['asvid'].unique().shape)
print("After blasting...")

blast_asv_file = pd.read_csv('data/221117-1910.P16N-S.16S.dna-sequences.tsv', sep='\t', header=None)

print("The number of ASVs in the blast file is: ", blast_asv_file[0].unique().shape)
print("The number of genomes in the blast file is: ", blast_asv_file[1].unique().shape)


###########################################################################
 #####################      Plot the growth rate      #####################
###########################################################################

# read the full data
# estimate using default temperature
full_data_type1 = pd.read_csv('data/P16NS_full_data_1hit.csv')
# estimate using overall abundance ranked for genomes
full_data_type2 = pd.read_csv('data/P16NS_full_data_1hit_temp2.csv')


print("The number of samples in type1 is: ", full_data_type1['sample'].unique().shape)
print("The number of tags in type1 is: ", full_data_type1['tag'].unique().shape)
print("The number of genomes in type1 is: ", full_data_type1['genomeid'].unique().shape)


# filter dCUB
full_data_type1 = full_data_type1[full_data_type1['dCUB']<-0.08]
full_data_type2 = full_data_type2[full_data_type2['dCUB']<-0.08]


# filter nHE
full_data_type1 = full_data_type1[full_data_type1['nHE']>10]
full_data_type2 = full_data_type2[full_data_type2['nHE']>10]


data1 = full_data_type1.loc[:, ['depth', 'maxg', 'relative_a', 'Lat']]
data2 = full_data_type2.loc[:, ['depth', 'maxg', 'relative_a', 'Lat']]
data1['type'] = 1
data2['type'] = 2

full_data = pd.concat([data1, data2], axis=0)


# remove the outliers
full_data = full_data[full_data['maxg']<100]

full_data = full_data[full_data['type']==2]

meang_lat_depth_df = pd.DataFrame(columns=['Depth', 'Lat', 'd', 'shannond'])
for depthid in full_data['depth'].unique():
    for latid in full_data['Lat'].unique():
        # calculate the mean max g weighted by relative a in depth for each sample
        matchedid = (full_data['depth']==depthid) & (full_data['Lat']==latid)
        if matchedid.sum() > 0:
            norm_relative_a = full_data[matchedid]['relative_a'].values / full_data[matchedid]['relative_a'].values.sum()
            meang = np.dot(full_data[matchedid]['maxg'].values,norm_relative_a)
            shannond = -np.sum(norm_relative_a * np.log(norm_relative_a))
            meang_lat_depth_df = pd.concat([meang_lat_depth_df, pd.DataFrame({'Depth':np.round(depthid,2), 'Lat':np.round(latid, 2), 'd':meang, 'shannond':shannond}, index=[0])], ignore_index=True)

meang_lat_depth_df['maxg'] = np.log(2) / meang_lat_depth_df['d']

# plot the heatmap of the richness and shannon index in depth with the Lat on x axis
plt.figure(figsize=(10, 6))
ax = sns.scatterplot(y='Depth', x='Lat', s = 80, data=meang_lat_depth_df, hue='maxg', palette='RdBu_r')
plt.gca().invert_yaxis()
plt.title('Mean maximum growth rates')

norm = plt.Normalize(meang_lat_depth_df['maxg'].min(), meang_lat_depth_df['maxg'].max())
sm = plt.cm.ScalarMappable(cmap="RdBu_r", norm=norm)
sm.set_array([])
# Remove the legend and add a colorbar
ax.get_legend().remove()
cbar = plt.colorbar(
    sm,
    ax=plt.gca()
)

# save
plt.savefig('figures/P16NS_meang.png', dpi=300)