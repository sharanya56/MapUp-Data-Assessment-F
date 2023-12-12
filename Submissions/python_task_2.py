import pandas as pd
from datetime import datetime,time, timedelta
import networkx as nx


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    matrix=pd.read_csv('/home/codespace/MapUp-Data-Assessment-F/datasets/dataset-3.csv')
    G=nx.DiGraph() #directed Graph
    for _, row in matrix.iterrows():
       G.add_edge(row['id_start'],row['id_end'],distance=row['distance'])
       G.add_edge(row['id_end'],row['id_start'],distance=row['distance'])
       nodes=list(G.nodes())
       df=pd.DataFrame(index=nodes,columns=nodes)

       for start_node in nodes:
          for end_node in nodes:
             if start_node==end_node:
                df.at[start_node,end_node]=0.0
             elif nx.has_path(G,start_node,end_node):
                 distance=nx.shortest_path_length(G,start_node,end_node,weight='distance')
                 df.at[start_node,end_node]=distance
             else:
                 df.at[start_node,end_node]=float('nan')
    return df



def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    matrix=calculate_distance_matrix(df)

    unroll_dist=[]
    for id_start in matrix.columns:
        for id_end in matrix.columns:
            if id_start != id_end:
                try:
                    distance = matrix.at[id_start, id_end]
                except KeyError:
                    distance = float('nan')
                unroll_dist.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    df=pd.DataFrame(unroll_dist)
    return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    matrix=unroll_distance_matrix(df)
    avg_distance=matrix[matrix['id_start']==reference_id]['distance'].mean()

    lower_bound=avg_distance*0.9
    upper_bound=avg_distance*1.1

    result_df=matrix[(matrix['distance']>= lower_bound)&(matrix['distance']<= upper_bound) ]
    df=sorted(result_df['id_start'].unique())
    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    matrix=unroll_distance_matrix(df)
    rate_coef ={ 'moto':0.8, 'car':1.2,'rv':1.5,'bus':2.2,'truck':3.6}

    for vehicle_type, rate_coefficient in rate_coef.items():
        matrix[vehicle_type]=matrix['distance']*rate_coefficient
    df=matrix
    return df

    
def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    
    return df

