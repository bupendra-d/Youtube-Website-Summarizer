import os
import validators
import requests
import streamlit as st

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

from langchain_groq import ChatGroq
from langchain_classic.prompts import PromptTemplate
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Configuration
load_dotenv()

st.set_page_config(
    page_title="YouTube & Website Summarizer",
    page_icon="🦜"
)

st.title("🦜 YouTube & Website Summarizer")
st.write("Summarize YouTube videos and website content instantly.")

url = st.text_input("Enter YouTube or Website URL")


# Summarization Prompt
prompt = PromptTemplate(
    template="""
    Summarize the following content in approximately 300 words.
    Include all important points and key concepts.
    Write the summary in clear, simple English.

    Content:
    {text}
    """,
    input_variables=["text"]
)


# Extract YouTube Video ID
def extract_video_id(url):
    parsed = urlparse(url)
    host = parsed.hostname or ""

    if host in ["youtube.com", "www.youtube.com", "m.youtube.com"]:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]

        if parsed.path.startswith(("/shorts/", "/embed/", "/live/")):
            parts = parsed.path.strip("/").split("/")
            return parts[1] if len(parts) > 1 else None

    if host in ["youtu.be", "www.youtu.be"]:
        return parsed.path.strip("/").split("/")[0]

    return None


# Extract YouTube Transcript
def get_youtube_transcript(video_id):
    api = YouTubeTranscriptApi()
    transcripts = api.list(video_id)

    try:
        transcript = transcripts.find_transcript(["en", "hi"])

    except Exception:
        available = list(transcripts)

        translatable = next(
            (item for item in available if item.is_translatable),
            None
        )

        if not translatable:
            raise ValueError(
                "No suitable transcript is available for this video."
            )

        transcript = translatable.translate("en")

    fetched = transcript.fetch()

    return " ".join(item.text for item in fetched)


# Extract Website Content
def get_website_content(url):
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup([
        "script", "style", "noscript", "svg",
        "nav", "footer", "header", "aside", "form"
    ]):
        tag.decompose()

    content = soup.get_text(separator="\n", strip=True)

    if not content.strip():
        raise ValueError("Unable to extract website content.")

    return content


# Summarize Content
if st.button("Summarize Content", type="primary"):

    if not url.strip():
        st.error("Please enter a URL.")

    elif not validators.url(url.strip()):
        st.error("Please enter a valid URL.")

    elif not os.getenv("GROQ_API_KEY"):
        st.error("Groq API key not found. Check your .env file.")

    else:
        try:
            with st.spinner("Extracting content and generating summary..."):

                # Initialize LLM
                llm = ChatGroq(
                    model="openai/gpt-oss-20b",
                    groq_api_key=os.getenv("GROQ_API_KEY")
                )

                # Load YouTube Transcript or Website Content
                video_id = extract_video_id(url.strip())

                if video_id:
                    content = get_youtube_transcript(video_id)

                else:
                    content = get_website_content(url.strip())

                if not content.strip():
                    raise ValueError("No content available to summarize.")

                docs = [
                    Document(
                        page_content=content,
                        metadata={"source": url.strip()}
                    )
                ]

                # Split Content into Chunks
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=8000,
                    chunk_overlap=500
                )

                docs = splitter.split_documents(docs)

                # Map-Reduce Summarization
                chain = load_summarize_chain(
                    llm=llm,
                    chain_type="map_reduce",
                    map_prompt=prompt,
                    combine_prompt=prompt
                )

                response = chain.invoke({
                    "input_documents": docs
                })

                # Display Summary
                st.success("Summary generated successfully!")
                st.subheader("Summary")
                st.write(response["output_text"])

        except requests.exceptions.RequestException as e:
            st.error(f"Website extraction failed: {e}")

        except Exception as e:
            st.error(f"Unable to summarize content: {e}")
