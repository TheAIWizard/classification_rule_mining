from ..agents import create_agent
from ..tools.tool_loader import load_and_register_tools


def run_date():
    date_agent = create_agent("date_agent", human_input_mode="NEVER")
    executor_agent = create_agent("executor_agent", human_input_mode="NEVER")

    # ✅ Déclaratif : on liste juste ce qu'on veut
    load_and_register_tools(["get_weekday"], date_agent, executor_agent)

    day_birthday_res = executor_agent.initiate_chat(
        recipient=date_agent,
        message="I was born on the 25th of March 1995, what day was it?",
        max_turns=2,
        summary_method="last_msg"  # "reflection_with_llm" => resume history with llm
    )
    day_birthday = day_birthday_res.summary.strip()
    return {
        "day_birthday": day_birthday,
    }
