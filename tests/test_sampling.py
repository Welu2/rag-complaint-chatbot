import pandas as pd

from src.sampling import stratified_sample


def test_sample_size():

    df = pd.DataFrame({
        "Product": ["A"] * 100 + ["B"] * 100
    })

    sample = stratified_sample(
        df,
        sample_size=50
    )

    assert len(sample) == 50