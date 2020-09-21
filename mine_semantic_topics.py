import csv

def get_all_topics():
    topic_list = [["id", "t1", "t2", "t3", "t4"]]
    with open("SourceData/listingsNY_aug.csv", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            topics = topics_from_description(row['description'])
            topic_list.append([row['id'], topics['t1'], topics['t2'], topics['t3'], topics['t4']])
    return topic_list

def topics_from_description(description):
    t1 = ["My", "I'm", "work", "frienly", "easy", "going", "clean", "apartment", "person", "busy", "respectful", "quiet", "professional"]
    t2 = ["available", "phone", "questions", "text", "email", "stay", "answer", "help", "guests", "contact", "meet", "needs"]
    t3 = ["Brooklyn", "restaurants", "New York", "Manhattan", "neighborhood", "apartment", "park", "great", "city", "welcome", "living", "guests"]
    t4 = ["love", "music", "art", "food", "travel", "design", "wine", "enjoy", "friends", "cooking", "fashion", "places"]

    topics = {"t1":t1, "t2":t2, "t3":t3, "t4":t4}
    topic_quantities = {"t1":0, "t2":0, "t3":0, "t4":0}

    for key,values in topics.items():
        for value in values:
            if value.lower() in description.lower():
                topic_quantities[key] += 1

    # Normalize from 0 to 1
    for key,value in topic_quantities.items():
        topic_quantities[key] = value/len(topics[key])

    return topic_quantities

def create_csv():
    with open("semantic_topics.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(get_all_topics())

if __name__ == "__main__":
    create_csv()
