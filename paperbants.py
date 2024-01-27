import streamlit as st

FILENAME = "user_inputs.txt"
COMMENTS_FILE = "comments.txt"
QUERIES_FILE = "queries.txt"

# Function to store inputs
def store_inputs(title, url, summary, usecase):
    with open(FILENAME, "a") as file:
        file.write(f"Title: {title}\n")
        file.write(f"URL: {url}\n")
        file.write("===\n")
        file.write(f"Summary: {summary}\n")
        file.write(f"Use Case: {usecase}\n")
        file.write("===\n")

# Function to store comments
def store_comment(submission_title, comment):
    if comment.strip():  # Ensure the comment is not empty
        with open(COMMENTS_FILE, "a") as file:
            file.write(f"Submission Title: {submission_title}\n")
            file.write(f"Comment: {comment}\n")
            file.write("===\n")

def display_submissions():
    try:
        with open(FILENAME, "r") as file:
            submissions = file.read().split("===\n")
            for submission in submissions:
                if submission.strip():
                    submission_details = submission.strip().split('\n')
                    if len(submission_details) > 1:  # Check if the title is present
                        submission_title = submission_details[0].split('Title: ')[1]
                        st.text_area("", submission.strip(), height=200, key=f'submission_{submission_title}')
                        if st.button("Add Comment", key=f'btn_{submission_title}'):
                            st.session_state['comment_submission_title'] = submission_title
                            st.experimental_rerun()
                        st.markdown("---")
    except FileNotFoundError:
        st.write("No submissions yet.")

def display_comments(submission_title):
    try:
        with open(COMMENTS_FILE, "r") as file:
            comments = file.read().split("===\n")
            for index, comment in enumerate(comments):
                if comment.strip():
                    comment_details = comment.strip().split('\n')
                    title_line = next((line for line in comment_details if line.startswith('Submission Title: ')), None)
                    comment_line = next((line for line in comment_details if line.startswith('Comment: ')), None)
                    if title_line and comment_line:
                        title = title_line.split('Submission Title: ')[1]
                        if title == submission_title:
                            comment_text = comment_line.split('Comment: ')[1]
                            st.text(comment_text)
                            st.markdown("---")
    except FileNotFoundError:
        st.write("No comments yet.")

def comment_page():
    st.title("Discussion")
    submission_title = st.session_state.get('comment_submission_title', '')
    if submission_title:
        st.write(f"Discussion for: {submission_title}")

        # Add a comment section within a form
        with st.form("comment_form"):
            comment = st.text_area("Add a Comment", height=200)
            submit_comment = st.form_submit_button("Submit Comment")

        if submit_comment and comment.strip():
            store_comment(submission_title, comment)
            st.success("Comment added!")

        # Display all comments (including the newly added one) under the comment form
        display_comments(submission_title)

    else:
        st.write("No submission selected for commenting.")

# Function to store queries
def store_query(query):
    with open(QUERIES_FILE, "a") as file:
        file.write(f"{query}\n===\n")

def main():
    page = st.sidebar.selectbox("Choose a page:", ["Home", "Submit", "Feed", "Discussion"])

    if page == "Home":
        st.title("Ask a Question")
        with st.form("query_form"):
            query = st.text_area("Explore knowledge", height=100)
            submit_query = st.form_submit_button("Submit Question")

        if submit_query and query.strip():
            store_query(query)
            st.success("Question submitted!")

    elif page == "Submit":
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

    elif page == "Discussion":
        comment_page()

if __name__ == "__main__":
    main()
