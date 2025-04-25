# ProjectCraft: Educational Mini-Project Generator

## Overview

ProjectCraft is a Streamlit web application designed to help educators create comprehensive, well-structured mini-project assignments for their students. Using OpenAI's powerful GPT-4 model, ProjectCraft generates detailed project specifications based on simple inputs from teachers, saving hours of preparation time while ensuring pedagogically sound project design.

## Features

- **Instant Project Generation**: Create complete mini-project assignments in minutes
- **Customizable Projects**: Tailor projects to any subject, academic level, and duration
- **Well-Structured Output**: Every project includes learning objectives, technical requirements, deliverables, and evaluation criteria
- **Interactive Refinement**: Chat with the AI to refine and improve your project
- **Microsoft Word Export**: Download projects as well-formatted Word documents ready to share with students
- **Markdown Export**: Alternative download option in markdown format for easy editing
- **Modern UI**: Clean, intuitive interface designed for educators

## Demo

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/projectcraft.git
   cd projectcraft
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install streamlit openai python-docx markdown python-dotenv
   ```

4. Set up your API key:
   - Create a `.streamlit` directory in the project root (if it doesn't exist)
   - Create a `secrets.toml` file inside the `.streamlit` directory
   - Add your OpenAI API key:
     ```toml
     OPENAI_API_KEY = "your_api_key_here"
     ```
   - Note: When deploying to Streamlit Cloud, add this key to the app secrets in the dashboard

## Usage

1. Start the Streamlit app:
   ```bash
   streamlit run projectcraft.py
   ```

2. The app will open in your default web browser (typically at http://localhost:8501)

3. Fill in the project details:
   - Subject/Course
   - Academic Level
   - Project Duration
   - Key Learning Objectives
   - Available Resources
   - Optional: Project Theme/Focus

4. Click "Generate Project" to create your mini-project assignment

5. Review the generated project across all sections

6. Refine the project by asking questions in the chat interface

7. Download the final project as a Word document or markdown file

## Configuration Options

The application can be configured by modifying the following variables in the `projectcraft.py` file:

- `st.session_state.selected_model`: Change to use different OpenAI models
- Custom CSS in the style section to modify the appearance

## Project Structure

Each generated mini-project follows this template:

- **Overview**: Brief introduction explaining the project's purpose and relevance
- **Learning Objectives**: Specific skills students will develop
- **Project Description**: Context and explanation of the core task
- **Technical Requirements**: Detailed specifications organized by category
- **Deliverables**: Concrete outputs students must submit
- **Evaluation Criteria**: How the project will be assessed
- **Additional Resources**: Helpful links and references
- **Submission Guidelines**: Instructions for submitting work

## Deployment

This app can be deployed on Streamlit Cloud or any other platform that supports Streamlit apps:

1. Push your code to GitHub
2. Set up a new app on [Streamlit Cloud](https://streamlit.io/cloud)
3. Add your OpenAI API key as a secret in the Streamlit Cloud dashboard

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI API](https://openai.com/api/)
- Document generation using [python-docx](https://python-docx.readthedocs.io/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Created with ❤️ for educators