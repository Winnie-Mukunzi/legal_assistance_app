import streamlit as st
import requests
import re
import nltk


# Function to extract sentences from text
def extract_sentences(text):
    """
    This function takes a text string as input and splits it into individual sentences.
    It assumes sentences are separated by periods ('.').
    Args:
        text: A string containing the text to be split into sentences.
    Returns:
        A list of strings, where each string represents a sentence from the original text.
    """
    return text.split('.')  # Split by sentences

# Function to search for keyword in text using regular expressions (exact match)
def search_text_regex(text, keyword):
    """
    This function searches for the exact keyword within sentences of the provided text document.
    It uses regular expressions for flexible pattern matching.
    Args:
        text: A string containing the text document to be searched.
        keyword: A string representing the keyword to search for.
    Returns:
        A list of tuples containing (part_heading, sentence_with_highlight) for matching sentences.
    """
    sentences = extract_sentences(text)
    matching_sentences = []
    part_heading = None

    for sentence in sentences:
        # Check if the sentence contains a "PART" heading
        part_match = re.match(r'\s*PART\s+[IVXLCDM]+\s*[-–—]\s*[A-Z\s]+', sentence, re.IGNORECASE)
        if part_match:
            part_heading = part_match.group().strip()

        if re.search(keyword, sentence, flags=re.IGNORECASE):  # Ignore case for flexibility
            # Highlight keyword in the sentence with red color
            highlighted_sentence = re.sub(rf'({re.escape(keyword)})', r'<span style="color:red"><b>\1</b></span>', sentence, flags=re.IGNORECASE)
            matching_sentences.append((part_heading, highlighted_sentence))

    return matching_sentences

# Streamlit App
def main():
    st.title("Keyword Search in Text Document")

    # Fetch the text document from GitHub URL
    url = "https://raw.githubusercontent.com/Winnie-Mukunzi/Module-IV/main/RetirementBenefitsAct3of1997_subsidiary_Rev2022.txt"
    response = requests.get(url)
    text = response.text

    # Get user input for search keyword
    keyword = st.text_input("Enter keyword to search:")

    if st.button("Search"):
        # Search method
        matching_sentences = search_text_regex(text, keyword)  # Recommended for exact keyword matching

        # Display the matching sentences with highlighted keywords and associated "PART" headings
        if matching_sentences:
            st.markdown(f"Found matching sentences for '**{keyword}**':")
            for part_heading, sentence_with_highlight in matching_sentences:
                if part_heading:
                    # Print PART heading in bold
                    st.markdown(f"**{part_heading}**: {sentence_with_highlight}")
                else:
                    st.markdown(sentence_with_highlight)
        else:
            st.markdown(f"No matching sentences found for '**{keyword}**'.")

if __name__ == "__main__":
    main()
