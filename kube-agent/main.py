import os
import autogen
import argparse
from kube_agent import kube_engineer, kube_identifier, user_agent
from tools import KubeTool

from dotenv import load_dotenv

load_dotenv()

llm_config = {
    "config_list": [
        {
            "model": "llama-3.1-70b-versatile",
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": os.getenv("GROQ_API_KEY"),
        }
    ]
}


def main(prompt: str):
    kube_tool = KubeTool()
    engineer = kube_engineer(llm_config, kube_tool)

    expert = kube_identifier(llm_config)

    user = user_agent()

    manager = autogen.GroupChatManager(
        groupchat=autogen.GroupChat(
            agents=[user, expert, engineer],
            messages=[],
            max_round=10,
        ),
        llm_config=llm_config,
    )

    user.initiate_chat(
        manager,
        clear_history=True,
        message="""Provide the user with the details from their kubernetes cluster in the provided PROMPT."""
        """find the api version and kind of the kubernetes resources from the discovered api list"""
        """infer the api version and kind by fuzzy matching with resources in PROMPT"""
        """PROMPT: {{prompt}}""",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Multi-Agent system for Kubernetes Applications"
    )
    parser.add_argument("-p", "--prompt", type=str, help="Action you want to perform.")

    args = parser.parse_args()
    main(args.prompt)
