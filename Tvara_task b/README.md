## Gemini CLI Client

This repository contains a simple Python command‑line client for Google's Gemini API, implemented in `gemini_client.py`. It allows you to have an interactive chat‑style conversation with the Gemini model directly from your terminal.

---

### 1. Prerequisites

- **Python**: 3.8 or higher
- **Google Gemini API key**: You must have a valid API key and enable access to the Gemini API in your Google Cloud project.
- **Internet access**: The client sends HTTPS requests to the Gemini API endpoint.

---

### 2. Installation & Setup

#### **Clone or download the project**

Place the files (including `gemini_client.py`) in a directory of your choice.

#### **Create and activate a virtual environment** (recommended)

```bash
python -m venv .venv
.venv\Scripts\activate
```

On PowerShell (your current shell), you can run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### **Install dependencies**

The script uses `requests` for HTTP calls and `python-dotenv` to load environment variables from a `.env` file.

```bash
pip install requests python-dotenv
```

Optionally, create a `requirements.txt`:

```text
requests
python-dotenv
```

and install with:

```bash
pip install -r requirements.txt
```

#### **Configure your API key**

Create a `.env` file in the same directory as `gemini_client.py`:

```text
GEMINI_API_KEY=your_real_gemini_api_key_here
```

The script uses:

```python
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
```

If `GEMINI_API_KEY` is missing, the script raises:

> `RuntimeError("GEMINI_API_KEY not found in .env")`

---

### 3. How to Run

From the project directory (where `gemini_client.py` is located), run:

```bash
python gemini_client.py
```

For debug mode (prints the raw JSON response from Gemini in addition to the model's text):

```bash
python gemini_client.py --debug
```

or:

```bash
python gemini_client.py -d
```

You will see a prompt like:

```text
🤖 Gemini CLI (type 'exit' to quit)

You:
```

Type your message and press Enter. Type `exit` or `quit` to end the session, or press `Ctrl+C` to interrupt.

---

### 4. Implementation Details & Approach

- **Environment loading**: The script uses `python-dotenv` (`load_dotenv()`) to read configuration from a `.env` file so secrets are not hard‑coded.
- **Configuration**:
  - Reads `GEMINI_API_KEY` from the environment.
  - Defines the Gemini API endpoint as:

    ```python
    GEMINI_ENDPOINT = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.0-flash:generateContent"
    )
    ```

- **Core request function**: `ask_gemini(prompt: str, debug: bool = False)`:
  - Builds the request payload according to the Gemini `generateContent` API:

    ```python
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    ```

  - Sends an HTTP POST using `requests.post` with JSON body and a 30‑second timeout.
  - Raises an error for non‑2xx responses (`response.raise_for_status()`).
  - Parses the JSON and extracts the model's reply from `data["candidates"][0]["content"]["parts"][0]["text"]`.
  - Returns `(answer, raw_json)` when `debug` is `True`, otherwise `(answer, None)`.

- **CLI loop** (`main()`):
  - Uses `argparse` to support a `--debug` / `-d` flag.
  - Prints a simple header and then enters a loop:
    - Reads user input (`You: `).
    - Exits on `exit` or `quit`.
    - Skips empty input.
    - Calls `ask_gemini` and prints the response.
    - In debug mode, also prints the entire raw response for inspection.
  - Catches `KeyboardInterrupt` (`Ctrl+C`) and other exceptions, printing a friendly message instead of crashing.

This structure keeps the core Gemini call isolated in `ask_gemini` while `main()` focuses on user interaction and basic error handling, making the script easy to extend (e.g., adding system prompts, conversation history, or other CLI options) later.


