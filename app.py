import streamlit as st
import spacy
import json
import re

@st.cache_resource
def load_nlp_model():
    return spacy.load("en_core_web_sm")

def query_ner(text, nlp):
    doc = nlp(text)
    
    result = {
        "main_topic": "",
        "author": "",
        "years": []
    }
    
    # Extract main topic (everything before "by")
    by_index = text.lower().find(" by ")
    if by_index != -1:
        result["main_topic"] = text[:by_index].strip()
    
    # Extract author (everything between "by" and "from")
    from_index = text.lower().find(" from ")
    if by_index != -1 and from_index != -1:
        result["author"] = text[by_index + 4:from_index].strip()
    
    # Extract years
    years = re.findall(r'\b\d{4}\b', text)
    result["years"] = [int(year) for year in years]
    
    return result

def main():
    st.title("Named Entity Recognition App")
    st.write("Enter text to extract main topic, author, and years.")

    # Load the spaCy model
    nlp = load_nlp_model()

    # Text input
    text = st.text_area("Enter your text here:", height=100)

    if st.button("Analyze"):
        if text:
            result = query_ner(text, nlp)
            
            st.subheader("Extracted Information:")
            st.json(result)
        else:
            st.warning("Please enter some text to analyze.")

if __name__ == "__main__":
    main()