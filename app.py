import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
from langchain.llms import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

llm = OpenAI(openai_api_key=openai_api_key)

from datetime import datetime


@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/generate_toc', methods=['POST'])
def generate_toc():
    description = request.form.get('description')
    length = request.form.get('length')

    toc_template = PromptTemplate(
        input_variables=["description", "length"],
        template="Generate a table of contents for a book about {description}, aiming for {length} chapters. "
                 "Format output as 'Chapter #. Chapter Name.\\n' without any empty lines."
    )

    toc_chain = toc_template | llm
    toc = toc_chain.invoke({"description": description, "length": length}).strip()

    titles = toc.split("\n")

    session['description'] = description
    session['length'] = length
    session['chapters'] = [{'title': title.strip(), 'content': ''} for title in titles if title.strip()]

    return jsonify({'titles': titles})


@app.route('/generate_all_chapters', methods=['POST'])
def generate_all_chapters():
    chapters = session.get('chapters', [])

    first_chapter_prompt = PromptTemplate(
        input_variables=["book_title", "chapter_name"],
        template="Generate a book chapter based on the book's title {book_title} and chapter's header: {chapter_name}. Do not include the chapter header, only the text."
    )
    other_chapter_prompt = PromptTemplate(
        input_variables=["book_title", "chapter_name", "summary"],
        template="Generate a book chapter based on the book's title {book_title} and chapter's header: {chapter_name}. "
                 "Do not include the chapter header, only the text. "
                 "For the information purposes only, here's the summary of the previous chapter, do not include this summary in the current chapter: {summary}."
    )
    summary_prompt = PromptTemplate(
        input_variables=["document"],
        template="Generate a short document summary for the following text: {document}."
    )

    latest_summary = None
    for index, chapter in enumerate(chapters):

        prompt = first_chapter_prompt if index == 0 else other_chapter_prompt
        chapter_chain = prompt | llm | StrOutputParser()
        summary_chain = summary_prompt | llm | StrOutputParser()

        aggregate_chain = chapter_chain | {
            "document": RunnablePassthrough(),
            "summary": summary_chain
        }

        content = aggregate_chain.invoke({"book_title": session['description'],
                                          "chapter_name": chapter,
                                          "summary": latest_summary})
        chapters[index]['content'] = content['document']
        chapters[index]['summary'] = content['summary']
        latest_summary = content['summary']

        session['chapters'] = chapters

    return jsonify({'chapters': chapters})


@app.route('/update_chapter_title', methods=['POST'])
def update_chapter_title():
    chapter_index = int(request.form.get('index'))
    new_title = request.form.get('title')
    chapters = session.get('chapters', [])
    chapters[chapter_index]['title'] = new_title
    session['chapters'] = chapters
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
