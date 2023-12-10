import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    car=pd.DataFrame()
    car=pd.read_csv('/workspaces/MapUp-Data-Assessment-F/datasets/dataset-1.csv')
    df=car.pivot(index='id_1',columns='id_2',values='car')
    df=df.fillna(0)
    return df

def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df=pd.read_csv('/workspaces/MapUp-Data-Assessment-F/datasets/dataset-1.csv')
    df['car_type']=pd.cut(df['car'],bins=[-float('inf'),15,25,float('inf')],labels=['low','medium','high'])
    type_count=df['car_type'].value_counts()
    count_dict=type_count.to_dict()
    count_dict=dict(sorted(count_dict.items()))
    return count_dict


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    df=pd.read_csv('/workspaces/MapUp-Data-Assessment-F/datasets/dataset-1.csv')
    mean=df['bus'].mean()
    indexes=df[df['bus']>2*mean].index.tolist()
    indexes.sort()
    return indexes

def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    df=pd.read_csv('/workspaces/MapUp-Data-Assessment-F/datasets/dataset-1.csv')
    avg=df.groupby('route')['truck'].mean()
    routes=avg[avg>7].index.tolist()
    routes.sort()
    return routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    df=pd.DataFrame()
    mod_matrix=generate_car_matrix(df)
    matrix=mod_matrix.applymap(lambda x: x*0.75 if x>20 else x*1.25)  
    matrix=matrix.round(1) 
    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df=pd.read_csv('/workspaces/MapUp-Data-Assessment-F/datasets/dataset-2.csv')
    df['start_datetime']=pd.to_datetime(df['startDay']+' '+df['startTime'],format='%A %H:%M:%S')
    df['end_datetime']=pd.to_datetime(df['endDay']+' '+df['endTime'],format='%A %H:%M:%S')
    grouped=df.groupby(['id','id_2'])
    check=grouped.apply(check_completeness)
    return check

def check_completeness(group):
    start_times=group['start_datetime'].dt.time
    end_times=group['end_datetime'].dt.time

    days_of_week=set(group['start_datetime'].dt.day_name())
    days_complete=set(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
    start_times_coverage = all(start_time <= pd.Timestamp('23:59:59').time() for start_time in start_times)
    end_times_coverage = all(end_time >= pd.Timestamp('00:00:00').time() for end_time in end_times)
    days_of_week_coverage = days_of_week == days_complete

    return start_times_coverage and end_times_coverage and days_of_week_coverage

