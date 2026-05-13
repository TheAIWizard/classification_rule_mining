from .workflows.extract_rules import run_extract_rules_batch


def main():
    rules = run_extract_rules_batch()
    print("\n✅ Workflow 1 - rules extraction done :")
    # for k, v in rules.items():
    #     print(f"  {k}: {v}")
    print(rules)


if __name__ == "__main__":
    main()
