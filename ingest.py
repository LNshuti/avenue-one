import requests
import pandas as pd
import datetime
import pyarrow as pa
import pyarrow.parquet as pq
import boto3

def fetch_data_from_zillow(api_key):
    url = "https://api.example.com/zillow"  # Replace with the actual API endpoint for Zillow

    # Set up request parameters
    params = {
        "api_key": api_key,
        "location": "your_location",
        "property_type": "your_property_type",
        "filters": "your_filters"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        # Process the data as per your requirements
        cleaned_data = preprocess_zillow_data(data)
        return cleaned_data
    except requests.exceptions.RequestException as e:
        print("Error fetching data from Zillow:", e)
        return None

def fetch_data_from_realtor(api_key):
    url = "https://api.example.com/realtor"  # Replace with the actual API endpoint for Realtor.com

    # Set up request parameters
    params = {
        "api_key": api_key,
        "location": "your_location",
        "property_type": "your_property_type",
        "filters": "your_filters"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        # Process the data as per your requirements
        cleaned_data = preprocess_realtor_data(data)
        return cleaned_data
    except requests.exceptions.RequestException as e:
        print("Error fetching data from Realtor.com:", e)
        return None

def preprocess_zillow_data(data):
    # Extract relevant information from the raw data
    # Perform data cleaning and formatting
    # Return the cleaned data as a Pandas DataFrame
    # Example:
    cleaned_data = pd.DataFrame(data["listings"])
    cleaned_data = cleaned_data[["id", "price", "bedrooms", "bathrooms", "sqft"]]
    cleaned_data["price"] = cleaned_data["price"].apply(lambda x: int(x.strip("$").replace(",", "")))
    return cleaned_data

def preprocess_realtor_data(data):
    # Extract relevant information from the raw data
    # Perform data cleaning and formatting
    # Return the cleaned data as a Pandas DataFrame
    # Example:
    cleaned_data = pd.DataFrame(data["listings"])
    cleaned_data = cleaned_data[["id", "price", "beds", "baths", "sqft"]]
    cleaned_data["price"] = cleaned_data["price"].apply(lambda x: int(x.strip("$").replace(",", "")))
    return cleaned_data

def save_data_to_s3(data, bucket_name):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    path = f"{current_date}/data.parquet"
    
    # Convert the Pandas DataFrame to a PyArrow Table
    table = pa.Table.from_pandas(data)
    
    # Write the table as Parquet file in memory
    pq_buffer = pa.BufferOutputStream()
    pq.write_table(table, pq_buffer)
    
    # Save the Parquet file to S3
    bucket.upload_fileobj(pq_buffer, path)


def main():
    zillow_api_key = "your_zillow_api_key"
    realtor_api_key = "your_realtor_api_key"
    aws_access_key = "your_aws_access_key"
    aws_secret_key = "your_aws_secret_key"
    s3_bucket_name = "your_s3_bucket_name"

    # Fetch data from Zillow API
    zillow_data = fetch_data_from_zillow(zillow_api_key)
    if zillow_data is not None:
        # Save Zillow data to AWS S3 bucket
        save_data_to_s3(zillow_data, s3_bucket_name)

    # Fetch data from Realtor.com API
    realtor_data = fetch_data_from_realtor(realtor_api_key)
    if realtor_data is not None:
        # Save Realtor.com data to AWS S3 bucket
        save_data_to_s3(realtor_data, s3_bucket_name)

if __name__ == "__main__":
    main()