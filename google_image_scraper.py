import io
import sys
import logging
import asyncio
import uuid
import os
import requests
from PIL import Image
import database
import base64


def create_image_folder():
    folder_name = "images"
    if not os.path.exists(folder_name):
        logging.info(f" Creating folder: {folder_name}")
        os.makedirs(folder_name)
    logging.info(f' Folder already exists: {folder_name}')
    return folder_name


def get_new_file_path(folder_name):
    filename = str(uuid.uuid4()) + ".jpg"
    file_path = os.path.join(folder_name, filename)
    logging.info(f' File will be downloaded in: {file_path}')
    return file_path, filename


async def download_and_save(url):
    logging.info(f"Downloading {url}")

    folder_name = create_image_folder()
    file_path, filename = get_new_file_path(folder_name)

    request = requests.get(url, stream=True, proxies={'http': '', 'https': ''})
    if request.ok:
        logging.info(f' Image downloaded, saving to {os.path.abspath(file_path)}')
        with open(file_path, 'wb') as file:
            for chunk in request.iter_content(chunk_size=1024 * 8):
                if chunk:
                    file.write(chunk)
                    file.flush()
                    os.fsync(file.fileno())
        logging.info(f' Image successfully saved in: {os.path.abspath(file_path)}')
        await save_to_database(file_path)
    else:  # http status code 4XX or 5XX
        logging.error(f'Download failed: {url}\n Status code: {request.status_code}\n{request.text}')


def resize_image(file_path):
    try:
        logging.info(f" Resizing {file_path}")
        image = Image.open(file_path)
        image.thumbnail((120, 120))
        output = io.BytesIO()
        image.save(output, format='JPEG')
        logging.info(f' Image {file_path} Successfully resized to 120*120')
        return output.getvalue()

    except IOError as e:
        logging.error(e)


async def save_to_database(file_path):
    logging.info(f" Start Saving {file_path} to database")
    resized_image = resize_image(file_path)
    database.insert_image(resized_image)
    logging.info(f' Image {file_path} saved to database')


async def download_images(urls):
    urls_count = len(urls)
    logging.info(f' Start Downloading {urls_count} images')
    filenames = list()
    for i in range(urls_count):
        filename = await download_and_save(urls[i])
        filenames.append(filename)
    return filenames


async def fetch_image_urls(q):
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


def clear_cache():
    try:
        folder_name = 'images'
        files = os.listdir(folder_name)
        for file in files:
            file_path = os.path.join(folder_name, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        logging.info('all cached images deleted.')
    except OSError:
        logging.error("Error occurred while clearing cache.")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    count = int(os.getenv('COUNT', 5))

    query = os.getenv('QUERY', None)

    if query is None or query == '':
        logging.error('The QUERY environment variable is not set. Please provide a valid value.')
        sys.exit(1)

    logging.info(f" Searching for {count} images of {query}")

    loop = asyncio.get_event_loop()
    urls = loop.run_until_complete(fetch_image_urls(query))
    filenames = loop.run_until_complete(download_images(urls))
    clear_cache()
