import os
import requests
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)

def ask_gemini(prompt: str, debug: bool = False):
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(
        f"{GEMINI_ENDPOINT}?key={API_KEY}",
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    data = response.json()

    output = data["candidates"][0]["content"]["parts"][0]["text"]

    if debug:
        return output, data
    return output, None

def main():
    parser = argparse.ArgumentParser(description="Gemini CLI Chat")
    parser.add_argument("-d", "--debug", action="store_true", help="Show raw response")
    args = parser.parse_args()

    print("🤖 Gemini CLI (type 'exit' to quit)\n")

    while True:
        try:
            prompt = input("You: ").strip()
            if prompt.lower() in {"exit", "quit"}:
                print("👋 Bye!")
                break

            if not prompt:
                continue

            answer, raw = ask_gemini(prompt, args.debug)

            print("\nGemini:\n")
            print(answer)

            if args.debug:
                print("\n--- RAW RESPONSE ---\n")
                print(raw)

            print("\n" + "-" * 60)

        except KeyboardInterrupt:
            print("\n👋 Interrupted. Exiting.")
            break

        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
