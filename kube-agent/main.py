import os
import sys
import autogen
import kube_agents
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

    rag_assistant = kube_agents.rag_assistant(llm_config)
    rag_agent = kube_agents.rag_agent(llm_config["config_list"])
    rag_assistant.reset()
    # qa_problem = "How to configure the global hub system by api?"
    result = rag_agent.initiate_chat(
        rag_assistant,
        message=rag_agent.message_generator,
        problem=prompt,
    )
    # print(result.chat_history)

    # user = user_proxy()
    # kubectl = kubectl_proxy()
    # engineer = kube_engineer(llm_config)
    # application = application_proxy(llm_config)
    # planner = kube_planner(llm_config)

    # user.reset()
    # kubectl.reset()
    # application.reset()
    # planner.reset()

    # group_chat = autogen.GroupChat(
    #     agents=[user, engineer, kubectl, application, planner],
    #     messages=[],
    #     max_round=20,
    # )

    # group_chat = autogen.GroupChat(
    #     agents=[user, engineer, application, planner],
    #     messages=[],
    #     max_round=10,
    #     allowed_or_disallowed_speaker_transitions={
    #         user: [engineer, application, planner],
    #         planner: [user, engineer, application],
    #         engineer: [user],
    #         application: [user, planner],
    #     },
    #     speaker_transitions_type="allowed",
    # )

    # # manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)

    # # group_chat_result = user.initiate_chat(
    # #     manager,
    # #     message=prompt,
    # # )
    # # chat_result = kubectl.initiate_chat(engineer, message=prompt)

    print(">> END =================================")
    # print(group_chat_result.summary)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("No parameters were provided.")
