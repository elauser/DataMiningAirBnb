import csv
import urllib.request

with open("../SourceData/listingsNY_aug.csv", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=",")
    for row in csv_reader:
        print(row["host_picture_url"])
        urllib.request.urlretrieve(row["host_picture_url"], "Images/" + row["id"] + ".jpg")