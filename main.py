from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
from langchain.agents import AgentExecutor
from agent import get_agent
from functools import partial
from datetime import datetime as dt
from telegram.constants import ParseMode


load_dotenv()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE,  agent: AgentExecutor):
    """Echo back user messages"""
    print(dt.now(), " - ", "A user started the bot...")
    start_message = """
        You have been launched as a telegram bot, so remember to ask the user to send directly the file, not to ask for a path
        in case it wants to upload a new file.

        Now, reply with a message explaning all your capabilities. Present yourself as Studybuddy, then try to convince to user 
        of your usefulness.
        """
    res = agent.invoke({
        'query': start_message
    })

    rep = res.get('output')

    await update.message.reply_text(rep)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE, agent: AgentExecutor):
    print(dt.now(), " - ","A user asked for help ")

    help_message = """
        The user does not know how to use you. Explain yourself and your capabilities.
        """
    res = agent.invoke({
        'query': help_message
    })

    rep = res.get('output')

    await update.message.reply_text(rep)

async def agent_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, agent: AgentExecutor):
    """Echo back user messages"""
    user_message = update.message.text
    print(dt.now(), " - USER: ", user_message)

    res = agent.invoke({
        'query': user_message
    })

    rep = res.get('output')

    await update.message.reply_text(rep)

# --- File Handler ---
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE, agent: AgentExecutor):
    """Handles documents sent by the user"""

    print(dt.now(), " - ", "A user sent a file")
    document = update.message.document  # file metadata

    if not document:
        await update.message.reply_text("That doesn't look like a file 😅")
        print(dt.now(), " - ", "File not correct")

        return
    
    file_name = document.file_name.lower()
    if not (file_name.endswith(".pdf") or file_name.endswith(".docx")):
        await update.message.reply_text("❌ Only PDF and DOCX files are allowed.")
        print(dt.now(), " - ", "File is not a docx or pdf")

        return
    file = await context.bot.get_file(document.file_id)

    save_path = os.path.join("bot_sent_notes", document.file_name)

    print(dt.now(), " - ", "Downloading the file...")
    await file.download_to_drive(save_path)

    await update.message.reply_text(f"File received and saved as: {save_path}")
    await update.message.reply_text(f"Calling the bot to upload the file...: {save_path}")
    print(dt.now(), " - ", "Called the bot to upload the file...")

    res = agent.invoke({
        'query': f"Upload the file at the path {save_path}"
    }).get('output')
    
    await update.message.reply_text(res)




def run_bot(AI_agent):
    BOT_API_KEY = os.getenv('telegram_bot_api_key')
    app = ApplicationBuilder().token(BOT_API_KEY).build()

    # Add handlers
    app.add_handler(CommandHandler("start", partial(start, agent=AI_agent)))
    app.add_handler(CommandHandler("help", partial(help_command, agent=AI_agent)))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, partial(agent_reply, agent = AI_agent)))
    app.add_handler(MessageHandler(filters.Document.ALL, partial(handle_file, agent=AI_agent)))

    # Run bot
    print("Starting the bot....")

    app.run_polling()


if __name__ == '__main__':
    studybuddy = get_agent()
    print("Studybuddy is ready to help you....\n")

    res = input("Do you want to interact with with him via Telegram or the terminal? \n \t1. Telegram bot \n \t2. Terminal \n Choose an option: ")
    if res == "1":
        print("Running the bot. To quit, press ctrl+c")
        run_bot(studybuddy)


    elif res == "2":
        print("Running the bot in the terminal. To quit, just tell the bot that you want to quit.")
        query = "Present yourself to the user, explaining your capabilities"
        print("\n\n ****** CONVERTATION ****** \n\n")
        active = True
        while active:
            res = studybuddy.invoke(
                {
                    'query': query
                }
            ).get('output')

            if "QUIT" in res:
                break

            print("Studybuddy: ", res, "\n")

            query = input("You: ")
            print("\n")

        print("Studybuddy shut down")
    else:
        print("Only 1 or 2 are valide choices ")
    
    #run_bot()
#response = llm.invoke('What is the answer to everything?')
#print(response)
