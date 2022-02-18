from multiprocessing import AuthenticationError
import os

import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from time import process_time
import time
import sys
# from qbittorrent import Client
# from clint.textui import progress

from googleapiclient.http import MediaFileUpload

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def authentication():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_1.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    print(type(credentials
    ))
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    return youtube

def upload_video(youtube, title):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.

    print("Uploading video...")
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title
            },
            "status": {
                "madeForKids": True
            }
        },

        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        media_body=MediaFileUpload(title, chunksize=4 * 1024 * 1024, resumable=True, mimetype=None)
    )
    response = request.execute()

    print("Video uploaded successfully.")
    print(response)
    delete_file(title)


def download_video_series(download_url):
    # r = requests.get(download_url, stream=True)
    #
    # with open("movie1.mp4", "wb") as Pypdf:
    #
    #     for chunk in r.iter_content(chunk_size=1024):
    #
    #         if chunk:
    #             Pypdf.write(chunk)

    movie_title = download_url.split("/")[-1]

    with open(movie_title, "wb") as f:
        # print("Downloading %s" % file_name)
        start = process_time()
        response = requests.get(download_url, stream=True)
        total_length = response.headers.get('content-length')
        total_size = int(total_length) / (1024 * 1024)

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                f.flush()
                done = int(100 * dl / total_length)
                current_size = dl / (1024 * 1024)

                sys.stdout.write("\r[%s%s] %s%s   %s/%s mb    %s mbps" % (
                '#' * done, ' ' * (100 - done), done, "%", round(current_size, 2), round(total_size, 2),
                (process_time() - start)))
                sys.stdout.flush()

            print("Video downloaded")

def delete_file(title):
    os.remove(title)

def download_torrent(file_name):
    qb = Client("http://127.0.0.1:8080/")

    qb.login("admin", "Ritik@4")
    # open the torrent file of the file you wanna download
    torrent_file = open(file_name, "rb")
    qb.download_from_file(torrent_file)

def get_video_name():
    for x in os.listdir():
        if x.endswith(".mp4"):
            print(x)
            return x


if __name__ == "__main__":
    download_url_list = 'https://my.kirtijpl5.workers.dev/0:/web/The.Silent.Sea/s1/1080p/The.Silent.Sea.S01E08.the.Silent.Sea.1080p.NF.WEB-DL.DDP5.1.Atmos.x264.mkv'
    youtube = authentication()
    download_video_series(download_url_list)
    time.sleep(1)
    upload_video(youtube, "title")

    # movie_links = download_url_list.split("<$>")

    # for link in movie_links:
    #     title = link.split("/")[-1]
    #     download_video_series(link)
    #     # time.sleep(1)
    #     upload_video(youtube, title)
        




    # videoName = get_video_name()
    # download_video_series(download_url)
    # upload_video(movie_title)
    # i = 0
    # while(i<3):
    #     upload_video(youtube, f"Testing {i}")
    #     i += 1
    # download_torrent("black-widow-2021-720p.torrent")



# download_url = 'https://my.kirtijpl5.workers.dev/0:/web/The.Silent.Sea/s1/1080p/The.Silent.Sea.S01E01.Balhae.Lunar.Research.Station.1080p.NF.WEB-DL.DDP5.1.Atmos.x264.mkv'
# movie_title = "Testing"
