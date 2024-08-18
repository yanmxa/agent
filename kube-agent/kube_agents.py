import json
import os

import autogen
import chromadb
from autogen.coding import LocalCommandLineCodeExecutor
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from langchain.text_splitter import RecursiveCharacterTextSplitter

from tools import termination_message

current_working_directory = os.path.dirname(os.path.realpath(__file__))


def kube_planner(llm_config: dict) -> autogen.ConversableAgent:
    planner = autogen.ConversableAgent(
        name="Planner",
        llm_config=llm_config.copy(),
        description="""Planner. Given a task, determine what information is needed to complete the task.
        After each step is done by others, check the progress and instruct the remaining steps""",
        system_message="""Given a task, please determine what information is needed to complete the task. 
        
        Currently, this plan supports two cases.
        
        1.If the User want to troubleshooting a application system. 
          Start by consulting the Application Agent to gather the system's context or architecture.
          Based on the retrieved application information, create a plan or checklist. Each item on this checklist should either:
            - Retrieve more detailed app information from the Application Agent, or
            - Gather Kubernetes environment details (e.g., resource status, pod logs, configurations) through the Kubernetes Engineer.
        
          After each step is completed by others, monitor progress and guide the remaining steps. If a step fails, attempt a workaround.
          
          Once the root cause of the system issue is identified, summarize the findings and mark the task as complete.
          
        2.If the user perform actions on a Kubernetes resource: 
          Direct the task to the Kubernetes Engineer.
          Mark the task as finished once the Kubernetes Engineer returns a 'TERMINATE' response.
        
        Return 'TERMINATE' when the task is complete.
        """,
    )
    return planner


def kubectl_proxy() -> autogen.ConversableAgent:
    return autogen.ConversableAgent(
        "Executor",
        description="Execute the code written by the 'Kubernetes Engineer' and report the result",
        llm_config=False,
        code_execution_config={
            "executor": LocalCommandLineCodeExecutor(
                timeout=10,
                work_dir=os.path.join(current_working_directory, "__kubecache__"),
            )
        },
        is_termination_msg=termination_message,
        human_input_mode="ALWAYS",
    )


def user_proxy():
    return autogen.UserProxyAgent(
        name="User",
        human_input_mode="ALWAYS",
        is_termination_msg=termination_message,
        code_execution_config=False,  # we don't want to execute code in this case.
        default_auto_reply="Reply `TERMINATE` if the task is done.",
        description="The user who ask questions and give tasks.",
    )


def rag_assistant(llm_config):
    return RetrieveAssistantAgent(
        name="assistant",
        system_message="You are a helpful assistant.",
        llm_config=llm_config.copy(),
    )


def rag_agent(config_list):
    recur_splitter = RecursiveCharacterTextSplitter(separators=["\n", "\r", "\t"])
    return RetrieveUserProxyAgent(
        name="Rag Agent",
        is_termination_msg=termination_message,
        human_input_mode="NEVER",
        default_auto_reply="Reply `TERMINATE` if the task is done.",
        max_consecutive_auto_reply=3,
        retrieve_config={
            "task": "default",
            "docs_path": [
                "https://raw.githubusercontent.com/stolostron/multicluster-global-hub/main/doc/README.md",
                "https://raw.githubusercontent.com/stolostron/multicluster-global-hub/main/operator/apis/v1alpha4/multiclusterglobalhub_types.go",
            ],
            "chunk_token_size": 1000,
            "model": config_list[0]["model"],
            "client": chromadb.PersistentClient(
                path=os.path.join(current_working_directory, "__chromadb__")
            ),
            "collection_name": "groupchat",
            "get_or_create": True,
            "custom_text_split_function": recur_splitter.split_text,
        },
        code_execution_config=False,  # we don't want to execute code in this case.
        description="Rag Agent who is equipped with advanced content retrieval abilities, specifically focused on acquiring and processing information related to the Global Hub System. This includes detailed knowledge of the system's API and the various components that comprise the system.",
    )


def kube_engineer(llm_config: dict):
    engineer = autogen.AssistantAgent(
        name="Kubernetes Engineer",
        is_termination_msg=termination_message,
        human_input_mode="ALWAYS",
        llm_config=llm_config.copy(),
        description="Analyze the Planner's plan content or User's intent to write some shell/command",
        system_message="""You are a Kubernetes Engineer.

Your task is to analyze the user's intent to perform actions on resources and convert this intent into shell commands using your expertise with CLI like `kubectl`, `grep` and `awk`.

Examples:

Example 1: Checking the Status of `globalhub`

Since `globalhub` is not a core Kubernetes resource, you'll break down the task into the following steps:

Step 1: Identify the Custom Resource

Run the following command to check for the `globalhub` resource:

```shell
kubectl api-resources | grep globalhub
```

Send this command to Executor and wait for the response.

- If no information is retrieved: Return a message indicating that the `globalhub` resource was not found and mark the task as complete.
- If information is retrieved, for example:
  "
  multiclusterglobalhubs                     mgh,mcgh                                                                               operator.open-cluster-management.io/v1alpha4          true         MulticlusterGlobalHub
  "

This indicates a namespaced resource called `multiclusterglobalhubs`. Proceed to the next step.

Step 2: Find Instances of the Resource

Since the resource is namespaced, list all instances in the cluster:

```shell
kubectl get multiclusterglobalhubs -A
```

Send this command to Executor and wait for the response.

- If no instances are found: Return a message indicating that there are no instances of globalhub and mark the task as complete.
- If instances are found, for example:
  "
  NAMESPACE                 NAME                    AGE
  multicluster-global-hub   multiclusterglobalhub   3d8h
  "

There's 1 instance in the `multicluster-global-hub` namespace. Retrieve its detailed information:

  ```shell
  kubectl get multiclusterglobalhubs -n multiclusterglobalhub -oyaml
  ```
  
Wait for the response from Executor, summarize the status based on the retrieved information.
Then mark the task as complete.

Example 2: Find the Resource Usage of `global-hub-manager`

Step 1: Identify the Resource Instances

You didn't specify the type of `global-hub-manager`, so it appears to be a pod prefix. Use the following command to find matching pods:

```shell
kubectl get pods -A | grep global-hub-manager
```
Send this command to Executor and wait for the response. If matching instances are found, such as:
"
multicluster-global-hub                            multicluster-global-hub-manager-696967c747-kbb8r                  1/1     Running                  0             9h
multicluster-global-hub                            multicluster-global-hub-manager-696967c747-sntpv                  1/1     Running                  0             9h
"
Proceed to the next step.

Step 2: Retrieve Resource Usage for the Instances

Run the following commands to get the resource usage for each instance:
```shell
kubectl top pod multicluster-global-hub-manager-696967c747-kbb8r -n multicluster-global-hub
kubectl top pod multicluster-global-hub-manager-696967c747-sntpv -n multicluster-global-hub
```
Wait for the expected output from Executor, such as:
"
NAME                                               CPU(cores)   MEMORY(bytes)
multicluster-global-hub-manager-696967c747-kbb8r   1m           36Mi
multicluster-global-hub-manager-696967c747-sntpv   2m           39Mi
"
Go to the final step.

Step 3: Summarize the Results

Summarize the resource usage like this, but you make make the output more clear and beautiful:

- Two pod instances of `global-hub-manager` were found: `multicluster-global-hub-manager-696967c747-kbb8r` with 1m CPU cores and 36Mi memory, and `multicluster-global-hub-manager-696967c747-sntpv` with 2m CPU cores and 39Mi memory.
- Both pods belong to the `multicluster-global-hub-manager` deployment, with a total CPU usage of 3m and memory usage of 75Mi.

Please remember: 
- Try to using English and avoid using some wired characters
- Try to complete the task in as few steps as possibly.For example, you can combine shell commands into scripts
- Each message you send to Executor can contain only 1 code block

Return 'TERMINATE' when the task is complete.
""",
    )
    return engineer


def application_proxy(llm_config: dict) -> autogen.ConversableAgent:
    return autogen.ConversableAgent(
        "Application",
        description="Provide the application information of the Planner want to achieve",
        llm_config=llm_config.copy(),
        is_termination_msg=termination_message,
        human_input_mode="TERMINATE",
        system_message="""
        You can achieve the information of an application system. currently you only return the global hub application's information. Detailed in the following:

        The multicluster global hub is a set of components that enable you to import one or more hub clusters and manage them from a single hub cluster.

        After importing the hub clusters as managed hub clusters, you can use multicluster global hub to complete the following tasks across all of the managed hub clusters:

          - Report the policy compliance status and trend
          - Inventory all managed hubs and managed clusters on the overview page
          - Detect and alert in cases of irregular policy behavior
          
        The multicluster global hub is useful when a single hub cluster cannot manage the large number of clusters in a high-scale environment. When this happens, you divide the clusters into smaller groups of clusters and configure a hub cluster for each group.

        It is often inconvenient to view the data on multiple hub clusters for the managed clusters that are managed by that hub cluster. The multicluster global hub provides an easier way to view information from multiple hubs by designating multiple hub clusters as managed hub clusters. The multicluster global hub cluster manages the other hub clusters and gathers summarized information from the managed hub clusters.
        
        The multicluster global hub consists of the following components that are used to access and manage your hub clusters:
        
          - The multiclusterglobalhub crd, it the configurations of the global hub system
          - The multicluster global hub operator contains the components of multicluster global hub. The operator
          deploys all of the required components for global multicluster management. The components include `multicluster-global-hub-manager`, `multicluster-global-hub-grafana`, and provided versions of `Kafka` and `PostgreSQ`L in the multicluster global hub cluster and `multicluster-global-hub-agent` in the managed hub clusters.
          - The multicluster global hub manager is used to persist the data into the postgreSQL database. The data is from Kafka transport. The manager also posts the data to the Kafka transport, so it can be synchronized with the data on the managed hub clusters.
          - The multicluster global hub agent runs on the managed hub clusters. It synchronizes the data between the multicluster global hub cluster and the managed hub clusters. For example, the agent synchronizes the information of the managed clusters from the managed hub clusters to the multicluster global hub cluster and synchronizes the policy or application from the multicluster global hub cluster to the managed hub clusters.
          - Grafana runs on the multicluster global hub cluster as the main service for multicluster global hub visualizations. The PostgreSQL data collected by the Global Hub Manager is its default DataSource. By exposing the service using the route called multicluster-global-hub-grafana, you can access the multicluster global hub Grafana dashboards by accessing the console.
        """,
    )
