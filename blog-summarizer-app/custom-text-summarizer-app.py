# Author: Garry Singh
# Version: 2.0
# Last Updated: 2023-10-31
# Description: App for summarizing content of blog articles

# Import necessary libraries/modules
import os
import openai
import tiktoken
from bs4 import BeautifulSoup
import config

# Constants
OPENAI_API_KEY = config.OPENAI_API_KEY
BLOG_DIR = config.BLOG_DIR
BLOG_FILE_EXT = config.BLOG_FILE_EXT
BLOG_OFFSET = config.BLOG_OFFSET # Offset to start processing blog content after this line number
MODEL_NAME = config.MODEL_NAME
MAX_RESPONSE_TOKENS = config.MAX_RESPONSE_TOKENS
INSERTION_MARKER = config.INSERTION_MARKER # Placeholder for blog summary in blog files

# Initialize the OpenAI client
openai.api_key = OPENAI_API_KEY

def num_tokens_in_content(content: str, model_name: str) -> int:
    """
    Count the number of tokens in a text string.

    Args:
        content (str): The text content to count tokens in.
        model_name (str): The name of the language model used for tokenization.

    Returns:
        int: The number of tokens in the content.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(content))
    return num_tokens

def generate_blog_summary(content: str, model_name: str, max_tokens: int) -> str:
    """
    Generate a summary of the content using OpenAI.

    Args:
        content (str): The content to generate a summary for.
        model_name (str): The name of the language model to use.
        max_tokens (int): The maximum number of tokens in the generated summary.

    Returns:
        str: The generated summary.
    """
    prompt = f"Please provide a coherent and complete summary of the following content:\n{content}\n"

    # Generate a summary request to the OpenAI client
    response = openai.Completion.create(
        engine=model_name,
        prompt=prompt,
        max_tokens=max_tokens
    )

    generated_summary = response.choices[0].text.strip()

    # Find the last occurrence of a period in the generated summary
    last_period_index = generated_summary.rfind(".")

    # Check if a period was found in the generated summary
    if last_period_index != -1:
        # Trim the content after the last period
        return generated_summary[:last_period_index + 1]

    return generated_summary

def add_summary_to_blogs():
    """
    Process and update blog files with generated summaries.
    """
    # Iterate through the files in the input directory
    for blog_file_name in os.listdir(BLOG_DIR):
        # Process only the Markdown files
        if blog_file_name.endswith(BLOG_FILE_EXT):
            with open(os.path.join(BLOG_DIR, blog_file_name), 'r', encoding='utf-8') as file:
                # Read all lines into a list
                lines = file.readlines()

                # Start reading from the 12th line and join the remaining lines
                content = "".join(lines[BLOG_OFFSET:])

                if content.__contains__(INSERTION_MARKER):
                    soup = BeautifulSoup(content, "html.parser")
                    cleaned_content = soup.get_text()

                    # Create a prompt that instructs the model to summarize the content
                    summary = generate_blog_summary(cleaned_content, MODEL_NAME, MAX_RESPONSE_TOKENS)

                    # Replace the insertion marker with the trimmed summary in the content
                    updated_content = "".join(lines).replace(INSERTION_MARKER, summary)

                    # Write the updated content with generated summary to the Markdown file
                    with open(os.path.join(BLOG_DIR, blog_file_name), 'w', encoding='utf-8') as file:
                        file.write(updated_content)

if __name__ == "__main__":
    add_summary_to_blogs()
