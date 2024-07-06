# Personalized AI Email Assistant

## Overview

The AI Email Assistant aims to simplify email management for Gmail users by automating the process of email categorization and summarization. It's designed for individuals overwhelmed by their inbox, helping them quickly prioritize and process their emails.

### Project Intent
As a college student or any knowledge professional, we tend to receive a lot of mails daily, most of which might not be relevant for the individual. This can cause a lot of inbox clutter if the mails are not managed on a daily basis, which can take a lot of time. This assistant aims to solve the issue of inbox clutter by leveraging the power of generative AI and utilizing techniques like RAG to make the agent adaptable to any individuals' needs by simply stating their preferences.

## What It Does

### Features
- **Personalization**: Utilizing RAG, users can fill in their preferences and details which the generative agent uses to manage the emails.
- **Email Organization**: The assistant categorizes and organizes incoming emails based on the users preferences.
- **Email Summarization**: The generative agent summarizes the content to make it easier to manage emails.
- **Email Filtering**: Owing to generative AI and RAG, we can aim to filter mails that are not relevant to the user even if the mail is from a whitelisted source.

### How It Works
1. The system authenticates with your Gmail account using OAuth 2.0
2. It retrieves unread emails from your inbox using the Gmail API
3. Each email is processed by an AI model (Gemini 1.5 Pro) to generate a summary and category
4. Email content and AI-generated data are saved as local files
5. An Excel spreadsheet is created, compiling all email metadata and AI results
6. The system can update email status (read/unread, starred) based on user preferences

#### Project Structure and Script Descriptions
The system consists of several Python scripts, each handling specific functionalities:

- `Main.py`: The entry point of the application. It orchestrates the entire process by calling functions from other scripts.
- `GmailAPI.py`: Manages interactions with the Gmail API, including fetching emails and updating their status.
- `EmailAssistant.py`: Contains the AI-powered functions for generating email summaries and categories using the Gemini 1.5 Pro model.
- `FileManagement.py`: Handles reading from and writing to Excel files, managing the storage of processed email data.

## How to Use It

1. Clone the repository and install dependencies:
```
git clone https://github.com/AbhayKejriwal/AI_Email_Assistant
```
```
cd AI_Email_Assistant
pip install -r requirements.txt
```

2. Set up Google Cloud Project and Gmail API:
- Create a project in Google Cloud Console
- Enable Gmail API for your project
- Create OAuth 2.0 credentials and download as `credentials.json`
- Place `credentials.json` in the project directory

3. Run the main script:
```
python Main.py
```

4. The system will process your unread emails and generate an Excel file with summaries and categories. You can review this file to quickly assess your inbox.

## Features to add
- Intuitive GUI
- Ads and junk filtering in email
- Multiple user accounts
- Other email clients 