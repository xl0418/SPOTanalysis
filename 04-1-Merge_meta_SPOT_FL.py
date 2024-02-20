import pandas as pd
import multiprocess as mp

# set the threshold for the relative abundance
a_thd = 0

# read the geo meta data
geo_meta = pd.read_csv('data/SPOT_Metadata_Seq_Envi_QC.csv')
## remove the rows with Depth.m == 'NaN'; 2 rows
# geo_meta = geo_meta[pd.isna(geo_meta['Depth.m'])]



def generate_df(ii):
    # read the geo meta data
    geo_meta = pd.read_csv('data/SPOT_Metadata_Seq_Envi_QC.csv')
    # read the tag2genome data
    tag2genome = pd.read_csv('data/SPOT_Prokaryotic16S_ASV_dna-sequences_BLASToutput.tsv', sep='\t', header=None)
    blastout_asv = tag2genome.iloc[:, 0].unique()

    # read the tag2sample data relative abundance data
    file_relative_a = 'data/SPOT_Prokaryotic16S_ASV_Table_FL.csv'
    tag2sample = pd.read_csv(file_relative_a, sep=',')

    batch_data = pd.DataFrame(columns=['sample',
                                       'depth',
                                       'temp',
                                       'tag',
                                       'genomeid',
                                       'relative_a'])

    sample1, sample2, sample3, sample4 = geo_meta.iloc[ii, 0].split('_')

    year = int(sample4.split('.')[0])
    month = int(sample4.split('.')[1])
    day = int(sample4.split('.')[2])

    sample = str(year) + '_' + str(month) + '_' + str(day) + '_' + sample2 + '_' + sample3


    depth = geo_meta['Depth.m'].iloc[ii]
    if pd.isna(depth):
        depth = 100
        temp = 10
    elif depth < 300:
        temp = geo_meta['SST'].iloc[ii]
    elif 300 <= depth < 700:
        temp = 7
    elif 700 <= depth < 1200:
        temp = 5
    else:
        print("Depth is not in the range of 0-1200m")
    # Lat = geo_meta['Latitude'][ii]
    # temp = geo_meta['CTDTemp'].iloc[ii]

    # if sample is not in relative abundance data, skip
    if sample in tag2sample.columns[1:]:
        present_tags = tag2sample[tag2sample[sample] > a_thd]
        intersects_asvs = set(present_tags.loc[:, 'OTU_ID']).intersection(set(blastout_asv))
        if len(intersects_asvs) > 0:
            for pres_tag in intersects_asvs:
                relative_a_tag = present_tags[present_tags.loc[:, 'OTU_ID'] == pres_tag][sample].values[0]
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
