from src.input_parser import load_inputs
from src.story_generator import generate_user_stories
from src.jira_formatter import convert_to_jira_csv
from src.tdd_generator import generate_tdd
from src.test_generator import generate_unit_tests
from src.e2egenerator import generate_e2e_tests


# options: "stories", "tdd", "unit", "e2e", "all"
mode = "all"


def main():
    input_data = load_inputs()

    # -----------------------------
    # USER STORIES + JIRA CSV
    # -----------------------------
    if mode == "stories" or mode == "all":
        result = generate_user_stories(input_data)

        with open("outputs/user_stories.json", "w", encoding="utf-8") as f:
            f.write(result)

        convert_to_jira_csv(result)

        print("✅ User stories + Jira CSV generated!")

    # -----------------------------
    # TDD
    # -----------------------------
    if mode == "tdd" or mode == "all":
        tdd = generate_tdd(input_data)

        with open("outputs/tdd.md", "w", encoding="utf-8") as f:
            f.write(tdd)

        print("✅ TDD generated!")

    # -----------------------------
    # UNIT TESTS
    # -----------------------------
    if mode == "unit" or mode == "all":
        unit_tests = generate_unit_tests(input_data)

        with open("outputs/unit_tests.md", "w", encoding="utf-8") as f:
            f.write(unit_tests)

        print("✅ Unit tests generated!")

    # -----------------------------
    # E2E TESTS
    # -----------------------------
    if mode == "e2e" or mode == "all":
        e2e_tests = generate_e2e_tests(input_data)

        with open("outputs/e2e_tests.md", "w", encoding="utf-8") as f:
            f.write(e2e_tests)

        print("✅ E2E tests generated!")


if __name__ == "__main__":
    main() 