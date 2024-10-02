# AI Document Generator

This is a Flask web application that interactively generates a structured document using OpenAI's GPT models. Users can input a topic and the desired number of chapters, edit the generated table of contents, and generate content for each chapter. The application features a responsive and user-friendly interface built with Bootstrap.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Clone the Repository](#clone-the-repository)
  - [Set Up the Virtual Environment](#set-up-the-virtual-environment)
  - [Install Dependencies](#install-dependencies)
  - [Set Up Environment Variables](#set-up-environment-variables)
- [Running the Application](#running-the-application)
- [Using Docker](#using-docker)
  - [Build the Docker Image](#build-the-docker-image)
  - [Run the Docker Container](#run-the-docker-container)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Dynamic Table of Contents Generation**: Input a topic and number of chapters to generate a customizable table of contents.
- **Inline Editing**: Edit chapter titles directly on the page before generating content.
- **Chapter Content Generation**: Generate content for all chapters with a single click.
- **Responsive Design**: Built with Bootstrap for a clean, responsive user interface.
- **Single-Page Application**: Seamless user experience without page reloads.
- **Docker Support**: Easily build and run the application using Docker.

## Demo

[Live Demo Link] *(If you have deployed the application, you can provide a link here. Otherwise, you can remove this section.)*

## Prerequisites

- **Python 3.9+**
- **OpenAI API Key**: You need an API key from [OpenAI](https://beta.openai.com/signup/) to use their GPT models.

## Installation

### Clone the Repository

```
git clone https://github.com/ideruga/ai-document-generator.git
cd ai-document-generator
```

### Set Up the Virtual Environment

Create and activate a virtual environment to manage dependencies.

**On macOS/Linux:**

```
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Set Up Environment Variables

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

**Important**: Do not share your `.env` file or API key publicly.

## Running the Application

Start the Flask development server:

```
python app.py
```

Access the application at [http://localhost:5000](http://localhost:5000).

## Using Docker

Alternatively, you can run the application inside a Docker container.

### Build the Docker Image

```
docker build -t ai-document-generator .
```

### Run the Docker Container

**Pass the API Key as an Environment Variable**

```
docker run -d -p 5000:5000 --name ai-doc-gen \
  -e OPENAI_API_KEY=your_openai_api_key_here \
  ai-document-generator
```

Access the application at [http://localhost:5000](http://localhost:5000).

## Usage

1. **Enter Topic and Number of Chapters**: On the main page, input the document topic and the desired number of chapters. Default values are provided.

2. **Generate Table of Contents**: Click the "Generate Table of Contents" button to create a preliminary table of contents.

3. **Edit Table of Contents**: The generated table of contents appears on the same page. Click on any chapter title to edit it inline.

4. **Generate Chapters**: Once satisfied with the table of contents, click the "Generate Chapters" button to create content for all chapters.

5. **View Generated Document**: The generated chapters are displayed below the table of contents. You can read and review the content directly on the page.

6. **Start Over**: Use the "Start Over" button to reset the application and generate a new document.

## Project Structure

```
ai-document-generator/
├── app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── README.md
├── .env.example
├── templates/
│   ├── base.html
│   └── index.html
└── static/
    └── styles.css
```

- **app.py**: Main Flask application.
- **requirements.txt**: Python dependencies.
- **Dockerfile**: Instructions to build the Docker image.
- **templates/**: HTML templates using Jinja2.
- **static/**: Static files like CSS.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```
   git commit -m "Add your feature"
   ```

4. **Push to Your Fork**

   ```
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

## License

This project is licensed under the [MIT License](LICENSE).

---

*Note: Replace `yourusername` with your actual GitHub username in the clone URL. If you have any additional details, such as deployment instructions or links, feel free to add them.*
