import streamlit as st
import requests
import re


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
            # Highlight keyword in the sentence with red color using HTML/CSS
            highlighted_sentence = re.sub(rf'({re.escape(keyword)})', r'<span style="color:red;"><b>\1</b></span>', sentence, flags=re.IGNORECASE)
            matching_sentences.append((part_heading, highlighted_sentence))

    return matching_sentences

# Streamlit App
def main():
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("retirement_benefits_image.jpg")  # Replace with your image

    with col2:
        st.title("Retirement Benefits Regulations Search Tool")
        st.markdown("**Document:** [GitHub Repository Link](...)")  # Add a link

        # Fetch the text from GitHub with loading indicator
        with st.spinner("Fetching document..."): 
            url = "https://raw.githubusercontent.com/Winnie-Mukunzi/Module-IV/main/RetirementBenefitsAct3of1997_subsidiary_Rev2022.txt"
            try:
                response = requests.get(url)
                response.raise_for_status()  # Check for HTTP errors
                text = response.text
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching document: {e}")
                return 

        # Get user input with a search button
        keyword = st.text_input("Enter keyword to search:")
        if st.button("Search"):
            # Search and display results with loading indicator
            with st.spinner("Searching for keyword..."):
                matching_sentences = search_text_regex(text, keyword)

            if matching_sentences:
                st.markdown(f"Found matching sentences for '**{keyword}**':")
                # ... (Display logic with styling) ... 
            else:
                st.markdown(f"No matching sentences found for '**{keyword}**'.")

if __name__ == "__main__":
    main()
