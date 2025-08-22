# Studybuddy
## Introduction
The project is for the [TiDB Devopost Hackaton](https://tidb-2025-hackathon.devpost.com/?ref_content=default&ref_feature=challenge&ref_medium=portfolio).

Studybuddy is an AI agent that wants to help a student with their studies. 
The user can interract with its studybuddy through a Telegram Bot (@hackaton_study_buddy_bot). 

## Capabilities
What can the Studybuddy do?

1. **Upload Notes:** Users can upload their study notes (supported formats: DOCX and PDF) directly in the chat. The files are stored in TiDB, and their content is embedded to enable semantic search.

2. **Search Notes:** Users can search through their notes using natural language queries, such as “What notes do I have about machine learning?”.

3. **List Notes:** Users can retrieve a list of all the notes stored in the database for easy navigation.

4. **Interact with Notes (LLM-Powered):** Users can select a specific note and interact with it using StudyBuddy’s AI capabilities. For example, they might ask the assistant to generate practice questions, summarize content, or explain complex concepts. The possibilities are as broad as the user’s imagination.

5. **Online search**: StudyBuddy is equipped with Wikipedia search, allowing users to enrich and expand their notes with reliable external information.

The main feature of StudyBuddy is its simplicity: it feels like a regular chat where users can interact naturally, using nothing but their own language.

## Running StudyBuddy

### 1. Install dependencies

Make sure you have Python 3.10+ installed, then install the required packages:

```
pip install -r requirements.txt
```

### 2. Set up your TiDB account
1. Create an account on TiDB Cloud

2. Create a database.

3. Using the SQL editor, create the following tables:
    ```
    CREATE TABLE notes (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(55),
    ext VARCHAR(10),
    upload_timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    ); 

    CREATE TABLE note_chunks (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    note_id VARCHER(55),
    chunck_order INTEGER,
    content TEXT,
    embedding VECTOR(1536),
    VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)))
    )
    ```
4. Click the button "Connect" and copy the following parameters into a ```.env``` file with the structure:

```
tidb_pass=""
tidb_user='"
tidb_host=""
tidb_port=""
tidb_db=""
```

### 3. Get a OpenAI API key

Get an openAI API key and copy it into the .env file, as:

```
openai_api_key=""
```

### 2. Set up your Telegram bot
You can try studybuddy with the bot @hackaton_study_buddy_bot.

If you prefer to build one from scratch: 
1. Create a bot via BotFather on Telegram.
2. Copy the generated bot token.
3. Add it to the .env file under the variable name
 
    ```
    telegram_bot_api_key=""
    ```


### 3. Run the script
After installing the required dependencies and setting up your environment, you can start Studybuddy by running the main script:

```
python main.py
```

On startup, you’ll be prompted to choose how you want to interact with Studybuddy:

Option 1 (Telegram bot): Runs Studybuddy as a Telegram bot. Make sure you have configured your Telegram bot token (e.g., in your environment variables or config file) before choosing this option. Once started, you can chat with Studybuddy directly in Telegram. Stop it anytime with Ctrl + C.

Option 2 (Terminal): Runs Studybuddy in your terminal. The bot will introduce itself and you can then type your messages directly. To exit, simply tell the bot you want to quit, or let it detect the "QUIT" keyword.

If you enter anything other than 1 or 2, you’ll be reminded that only those choices are valid.

