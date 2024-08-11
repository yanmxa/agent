import autogen
from tools import termination_message, KubeTool


def kube_engineer(llm_config: dict, kube_tool: KubeTool):
    engineer = autogen.AssistantAgent(
        name="Kubernetes Engineer",
        llm_config=llm_config.copy(),
        system_message="You are a Kubernetes Engineer."
        "You can discovery the kube apis and also list the resources by kind and version",
        # "Return 'TERMINATE' when the task is done.",
        is_termination_msg=termination_message,
    )
    # Register the tool signature with the assistant agent.
    engineer.register_for_llm(
        name="discovery kubernetes api",
        description="list of available Kubernetes API versions, similar to `kubectl api-versions`",
    )(kube_tool.discovery_api)

    # Register the tool signature with the assistant agent.
    engineer.register_for_llm(
        name="list kubernetes resources",
        description="list kubernetes resources of a specified kind and version",
    )(kube_tool.list_resources)

    return engineer


def kube_identifier(llm_config: dict):
    return autogen.AssistantAgent(
        name="Kubernetes Resource Identifier",
        llm_config=llm_config.copy(),
        system_message="""
        A Kubernetes Identifier.
        Provide the API version and kind for the specific Kubernetes resource the user wants to retrieve.
        Return the information in JSON format, with the `kind` in singular form.
        Example: {"version": "...", "kind": "..."}.
        """,
        is_termination_msg=termination_message,
    )


def user_agent():
    return autogen.UserProxyAgent(
        name="User",
        system_message="Input your initial prompt",
        human_input_mode="NEVER",
        is_termination_msg=termination_message,
    )
