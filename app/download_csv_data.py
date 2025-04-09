from kaggle.api.kaggle_api_extended import KaggleApi
import kaggle

def download_csv(
    dataset_name: str, download_directory: str, download_csv_file_name: str
) -> str:
    _ = kaggle.api.dataset_download_files(dataset_name, path=download_directory, unzip=True, quiet=False)
    # api = KaggleApi()
    # api.authenticate()
    # _ = api.dataset_download_file(
    #     dataset=dataset_name,
    #     file_name=download_csv_file_name,
    #     path=download_directory,  # "~/Traffic-fatalities-analyse/data"
    #     quiet=False,
    # )
    return f"{download_directory}/{download_csv_file_name}"  # "~/Traffic-fatalities-analyse/data/Parking_Transactions.csv"
