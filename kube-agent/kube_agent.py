import autogen
from tools import termination_message, KubeTool


def kube_executor(kube_tool: KubeTool):
    executer = autogen.UserProxyAgent(
        name="Kubernetes Executor",
        system_message="""You are an Kubernetes Executor""",
        human_input_mode="NEVER",
        is_termination_msg=termination_message,
    )
    executer.register_for_execution(name="discovery-api")(kube_tool.discovery_api)
    executer.register_for_execution(name="list-resources")(kube_tool.list_resources)
    return executer


def kube_engineer(llm_config: dict, kube_tool: KubeTool):
    engineer = autogen.AssistantAgent(
        name="Kubernetes Engineer",
        llm_config=llm_config.copy(),
        system_message="""You are a Kubernetes Engineer. You can analyse the User's intention and leverage the "Kubernetes Executor" to help you achieve that. A possible workflow can be the following step:
        1. Determine the Kubernetes resource("API version" and "kind"). You can use the discovery-api to match the most likely resource if you cann't get the version and kind directly.
        
        2. Perform the action on the resource, currently you have the following abilities:
        2.1 Get or list the resources by the tool: list-resources, the parameter is analyzed by the step 1
        
        Return 'TERMINATE' when the task is done.
        """,
        is_termination_msg=termination_message,
    )
    # Register the tool signature with the assistant agent.
    engineer.register_for_llm(
        name="discovery-api",
        description="list of available Kubernetes API versions, similar to `kubectl api-versions`",
    )(kube_tool.discovery_api)

    # Register the tool signature with the assistant agent.
    engineer.register_for_llm(
        name="list-resources",
        description="list kubernetes resources of a specified kind and version",
    )(kube_tool.list_resources)
    return engineer


def user_proxy():
    return autogen.UserProxyAgent(
        name="User",
        system_message="Input your initial prompt",
        human_input_mode="NEVER",
        is_termination_msg=termination_message,
    )
