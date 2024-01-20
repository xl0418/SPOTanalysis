import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import pandas as pd

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

meang_lat_depth_df = pd.DataFrame(columns=['depth', 'Lat', 'meang', 'shannond'])
for depthid in full_data['depth'].unique():
    for latid in full_data['Lat'].unique():
        # calculate the mean max g weighted by relative a in depth for each sample
        matchedid = (full_data['depth']==depthid) & (full_data['Lat']==latid)
        if matchedid.sum() > 0:
            norm_relative_a = full_data[matchedid]['relative_a'].values / full_data[matchedid]['relative_a'].values.sum()
            meang = np.dot(full_data[matchedid]['maxg'].values,norm_relative_a)
            shannond = -np.sum(norm_relative_a * np.log(norm_relative_a))
            meang_lat_depth_df = pd.concat([meang_lat_depth_df, pd.DataFrame({'depth':np.round(depthid,2), 'Lat':np.round(latid, 2), 'meang':meang, 'shannond':shannond}, index=[0])], ignore_index=True)





lat = meang_lat_depth_df['Lat']
depth = meang_lat_depth_df['depth']

plot_what = "shannond"

if plot_what == "meang":
    d = np.log(2) / meang_lat_depth_df['meang']
    orgname = 'P16NS mean growth rates'
    save_name = 'figures/P16NS_mean_growth_rates.png'
elif plot_what == "shannond":
    d = meang_lat_depth_df['shannond']
    orgname = 'P16NS Shannon diversity'
    save_name = 'figures/P16NS_Shannon_diversity.png'



def f_Interp600(lat, depth, d, orgname, save_name):
    # data coordinates and values
    x = lat
    y = depth
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
    im0 = plt.contourf(xi[:598,:],yi[:598,:],zi[:598,:], cmap = 'viridis')
    plt.ylim([0,600])
    plt.xlim(-70,60)
    cbar = plt.colorbar()
    #cbar.ax.locator_params(nbins = 5)
    cbar.ax.tick_params(labelsize=16)
    cbar.ax.set_title('H', fontsize = 18)
    plt.title(orgname, fontsize = 18, loc = 'left')
    #plt.clim(0,3)
    #May 2023:
    #plt.plot(x,y,‘k.’, markersize = 3)
    plt.scatter(np.array(x),np.array(y),color='#1a1a1a', s = 15)
    plt.xlabel('Latitude',fontsize=16)
    plt.ylabel('Depth (m)',fontsize=16)
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(save_name, dpi = 1000)
    print('Plotted and Saved: ' + orgname)


f_Interp600(lat, depth, d, orgname, save_name)


