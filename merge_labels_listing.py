import pandas as pd
import json
import statistics
from pandas.io.json import json_normalize
import os
import csv

csv_path = "cleaned_labels.csv"
csv_rows = [
    ["id", "face_amount", "happy", "sad", "angry", "confused", "disgusted", "surprised", "calm", "fear", "beard",
     "mustache"]]

json_dir = 'Labels'
for json_path in os.listdir(json_dir):
    with open(json_dir + '/' + json_path) as file:
        json_labels = json.load(file)
        json_labels = json_labels['FaceDetails']
        faces = [x['Emotions'] for x in json_labels]
        mustaches = [x['Mustache'] for x in json_labels]
        beards = [x['Beard'] for x in json_labels]

        id = json_path[0:-9]
        face_amount = 0
        happy = []
        sad = []
        angry = []
        confused = []
        disgusted = []
        surprised = []
        calm = []
        fear = []
        beard_factor = []
        mustache_factor = []

        for face in faces:
            face_amount += 1

            facial_emotions = {}
            for emotion in face:
                facial_emotions[emotion['Type']] = emotion['Confidence']

            happy.append(facial_emotions['HAPPY'])
            sad.append(facial_emotions['SAD'])
            angry.append(facial_emotions['ANGRY'])
            confused.append(facial_emotions['CONFUSED'])
            disgusted.append(facial_emotions['DISGUSTED'])
            surprised.append(facial_emotions['SURPRISED'])
            calm.append(facial_emotions['CALM'])
            fear.append(facial_emotions['FEAR'])

    for beard in beards:
        if beard['Value']:
            beard_factor.append(1)
        else:
            beard_factor.append(0)

    for mustache in mustaches:
        if mustache['Value']:
            mustache_factor.append(1)
        else:
            mustache_factor.append(0)

    happy_mean = statistics.mean(happy)
    sad_mean = statistics.mean(sad)
    angry_mean = statistics.mean(angry)
    confused_mean = statistics.mean(confused)
    disgusted_mean = statistics.mean(disgusted)
    surprised_mean = statistics.mean(surprised)
    calm_mean = statistics.mean(calm)
    fear_mean = statistics.mean(fear)
    beard_mean = statistics.mean(beard_factor)
    mustache_mean = statistics.mean(mustache_factor)

    csv_rows.append(
        [id, face_amount, happy_mean, sad_mean, angry_mean, confused_mean, disgusted_mean, surprised_mean, calm_mean,
         fear_mean, beard_mean, mustache_mean])

with open(csv_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_rows)

# j = pd.json_normalize(json_labels)
# print(j)

"""
    for key, value in json_labels['FaceDetails']:
        if key == "Emotions":
            print(value)"""
