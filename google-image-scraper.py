import io
import sys
import fire
import logging
import asyncio
import uuid
import os
import requests
from PIL import Image
import database
import base64


async def download_and_save(url):
    logging.info(f"Downloading {url}")
    folder_name = "images"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    filename = str(uuid.uuid4()) + ".jpg"
    file_path = os.path.join(folder_name, filename)

    request = requests.get(url, stream=True, proxies={'http': '', 'https': ''})
    if request.ok:
        logging.info(f'image downloaded, saving to {os.path.abspath(file_path)}')
        with open(file_path, 'wb') as file:
            for chunk in request.iter_content(chunk_size=1024 * 8):
                if chunk:
                    file.write(chunk)
                    file.flush()
                    os.fsync(file.fileno())
        logging.info(f' 1 image downloaded successfully')
    else:  # http status code 4XX or 5XX
        logging.error(f'Download failed: status code: {request.status_code}\n{request.text}')


async def download_images(loop, urls):
    urls_count = len(urls)
    logging.info(f' Start Downloading {urls_count} images')
    for i in range(urls_count):
        await download_and_save(urls[i])


async def fetch_image_urls(loop, q):
    """
    "Due to US sanctions, my Google account is restricted,
     preventing me from obtaining an API access key.
     For now, I'll skip this part of the task."
    """
    logging.info(' Start searching in google images')
    urls = [
        "https://picsum.photos/id/237/200/300",
        "https://picsum.photos/id/2/200/300",
        "https://picsum.photos/id/3/200/300",
        "https://picsum.photos/id/4/200/300",
        "https://picsum.photos/id/5/200/300"
    ]
    logging.info(' Search finished')
    return urls


def start_script(q: str, c: int):
    """
    download images from Google, resize it and save it to Postgresql database
    :param str q: search query
    :param int c: number of images to download
    """
    if type(c) is not int:
        logging.error(" number of images must be an integer")
        return

    logging.info(f" Searching for {c} images of {q}")

    loop = asyncio.get_event_loop()
    urls = loop.run_until_complete(fetch_image_urls(loop, q))
    loop.run_until_complete(download_images(loop, urls))


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    fire.Fire(start_script)
