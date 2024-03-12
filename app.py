import streamlit as st
from bs4 import BeautifulSoup
import requests
import openai

# Initialize OpenAI with API key from Streamlit's secrets (or directly if you prefer)
openai.api_key = st.secrets["openai_api_key"]

def analyze_url(url):
    # Define headers with a User-Agent to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will raise an exception for HTTP error codes
        return response.text
    except requests.RequestException as e:
        st.error(f"Failed to retrieve data for {url}: {e}")
        return None

def get_meta_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else "No Title Found"
    description = soup.find("meta", attrs={"name": "description"})
    description = description["content"] if description else "No Description Found"
    return title, description

def generate_suggestions(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"Failed to generate suggestions: {e}")
        return "No suggestion available"

st.title("Single Page SEO Auditor")

url = st.text_input("Enter the URL of the page to audit:")

if url:
    html_content = analyze_url(url)
    if html_content:
        title, description = get_meta_data(html_content)
        st.write(f"**Current Meta Title:** {title}")
        st.write(f"**Current Meta Description:** {description}")
        
        # Generate suggestions
        new_title_prompt = f"Suggest a new meta title for a webpage with the current title '{title}' and description '{description}'."
        new_description_prompt = f"Suggest a new meta description for a webpage with the current title '{title}' and description '{description}'."
        
        new_title = generate_suggestions(new_title_prompt)
        new_description = generate_suggestions(new_description_prompt)
        
        st.write(f"**Suggested Meta Title:** {new_title}")
        st.write(f"**Suggested Meta Description:** {new_description}")
