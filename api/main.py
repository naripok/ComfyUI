import json
from urllib import request

SERVER_URL = "http://localhost:8080/prompt"


def get_node_by_title(workflow, title):
    for node in workflow.values():
        if node["_meta"]["title"] == title:
            return node


def queue_prompt(workflow):
    p = {"prompt": workflow}
    data = json.dumps(p).encode("utf-8")
    req = request.Request(SERVER_URL, data=data)
    return request.urlopen(req).read()


if __name__ == "__main__":
    prompt_workflow = json.load(open("api/workflows/example.json"))

    positive_prompt = get_node_by_title(prompt_workflow, "Positive Prompt")
    if not positive_prompt:
        raise ValueError("Positive Prompt not found")

    positive_prompt["inputs"]["text"] = "a bottle full of wonders"
    print(queue_prompt(prompt_workflow))
