from langchain.tools import Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime
import utils
from openai import OpenAI
import os
from dotenv import load_dotenv
import pymysql.cursors
from utils import upload_file, get_db_connection


load_dotenv()


def search_note(query:str):
    """Search most similar notes to a query"""

    conn = get_db_connection()
    openai_client = OpenAI(api_key=os.getenv('openai_api_key'))


    query_emb = openai_client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    ).data[0].embedding
    
    
    sql = """
        SELECT 
            notes.id,
            notes.name as note_name, 
            notes.subject as subject, 
            notes.upload_timestamp,
            MIN(VEC_COSINE_DISTANCE(note_chunks.embedding, %s)) AS dist
        FROM notes join note_chunks on notes.id = note_chunks.note_id
        GROUP BY 
            notes.id, 
            notes.name,
            notes.upload_timestamp
        HAVING dist < 0.5

    """

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql, (str(query_emb)))
    results = cursor.fetchall()
    return results

def ingest_func(filepath: str):
    conn = get_db_connection()
    openai_client = OpenAI(api_key=os.getenv('openai_api_key'))

    if not os.path.isfile(filepath):
        return "File non corretto o non esistente"
    
    return upload_file(
        connection=conn,
        openai_client=openai_client,
        filepath=filepath
    )


def get_note(note_id: int):
    conn = get_db_connection()
        # 3. Run vector search on TiDB
    sql = """
        SELECT 
            note_id,
            chunk_order, 
            content
        FROM note_chunks as nc
        WHERE note_id = %s
        ORDER BY nc.chunk_order

    """

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql, (note_id))
    results = cursor.fetchall()

    full_content = ""

    for r in results:
        full_content += r['content']
    
    return full_content


def list_notes(a: str):
    conn = get_db_connection()
        # 3. Run vector search on TiDB
    sql = """
        SELECT 
            *
        FROM notes
    """

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    results = cursor.fetchall()
    
    return results


api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=300)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

search_notes_tool = Tool(
    name='search_notes',
    func=search_note,
    description="Search into the database for user's notes regarding a specific topic. Returns just the list of notes, not the contents"
)

upload_file_tool = Tool(
    name='upload_note',
    func=ingest_func,
    description="Uploads a note (DOCX or PDF) into the database"
)

get_note_tool = Tool(
    name='get_note',
    func=get_note,
    description='Given the id a note, it returns the full content (as text). Remember: it takes the id of the note, not the name. The user will tell you the name'
)

list_notes_tool = Tool(
    name='list_note',
    func=list_notes,
    description='It lists all the notes in the database. For each note, it returns id, name, extension, subject and an array of keywords'
)

if __name__ == '__main__':
    conn = get_db_connection()
    res = list_notes()

    print(res)