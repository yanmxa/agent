import os
import sys
import autogen

from kube_agents import (
    kube_engineer,
    kubectl_proxy,
    application_proxy,
    kube_planner,
    user_proxy,
)

from dotenv import load_dotenv

load_dotenv()

llm_config = {
    "config_list": [
        {
            "model": "llama-3.1-70b-versatile",
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": os.getenv("GROQ_API_KEY"),
            "price": [0, 0],
        }
    ]
}


def main(prompt):
    user = user_proxy()
    kubectl = kubectl_proxy()
    engineer = kube_engineer(llm_config)
    application = application_proxy(llm_config)
    planner = kube_planner(llm_config)

    group_chat = autogen.GroupChat(
        agents=[user, engineer, kubectl, application, planner],
        messages=[],
        max_round=10,
        allowed_or_disallowed_speaker_transitions={
            user: [engineer, application, kubectl, planner],
            planner: [user, engineer, application],
            engineer: [user, kubectl],
            application: [user, planner],
            kubectl: [user, engineer, planner],
        },
        speaker_transitions_type="allowed",
    )

    manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)

    group_chat_result = user.initiate_chat(
        manager,
        message=prompt,
    )
    # chat_result = kubectl.initiate_chat(engineer, message=prompt)

    print(">> Summary =================================")
    print(group_chat_result.summary)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("No parameters were provided.")
