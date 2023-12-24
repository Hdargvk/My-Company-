import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from itertools import combinations
from datetime import time


def calculate_distance_matrix(csv_file):
    # Load the dataset from the CSV file
    data = pd.read_csv(r"C:\Users\Dell\Downloads\dataset-3.csv")

    # Extract IDs and numeric features from the dataset
    ids = data["id_start"]
    features = data.drop("id_start", axis=1)

    # Calculate the distance matrix using Euclidean distances
    distance_matrix = pd.DataFrame(
        euclidean_distances(features), index=ids, columns=ids
    )

    return distance_matrix


# Example usage:
csv_file_path = "path/to/dataset-3.csv"
result_matrix = calculate_distance_matrix(csv_file_path)

# Display the resulting distance
print(result_matrix)


def unroll_distance_matrix(distance_matrix):
    # Get the unique IDs from the distance_matrix DataFrame
    unique_ids = distance_matrix.index.tolist()

    # Initialize lists to store unrolled data
    id_start_list = []
    id_end_list = []
    distance_list = []

    # Iterate over the unique IDs to create combinations
    for id_start in unique_ids:
        for id_end in unique_ids:
            # Exclude same id_start to id_end combinations
            if id_start != id_end:
                # Append values to lists
                id_start_list.append(id_start)
                id_end_list.append(id_end)
                distance_list.append(distance_matrix.at[id_start, id_end])

    # Create a DataFrame from the lists
    unrolled_df = pd.DataFrame(
        {"id_start": id_start_list, "id_end": id_end_list, "distance": distance_list}
    )

    return unrolled_df


# Example usage:
result_unrolled = unroll_distance_matrix(result_matrix)
print(result_unrolled)

import pandas as pd


def find_ids_within_ten_percentage_threshold(input_df, reference_value):
    # Filter rows with the given reference_value as id_start
    reference_rows = input_df[input_df["id_start"] == reference_value]

    # Calculate the average distance for the reference_value
    average_distance = reference_rows["distance"].mean()

    # Calculate the threshold values (10% above and below the average)
    lower_threshold = average_distance - 0.1 * average_distance
    upper_threshold = average_distance + 0.1 * average_distance

    # Filter rows within the 10% threshold
    within_threshold_rows = input_df[
        (input_df["distance"] >= lower_threshold)
        & (input_df["distance"] <= upper_threshold)
    ]

    # Get the unique values from the id_start column and sort them
    result_list = sorted(within_threshold_rows["id_start"].unique().tolist())

    return result_list


# Example usage:
reference_value = 1
result_within_threshold = find_ids_within_ten_percentage_threshold(
    result_unrolled, reference_value
)
print(result_within_threshold)


def calculate_toll_rate(unrolled_df):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {"moto": 0.8, "car": 1.2, "rv": 1.5, "bus": 2.2, "truck": 3.6}

    # Add columns for toll rates based on vehicle types
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        unrolled_df[vehicle_type] = unrolled_df["distance"] * rate_coefficient

    return unrolled_df


# Example usage:
result_with_toll_rates = calculate_toll_rate(result_unrolled)
print(result_with_toll_rates)

import pandas as pd
from datetime import time, datetime, timedelta


def calculate_time_based_toll_rates(input_df):
    # Define time ranges and discount factors
    time_ranges = [
        {
            "start": time(0, 0, 0),
            "end": time(10, 0, 0),
            "weekday_discount": 0.8,
            "weekend_discount": 0.7,
        },
        {
            "start": time(10, 0, 0),
            "end": time(18, 0, 0),
            "weekday_discount": 1.2,
            "weekend_discount": 0.7,
        },
        {
            "start": time(18, 0, 0),
            "end": time(23, 59, 59),
            "weekday_discount": 0.8,
            "weekend_discount": 0.7,
        },
    ]

    # Create a list to store rows for the output DataFrame
    output_rows = []

    # Iterate over each unique (id_start, id_end) pair
    for _, group in input_df.groupby(["id_start", "id_end"]):
        id_start, id_end = _

        # Iterate over each day of the week
        for day_index, day_name in enumerate(
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        ):
            for time_range in time_ranges:
                # Calculate start and end datetime for the current time range
                start_datetime = datetime.combine(
                    datetime.today(), time_range["start"]
                ) + timedelta(days=day_index)
                end_datetime = datetime.combine(
                    datetime.today(), time_range["end"]
                ) + timedelta(days=day_index)

                # Apply the weekday or weekend discount factor
                discount_factor = (
                    time_range["weekday_discount"]
                    if day_index < 5
                    else time_range["weekend_discount"]
                )

                # Create a row for the output DataFrame
                output_row = {
                    "id_start": id_start,
                    "id_end": id_end,
                    "distance": group["distance"].iloc[0],
                    "start_day": day_name,
                    "start_time": start_datetime.time(),
                    "end_day": day_name,
                    "end_time": end_datetime.time(),
                    "moto": group["moto"].iloc[0] * discount_factor,
                    "car": group["car"].iloc[0] * discount_factor,
                    "rv": group["rv"].iloc[0] * discount_factor,
                    "bus": group["bus"].iloc[0] * discount_factor,
                    "truck": group["truck"].iloc[0] * discount_factor,
                }

                # Append the row to the output_rows list
                output_rows.append(output_row)

    # Create the output DataFrame
    output_df = pd.DataFrame(output_rows)

    return output_df


# Example usage:
result_with_time_based_toll_rates = calculate_time_based_toll_rates(
    result_with_toll_rates
)
print(result_with_time_based_toll_rates)
