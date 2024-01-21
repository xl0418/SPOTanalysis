import pandas as pd
import multiprocess as mp

# set the threshold for the relative abundance
a_thd = 0

# read the geo meta data
geo_meta = pd.read_csv('data/SPOT_CTD_Nutrients_BP_5Depths.csv')
# remove the first two rows
geo_meta = geo_meta.iloc[2:, :]


def generate_df(ii):
    # read the geo meta data
    geo_meta = pd.read_csv('data/SPOT_CTD_Nutrients_BP_5Depths.csv')
    # remove the first two rows
    geo_meta = geo_meta.iloc[2:, :]
    # read the tag2genome data
    tag2genome = pd.read_csv('data/SPOT_Prokaryotic16S_ASV_dna-sequences_BLASToutput.tsv', sep='\t', header=None)

    # read the tag2sample data relative abundance data
    file_relative_a = 'data/SPOT_FreeLivingProkaroytes_ASV_2005_2018_5depths.csv'
    tag2sample = pd.read_csv(file_relative_a, sep=',')

    sample1, sample2, sample3 = geo_meta.iloc[ii, 0].split('/')
    depthbin = geo_meta.iloc[ii, 1]
    sample = '20' + sample3 + '_' + sample1 + '_' + sample2 + '_' + depthbin + '_' + 'PA'

    depth = geo_meta['depth'].iloc[ii]
    # Lat = geo_meta['Latitude'][ii]
    temp = geo_meta['CTDTemp'].iloc[ii]
    batch_data = pd.DataFrame(columns=['sample',
                                       'depth',
                                       'temp',
                                       'tag',
                                       'genomeid',
                                       'relative_a'])
    # if sample is not in relative abundance data, skip
    if sample in tag2sample.columns:
        present_tags = tag2sample[tag2sample[sample] > a_thd]
        for pres_tag in present_tags.index:
            relative_a_tag = present_tags[present_tags.index == pres_tag][sample].values[0]
            genomes = tag2genome[tag2genome.iloc[:, 0] == pres_tag].iloc[:, 1]
            if genomes.__len__() > 0:
                for genome in genomes.values:
                    temp_df = pd.DataFrame({'sample': sample,
                                            'depth': depth,
                                            'temp': temp,
                                            'tag': pres_tag,
                                            'genomeid': genome,
                                            'relative_a': relative_a_tag
                                            }, index=[0])

                    batch_data = pd.concat([batch_data, temp_df], ignore_index=True)

    return batch_data


with mp.Pool(processes=(16)) as pool:
    data = pool.map(generate_df, [ii for ii in range(geo_meta.__len__())])

full_data = pd.concat(data, axis=0)

# save the full data
full_data.to_csv('data/SPOT_fullhits_FL.csv', index=False)
