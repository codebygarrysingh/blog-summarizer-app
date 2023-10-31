# 
# Author: Garry Singh
# Version: 1.0
# Last Updated: 2023-10-31
# Description: App for summarizing content of blog articles
#

# Import necessary libraries/modules
import os
import openai
import tiktoken
from bs4 import BeautifulSoup

# Initialize the OpenAI client
openai.api_key = "<OPEN_API_KEY>"

# Set the input directory that contains the Markdown files to be summarized
input_dir = "<PATH_TO_INPUT_DIR>"

# Maximum number of tokens allowed for the prompt
max_prompt_tokens = 1000

# Insertion marker for the blog file
insertion_marker = "<!-- Insert Summary Here -->"

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("text-davinci-002")
    num_tokens = len(encoding.encode(string))
    return num_tokens

# Iterate through the Markdown files in the input directory
for filename in os.listdir(input_dir):
    # Process only the Markdown files
    if filename.endswith(".markdown"):
        with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
            # Read all lines into a list
            lines = file.readlines()

            # Start reading from the 12th line and join the remaining lines
            content = "".join(lines[11:])

            if content.__contains__(insertion_marker):
                soup = BeautifulSoup(content, "html.parser")
                cleaned_content = soup.get_text()
                
                #token_count = num_tokens_from_string(cleaned_content, "text-davinci-002")
                
                # Check if the prompt exceeds the maximum allowed tokens
                #if token_count > max_prompt_tokens:
                    # Truncate the cleaned content to the maximum allowed tokens
                #    cleaned_content = cleaned_content[:max_prompt_tokens]

                # Create a prompt that instructs the model to summarize the content
                prompt = f"Please provide a coherent and complete summary of the following content:\n{cleaned_content}\n"

                # Generate a summary request to the OpenAI client
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=prompt,  # Using the content of the file as the prompt
                    max_tokens=150
                )

                generated_summary = response.choices[0].text.strip()

                # Find the last occurrence of a period in the generated summary
                last_period_index = generated_summary.rfind(".")
                
                # Check if a period was found in the generated summary
                if last_period_index != -1:
                    # Trim the content after the last period
                    trimmed_summary = generated_summary[:last_period_index + 1]

                    # Replace the insertion marker with the trimmed summary in the content
                    updated_content = "".join(lines).replace(insertion_marker, trimmed_summary)
                else:
                    # Handle the case where no period was found in the generated summary
                    updated_content = "".join(lines)

                # Write the updated content with generated summary to the Markdown file
                with open(os.path.join(input_dir, filename), 'w', encoding='utf-8') as file:
                    file.write(updated_content)
