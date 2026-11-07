# YouTube & Website Summarizer

An AI-powered application that summarizes YouTube videos and website content using **LangChain and Groq LLMs**. Supports English and Hindi YouTube transcripts and generates concise summaries in English.

## Live Demo

[Try the YouTube & Website Summarizer](https://youtube-website-summarizer-m7e27sfw6xkwkabumpwilg.streamlit.app/)

## Features

- Summarizes YouTube videos and website content.
- Supports English and Hindi YouTube transcripts.
- Translates available transcripts into English when required.
- Extracts website content using Requests and BeautifulSoup.
- Uses text splitting and Map-Reduce summarization for longer content.
- Generates summaries of approximately 300 words.
- Simple and interactive interface built with Streamlit.

## Tech Stack

- **Python** – Core programming language
- **Streamlit** – Web application interface
- **LangChain** – LLM integration and summarization
- **Groq** – LLM inference using GPT-OSS 20B / 120B
- **Supadata API** – YouTube transcript extraction
- **BeautifulSoup** – Website content extraction
- **Requests** – HTTP requests
- **Recursive Character Text Splitter** – Text chunking

## Local Setup

**1. Clone the repository**

```bash
git clone https://github.com/bupendra-d/Youtube-Website-Summarizer.git
cd Youtube-Website-Summarizer
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project directory:

GROQ_API_KEY=your_groq_api_key
SUPADATA_API_KEY=your_supadata_api_key

Get your API keys from:
- [Groq Console](https://console.groq.com/keys)
- [Supadata](https://supadata.ai/)

**5. Run the application**

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Deployment

The application is deployed using Streamlit Community Cloud.

Configure the following secrets under your Streamlit application's **Settings → Secrets**:

GROQ_API_KEY = "your_groq_api_key"
SUPADATA_API_KEY = "your_supadata_api_key"

The API key is securely managed through environment variables and is not exposed in the application interface.

## Note

- YouTube summarization requires an accessible transcript. Videos without available transcripts or with restricted access may not be supported.
- Website summarization depends on the website allowing automated content extraction.
- Very large content may require additional processing time and API usage.