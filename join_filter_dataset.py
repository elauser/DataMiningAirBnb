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
    perc_trust = pd.read_csv("perceived_trust.csv")

    full_listings = pd.concat(
        [listings.set_index('id'), semantic_topics.set_index('id'), labels.set_index('id'), perc_trust.set_index('id')],
        axis=1,
        join='inner')

    return full_listings


def prepare_listings():
    listings = pd.read_csv("filtered_listings.csv")

    listings['description_length'] = listings['description'].apply(word_count)
    listings['response_time'] = listings['host_response_time'].apply(quantify_response_time)
    listings['superhost'] = listings['host_is_superhost'].apply(normalize_boolean)
    listings['response_rate'] = listings['host_response_rate'].apply(p2f)
    listings['number_of_verifications'] = listings['host_verifications'].apply(len)

    listings = listings[['id', 'response_time', 'response_rate', 'superhost',
                         'description_length', 'number_of_reviews',
                         'review_scores_rating', 'number_of_verifications']]
    listings = listings.dropna()

    return listings
    # print(listings.shape[0])
    # print(listings.head(5))


def quantify_response_time(time):
    if time == 'within an hour':
        return 1
    elif time == 'within a few hours':
        return 2
    elif time == 'within a day':
        return 3
    elif time == 'a few days or more':
        return 4


def normalize_boolean(bool):
    if bool == 't':
        return 1
    else:
        return 0


def word_count(description):
    return len(description.split())


def p2f(x):
    return float(str(x).strip('%'))/100


if __name__ == "__main__":
    main()
