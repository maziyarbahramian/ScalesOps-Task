import sys
import fire
import logging


def start_script(q: str, c: int):
    """
    download images from Google, resize it and save it to Postgresql database
    :param str q: search query
    :param int c: number of images to download
    """
    if type(c) is not int:
        logging.error("number of images must be an integer")
        return

    logging.info(f"Searching for {c} images of {q}")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    fire.Fire(start_script)
