# -*- coding: utf-8 -*-
"""python_section_2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/182SEoGXb4APqijXx3pQeC97niwSEvxqN
"""

import pandas as pd
import numpy as np

def calculate_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame): DataFrame containing columns 'From', 'To', and 'Distance'

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Extract unique locations
    locations = pd.concat([df['From'], df['To']]).unique()
    n = len(locations)

    # Initialize the distance matrix with infinity
    distance_matrix = pd.DataFrame(np.inf, index=locations, columns=locations)

    # Set the diagonal to 0
    np.fill_diagonal(distance_matrix.values, 0)

    # Populate the matrix with the direct distances
    for _, row in df.iterrows():
        distance_matrix.at[row['From'], row['To']] = row['Distance']
        distance_matrix.at[row['To'], row['From']] = row['Distance']  # Ensure symmetry

    # Apply the Floyd-Warshall algorithm to calculate cumulative distances
    for k in locations:
        for i in locations:
            for j in locations:
                if distance_matrix.at[i, k] + distance_matrix.at[k, j] < distance_matrix.at[i, j]:
                    distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]

    return distance_matrix
    df = pd.read_csv('C:\\Users\\Lenovo\\Downloads\\dataset-2.csv')
    distance_matrix = calculate_distance_matrix(df)
    print(distance_matrix)

import pandas as pd

def unroll_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame): Distance matrix with toll locations as index and columns.

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Initialize a list to hold the unrolled data
    unrolled_data = []

    # Iterate over the index and columns of the DataFrame
    for id_start in df.index:
        for id_end in df.columns:
            if id_start != id_end:  # Exclude the same id_start and id_end
                distance = df.at[id_start, id_end]
                if distance < float('inf'):  # Only include valid distances
                    unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    # Convert the list of dictionaries to a DataFrame
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df

# Usage example:
# Assuming distance_matrix is calculated from the previous question
# distance_matrix = ...  # Removed the indentation here
# unrolled_df = unroll_distance_matrix(distance_matrix)
# print(unrolled_df) #Removed the indentation here

import pandas as pd

def find_ids_within_ten_percentage_threshold(df: pd.DataFrame, reference_id: int) -> pd.DataFrame:
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame): DataFrame containing 'id_start', 'id_end', and 'distance' columns.
        reference_id (int): The ID to use as a reference for calculating the average distance.

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Calculate average distance for the reference_id
    avg_distance_ref = df[df['id_start'] == reference_id]['distance'].mean()

    # Calculate the 10% threshold
    lower_bound = avg_distance_ref * 0.90
    upper_bound = avg_distance_ref * 1.10

    # Calculate average distances for each id_start
    avg_distances = df.groupby('id_start')['distance'].mean().reset_index()

    # Filter for IDs within the 10% threshold
    filtered_ids = avg_distances[(avg_distances['distance'] >= lower_bound) &
                                  (avg_distances['distance'] <= upper_bound)]

    # Sort the resulting DataFrame by id_start
    sorted_ids = filtered_ids.sort_values(by='id_start')

    return sorted_ids

# Usage example (uncomment the line below to use):
# The following two lines were incorrectly indented
# unrolled_df = ...  # Assume this is the result from the previous question
# reference_id = 1  # Example reference ID
# result_df = find_ids_within_ten_percentage_threshold(unrolled_df, reference_id)
# print(result_df)

import pandas as pd

def calculate_toll_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame containing 'id_start', 'id_end', and 'distance' columns.

    Returns:
        pandas.DataFrame: DataFrame with additional columns for toll rates for each vehicle type.
    """
    # Define the rate coefficients for each vehicle type
    rates = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    # Calculate toll rates by multiplying distance with the respective rates
    for vehicle, rate in rates.items():
        df[vehicle] = df['distance'] * rate

    return df

# Usage example (uncomment the line below to use):
# unrolled_df = ...  # Assume this is the result from the previous question
# toll_rates_df = calculate_toll_rate(unrolled_df)
# print(toll_rates_df)

import pandas as pd
import datetime

def calculate_time_based_toll_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame): DataFrame containing toll rates for different vehicle types.

    Returns:
        pandas.DataFrame: DataFrame with additional columns for time-based toll rates.
    """
    # Define the time intervals and corresponding discount factors
    time_discount_factors = {
        'weekday': {
            (datetime.time(0, 0), datetime.time(10, 0)): 0.8,
            (datetime.time(10, 0), datetime.time(18, 0)): 1.2,
            (datetime.time(18, 0), datetime.time(23, 59, 59)): 0.8,
        },
        'weekend': 0.7,
    }

    # Create a new DataFrame to store the results
    results = []

    # Define days of the week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Iterate through each unique id_start and id_end pair
    for _, row in df.iterrows():
        id_start = row['id_start']
        id_end = row['id_end']

        # For each day of the week
        for day in days_of_week:
            if day in days_of_week[:5]:  # Weekdays
                for time_range, factor in time_discount_factors['weekday'].items():
                    start_time, end_time = time_range
                    results.append({
                        'id_start': id_start,
                        'id_end': id_end,
                        'start_day': day,
                        'start_time': start_time,
                        'end_day': day,
                        'end_time': end_time,
                        'moto': row['moto'] * factor,
                        'car': row['car'] * factor,
                        'rv': row['rv'] * factor,
                        'bus': row['bus'] * factor,
                        'truck': row['truck'] * factor
                    })
            else:  # Weekends
                for hour in range(24):  # Full 24 hours
                    time = datetime.time(hour, 0)
                    results.append({
                        'id_start': id_start,
                        'id_end': id_end,
                        'start_day': day,
                        'start_time': time,
                        'end_day': day,
                        'end_time': time,
                        'moto': row['moto'] * time_discount_factors['weekend'],
                        'car': row['car'] * time_discount_factors['weekend'],
                        'rv': row['rv'] * time_discount_factors['weekend'],
                        'bus': row['bus'] * time_discount_factors['weekend'],
                        'truck': row['truck'] * time_discount_factors['weekend']
                    })

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    return results_df

# Usage example (uncomment the line below to use):
# toll_rates_df = ...  # Assume this is the result from the previous question
# time_based_toll_rates_df = calculate_time_based_toll_rates(toll_rates_df)
# print(time_based_toll_rates_df)