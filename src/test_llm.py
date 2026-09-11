from llm import GeminiLLM

llm = GeminiLLM()

response = llm.invoke("Say hello in one sentence.")

print(response)