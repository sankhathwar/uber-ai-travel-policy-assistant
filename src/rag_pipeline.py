"""
rag_pipeline.py

End-to-End Retrieval-Augmented Generation (RAG) Pipeline
for the Uber AI Travel Policy Assistant.
"""
from src.retriever import PolicyRetriever
from src.llm import GeminiLLM
from src.prompts import role_based_prompt


class TravelPolicyRAG:

    def __init__(self):

        print("\nInitializing Travel Policy Assistant...\n")

        self.retriever = PolicyRetriever()
        self.llm = GeminiLLM()

        print("✓ Assistant Ready!\n")

    def retrieve_context(self, question):

        documents = self.retriever.search(question)

        context = ""

        for i, (doc, score) in enumerate(documents, start=1):

            context += f"""
Source: {doc.metadata.get("source")}
Policy Type: {doc.metadata.get("policy_type")}
Country: {doc.metadata.get("country")}
Similarity Score: {score:.4f}

{doc.page_content}

------------------------------------------------------------
"""

        return context, documents

    def answer_question(self, question):

        context, documents = self.retrieve_context(question)

        prompt = role_based_prompt(
            question=question,
            context=context
        )

        answer = self.llm.invoke(prompt)

        return answer, documents


def display_sources(documents):

    print("\nSources Used")
    print("-" * 60)

    seen = set()

    for doc, score in documents:

        source = doc.metadata.get("source")

        if source not in seen:

            seen.add(source)

            print(f"• {source}")


def main():

    assistant = TravelPolicyRAG()

    while True:

        print("\n" + "=" * 80)

        question = input(
            "Ask a travel policy question ('exit' to quit): "
        )

        if question.lower() == "exit":
            break

        answer, docs = assistant.answer_question(question)

        print("\nAnswer")
        print("-" * 80)

        print(answer)

        display_sources(docs)


if __name__ == "__main__":
    main()