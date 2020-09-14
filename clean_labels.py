import json
import statistics
import os
import csv

#todo modularize and clean the code

csv_path = "cleaned_labels.csv"
csv_rows = [
    ["id", "face_amount", "happy", "sad", "angry", "confused", "disgusted", "surprised", "calm", "fear", "beard",
     "mustache", "key_emotion", "polarity"]]
json_dir = 'Labels'


def get_key_emotion(dict):
    key_emo = ''
    max_value = 0.
    for emo, value in dict.items():
        if max_value < value:
            key_emo = emo
            max_value= value
    return key_emo

def get_polarity(emo):
    positive_emotions = ['HAPPY']
    negative_emotions = ['SAD', 'ANGRY', 'DISGUSTED', 'FEAR']

    if emo in positive_emotions:
        return 1
    elif emo in negative_emotions:
        return -1
    else:
        return 0

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



    em = {}
    em['HAPPY'] = statistics.mean(happy)
    em['SAD'] = statistics.mean(sad)
    em['ANGRY'] = statistics.mean(angry)
    em['CONFUSED'] = statistics.mean(confused)
    em['DISGUSTED'] = statistics.mean(disgusted)
    em['SURPRISED'] = statistics.mean(surprised)
    em['CALM'] = statistics.mean(calm)
    em['FEAR'] = statistics.mean(fear)

    key_emotion = get_key_emotion(em)
    polarity = get_polarity(key_emotion)


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

    beard_mean = statistics.mean(beard_factor)
    mustache_mean = statistics.mean(mustache_factor)


    csv_rows.append(
        [id, face_amount, em['HAPPY'], em['SAD'], em['ANGRY'], em['CONFUSED'], em['DISGUSTED'], em['SURPRISED'],
         em['CALM'], em['FEAR'], beard_mean, mustache_mean, key_emotion, polarity])

with open(csv_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_rows)
