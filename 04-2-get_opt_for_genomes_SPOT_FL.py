import pandas as pd
import multiprocessing as mp
import numpy as np
# read all hits file FL or PA
all_hits = pd.read_csv("data/SPOT_fullhits_FL.csv", sep=',')
# replace NaN with 17, NaN only appears in 5m up to 150m
all_hits.loc[:,'temp'].fillna(17, inplace=True)


# combine unique genomes in FL or PA
unique_genomes = all_hits.loc[:, 'genomeid'].unique()


def get_opt_genome(genomeid):
    """
    This function returns the optimal genome for a given genomeid
    """
    genomedf = all_hits[all_hits['genomeid'] == genomeid]
    if genomedf.__len__() > 0:
        # get the mean of the temp
        opt = np.dot(genomedf.loc[:, 'temp'].values, genomedf.loc[:, 'relative_a'].values / genomedf.loc[:,
                                                                                        'relative_a'].values.sum())
        return pd.DataFrame({'genomeid': genomeid, 'opt': opt}, index=[0])
    else:
        return pd.DataFrame()


if __name__ == '__main__':
    with mp.Pool(processes=(16)) as pool:
        data = pool.map(get_opt_genome, unique_genomes)

    opt_genomes = pd.concat(data, axis=0)

    opt_genomes.to_csv('data/SPOT_opt_genomes_FL.csv', index=False)
