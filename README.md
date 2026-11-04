# YouTube & Website Summarizer

An AI-powered application that summarizes YouTube videos and website content using **LangChain and Groq LLMs**. Supports English and Hindi YouTube transcripts and generates concise summaries in English.

## Live Demo

[Try the YouTube & Website Summarizer](https://youtube-website-summarizer-m7e27sfw6xkwkabumpwilg.streamlit.app/)

### Deployment Note

The live application currently supports **website summarization**.

YouTube summarization is available when running the application locally. However, transcript retrieval may be restricted on Streamlit Community Cloud due to YouTube's IP-based access restrictions.

To use the complete functionality, including YouTube video summarization in English and Hindi, follow the local setup instructions below.

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
- **Groq** – LLM inference using GPT-OSS 20B
- **YouTube Transcript API** – YouTube transcript extraction
- **BeautifulSoup** – Website content extraction
- **Requests** – HTTP requests
- **Recursive Character Text Splitter** – Text chunking

## Local Setup

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/youtube-website-summarizer.git
cd youtube-website-summarizer
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

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from [Groq Console](https://console.groq.com/keys).

**5. Run the application**

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Deployment

The application is deployed using Streamlit Community Cloud.

Configure your `GROQ_API_KEY` under the application's **Settings → Secrets**:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

The API key is securely managed through environment variables and is not exposed in the application interface.

## Note

- YouTube summarization requires an accessible transcript. Videos without available transcripts or with restricted access may not be supported.
- Website summarization depends on the website allowing automated content extraction.
- Very large content may require additional processing time and API usage.