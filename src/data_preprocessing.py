import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import (
    RAW_DATA_FILE,
    PROCESSED_DATA_FILE,
    TARGET_PRODUCTS
)


class ComplaintPreprocessor:

    def __init__(self, file_path=RAW_DATA_FILE):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """
        Load CFPB complaint dataset.
        """
        self.df = pd.read_csv(self.file_path)

        print(f"Dataset Shape: {self.df.shape}")
        return self.df

    def perform_eda(self):
        """
        Initial exploratory data analysis.
        """

        print("\n=== Dataset Info ===")
        print(self.df.info())

        print("\n=== Missing Values ===")
        print(self.df.isnull().sum())

        # Product Distribution
        plt.figure(figsize=(12, 6))

        self.df["Product"].value_counts().plot(
            kind="bar"
        )

        plt.title("Complaint Distribution by Product")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

        # Narrative Availability

        narrative_col = "Consumer complaint narrative"

        with_narrative = self.df[narrative_col].notna().sum()
        without_narrative = self.df[narrative_col].isna().sum()

        print("\nComplaints with narratives:", with_narrative)
        print("Complaints without narratives:", without_narrative)

        # Word Count Analysis

        temp = self.df.copy()

        temp["word_count"] = (
            temp[narrative_col]
            .fillna("")
            .apply(lambda x: len(str(x).split()))
        )

        plt.figure(figsize=(10, 5))

        sns.histplot(
            temp["word_count"],
            bins=50,
            kde=True
        )

        plt.title("Narrative Word Count Distribution")
        plt.xlabel("Word Count")
        plt.show()

        print("\nNarrative Statistics")
        print(temp["word_count"].describe())

    @staticmethod
    def clean_text(text):
        """
        Clean complaint narratives.
        """

        if pd.isna(text):
            return ""

        text = str(text).lower()

        # Remove CFPB boilerplate examples
        boilerplates = [
            "i am writing to file a complaint",
            "this complaint is regarding",
            "dear sir or madam"
        ]

        for phrase in boilerplates:
            text = text.replace(phrase, "")

        # Remove URLs
        text = re.sub(r"http\S+", " ", text)

        # Remove special characters
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def filter_dataset(self):
        """
        Filter target products and remove empty narratives.
        """

        narrative_col = "Consumer complaint narrative"

        filtered = self.df[
            self.df["Product"].isin(TARGET_PRODUCTS)
        ].copy()

        filtered = filtered[
            filtered[narrative_col].notna()
        ]

        filtered = filtered[
            filtered[narrative_col].str.strip() != ""
        ]

        filtered["cleaned_narrative"] = (
            filtered[narrative_col]
            .apply(self.clean_text)
        )

        self.df = filtered

        print(
            f"Filtered Dataset Shape: {self.df.shape}"
        )

        return self.df

    def save_processed_data(self):
        """
        Save cleaned dataset.
        """

        PROCESSED_DATA_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.df.to_csv(
            PROCESSED_DATA_FILE,
            index=False
        )

        print(
            f"Saved to {PROCESSED_DATA_FILE}"
        )


def run_pipeline():

    processor = ComplaintPreprocessor()

    processor.load_data()

    processor.perform_eda()

    processor.filter_dataset()

    processor.save_processed_data()


if __name__ == "__main__":
    run_pipeline()