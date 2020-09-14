import pandas as pd


def main():
    dataset = get_dataset()
    statistics = dataset.describe()
    statistics.to_csv(r'dataset_statistics.csv', index=True)
    dataset.to_csv(r'joined_filtered_dataset.csv')

def get_dataset():
    listings = prepare_listings()
    semantic_topics = pd.read_csv("semantic_topics.csv")
    labels = pd.read_csv("cleaned_labels.csv")

    full_listings = pd.concat([listings.set_index('id'), semantic_topics.set_index('id'), labels.set_index('id')],
                              axis=1,
                              join='inner')

    return full_listings


def prepare_listings():
    listings = pd.read_csv("filtered_listings.csv")
    listings['description_words'] = listings['description'].apply(word_count)
    listings = listings[['id', 'host_response_time', 'host_response_rate', 'host_acceptance_rate', 'host_is_superhost',
                         'host_verifications', 'description_words', 'availability_365', 'number_of_reviews',
                         'review_scores_rating']]
    listings = listings.dropna()
    listings['host_response_time'] = listings['host_response_time'].apply(quantify_response_time)
    listings['host_is_superhost'] = listings['host_is_superhost'].apply(normalize_boolean)
    listings['host_response_rate'] = listings['host_response_rate'].apply(remove_percent)
    listings['host_acceptance_rate'] = listings['host_acceptance_rate'].apply(remove_percent)

    listings['host_verifications'] = listings['host_verifications'].apply(len)

    listings = listings[listings['availability_365'] > 0]
    listings['perceived_trust'] = listings.apply(perceived_trust, axis=1)
    return listings
    # print(listings.shape[0])
    # print(listings.head(5))


def quantify_response_time(time):
    if time == 'within an hour':
        return 0
    elif time == 'within a few hours':
        return 1
    elif time == 'within a day':
        return 2
    else:
        return 3


def normalize_boolean(bool):
    if bool:
        return 1
    else:
        return 0


def word_count(description):
    return len(description.split())


def perceived_trust(row):
    return row['number_of_reviews'] / row['availability_365']

def remove_percent(string):
    return string.replace('%','')

if __name__ == "__main__":
    main()
