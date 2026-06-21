import os
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

        self.df = pd.read_csv(
            self.file_path,
            low_memory=False
        )

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

        figures_dir = "data/processed/figures"
        os.makedirs(figures_dir, exist_ok=True)

        # ----------------------------
        # Product Distribution
        # ----------------------------

        plt.figure(figsize=(16, 8))

        self.df["Product"].value_counts().plot(kind="bar")

        plt.title("Complaint Distribution by Product")
        plt.ylabel("Count")
        plt.xlabel("Product")
        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()

        plt.savefig(
            f"{figures_dir}/product_distribution.png",
            bbox_inches="tight"
        )

        plt.close()

        print(
            f"\nSaved product distribution plot to "
            f"{figures_dir}/product_distribution.png"
        )

        # ----------------------------
        # Narrative Analysis
        # ----------------------------

        narrative_col = "Consumer complaint narrative"

        with_narrative = self.df[narrative_col].notna().sum()
        without_narrative = self.df[narrative_col].isna().sum()

        print(f"\nComplaints with narratives: {with_narrative}")
        print(f"Complaints without narratives: {without_narrative}")

        # Analyze ONLY rows that actually contain narratives
        narratives_only = self.df[
            self.df[narrative_col].notna()
        ].copy()

        word_counts = (
    narratives_only[narrative_col]
    .astype(str)
    .str.count(r"\S+")
)

        narratives_only["word_count"] = word_counts

        short_narratives = (
            narratives_only["word_count"] < 10
        ).sum()

        long_narratives = (
            narratives_only["word_count"] > 1000
        ).sum()

        print(
            f"Very short narratives (<10 words): "
            f"{short_narratives}"
        )

        print(
            f"Very long narratives (>1000 words): "
            f"{long_narratives}"
        )

        print("\nNarrative Statistics")
        print(word_counts.describe())

        plt.figure(figsize=(12, 6))

        sns.histplot(
            word_counts,
            bins=50,
            kde=True
        )

        plt.title(
            "Consumer Narrative Word Count Distribution"
        )

        plt.xlabel("Word Count")
        plt.ylabel("Frequency")

        plt.tight_layout()

        plt.savefig(
            f"{figures_dir}/word_count_distribution.png",
            bbox_inches="tight"
        )

        plt.close()

        print(
            f"\nSaved word count plot to "
            f"{figures_dir}/word_count_distribution.png"
        )

    @staticmethod
    
    def clean_text(text):
        """
        Clean complaint narratives.
        """

        if pd.isna(text):
            return ""

        text = str(text).lower()

        # Remove common boilerplate phrases
        boilerplate_patterns = [
            r"\bi am writing to file a complaint\b",
            r"\bi would like to file a complaint\b",
            r"\bthis complaint is regarding\b",
            r"\bdear sir or madam\b",
            r"\bto whom it may concern\b"
        ]

        for pattern in boilerplate_patterns:
            text = re.sub(pattern, " ", text)

        # Remove URLs
        text = re.sub(r"http\S+|www\.\S+", " ", text)

        # Remove emails
        text = re.sub(r"\S+@\S+", " ", text)

        # Remove numbers-only tokens if desired
        text = re.sub(r"\b\d+\b", " ", text)

        # Remove special characters
        text = re.sub(
            r"[^a-zA-Z0-9\s]",
            " ",
            text
        )

        # Remove extra whitespace
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def filter_dataset(self):
        """
        Keep only required products and
        remove empty narratives.
        """

        narrative_col = "Consumer complaint narrative"

        filtered = self.df[
            self.df["Product"].isin(
                TARGET_PRODUCTS
            )
        ].copy()

        filtered = filtered[
            filtered[narrative_col].notna()
        ]

        filtered = filtered[
            filtered[narrative_col]
            .astype(str)
            .str.strip()
            != ""
        ]

        filtered["cleaned_narrative"] = (
        filtered[narrative_col]
        .apply(self.clean_text)
    )

        filtered["cleaned_word_count"] = (
            filtered["cleaned_narrative"]
            .str.split()
            .str.len()
        )

        filtered = filtered[
    filtered["cleaned_word_count"] > 0
]

        self.df = filtered

        print(
                f"\nFiltered Dataset Shape: "
                f"{self.df.shape}"
            )

        print("\nFiltered Product Distribution:")
        print(
                self.df["Product"]
                .value_counts()
            )

        return self.df

    def save_processed_data(self):
        """
        Save processed dataset.
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
            f"\nSaved processed dataset to:\n"
            f"{PROCESSED_DATA_FILE}"
        )


def run_pipeline():

    processor = ComplaintPreprocessor()

    processor.load_data()

    processor.perform_eda()

    processor.filter_dataset()

    processor.save_processed_data()


if __name__ == "__main__":
    run_pipeline()
