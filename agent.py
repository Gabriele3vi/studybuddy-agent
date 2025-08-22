import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_notes_tool, upload_file_tool, get_note_tool, list_notes_tool, wiki_tool

load_dotenv() 

OPENAI_API_KEY = os.getenv('openai_api_key')

def get_agent():
    memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True)
    llm = ChatOpenAI(model='gpt-4o-mini', api_key=OPENAI_API_KEY)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", 
            """ 
                You are a study buddy of a high school or university student. You will help him organizing his notes, summarize them, and make questions to review for an exam.
                Answer the user query and use the necessary tools to get his notes and help him.
                You are given four tools:
                    - search_note_tool: to search for notes given a query to search them
                    - upload_file_tool: the user will give you a filepath, you use this tool to upload the file into the dataset
                    - get_note_tool: Given a note id, returns its content
                    - list_notes_tool: returns all the notes in the database 

                You will receive questions like "Tell me the notes that speaks about <something>". You will need to use search_note_tool passing the concept given by the user.

                In return, format the output reporting the notes retrived by the database with this structure
                
                ID: <note_id>
                Note: <note_name>
                upload_timestamp: [timestamp]

                If the user asks to return a note, use "get_note_tool" and always return the exact content, without altering it. The only thing you are allowed to remove is the part in which are reported they keyword about the text.
                The function accepts only the id of the note. If the user does not give the id but only the name, first search the notes for the name, then use the id of the note that best fit the question of the user.

                If the user asks for the list, return the results with the following structure for each note.

                Give to the output this structure: 
                ID: <not_id>
                Note: <note_name>
                upload_timestamp: [timestamp]

                If the users asks to quit the conversation or to shut you down, just reply with QUIT, nothing else.

                If you are runned as a telegram bot, tell the user to just send the file, not to send the file path. Otherwise,
                you need the path to get the file.

                If the user asks to list their notes, use the list_notes tool, and ALWAYS pass the string "test" as argument

                If you find markdown character in the text, remove them.

                If the user asks for a web research, present the sources in a nice way.
            """
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    ).partial()


    tools = [search_notes_tool, upload_file_tool, get_note_tool, list_notes_tool, wiki_tool]
    agent = create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools
    )

    agent_exec = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)
    return agent_exec

if __name__ == "__main__":
    print("aaaa")