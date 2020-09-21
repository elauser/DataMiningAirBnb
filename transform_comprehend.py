import json
import csv


def format_data():
    with open('SemanticIntensity/output', 'r', encoding='utf8') as f:
        csv_rows = [['row', 'Sentiment_intensity', 'Mixed', 'Negative', 'Neutral', 'Positive']]
        for json_doc in f.readlines():
            sentiment = json.loads(json_doc)
            sentiment_score = sentiment['SentimentScore']
            row = [sentiment['Line'], sentiment_intensity(sentiment["Sentiment"])]
            for key, value in sentiment_score.items():
                row.append(value)
            csv_rows.append([str(r) for r in row])

        with open('comprehend_final.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for line in csv_rows:
                writer.writerow(line)


def sentiment_intensity(row):
    if row == 'POSITIVE':
        return 1
    elif row == 'NEGATIVE':
        return -1
    else:
        return 0


if __name__ == "__main__":
    format_data()
