import os
import autogen
import argparse
from kube_agent import kube_engineer, kube_executor, user_proxy
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
    executor = kube_executor(kube_tool)

    user = user_proxy()

    manager = autogen.GroupChatManager(
        groupchat=autogen.GroupChat(
            agents=[user, engineer, executor],
            messages=[],
            max_round=10,
        ),
        llm_config=llm_config,
    )

    user.initiate_chat(
        manager,
        clear_history=True,
        message="""
        Try to analyze the user provided PROMPT by the "Kubernetes Engineer"
        
        PROMPT: {{prompt}}""",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Multi-Agent system for Kubernetes Applications"
    )
    parser.add_argument("-p", "--prompt", type=str, help="Action you want to perform.")

    args = parser.parse_args()
    main(args.prompt)
