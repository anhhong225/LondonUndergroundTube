# import requests
# import zipfile
# import io
# import pandas as pd

# # Step 1: Download the zip file from the TfL API
# url = 'https://api.tfl.gov.uk/stationdata/tfl-stationdata-detailed.zip'

# response = requests.get(url)

# # Unzip the file content
# with zipfile.ZipFile(io.BytesIO(response.content)) as z:
#     z.extractall("tfl_station_data")

import requests
import zipfile
import io

def download_and_extract(url, extract_to):
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(extract_to)

# URLs to download
urls = ['https://api.tfl.gov.uk/stationdata/tfl-stationdata-detailed.zip']

# Extract to the same folder
for url in urls:
    download_and_extract(url, "tfl_station_data")
