# AI-github-assistant

An AI-powered tool to automatically analyze and summarize GitHub issues using **OpenAI GPT** or **Google Gemini 1.5 Pro**.  
Built with FastAPI and Streamlit — this app fetches issue data, runs an LLM-based analysis, and returns a structured JSON with the issue’s **summary**, **type**, **priority**, **labels**, and **impact**.

---

## 🚀 Features

✅ Analyze any public GitHub issue by just pasting the repository URL and issue number  
🧠 Toggle between OpenAI and Gemini 1.5 Pro for LLM inference  
🗂️ Get structured metadata including:
- `summary`: Brief explanation of the issue
- `type`: bug, feature, documentation, question, etc.
- `priority`: high, medium, low
- `labels`: relevant tags
- `impact`: low, medium, high

---

## 🧱 Tech Stack

| Component     | Technology      |
|---------------|------------------|
| Frontend UI   | Streamlit        |
| Backend API   | FastAPI          |
| LLMs          | OpenAI + Gemini  |
| Deployment    | Localhost        |
| Data Source   | GitHub REST API  |

---

## 📦 Project Structure

```
github-issue-analyzer/
│
├── main.py          # FastAPI backend (LLM + GitHub logic)
├── ui.py            # Streamlit UI
├── .env             # API keys
├── requirements.txt
└── README.md
```

---

## 🔐 Environment Setup

Create a `.env` file:

```env
OPENAI_API_KEY=your-openai-key
GOOGLE_API_KEY=your-gemini-key
```

---

## 🛠️ Installation

### Step 1: Clone the Repo

```bash
git clone https://github.com/Peeps16/AI-github-assistant
cd AI-github-assistant
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Backend (FastAPI)

```bash
uvicorn main:app --reload
```

### Step 4: Run the Frontend (Streamlit)

```bash
streamlit run ui.py
```

---

## 🧪 Example Input

| Field              | Value                                  |
|--------------------|----------------------------------------|
| GitHub Repo URL    | `https://github.com/psf/requests`      |
| Issue Number       | `6500`                                 |
| Use Gemini?        | ✅ (checkbox)                           |

---

## ✅ Sample Output

```json
{
  "summary": "This issue discusses a bug in the session timeout behavior.",
  "type": "bug",
  "priority": "medium",
  "labels": ["session", "timeout", "bug"],
  "impact": "medium"
}
```

---

## 💡 How it Works

1. The frontend (`ui.py`) collects the repo URL, issue number, and model preference.
2. It sends the data to the FastAPI backend (`main.py`).
3. The backend:
   - Calls the GitHub REST API to fetch the issue.
   - Formats the prompt and sends it to **OpenAI** or **Gemini 1.5 Pro**.
   - Parses and returns the structured response.
4. The frontend displays the results as prettified JSON.

---

## ⚙️ requirements.txt

```txt
fastapi
uvicorn
openai>=1.0.0
google-generativeai
requests
streamlit
python-dotenv
```

---

## 📌 Notes

- Make sure to enable the **Generative Language API** in your Google Cloud Console.
- You must have access to **gemini-1.5-pro** to use Gemini inference.

---

## 👨‍💻 Author

**Pratyush Pankaj**  
PES University | PES1UG21CS445  
Intern @ Juniper Networks  
Submitted for Seedling Labs LLM Challenge

---

## 🤝 Acknowledgements

- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Google Generative AI SDK](https://ai.google.dev/)
- [GitHub REST API](https://docs.github.com/en/rest)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
