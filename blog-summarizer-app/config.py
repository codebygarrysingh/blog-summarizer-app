# Configuration for the Blog Summarizer App

# OpenAI API Key (Replace with your actual API key)
OPENAI_API_KEY = "YOUR_API_KEY_HERE"

# Directory containing Markdown blog articles
BLOG_DIR = "YOUR_BLOG_DIR_PATH_HERE"

# File extension for blog articles, for example .markdown
BLOG_FILE_EXT = "YOUR_BLOG_FILE_EXT_HERE"

# Offset for starting to read content from Markdown files
BLOG_OFFSET = 11

# Name of the OpenAI model to use for summarization
MODEL_NAME = "text-davinci-002"

# Maximum number of tokens for the response
MAX_RESPONSE_TOKENS = 150

# Insertion marker for the blog files
INSERTION_MARKER = "<!-- Insert Summary Here -->"
