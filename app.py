import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, session, jsonify
from langchain.llms import OpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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

    for index, chapter in enumerate(chapters):
        chapter_prompt = PromptTemplate(
            input_variables=["chapter_name"],
            template="Generate a book chapter based on its header: {chapter_name}. Do not include the chapter header, only the text."
        )
        chapter_chain = chapter_prompt | llm

        content = chapter_chain.invoke({"chapter_name": chapter})
        chapters[index]['content'] = content

    session['chapters'] = chapters

    # Return the generated content
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
