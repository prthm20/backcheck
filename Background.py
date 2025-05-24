from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
import fitz
import re
from markdown import markdown
from bs4 import BeautifulSoup
load_dotenv()
YOUR_API_KEY = os.getenv("PERPLEXITY_API_KEY")

def markdown_to_text(md):
    # Convert markdown to HTML
    html = markdown(md)
    # Parse HTML to text
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()
def extract_links_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    links = []

    for page in doc:
        annotations = page.get_links()
        for link in annotations:
            if 'uri' in link:
                links.append(link['uri'])

    return links

def analyze_resume(pdf_path: Path) -> str:
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    context = "\n\n".join(doc.page_content for doc in docs)
    links = extract_links_from_pdf(pdf_path)
    links_str = "\n".join(links)

    full_prompt = f"""
    Here is the content of a resume:

    {context}

    Here are the extracted URLs from the resume (LinkedIn, GitHub, personal website, etc.):

    {links_str}

    Please perform a deep background analysis on this person.
    Check the URLs for:
    - Credibility and alignment with resume
    - Skills and contributions
    - Online presence and red flags
    - Professional achievements or inconsistencies

    Provide a detailed report.
    """

    messages = [
        {
            "role": "system",
            "content": "You are an AI that performs deep background analysis based on resumes and publicly available online information.",
        },
        {
            "role": "user",
            "content": full_prompt,
        },
    ]

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
       
    raw_response = response.choices[0].message.content
    cleaned_text = markdown_to_text(raw_response)
    return cleaned_text
