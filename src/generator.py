from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class ComplaintGenerator:

    def __init__(
        self,
        model_name="google/flan-t5-small",
    ):

        print("Loading generator model...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name
        )

        print("Generator loaded.")

    def generate(
        self,
        prompt,
    ):

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024,
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=False,
        )

        return self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
        )