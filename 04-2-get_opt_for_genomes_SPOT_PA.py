import pandas as pd
import multiprocessing as mp

# read all hits file FL or PA
all_hits = pd.read_csv("data/SPOT_fullhits_PA.csv", sep=',')
all_hits = all_hits[all_hits['temp'] != 'No data']
all_hits = all_hits[all_hits['depth'] != 'No data']

# change Dtype of depth and temp to float
all_hits['depth'] = all_hits['depth'].astype(int)
all_hits['temp'] = all_hits['temp'].astype(float)
# combine unique genomes in FL or PA
unique_genomes = all_hits.loc[:,'genomeid'].unique()

def get_opt_genome(genomeid):
    """
    This function returns the optimal genome for a given genomeid
    """
    genomedf = all_hits[all_hits['genomeid']==genomeid]
    if genomedf.__len__() > 0:
        # get the top 1% of the relative_a
        genomedf = genomedf.sort_values(by='relative_a', ascending=False)
        genomedf = genomedf.iloc[:int(genomedf.__len__()/100),:]
        # get the mean of the temp
        opt = genomedf['temp'].values.astype(float).mean()
        return pd.DataFrame({'genomeid':genomeid, 'opt':opt}, index=[0])
    else:
        return pd.DataFrame()

if __name__ == '__main__':
    with mp.Pool(processes = (16)) as pool:
        data = pool.map(get_opt_genome, unique_genomes)

    opt_genomes = pd.concat(data, axis=0)

    opt_genomes.to_csv('data/SPOT_opt_genomes_PA.csv', index=False)