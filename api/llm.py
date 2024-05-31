import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def call_llm(user_prompt: str, system_prompt: str = "") -> str:
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model="llama3-70b-8192",
    )

    if not chat_completion.choices[0].message.content:
        raise ValueError("No response")

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    print(call_llm("fast language models", "You're crazy"))
