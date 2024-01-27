from collections import defaultdict

# Path to the comments file
COMMENTS_FILE = "comments.txt"

# Function to read comments and organize them by title
def read_and_organize_comments():
    comments_by_title = defaultdict(list)
    
    try:
        with open(COMMENTS_FILE, "r") as file:
            comment_blocks = file.read().strip().split("===\n")
            for block in comment_blocks:
                if '|' in block:
                    title, comment = block.split('|', 1)
                    comments_by_title[title.strip()].append(comment.strip())
                else:
                    print(f"Invalid comment block detected: {block}")

    except FileNotFoundError:
        print(f"The file {COMMENTS_FILE} does not exist.")
    
    return comments_by_title

comments_by_title = read_and_organize_comments()

from rank_bm25 import BM25Okapi
import numpy as np

# Flatten the comments for BM25 processing
titles = list(comments_by_title.keys())
flattened_comments = [comment for comments in comments_by_title.values() for comment in comments]

# Tokenize the comments
tokenized_comments = [doc.split(" ") for doc in flattened_comments]

# Create the BM25 object
bm25 = BM25Okapi(tokenized_comments)

# Function to use BM25 to retrieve comments based on a query
def bm25_retrieve_comments(query):
    tokenized_query = query.split(" ")
    scores = bm25.get_scores(tokenized_query)
    top_indexes = np.argsort(scores)[::-1]  # Get the indexes of the comments in descending order of relevance
    top_comments = [flattened_comments[i] for i in top_indexes if scores[i] > 0]
    return top_comments

# Example usage
query = "What are they commenting about computer vision cars"
top_comments_for_query = bm25_retrieve_comments(query)

