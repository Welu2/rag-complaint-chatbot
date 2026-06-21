from src.data_preprocessing import ComplaintPreprocessor


def test_clean_text():

    sample = (
        "I am writing to file a complaint!!! "
        "Visit https://abc.com"
    )

    cleaned = ComplaintPreprocessor.clean_text(sample)

    assert "complaint" not in cleaned
    assert "http" not in cleaned