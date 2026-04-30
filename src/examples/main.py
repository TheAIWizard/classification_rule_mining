from .workflows.date_weather import run_date_weather_workflow
from .workflows.date import run_date


def main():
    date_weather = run_date_weather_workflow("25/03/1995", "Roma")
    date = run_date()
    print("\n✅ Workflow 1 terminé :")
    for k, v in date_weather.items():
        print(f"  {k}: {v}")
    print("\n✅ Workflow 2 terminé :")
    for k, v in date.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
