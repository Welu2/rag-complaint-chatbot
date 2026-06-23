from .retriever import ComplaintRetriever

from .generator import ComplaintGenerator
from .prompt_template import (
    PROMPT_TEMPLATE
)


class ComplaintRAG:

    def __init__(self):

        self.retriever = (
            ComplaintRetriever()
        )

        self.generator = (
            ComplaintGenerator()
        )

    def answer_question(
        self,
        question,
        k=5,
    ):

        docs = self.retriever.retrieve(
            question,
            k=k,
        )

        context = "\n\n".join(
            doc["text"]
            for doc in docs
        )

        prompt = PROMPT_TEMPLATE.format(
            context=context,
            question=question,
        )

        answer = self.generator.generate(
            prompt
        )

        return {
            "answer": answer,
            "sources": docs,
        }