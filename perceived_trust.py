import pandas as pd

listings_may = pd.read_csv("SourceData/listingsNY_may.csv", low_memory=False).set_index('id')
listings_jun = pd.read_csv("SourceData/listingsNY_jun.csv", low_memory=False).set_index('id')
listings_jul = pd.read_csv("SourceData/listingsNY_jul.csv", low_memory=False).set_index('id')
listings_aug = pd.read_csv("SourceData/listingsNY_aug.csv", low_memory=False).set_index('id')


def perceived_trust():
    df = growth_rate().join(online_days(), how='inner')
    df['perceived_trust'] = df.growth_rate / df.online_days
    return df[['perceived_trust']]


def growth_rate():
    # august - jun  number_of_reviews
    df = listings_aug.join(listings_jun, lsuffix='_aug', rsuffix='_jun', how='inner')
    df = df[['number_of_reviews_aug', 'number_of_reviews_jun']]
    df = df.dropna()
    df['growth_rate'] = df.number_of_reviews_aug - df.number_of_reviews_jun
    df = df[df.growth_rate >= 0]
    return df[['growth_rate']]


def online_days():
    df = listings_jun.join(listings_jul, rsuffix='_jul', how='inner')
    df = df.join(listings_aug, rsuffix='_aug', how='inner')
    df = df[['availability_30', 'availability_30_jul', 'availability_30_aug']].dropna()
    df['online_days'] = df.availability_30 + df.availability_30_jul + df.availability_30_aug
    df = df[['online_days']]
    df = df[df.online_days > 0]
    return df


if __name__ == '__main__':
    pt = perceived_trust()
    pt.to_csv(r'perceived_trust.csv', index=True)
