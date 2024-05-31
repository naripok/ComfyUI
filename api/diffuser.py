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


def call_workflow(positive_prompt="", negative_prompt="", image_prefix=""):
    prompt_workflow = json.load(open("api/workflows/workflow_api.json"))

    positive_prompt_node = get_node_by_title(prompt_workflow, "positive_prompt")
    if not positive_prompt_node:
        raise ValueError("positive_prompt node not found")

    negative_prompt_node = get_node_by_title(prompt_workflow, "negative_prompt")
    if not negative_prompt_node:
        raise ValueError("negative_prompt node not found")

    save_image_node = get_node_by_title(prompt_workflow, "save_image")
    if not save_image_node:
        raise ValueError("save_image node not found")

    positive_prompt_node["inputs"]["text"] = positive_prompt
    negative_prompt_node["inputs"]["text"] = negative_prompt
    save_image_node["inputs"]["filename_prefix"] = image_prefix

    return queue_prompt(prompt_workflow)


if __name__ == "__main__":
    print(call_workflow())
