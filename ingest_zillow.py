import os
from dotenv import load_dotenv
import requests
import pandas as pd

# Load environment variables from .env file
load_dotenv()

def fetch_data_from_zillow():
    api_key = os.getenv("API_KEY")
    base_url = "https://api.bridgedataoutput.com/api/v2/zgecon/"
    endpoint = "marketreport"
    url = f"{base_url}{endpoint}?access_token={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["bundle"]

    # Handle API request error
    print("Error fetching data from Zillow API.")
    return None

def preprocess_zillow_data(data):
    # Preprocess and clean Zillow data
    # Example data cleaning steps:
    df = pd.DataFrame(data)
    df = df.dropna()  # Remove rows with missing values
    # Apply other data cleaning and transformations as needed
    return df

def save_data_to_csv(data, file_path):
    # Save data to CSV file
    data.to_csv(file_path, index=False)
    print("Data saved to", file_path)

def main():
    # Step 2: Fetch data from Zillow API
    zillow_data = fetch_data_from_zillow()
    if zillow_data is not None:
        # Step 3: Preprocess and clean the data
        cleaned_data = preprocess_zillow_data(zillow_data)

        # Step 4: Save the cleaned data to a CSV file
        save_data_to_csv(cleaned_data, "zillow_data.csv")

if __name__ == "__main__":
    main()
