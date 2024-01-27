import streamlit as st 

FILENAME = "user_inputs.txt"
COMMENTS_FILE = "comments.txt"
QUERIES_FILE = "queries.txt"

# Function to store inputs
def store_inputs(title, url, summary, usecase):
    with open(FILENAME, "a") as file:
        file.write(f"Title: {title}\n")
        file.write(f"URL: {url}\n")
        file.write(f"Summary: {summary}\n")
        file.write(f"Use Case: {usecase}\n")
        file.write("===\n")

def display_submissions():
    try:
        with open(FILENAME, "r") as file:
            submissions = file.read().split("===\n")
            for index, submission in enumerate(submissions):
                if submission.strip():
                    # Split the submission into its individual lines
                    submission_details = submission.strip().split('\n')

                    # Initialize variables to store the details
                    title, url, summary, usecase = "No Title", "No URL", "No Summary", "No Use Case"

                    # Extract each detail
                    for detail in submission_details:
                        if detail.startswith("Title: "):
                            title = detail.split("Title: ")[1]
                        elif detail.startswith("URL: "):
                            url = detail.split("URL: ")[1]
                        elif detail.startswith("Summary: "):
                            summary = detail.split("Summary: ")[1]
                        elif detail.startswith("Use Case: "):
                            usecase = detail.split("Use Case: ")[1]

                    # Display all parts of the submission together
                    st.write(f"**Title:** {title}")
                    st.write(f"**URL:** {url}")
                    st.write(f"**Summary:** {summary}")
                    st.write(f"**Use Case:** {usecase}")

                    # Button for adding a comment
                    button_key = f"btn_{index}"
                    if st.button("Add Comment", key=button_key):
                        st.session_state['comment_submission_title'] = title
                        st.experimental_rerun()

                    st.markdown("---")

    except FileNotFoundError:
        st.write("No submissions yet.")


# Function to store comments
def store_comment(submission_title, comment, parent_id=None):
    with open(COMMENTS_FILE, "a") as file:
        if parent_id:
            # Store as a reply to an existing comment
            file.write(f"{submission_title}|{comment}\n===\n")
        else:
            # Store as a new top-level comment
            file.write(f"{submission_title}|{comment}\n===\n")


def display_comments(submission_title):
    try:
        with open(COMMENTS_FILE, "r") as file:
            comments = file.read().split("===\n")
            for index, comment in enumerate(comments):
                if comment.strip():
                    parts = comment.strip().split('|')
                    if len(parts) == 2 and parts[0] == submission_title:
                        st.text(parts[1])
                        if st.button("Reply", key=f'reply_btn_{index}'):
                            st.session_state['parent_comment_id'] = index
                            st.session_state['comment_submission_title'] = submission_title
                            st.experimental_rerun()
                        st.markdown("---")
                    elif len(parts) == 3 and parts[1] == submission_title:
                        st.text(f"Reply to {parts[0]}: {parts[2]}")
                        st.markdown("---")
    except FileNotFoundError:
        st.write("No comments yet.")

def comment_page():
    st.title("Discussion")
    submission_title = st.session_state.get('comment_submission_title', '')
    parent_comment_id = st.session_state.get('parent_comment_id', None)

    if submission_title:
        st.write(f"Discussion for: {submission_title}")

        # Add a comment section within a form
        with st.form("comment_form"):
            comment = st.text_area("Add a Comment", height=200)
            submit_comment = st.form_submit_button("Submit Comment")

        if submit_comment and comment.strip():
            store_comment(submission_title, comment, parent_id=parent_comment_id)
            st.success("Comment added!")
            st.session_state['parent_comment_id'] = None  # Reset the parent comment ID after submitting

        # Display all comments and replies
        display_comments(submission_title)

    else:
        st.write("No submission selected for commenting.")

# Function to store queries
def store_query(query):
    with open(QUERIES_FILE, "a") as file:
        file.write(f"{query}\n===\n")

def main():
    page = st.sidebar.selectbox("Navigate:", ["Home", "Submit", "Feed", "Discussion"])

    if page == "Home":
        st.title("Knowledge Explorer")
        with st.form("query_form"):
            query = st.text_area("Explore papers", height=100)
            submit_query = st.form_submit_button("Search Paper")

        if submit_query and query.strip():
            store_query(query)
            st.success("Paper Query submitted!")

        with st.form("query_comments_form"):
            query_comments = st.text_area("Explore Comments", height=100)
            submit_comment_query = st.form_submit_button("Search Comments")

        if submit_comment_query and query_comments.strip():
            store_query(query_comments)
            st.success("Comment search submitted!")

        

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