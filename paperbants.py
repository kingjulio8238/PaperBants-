import streamlit as st

FILENAME = "user_inputs.txt"

# Function to store inputs
def store_inputs(title, url, summary, usecase):
    # You can modify this function to store the inputs as needed,
    # e.g., saving to a database, a file, or another data structure.
    with open(FILENAME, "a") as file:
        file.write(f"Title: {title}\n")
        file.write(f"URL: {url}\n")
        file.write("===\n")
        file.write(f"Summary: {summary}\n")
        file.write(f"Use Case: {usecase}\n")
        file.write("===\n")

def display_submissions():
    try:
        with open(FILENAME, "r") as file:
            submissions = file.read().split("===\n")
            for submission in submissions:
                if submission.strip():
                    st.text_area("", submission.strip(), height=200)
                    st.markdown("---")
    except FileNotFoundError:
        st.write("No submissions yet.")

# Streamlit page layout
def main():
    page = st.sidebar.selectbox("Choose a page:", ["Submit", "Feed"])

    if page == "Submit":
        st.title("Submit your thoughts")
        with st.form("submission_form"):
            title = st.text_input("Title")
            url = st.text_input("URL to Paper")
            summary = st.text_area("Summary", height=200)
            usecase = st.text_input("Use Case")
            submitted = st.form_submit_button("Submit")

        if submitted:
            store_inputs(title, url, summary, usecase)
            st.success("Submission Saved!")

    elif page == "Feed":
        st.title("Submission Feed")
        display_submissions()

if __name__ == "__main__":
    main()