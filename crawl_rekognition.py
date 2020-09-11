import boto3
import concurrent.futures
import threading
import time
import os

client = boto3.client('rekognition')

def download_labels(image_url):
    image_url_path = "small_images/" + image_url
    with open(image_url_path, "rb") as image:
        f = image.read()
        b = bytearray(f)


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
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(download_labels, images)


if __name__ == "__main__":
    image_list = os.listdir("Images/")
    start_time = time.time()
    download_all(image_list)
    duration = time.time() - start_time
    print(f"Downloaded {len(image_list)} in {duration} seconds")
