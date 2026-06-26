import os
import json
import csv
from datetime import datetime

from openai import OpenAI

# ===========================
# API Configuration
# ===========================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = None

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)


def ask_openai(query):
    """Send a query to OpenAI and return the response."""

    if client is None:
        return "OpenAI API key not found."

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"OpenAI Error: {e}"


def run_citation_audit():

    print("=" * 60)
    print("MyAssignmentHelp AI Citation Tracker")
    print("=" * 60)
    print(f"Started : {datetime.now()}")
    print()

    # -------------------------
    # Load Queries
    # -------------------------

    if os.path.exists("queries.json"):
        with open("queries.json", "r", encoding="utf-8") as f:
            queries = json.load(f)
    else:
        queries = [
            "Best assignment help website",
            "Who can help me write my assignment?"
        ]

    # -------------------------
    # API Status
    # -------------------------

    print("Checking API Keys...")

    print(f"OpenAI      : {'✅ Found' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}")
    print(f"Gemini      : {'✅ Found' if os.getenv('GEMINI_API_KEY') else '❌ Missing'}")
    print(f"Claude      : {'✅ Found' if os.getenv('ANTHROPIC_API_KEY') else '❌ Missing'}")
    print(f"Perplexity  : {'✅ Found' if os.getenv('PERPLEXITY_API_KEY') else '❌ Missing'}")

    print("\nRunning OpenAI Tests...\n")

    results = []

    for index, query in enumerate(queries, start=1):

        print(f"[{index}] {query}")

        answer = ask_openai(query)

        print(answer[:300])
        print("-" * 80)

        results.append({
            "Query": query,
            "OpenAI Response": answer
        })

    # -------------------------
    # Save CSV
    # -------------------------

    os.makedirs("output", exist_ok=True)

    with open("output/audit.csv", "w", newline="", encoding="utf-8") as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=["Query", "OpenAI Response"]
        )

        writer.writeheader()
        writer.writerows(results)

    print()
    print("✅ Audit Finished Successfully")
    print("CSV Saved -> output/audit.csv")


if __name__ == "__main__":
    run_citation_audit()
