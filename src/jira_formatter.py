import json
import csv

def convert_to_jira_csv(json_text):
    data = json.loads(json_text)

    with open("outputs/jira_stories.csv", "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Header
        writer.writerow(["Summary", "Description", "Issue Type"])

        for item in data:
            summary = item["epic"]

            description = item["user_story"] + "\n\nAcceptance Criteria:\n"
            for ac in item["acceptance_criteria"]:
                description += f"- {ac}\n"

            writer.writerow([summary, description, "Story"])