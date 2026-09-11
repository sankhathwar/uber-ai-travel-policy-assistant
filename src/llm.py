from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import GOOGLE_API_KEY, LLM_MODEL, DEFAULT_TEMPERATURE
class GeminiLLM:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=DEFAULT_TEMPERATURE,
        )

    def invoke(self, prompt):

        response = self.llm.invoke(prompt)

        if isinstance(response.content, str):
            return response.content

        if isinstance(response.content, list):
            text = ""
            for item in response.content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text += item.get("text", "")
            return text

        return str(response)