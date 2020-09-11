import boto3
import concurrent.futures
import threading
import time
import os
import json

def download_labels(image_url):
    image_url_path = "Images/" + image_url
    with open(image_url_path, "rb") as image:
        f = image.read()
        b = bytearray(f)

        client = boto3.client('rekognition')
        response = client.detect_faces(
            Image={
                'Bytes': b
            },
            Attributes=[
                'ALL'
            ]
        )

        filename = "Labels/" + image_url + ".json"
        with open(filename, 'w') as json_file:
            json.dump(response, json_file)


def download_all(images):
    counter = 0
    for image in images:
        download_labels(image)
        print(++counter)


if __name__ == "__main__":
    images = os.listdir("Images/")
    start_time = time.time()
    download_all(images)
    duration = time.time() - start_time
    print(f"Downloaded {len(images)} in {duration} seconds")