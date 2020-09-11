import csv
import aiohttp
import aiofiles
import asyncio
import boto3
import concurrent.futures
import threading
import time
import os
import numpy as np

async def download_labels(images):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for image_uri in images:
            task = asyncio.ensure_future(download_label(image_uri))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


async def download_label(image_url):
    image_url_path = "small_images/" + image_url
    async with open(image_url_path, "rb") as image:
        f = image.read()
        b = bytearray(f)

        response = await client.detect_faces(
            Image={
                'Bytes': b
            },
            Attributes=[
                'ALL'
            ]
        )

        filename = "Labels/" + image_url + ".json"
        f = await aiofiles.open(filename, mode="wb")
        await f.write(await resp.read())
        await f.close()


def get_images():
    images_list = os.listdir("Images/")
    unchanged_list = os.listdir("small_Labels/")
    labels_list = map(remove_type, unchanged_list)

    return np.setdiff1d(images_list, labels_list)


def remove_type(string):
    return string[0,-5]


if __name__ == "__main__":
    image_list = get_images()
    asyncio.get_event_loop().run_until_complete(download_labels(image_list))
