import requests
from datetime import datetime
from google.cloud import storage
from google.cloud import storage_transfer
import os


from satellitecrops.params import GOOGLE_APPLICATION_CREDENTIALS
from satellitecrops.params import GCP_PROJECT, BUCKET_NAME
from satellitecrops.params import DATA_DIR_LOCAL

import json

# Customized stdout printing
from colorama import Fore, Style

def get_satellite_data(bbox, year, datetime_range, limit=200):
    '''Return urls of SAFE files (Standard Archive Format for Europe)
    standardly use for exchanging Earth Observation data (eo features),
    that correspond to the specified year, datetime_range and bbox.
    The SAFE file contains the different channels images (TrueColorImage, B2 etc)
    as well as description files.
    The datetime_range is a string with the following format "2024-01-01T00:00:00Z/2024-03-31T23:59:59Z"
    ATTENTION: if the datetime_range is too long, the number of results can become very large
    causing the API to not respond. For this concern, we suggest using per_trimester requests or
    even per_month requests. The size of the bbox influences also the number of results.
    Returns:
    A list of urls and a dict of properties
    Example:
    bbox_landes = [-1.52487, 43.487949, 0.136726,44.532196]
    datetime_range = "2019-08-01T00:00:00Z/2019-08-31T12:31:12Z"
    year = 2019
    get_satellite_data(bbox_landes, year, datetime_range, limit=2)
    '''
    url = 'https://earth-search.aws.element84.com/v1/search'
    data={"bbox": bbox,
         "datetime": datetime_range,
         "collections":["sentinel-2-l2a"],
         "limit": limit}
    response = requests.post(url, json=data).json()
    print(f"Number of matches: {response['numberMatched']}, number returned = {response['numberReturned']}")
    urls = []
    properties_dict = {}
    for feature in response['features']:
        urls.extend(get_urls_from_eo_feature(feature))
        properties = eo_feature2properties_dict(feature)
        properties_dict[properties['id']]=properties
    return urls, properties_dict

def get_satellite_data_per_trimester(bbox, year, trimester, limit=200):
    '''Return urls of SAFE files (Standard Archive Format for Europe),
    standardly use for exchanging Earth Observation data (eo features),
    that correspond to the specified year, trimester and bbox.
    The SAFE file contains the different channels images (TrueColorImage, B2 etc)
    as well as description files.
    ATTENTION: if the number of results is too large the API may not respond.
    For this concern, you can try with per_month requests.
    The size of the bbox influences the number of results.
    Returns:
    A list of urls and a dict of properties'''
    trimester_dateranges = {
        1: f"{year}-01-01T00:00:00Z/{year}-03-31T23:59:59Z",
        2: f"{year}-04-01T00:00:00Z/{year}-06-30T23:59:59Z",
        3: f"{year}-07-01T00:00:00Z/{year}-09-30T23:59:59Z",
        4: f"{year}-10-01T00:00:00Z/{year}-12-31T23:59:59Z",
    }
    return get_satellite_data(bbox, year, trimester_dateranges[trimester], limit)


def get_satellite_data_per_month(bbox, year, month, limit=100):
    '''Return urls of SAFE files (Standard Archive Format for Europe)
    standardly use for exchanging Earth Observation data (eo features),
    that correspond to the specified year, month and bbox.
    The SAFE file contains the different channels images (TrueColorImage, B2 etc)
    as well as description files.
    ATTENTION: if the number of results is too large the API may not respond.
    The size of the bbox influences the number of results.
    Returns:
    A list of urls and a dict of properties'''
    month_dateranges = {
        1: f"{year}-01-01T00:00:00Z/{year}-01-31T23:59:59Z",
        2: f"{year}-02-01T00:00:00Z/{year}-02-28T23:59:59Z",
        3: f"{year}-03-01T00:00:00Z/{year}-03-31T23:59:59Z",
        4: f"{year}-04-01T00:00:00Z/{year}-04-30T23:59:59Z",
        5: f"{year}-05-01T00:00:00Z/{year}-05-31T23:59:59Z",
        6: f"{year}-06-01T00:00:00Z/{year}-06-30T23:59:59Z",
        7: f"{year}-07-01T00:00:00Z/{year}-07-31T23:59:59Z",
        8: f"{year}-08-01T00:00:00Z/{year}-08-31T23:59:59Z",
        9: f"{year}-09-01T00:00:00Z/{year}-09-30T23:59:59Z",
        10: f"{year}-10-01T00:00:00Z/{year}-10-31T23:59:59Z",
        11: f"{year}-11-01T00:00:00Z/{year}-11-30T23:59:59Z",
        12: f"{year}-12-01T00:00:00Z/{year}-12-31T23:59:59Z"
    }
    return get_satellite_data(bbox, year, month_dateranges[month], limit)

def get_satellite_data_per_year(bbox, year, limit=200):
    '''Return urls of SAFE files (Standard Archive Format for Europe)
    standardly use for exchanging Earth Observation data (eo features),
    that correspond to the specified year, trimester and bbox.
    The SAFE file contains the different channels images (TrueColorImage, B2 etc)
    as well as description files.
    ATTENTION: this function uses get_satellite_data_per_month to ensure that
    the number of results per request is not too large.
    However, the size of the bbox influences the number of results too (it can be
    a cause of the API not responding).
    Returns:
    A list of urls and a dict of properties'''
    urls = []
    properties_dict = {}
    for month in range(1, 13):
        month_urls, month_properties = get_satellite_data_per_month(bbox, year, month, limit)
        urls.extend(month_urls)
        properties_dict.update(month_properties)
    return urls, properties_dict

def get_urls_from_eo_feature(eo_feature):
    '''EO features (Earth Observation features) contain ref to
    associated data to download'''
    assets_to_download = ['thumbnail', 'tileinfo_metadata', 'granule_metadata',
                          'red','green', 'blue', 'green', 'nir', 'nir08',
                          'nir09',  'scl', 'visual','swir16', 'swir22', 'wvp']
    urls = []
    for asset in assets_to_download:
        urls.append(eo_feature['assets'][asset]['href'])
    return urls

def eo_feature2properties_dict(eo_feature):
    ''' From eo_feature json (obtained from eart-search request) create dict of properties'''
    assets_to_download = ['thumbnail', 'tileinfo_metadata', 'granule_metadata',
                          'red','green', 'blue', 'green', 'nir', 'nir08',
                          'nir09',  'scl', 'visual','swir16', 'swir22', 'wvp']
    properties_dict = {
        'id':eo_feature['id'],
        'datetime': eo_feature['properties']['datetime'],
        'crs': eo_feature['properties']['proj:epsg'],
        'geometry': eo_feature['geometry'],
        'bbox': eo_feature['bbox'],
        'assets_list': assets_to_download,
        'urls_list': get_urls_from_eo_feature(eo_feature)
    }
    return properties_dict

def urls2file(file_path, urls_list):
    '''
    Example:
    urls, properties_dict = get_satellite_data(bbox_landes, 2019, limit=160)
    urls2file("data/sentinel2_data_examples/url_list_file.tsv", urls)
    '''
    with open(file_path, "w") as file:
        file.writelines("TsvHttpData-1.0\n") # requested head line for creating gcp transfer job from list of urls file
        for url in urls_list:
            file.writelines(url+"\n")

def one_time_immediate_http_transfer(
    list_url: str,
    sink_folder_in_bucket: str="sink_folder/",
    sink_bucket: str=BUCKET_NAME,
    description: str="one time http transfer of sentinel2 data",
    project_id: str=GCP_PROJECT
):
    """Creates a one-time immediate transfer job from Amazon S3 to Google Cloud
    Storage.
    Attention: sink_folder_in_bucket must end with a '/', it's a folder path
    in the bucket"""

    client = storage_transfer.StorageTransferServiceClient()

    now = datetime.now()
    # the same time creates a one-time transfer
    one_time_schedule = {"day": now.day, "month": now.month, "year": now.year}
    transfer_job_request = storage_transfer.CreateTransferJobRequest(
        {
            "transfer_job": {
                "project_id": project_id,
                "description": description,
                "status": storage_transfer.TransferJob.Status.ENABLED,
                "schedule": {
                    "schedule_start_date": one_time_schedule,
                    "schedule_end_date": one_time_schedule,
                },
                "transfer_spec": {
                    "http_data_source": storage_transfer.HttpData(list_url=list_url),
                    "gcs_data_sink": {
                        "bucket_name": sink_bucket,
                        "path": sink_folder_in_bucket
                    },
                },
            }
        }
    )

    result = client.create_transfer_job(transfer_job_request)
    print(f"Created immediate_http_transfer Job: {result.name}")

def upload_to_storage_and_return_signed_url(
    file_input_path: str, file_output_path: str, bucket_name: str
) -> str:
    '''Upload a local file to bucket and return a signed url (url + access token)
    usable during 15 minutes'''
    gcs = storage.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
    # # Get the bucket that the file will be uploaded to.
    bucket = gcs.bucket(bucket_name)
    # # Create a new blob and upload the file's content.
    blob = bucket.blob(file_output_path)
    blob.upload_from_filename(file_input_path)
    return blob.generate_signed_url(datetime.now())

def upload_satellite_data_to_bucket(bbox, year, limit=200):
    '''Currently the only uploaded file is the list of urls and a signed url,
    i.e. a url containing a time limited token for identification, is returned.
    Use this signe url to create and launch a job transfer on the bucket
    (a list of urls based job transfer).'''
    print(Fore.LIGHTCYAN_EX + "\n⏳ Get satellite data urls" + Style.RESET_ALL)
    urls, properties_dict = get_satellite_data_per_year(bbox, year, limit)
    print("✅ Satellite data urls gotten")
    print(Fore.LIGHTCYAN_EX + "\n⏳ Save urls and data properties to local files" + Style.RESET_ALL)
    urls_list_path = os.path.join("data", "sentinel2_data_examples", "url_list_file.tsv")
    sat_data_properties_path = os.path.join("data", "sat_data_properties.json")
    urls2file(urls_list_path, urls)
    with open(sat_data_properties_path, "w") as file:
        json.dump(properties_dict, file)
    print("✅ Urls and properties saved locally")
    print(Fore.LIGHTCYAN_EX + "\n⏳ Upload urls list file to bucket" + Style.RESET_ALL)
    tsv_url = upload_to_storage_and_return_signed_url(urls_list_path, "sentinel2_row_data/url_list_file.tsv", BUCKET_NAME)
    print("✅ Urls file saved to bucket, url of this file on bucket with access token obtained")
    print(Fore.LIGHTCYAN_EX + "\n⏳ Create and launch one time transfer" + Style.RESET_ALL)
    one_time_immediate_http_transfer(list_url=tsv_url, sink_folder_in_bucket="sentinel2_row_data/")
    print("✅ Files tranfered from urls to bucket\n")

if __name__=='__main__':
    # test upload_satellite_data_to_bucket with few examples
    bbox_landes = [-1.52487, 43.487949, 0.136726,44.532196]
    datetime_range = "2019-08-01T00:00:00Z/2019-08-31T12:31:12Z"
    year = 2019
    print(Fore.LIGHTCYAN_EX + "\n⏳ Get satellite data urls" + Style.RESET_ALL)
    urls, properties_dict = get_satellite_data(bbox_landes, year, datetime_range=datetime_range, limit=2)
    print("✅ Satellite data urls gotten")
    print(Fore.LIGHTCYAN_EX + "\n⏳ Save urls and data properties to local files" + Style.RESET_ALL)
    urls_list_path = os.path.join("data", "sentinel2_data_examples", "url_list_file.tsv")
    sat_data_properties_path = os.path.join("data", "sat_data_properties.json")
    urls2file(urls_list_path, urls)
    with open(sat_data_properties_path, "w") as file:
        json.dump(properties_dict, file)
    print("✅ Urls and properties saved locally")
    print(Fore.LIGHTCYAN_EX + "\n⏳ Upload urls list file to bucket" + Style.RESET_ALL)
    tsv_url = upload_to_storage_and_return_signed_url(urls_list_path, "sentinel2_row_data/url_list_file.tsv", BUCKET_NAME)
    print("✅ Urls file saved to bucket, url of this file on bucket with access token obtained")
    print(Fore.LIGHTCYAN_EX + "\n⏳ Create and launch one time transfer" + Style.RESET_ALL)
    one_time_immediate_http_transfer(list_url=tsv_url, sink_folder_in_bucket="sentinel2_row_data/")
    print("✅ Files tranfered from urls to bucket\n")
