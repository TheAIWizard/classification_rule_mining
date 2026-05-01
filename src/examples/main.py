from .workflows.date_weather import run_date_weather_workflow
from .workflows.date import run_date
from .workflows.docagent import run_doc


def main():
    date_weather = run_date_weather_workflow("25/03/1995", "Roma")
    date = run_date()
    print("\n✅ Workflow 1 terminé :")
    for k, v in date_weather.items():
        print(f"  {k}: {v}")
    print("\n✅ Workflow 2 terminé :")
    for k, v in date.items():
        print(f"  {k}: {v}")
    path = "/home/onyxia/work/classification_rule_mining/test_rag.md"
    result = run_doc(
        pdf_path=path,
        initial_query="Quelle code NAF (sous-classe) pour la coiffure ?",
        follow_ups=[
            "6220G",
            "code pour conseil en data"
        ],
        collection_name="news"
    )
    print("📊 Conversation structurée :", result["conversation"])


if __name__ == "__main__":
    main()
