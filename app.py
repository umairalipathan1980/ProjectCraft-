
import streamlit as st
import openai
import os
from dotenv import load_dotenv
import time
import json
import re
from datetime import datetime
import random
import uuid
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

# Get API key from .streamlit/secrets.toml
try:
    # First attempt to load from Streamlit secrets
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception as e:
    st.error("Error: OpenAI API key not found in .streamlit/secrets.toml")
    st.info("Please create a .streamlit/secrets.toml file with your API key: \n\nOPENAI_API_KEY='your_api_key_here'")
    OPENAI_API_KEY = None
    
# Check if key was successfully loaded
if not OPENAI_API_KEY:
    st.warning("No API key found. The application will not function without a valid OpenAI API key.")

# Configure page
st.set_page_config(
    page_title="ProjectCraft: Mini-Project Generator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Global styles */
    .main {
        background-color: #f8f9fa;
        color: #212529;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Header styles */
    .header-container {
        display: flex;
        align-items: center;
        background: linear-gradient(90deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .header-icon {
        font-size: 3rem;
        margin-right: 1rem;
    }
    .header-text h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }
    .header-text p {
        margin: 0;
        opacity: 0.9;
    }
    
    /* Card styles */
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #2c3e50;
        border-bottom: 2px solid #f1f1f1;
        padding-bottom: 0.5rem;
    }
    
    /* Form styles */
    .form-container label {
        font-weight: 600;
        color: #2c3e50;
    }
    .form-description {
        font-size: 0.9rem;
        color: #6c757d;
        margin-bottom: 0.5rem;
    }
    
    /* Button styles */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .generate-button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        transition: background-color 0.3s;
    }
    .generate-button:hover {
        background-color: #45a049;
    }
    
    /* Project output styles */
    .project-section {
        margin: 1.5rem 0;
    }
    .project-section h3 {
        color: #2c3e50;
        margin-bottom: 0.5rem;
        font-size: 1.3rem;
    }
    .project-highlight {
        background-color: #f8f9fa;
        border-left: 3px solid #4CAF50;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Chat styles */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        gap: 0.75rem;
    }
    .chat-message.user {
        background-color: #e3f2fd;
    }
    .chat-message.assistant {
        background-color: #f1f8e9;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    .chat-message .message {
        flex: 1;
    }
    
    /* Sidebar styles */
    .stSidebar {
        background-color: #f8f9fa;
        padding: 1.5rem 1rem;
    }
    .sidebar-title {
        text-align: center;
        font-weight: bold;
        margin-bottom: 1.5rem;
        color: #2c3e50;
    }
    .sidebar-section {
        margin-bottom: 2rem;
    }
    .sidebar-section h3 {
        font-size: 1.1rem;
        color: #2c3e50;
        border-bottom: 1px solid #dee2e6;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f1f1;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }
    p, div {
        font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }
    
    /* Custom pill badge */
    .pill-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .pill-badge.blue {
        background-color: #e3f2fd;
        color: #1565c0;
    }
    .pill-badge.green {
        background-color: #e8f5e9;
        color: #2e7d32;
    }
    .pill-badge.purple {
        background-color: #f3e5f5;
        color: #7b1fa2;
    }
    .pill-badge.orange {
        background-color: #fff3e0;
        color: #ef6c00;
    }
    
    /* Tooltip style */
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #ccc;
        cursor: help;
    }
    .tooltip .tooltip-text {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    
    /* Progress bar */
    .custom-progress {
        height: 10px;
        border-radius: 5px;
        margin-top: 10px;
        background-color: #f1f1f1;
        overflow: hidden;
    }
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        border-radius: 5px;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'project_data' not in st.session_state:
    st.session_state.project_data = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'chat_started' not in st.session_state:
    st.session_state.chat_started = False
if 'generation_in_progress' not in st.session_state:
    st.session_state.generation_in_progress = False
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "gpt-5.1-2025-11-13" # Use gpt-4.1 when available

# Project generator system prompt
PROJECT_GENERATOR_PROMPT = """
You are ProjectCraft, a specialized assistant designed to help educators create comprehensive mini-project assignments for their students. Your goal is to guide teachers through the process of designing structured, engaging projects with clear objectives, requirements, and evaluation criteria.

## Core Purpose
Help educators create detailed, well-structured mini-project assignments that are appropriate for their subject area, student level, and available resources. The projects should be engaging, educational, and achievable within the specified timeframe.

## Standard Mini-Project Template
Use this consistent template structure for all project assignments:

### Overview
A brief introduction (2-3 sentences) explaining the project's overall purpose and relevance.

### Learning Objectives
A bulleted list of 4-6 specific skills or knowledge areas students will develop through the project.

### Project Description
A paragraph (5-8 sentences) providing context and explaining the core task or problem students will address.

### Technical Requirements
Break this section into logical subsections based on the project type, such as:
- Data/Resource Collection
- Analysis/Development Process
- Implementation Requirements
- Testing/Evaluation Methods

Each subsection should include specific, measurable requirements with appropriate detail.

### Deliverables
A numbered list of concrete outputs students must submit, including:
- Format specifications
- Length/scope guidelines
- Presentation requirements
- Documentation needs

### Evaluation Criteria
A breakdown of how the project will be assessed, with percentage weights for different components.

### Additional Resources
A list of helpful resources, including:
- Relevant websites, APIs, or data sources (with URLs)
- Reference materials
- Tools or platforms
- Starter templates or examples (if applicable)

### Submission Guidelines
Clear instructions for how and when deliverables should be submitted.

## What to Avoid
1. Creating projects that are too vague or too prescriptive
2. Recommending resources that aren't freely accessible
3. Designing projects that require excessive time or resources beyond what's reasonable
4. Using overly technical language inappropriate for the specified academic level
5. Creating projects without clear, measurable learning outcomes
6. Suggesting projects that don't have real-world relevance or application

Based on the information provided by the user, generate a complete mini-project assignment following this template. Make it specific, practical, engaging, and appropriate for the subject area and academic level.
"""

# Function to convert project to markdown format
def get_project_markdown():
    """
    Convert the generated project to a markdown string format
    """
    if not st.session_state.project_data:
        return "No project has been generated yet."
        
    markdown_text = f"# {st.session_state.project_data.get('title', 'Student Mini-Project')}\n\n"
    markdown_text += f"**Subject:** {st.session_state.form_data.get('subject', 'N/A')}\n"
    markdown_text += f"**Academic Level:** {st.session_state.form_data.get('academic_level', 'N/A')}\n"
    markdown_text += f"**Duration:** {st.session_state.form_data.get('duration', 'N/A')}\n\n"
    
    # Add each section of the project
    for section, content in st.session_state.project_data.items():
        if section != 'title' and content:
            markdown_text += f"## {section}\n\n"
            markdown_text += f"{content}\n\n"
    
    markdown_text += f"---\n\n"
    markdown_text += f"Generated by ProjectCraft on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    markdown_text += f"Session ID: {st.session_state.session_id}\n"
    
    return markdown_text

# Function to call OpenAI API
# Function to call OpenAI API
def call_openai_api(messages, stream=True):
    client = openai.Client(api_key=OPENAI_API_KEY)
    
    try:
        if stream:
            # Set up placeholder for streaming
            placeholder = st.empty()
            collected_content = ""
            
            # Start streaming
            for chunk in client.chat.completions.create(
                model=st.session_state.selected_model,
                messages=messages,
                stream=True,
                max_tokens=4000,
                temperature=0.9  # Set a higher temperature to stimulate creativity
            ):
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    collected_content += content
                    placeholder.markdown(collected_content)
            
            return collected_content
        else:
            response = client.chat.completions.create(
                model=st.session_state.selected_model,
                messages=messages,
                stream=False,
                max_tokens=4000,
                temperature=0.9  # Set a higher temperature to stimulate creativity
            )
            return response.choices[0].message.content
            
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return "I'm sorry, there was an error processing your request. Please try again."

# Function to generate project
def generate_project(form_data):
    st.session_state.generation_in_progress = True
    
    # Store form data in session state
    st.session_state.form_data = form_data
    
    # Build the prompt
    project_prompt = f"""
    Please generate a mini-project assignment based on the following specifications:
    
    Subject/Course: {form_data['subject']}
    Academic Level: {form_data['academic_level']}
    Project Duration: {form_data['duration']}
    Key Learning Objectives: {form_data['objectives']}
    Available Resources: {form_data['resources']}
    Project Theme/Focus: {form_data['theme'] if form_data['theme'] else 'Any appropriate theme for the subject'}
    
    The project should be challenging but achievable within the given timeframe and with the specified resources.
    Please format your response using markdown and structure it according to the standard template.
    
    Additionally, provide a short, catchy title for the project at the beginning.
    """
    
    # Set up the messages
    messages = [
        {"role": "system", "content": PROJECT_GENERATOR_PROMPT},
        {"role": "user", "content": project_prompt}
    ]
    
    # Call the API
    with st.spinner("Crafting your project... this may take a moment..."):
        response = call_openai_api(messages, stream=False)
    
    # Parse the response
    # Extract the title (assuming it's in the first line with a # or ## prefix)
    title_match = re.search(r'^#+ (.+)$', response, re.MULTILINE)
    title = title_match.group(1) if title_match else "Student Mini-Project"
    
    # Create a structured project data object
    project_data = {
        "title": title,
        "Overview": extract_section(response, "Overview", "Learning Objectives"),
        "Learning Objectives": extract_section(response, "Learning Objectives", "Project Description"),
        "Project Description": extract_section(response, "Project Description", "Technical Requirements"),
        "Technical Requirements": extract_section(response, "Technical Requirements", "Deliverables"),
        "Deliverables": extract_section(response, "Deliverables", "Evaluation Criteria"),
        "Evaluation Criteria": extract_section(response, "Evaluation Criteria", "Additional Resources"),
        "Additional Resources": extract_section(response, "Additional Resources", "Submission Guidelines"),
        "Submission Guidelines": extract_section(response, "Submission Guidelines", None)
    }
    
    # Store the project data
    st.session_state.project_data = project_data
    st.session_state.generation_in_progress = False
    st.session_state.raw_response = response
    
    return project_data

# Helper function to extract sections from the response
def extract_section(text, section_name, next_section_name):
    start_pattern = f"### {section_name}"
    start_index = text.find(start_pattern)
    
    if start_index == -1:
        # Try with ## prefix
        start_pattern = f"## {section_name}"
        start_index = text.find(start_pattern)
        
        if start_index == -1:
            return ""
    
    # Add the length of the section heading to get to the content
    start_index += len(start_pattern)
    
    # Find the end of the section
    if next_section_name:
        end_pattern = f"### {next_section_name}"
        end_index = text.find(end_pattern, start_index)
        
        if end_index == -1:
            # Try with ## prefix
            end_pattern = f"## {next_section_name}"
            end_index = text.find(end_pattern, start_index)
            
            if end_index == -1:
                end_index = len(text)
    else:
        end_index = len(text)
    
    section_content = text[start_index:end_index].strip()
    return section_content

# Function to handle chat interaction for project improvements
def chat_with_project(question):
    # Add user question to the chat
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Build the context
    context = f"""
    The user has generated a mini-project with the following details:
    
    Subject/Course: {st.session_state.form_data['subject']}
    Academic Level: {st.session_state.form_data['academic_level']}
    Project Duration: {st.session_state.form_data['duration']}
    
    Here is the current project:
    
    {st.session_state.raw_response}
    
    The user is asking: {question}
    
    Provide helpful suggestions, modifications, or insights about the project. If they're asking for specific changes, explain how those changes could be implemented.
    """
    
    # Set up the messages
    messages = [
        {"role": "system", "content": PROJECT_GENERATOR_PROMPT},
        {"role": "user", "content": context}
    ]
    
    # Call the API
    with st.spinner("Thinking..."):
        response = call_openai_api(messages, stream=True)
    
    # Add the response to the chat
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.chat_started = True

# Sidebar
with st.sidebar:
    st.markdown("<h1 class='sidebar-title'>🎯 ProjectCraft</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
    st.markdown("<h3>About</h3>", unsafe_allow_html=True)
    st.markdown("""
    ProjectCraft helps educators design comprehensive, 
    engaging mini-projects for students at any academic level.
    
    Simply provide the basic information about your course
    and requirements, and we'll generate a fully structured
    project assignment ready to share with your students.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
    st.markdown("<h3>Tips for Great Projects</h3>", unsafe_allow_html=True)
    st.markdown("""
    - Be specific about learning objectives
    - Consider available resources and time constraints
    - Balance structure with creative freedom
    - Incorporate real-world applications
    - Include clear evaluation criteria
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
    st.markdown("<h3>Session Controls</h3>", unsafe_allow_html=True)
    
    if st.button("🔄 Start New Project", key="new_project", use_container_width=True):
        st.session_state.project_data = None
        st.session_state.messages = []
        st.session_state.chat_started = False
        st.session_state.form_data = None
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()
    
    if st.session_state.project_data:
        if st.button("📝 Export Project", key="export_project", use_container_width=True):
            # Generate markdown format
            markdown_text = get_project_markdown()
            # Encode to download
            b64 = base64.b64encode(markdown_text.encode()).decode()
            file_name = f"student_project_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            href = f'<a href="data:text/markdown;base64,{b64}" download="{file_name}">Click to download project (Markdown)</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Main content
# Custom header
st.markdown("""
<div class="header-container">
    <div class="header-icon">🎯</div>
    <div class="header-text">
        <h1>ProjectCraft: Mini-Project Generator</h1>
        <p>Create engaging, educational projects for your students in minutes</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Project Generation Form if no project has been generated yet
if not st.session_state.project_data and not st.session_state.generation_in_progress:
    st.markdown("""
    <div class="card">
        <div class="card-title">Create Your Project</div>
        <p>Fill in the form below to generate a structured mini-project assignment for your students.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p class="form-description">What subject is this project for?</p>', unsafe_allow_html=True)
            subject = st.text_input("Subject/Course", placeholder="e.g., Introduction to Data Science")
            
            st.markdown('<p class="form-description">Who are your students?</p>', unsafe_allow_html=True)
            academic_level = st.selectbox(
                "Academic Level",
                options=["High School", "Undergraduate (Year 1-2)", "Undergraduate (Year 3-4)", "Graduate", "Professional Development"]
            )
            
            st.markdown('<p class="form-description">How long will students work on this project?</p>', unsafe_allow_html=True)
            duration = st.selectbox(
                "Project Duration",
                options=["1 week", "2 weeks", "3-4 weeks", "5-6 weeks", "Full semester"]
            )
        
        with col2:
            st.markdown('<p class="form-description">What should students learn from this project?</p>', unsafe_allow_html=True)
            objectives = st.text_area("Key Learning Objectives", placeholder="e.g., data visualization, critical analysis, teamwork", height=100)
            
            st.markdown('<p class="form-description">What resources are available to students?</p>', unsafe_allow_html=True)
            resources = st.text_area("Available Resources", placeholder="e.g., Python, lab equipment, specific datasets", height=70)
            
            st.markdown('<p class="form-description">Optional: Any specific theme or focus?</p>', unsafe_allow_html=True)
            theme = st.text_input("Project Theme/Focus (optional)", placeholder="e.g., sustainability, public health")
        
        submit_button = st.form_submit_button("Generate Project")
        
        if submit_button:
            if not subject or not objectives or not resources:
                st.error("Please fill in all required fields (Subject, Learning Objectives, and Available Resources).")
            else:
                form_data = {
                    "subject": subject,
                    "academic_level": academic_level,
                    "duration": duration,
                    "objectives": objectives,
                    "resources": resources,
                    "theme": theme
                }
                generate_project(form_data)
                st.rerun()

# Display the generated project if available
elif st.session_state.project_data:
    project_data = st.session_state.project_data
    
    # Project title and basic info
    st.markdown(f"<h1>{project_data['title']}</h1>", unsafe_allow_html=True)
    
    # Info pills for project metadata
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <span class="pill-badge blue">Subject: {st.session_state.form_data['subject']}</span>
        <span class="pill-badge green">Level: {st.session_state.form_data['academic_level']}</span>
        <span class="pill-badge purple">Duration: {st.session_state.form_data['duration']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for the project sections
    tab1, tab2, tab3 = st.tabs(["📋 Project Details", "💬 Refine Project", "📊 Preview"])
    
    with tab1:
        # Overview
        st.markdown("""
        <div class="card">
            <div class="card-title">Overview</div>
            <div class="project-section">
        """, unsafe_allow_html=True)
        st.markdown(project_data["Overview"])
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Learning Objectives
        st.markdown("""
        <div class="card">
            <div class="card-title">Learning Objectives</div>
            <div class="project-section">
        """, unsafe_allow_html=True)
        st.markdown(project_data["Learning Objectives"])
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Project Description
        st.markdown("""
        <div class="card">
            <div class="card-title">Project Description</div>
            <div class="project-section">
        """, unsafe_allow_html=True)
        st.markdown(project_data["Project Description"])
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Technical Requirements
        st.markdown("""
        <div class="card">
            <div class="card-title">Technical Requirements</div>
            <div class="project-section">
        """, unsafe_allow_html=True)
        st.markdown(project_data["Technical Requirements"])
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Deliverables
        st.markdown("""
        <div class="card">
            <div class="card-title">Deliverables</div>
            <div class="project-section">
        """, unsafe_allow_html=True)
        st.markdown(project_data["Deliverables"])
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Evaluation Criteria
        st.markdown("""
        <div class="card">
            <div class="card-title">Evaluation Criteria</div>
            <div class="project-section">
        """, unsafe_allow_html=True)
        st.markdown(project_data["Evaluation Criteria"])
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Additional Resources
        st.markdown("""
        <div class="card">
            <div class="card-title">Additional Resources</div>
            <div class="project-section">
        """, unsafe_allow_html=True)
        st.markdown(project_data["Additional Resources"])
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Submission Guidelines
        st.markdown("""
        <div class="card">
            <div class="card-title">Submission Guidelines</div>
            <div class="project-section">
        """, unsafe_allow_html=True)
        st.markdown(project_data["Submission Guidelines"])
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Regenerate Project", key="regenerate", use_container_width=True):
                generate_project(st.session_state.form_data)
                st.rerun()
        with col2:
            # Encode markdown for download
            markdown_text = get_project_markdown()
            b64 = base64.b64encode(markdown_text.encode()).decode()
            file_name = f"student_project_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            download_button = f'<a href="data:text/markdown;base64,{b64}" download="{file_name}" style="text-decoration:none;"><button style="background-color:#4CAF50;color:white;border:none;padding:12px 20px;border-radius:8px;font-weight:600;cursor:pointer;width:100%;">📝 Download Project</button></a>'
            st.markdown(download_button, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Refine Your Project</div>
            <p>Ask questions or request specific modifications to improve your project.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display chat messages
        if st.session_state.messages:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user">
                        <div class="avatar">👤</div>
                        <div class="message">{message['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant">
                        <div class="avatar">🎯</div>
                        <div class="message">{message['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Suggestion buttons
        if not st.session_state.chat_started:
            st.markdown("### Quick Suggestions")
            suggestion_col1, suggestion_col2 = st.columns(2)
            
            with suggestion_col1:
                if st.button("Make it more challenging", key="more_challenging", use_container_width=True):
                    chat_with_project("Could you make this project more challenging for advanced students?")
                    st.rerun()
                    
                if st.button("Add teamwork component", key="teamwork", use_container_width=True):
                    chat_with_project("How can I incorporate more teamwork and collaboration into this project?")
                    st.rerun()
            
            with suggestion_col2:
                if st.button("Simplify requirements", key="simplify", use_container_width=True):
                    chat_with_project("I'd like to simplify some of the requirements to make this more accessible.")
                    st.rerun()
                    
                if st.button("More real-world relevance", key="real_world", use_container_width=True):
                    chat_with_project("How can I connect this project more directly to real-world applications?")
                    st.rerun()
        
        # Chat input
        user_input = st.text_area("Your question or request:", key="chat_input", help="Ask about modifying specific aspects of the project or request additional resources.", height=100)
        
        if st.button("Submit", key="submit_chat", use_container_width=True):
            if user_input:
                chat_with_project(user_input)
                st.rerun()
    
    with tab3:
        st.markdown("""
        <div class="card">
            <div class="card-title">Project Preview</div>
            <p>This is how your project will look when exported.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display the markdown preview
        st.markdown(get_project_markdown())

elif st.session_state.generation_in_progress:
    # Show loading state
    st.markdown("""
    <div class="card">
        <div class="card-title">Generating Your Project</div>
        <p>Please wait while we craft your custom project...</p>
        <div class="custom-progress">
            <div class="progress-bar" style="width: 70%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Animation for loading
    progress_placeholder = st.empty()
    for i in range(100):
        # Update progress every 0.1 seconds
        time.sleep(0.05)
        # Update the progress bar
        progress_placeholder.markdown(f"""
        <div class="custom-progress">
            <div class="progress-bar" style="width: {i}%;"></div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 20px; color: #6c757d; font-size: 0.8rem;">
    ProjectCraft • Educational Mini-Project Generator • Created with Streamlit and GPT-4.1
</div>
""", unsafe_allow_html=True)
