from sklearn.model_selection import train_test_split


def stratified_sample(df, sample_size=12000):

    sample_df, _ = train_test_split(
        df,
        train_size=sample_size,
        stratify=df["Product"],
        random_state=42,
    )

    return sample_df