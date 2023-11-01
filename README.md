# Blog Summarizer App

![License](https://img.shields.io/badge/License-MIT-green.svg)

## Overview

The Blog Summarizer App is a Python application designed to automate the process of summarizing the content of blog articles. It utilizes the OpenAI API to generate concise and coherent summaries from the input content. This app is useful for content creators and bloggers who want to provide a summary of their articles, making it easier for readers to grasp the main points.

## Features

- Summarize blog articles automatically.
- Customizable token limits and OpenAI model selection.
- Process Markdown files and add summaries to specified insertion markers.

## Prerequisites

Before using the Blog Summarizer App, ensure that you have the following prerequisites:

- Python 3.x installed on your system.
- An OpenAI API key for making API requests.

## Installation

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/codebygarrysingh/blog-summarizer-app.git
   cd blog-summarizer-app
2. Install the required Python packages using pip.
3. Configure your OpenAI API key in the config.py file:

## Usage

1. Place your blog articles in the designated directory
2. Configure the app using the constants in the config.py file. You can adjust token limits and other settings.
3. Run the app using the following command:
    ```shell
    python main.py

The app will process the blog files, generate summaries, and update the content using the specified insertion markers. The summarized content will replace the marker in each file.

## Customization

You can customize the behavior of the Blog Summarizer App by modifying the constants and configurations in the config.py file. For example, you can change the OpenAI model, token limits, and insertion markers.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Special thanks to OpenAI for their powerful language models.
Inspired by the need to simplify the process of summarizing blog articles.

