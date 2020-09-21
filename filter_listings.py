from langdetect import detect
import pandas as pd


def is_english(row):
    try:
        return len(row['description'].split(' ')) >= 5 and detect(row['description']) == 'en'
    except:
        return False


df = pd.read_csv("SourceData/listingsNY_aug.csv")
df.replace(to_replace='<.*?>', value="", regex=True, inplace=True)
df = df[df.apply(is_english, axis=1)]
df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True, inplace=True)
df.to_csv(r'filtered_listings.csv', index = False)
