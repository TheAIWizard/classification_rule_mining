from .agents import create_agent
from .tools.tool_loader import load_and_register_tools


def run():
    date_agent = create_agent("date_agent")
    executor_agent = create_agent("executor_agent", human_input_mode="NEVER")

    # ✅ Déclaratif : on liste juste ce qu'on veut
    load_and_register_tools(["get_weekday"], date_agent, executor_agent)

    chat_result = executor_agent.initiate_chat(
        recipient=date_agent,
        message="I was born on the 25th of March 1995, what day was it?",
        max_turns=2,
    )
    print("\n✅", chat_result.chat_history[-1]["content"])


if __name__ == "__main__":
    run()
