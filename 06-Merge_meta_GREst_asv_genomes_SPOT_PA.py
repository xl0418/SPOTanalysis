import pandas as pd
import multiprocess as mp

# set the threshold for the relative abundance
a_thd = 0

# read the geo meta data
geo_meta = pd.read_csv('data/SPOT_Metadata_Seq_Envi_QC.csv')



def generate_df(ii):
    # read the geo meta data
    geo_meta = pd.read_csv('data/SPOT_Metadata_Seq_Envi_QC.csv')

    # read the tag2genome data
    tag2genome = pd.read_csv('data/SPOT_Prokaryotic16S_ASV_dna-sequences_BLASToutput.tsv', sep='\t', header=None)

    # read the tag2sample data relative abundance data
    file_relative_a = 'data/SPOT_Prokaryotic16S_ASV_Table_PA.csv'
    tag2sample = pd.read_csv(file_relative_a, sep=',')

    # read the predicted growth rate data
    pred_d = pd.read_csv('data/SPOT_GRest.tsv', sep='\t')

    _, sample1, sample2, sample3 = geo_meta.iloc[ii, 0].split('_')
    year, month, day = sample3.split('.')
    year = int(year)
    month = int(month)

    sample = str(year) + '_' + str(month) + '_1_' + sample1 + '_' + 'PA'

    depth = geo_meta['Depth.m'].iloc[ii]
    # Lat = geo_meta['Latitude'][ii]
    temp = geo_meta['SST'].iloc[ii]
    batch_data = pd.DataFrame(columns=['sample',
                                       'depth',
                                       'temp_SST',
                                       'tag',
                                       'genomeid',
                                       'relative_a',
                                       'd_sT',
                                       'd_vT_PA',
                                       'OGT_PA'])
    # if sample is not in relative abundance data, skip
    if sample in tag2sample.columns:
        present_tags = tag2sample[tag2sample[sample] > a_thd]
        for pres_tag in present_tags.loc[:, 'OTU_ID']:
            relative_a_tag = present_tags[present_tags.loc[:, 'OTU_ID'] == pres_tag][sample].values[0]
            genomes = tag2genome[tag2genome.iloc[:, 0] == pres_tag].iloc[:, 1]
            if genomes.__len__() > 0:
                for genome in genomes.values:
                    matched_genome = pred_d[pred_d['genomeid'] == genome]
                    if matched_genome.__len__() > 0:
                        pred_d_genome = pred_d[pred_d['genomeid'] == genome]['d'].values[0]
                        pred_d_PA_genome = pred_d[pred_d['genomeid'] == genome]['d_PA'].values[0]
                        OGT_PA = pred_d[pred_d['genomeid'] == genome]['OGT_PA'].values[0]


                        temp_df = pd.DataFrame({'sample': sample,
                                                'depth': depth,
                                                'temp_SST': temp,
                                                'tag': pres_tag,
                                                'genomeid': genome,
                                                'relative_a': relative_a_tag,
                                                'd_sT': pred_d_genome,
                                                'd_vT_PA': pred_d_PA_genome,
                                                'OGT_PA': OGT_PA
                                                }, index=[0])

                        batch_data = pd.concat([batch_data, temp_df], ignore_index=True)

    return batch_data


with mp.Pool(processes=(16)) as pool:
    data = pool.map(generate_df, [ii for ii in range(geo_meta.__len__())])

full_data = pd.concat(data, axis=0)

# save the full data
full_data.to_csv('data/SPOT_GRest_meta_PA.csv', index=False)
