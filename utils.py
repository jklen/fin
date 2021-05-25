import pandas as pd
from scipy.spatial import distance
import pyfolio as pf
from sklearn.preprocessing import StandardScaler

def concat_top(d):
    
    dfs_topn = {}
    for name in d.keys():
        dff = d[name]['dataframe'].apply(lambda x: x.nlargest(d[name]['topn']) if d[name]['type'] == 'largest' else x.nsmallest(d[name]['topn']))
        dfs_topn[name] = dff
    
    dfs_results = {}
    for name in dfs_topn.keys():
        dfs_results[name] = dfs_topn[name]
        
    df = pd.concat(dfs_results,axis=1).swaplevel(axis = 'columns')\
        .sort_index(level = 0, axis = 'columns')
    return df


def calculate_distance(x, df2, stat_weights):
    dic = {}
    
    # get dictionary of pyfolio stats combinations
    for col2 in df2.columns:
        common_index = x.to_frame().dropna().join(df2[col2].to_frame().dropna(), how = 'inner').index
        s1_returns = x[x.index.isin(common_index)].pct_change().dropna()
        s2_returns = df2.loc[df2.index.isin(common_index), col2].pct_change().dropna()

        s1_stats = pf.timeseries.perf_stats(returns = s1_returns).to_frame().T
        s1_stats.index = [x.name]
        s2_stats = pf.timeseries.perf_stats(returns = s2_returns).to_frame().T
        s2_stats.index = [col2]

        df = pd.concat([s1_stats, s2_stats])
        
        dic[col2] = {}
        dic[col2]['df'] = df
    
    # make one big df from the dictionary of combinations for fitting scaler
    df = pd.DataFrame(columns = df.columns)    
    for i in dic.keys():
        df = pd.concat([df, dic[i]['df']])
    scaler = StandardScaler()
    scaler.fit(df)
    
    # calculating distance
    for i in dic.keys():
        df = dic[i]['df']
        s = scaler.transform(df)
        dic[i]['scaled df'] = pd.DataFrame(s, index = df.index, columns = df.columns)
        dist = distance.cdist(s, s, 'euclidean', w = stat_weights if stat_weights else None)[0, 1]
        dic[i]['distance'] = dist
    
    distances = pd.Series([dic[i]['distance'] for i in dic.keys()], index = dic.keys())
        
    return distances
                       
def calculate_dist(df1, df2, stat_weights = None):
    df_result = df1.apply(calculate_distance, args = (df2, stat_weights))
    return df_result

            
            