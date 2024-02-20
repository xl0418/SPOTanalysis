import pandas as pd
import multiprocessing as mp
# read  the data
p16ns_d_est = pd.read_csv("data/SPOT_GRest_meta_PA.csv", sep=',')

unique_tags = p16ns_d_est['tag'].unique()

def get_d_est_for_asvs(tag):
    tag_df = p16ns_d_est[p16ns_d_est['tag'] == tag]
    mean_d_tag_sT = tag_df['d_sT'].mean()
    mean_d_tag_vT = tag_df['d_vT_PA'].mean()
    # unique tag_df by depth, sample, and Lat
    unique_tag_df = tag_df.drop_duplicates(subset=['depth', 'sample'])
    unique_tag_df = unique_tag_df.loc[:, ['depth', 'sample', 'relative_a', 'temp_SST', 'tag', 'OGT_FL']]
    # add mean_d_tag to unique_tag_df
    unique_tag_df['mean_d_sT'] = mean_d_tag_sT
    unique_tag_df['mean_d_vT'] = mean_d_tag_vT
    return unique_tag_df

if __name__ == '__main__':
    # parallelize the process
    with mp.Pool(processes = (16)) as pool:
        data = pool.map(get_d_est_for_asvs, unique_tags)

    mean_d_tag_df = pd.concat(data, axis=0)

    mean_d_tag_df.to_csv('data/SPOT_mean_d_meta_PA.csv', index=False)
