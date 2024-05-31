import re

from .diffuser import call_workflow
from .llm import call_llm

IMG_PREFIX = "astronaut"

LLM_SYSTEM_PROMPT = """\
You're a master AI artist, who is very creative. You're tasked of crafting a POSITIVE_PROMPT and a NEGATIVE_PROMPT that describes the image you want to create. In POSITIVE_PROMPT, include what you want the image to contain. It may include elements, styles, structure, etc. In NEGATIVE_PROMPT, include things that you DON'T want your creation to contain.

For example:
```
POSITIVE_PROMPT: astronaut in the style of starry night
NEGATIVE_PROMPT: text, watermark
```

I'll parse your response with python, so always include the POSITIVE_PROMPT and NEGATIVE_PROMPT tokens in your response, followed by the information you want each to contain.
"""

LLM_USER_PROMPT = """\
Write the POSITIVE_PROMPT and NEGATIVE_PROMPT necessary for creating images of house interiors. The images should be detailed and interesting enough to generate traffic to my instagram page.
"""


def extract_prompt(text, key="POSITIVE_PROMPT"):
    prompt = re.search(rf"{key}: (.*)", text)
    if not prompt:
        raise ValueError(f"No {key} found")
    return prompt.group(1)


def main():
    llm_response = call_llm(
        user_prompt=LLM_USER_PROMPT, system_prompt=LLM_SYSTEM_PROMPT
    )

    positive_prompt = extract_prompt(llm_response, key="POSITIVE_PROMPT")
    print("POSITIVE_PROMPT:", positive_prompt)
    negative_prompt = extract_prompt(llm_response, key="NEGATIVE_PROMPT")
    print("NEGATIVE_PROMPT:", negative_prompt)

    print(
        call_workflow(
            positive_prompt=positive_prompt,
            negative_prompt=negative_prompt,
            image_prefix=IMG_PREFIX,
        )
    )


if __name__ == "__main__":
    main()
