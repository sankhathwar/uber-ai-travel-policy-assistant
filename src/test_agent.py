from agent import agent

while True:

    question = input("\nAsk a question (exit to quit): ")

    if question.lower() == "exit":
        break

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        }
    )

    print("\nAnswer")
    print("-" * 80)

    content = response["messages"][-1].content

    if isinstance(content, str):
        print(content)

    elif isinstance(content, list):

        for item in content:

            if isinstance(item, dict) and item.get("type") == "text":
                print(item["text"])