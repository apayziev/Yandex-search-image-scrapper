import os
import mimetypes
from urllib3.util import Retry
from urllib3 import PoolManager

mime_types = mimetypes.MimeTypes()


def download_failed_images(image_urls, directory):
    http = PoolManager(retries=Retry(total=5))
    for url in image_urls:
        response = http.request("GET", url.strip(), timeout=10)
        if response.status == 200:
            content_type = response.headers.get("Content-Type")
            extension = mime_types.guess_extension(content_type)
            if extension:
                image_name = url.split("/")[-1]
                TRANSLATION_TABLE = {ord(c): None for c in '\\/:*?"<>|'}
                image_name = image_name.translate(TRANSLATION_TABLE)
                image_name = f"{image_name.strip()}{extension}"
                file_path = os.path.join(directory, image_name)
                try:
                    with open(file_path, "wb") as file:
                        file.write(response.data)
                except IOError as e:
                    print(f"Error saving image: {e}")
        else:
            print(f"Request failed with status code {response.status}")


if os.path.exists("failed_urls.txt"):
    with open("failed_urls.txt", "r") as file:
        image_urls = file.readlines()
else:
    print("No failed urls found")

download_failed_images(image_urls, "scrapped_images")
