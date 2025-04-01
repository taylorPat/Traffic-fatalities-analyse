# https://www.nhtsa.gov/file-downloads?p=nhtsa/downloads/FARS/1975/National/

import pathlib
import requests
import zipfile
import io
import kagglehub
from kaggle.api.kaggle_api_extended import KaggleApi


#print("Path to dataset files:", path)

def download_data():
    api = KaggleApi()
    api.authenticate()
    path = api.dataset_download_file(
        dataset="aniket0712/parking-transactions",
        file_name="Parking_Transactions.csv",
        path="/home/patrick/Traffic-fatalities-analyse/data",
        quiet=False
        )
    print(path)



if __name__ == "__main__":
    download_data()