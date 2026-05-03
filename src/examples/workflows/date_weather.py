from ..agents import create_agent
from ..tools.tool_loader import load_and_register_tools


def run_date_weather_workflow(date_str: str = "25th of March 1995", location: str = "Roma") -> dict:
    """Pipeline séquentiel : date → weekday → météo."""

    # 1️⃣ Setup
    executor = create_agent("executor_agent", human_input_mode="NEVER")
    date_agent = create_agent("date_agent", human_input_mode="NEVER")
    weather_agent = create_agent("weather_agent", human_input_mode="NEVER")

    # 2️⃣ Registration par scope
    load_and_register_tools(["get_weekday"], date_agent, executor)
    load_and_register_tools(["get_weather"], weather_agent, executor)

    # 3️⃣ Étape 1 : jour de la semaine
    date_res = executor.initiate_chat(
        recipient=date_agent,
        message=f"I was born on the {date_str} in {location}, what day was it ? "
                f"I wonder if it's as hot as here there now.",
        max_turns=3,
    )
    # ⚠️ correction : chat_history[0] était ton message initial, on prend la dernière réponse
    weekday = date_res.chat_history[-1]["content"].strip()

    # 4️⃣ Étape 2 : prédiction météo
    weather_res = executor.initiate_chat(
        recipient=weather_agent,
        message=f"Based on date {date_str} (weekday: {weekday}) in {location},\
                  predict the weather.",
        max_turns=2,
    )
    weather = weather_res.chat_history[-2]["content"].strip()

    return {
        "date": date_str,
        "location": location,
        "weekday": weekday,
        "weather": weather
    }
