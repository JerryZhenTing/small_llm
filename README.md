# small

A lightweight, locally-deployed specialized language model for academic tasks such as grading assignments and analyzing research papers.

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 📋 Overview

Academic LLM Assistant is a specialized application that runs entirely on your local machine, allowing you to:

- Grade assignments according to custom rubrics
- Analyze research papers (text or PDF format) with domain-specific focus
- Operate with minimal computational resources using efficient models

This tool is designed for educators, researchers, and students who need academic assistance without sending data to external servers.

## 🔧 Requirements

- Python 3.8 or higher
- Ubuntu 20.04+ / Debian-based Linux (tested on Ubuntu 20.04)
- At least 4GB RAM (8GB recommended)
- 1GB disk space for models and code

## 🚀 Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/academic-llm-assistant.git
cd academic-llm-assistant

# Create and activate virtual environment
sudo apt update
sudo apt install python3.8-venv build-essential python3-dev
python3 -m venv llm_env
source llm_env/bin/activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Download model
mkdir -p models
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_0.gguf -O models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf

# Run the application
python academic_assistant.py
```

## ⚙️ Detailed Setup

### Step 1: Environment Setup

```bash
# Update package lists
sudo apt update

# Install required system packages
sudo apt install python3.8-venv build-essential python3-dev git wget

# Create a virtual environment
python3 -m venv llm_env
source llm_env/bin/activate

# Upgrade pip and essential packages
pip install --upgrade pip setuptools wheel
```

### Step 2: Install Dependencies

```bash
# Install PyTorch (CPU version)
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cpu

# Install other required packages
pip install transformers==4.31.0
pip install gradio==3.38.0
pip install llama-cpp-python
pip install pymupdf==1.22.5
pip install PyPDF2==3.0.1
```

Alternatively, you can install all dependencies at once using the requirements file:

```bash
pip install -r requirements.txt
```

### Step 3: Download the Model

```bash
# Create models directory
mkdir -p models

# Download TinyLlama (1.1B parameters, 4-bit quantized)
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_0.gguf -O models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf
```

For better performance (if you have more resources), you can download larger models:

```bash
# Mistral 7B (better quality, requires more RAM)
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_0.gguf -O models/mistral-7b-instruct-v0.2.Q4_0.gguf
```

### Step 4: Configure the Application

Edit the `academic_assistant.py` file to change the model path if you downloaded a different model:

```python
# Path to the model
MODEL_PATH = "models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf"  # Change this if using a different model
```

## 🖥️ Usage

### Running the Application

```bash
# Make sure you're in the project directory with the virtual environment activated
source llm_env/bin/activate
python academic_assistant.py
```

This will start the Gradio interface, accessible in your web browser at the URL shown in the terminal (typically http://127.0.0.1:7860).

### Assignment Grading

1. Navigate to the "Assignment Grading" tab
2. Enter the grading rubric in the first text box
3. Enter the student's submission in the second text box
4. Click "Grade Assignment"
5. View the AI-generated grading and feedback

### Research Paper Analysis

#### Text Analysis:
1. Navigate to the "Research Paper Analysis - Text" tab
2. Paste the research paper text
3. Select the domain and analysis focus
4. Click "Analyze Paper"
5. View the AI-generated analysis

#### PDF Analysis:
1. Navigate to the "Research Paper Analysis - PDF Upload" tab
2. Upload a PDF file
3. Select the domain and analysis focus
4. Click "Analyze PDF"
5. View the PDF structure summary, extracted text preview, and analysis

## 📁 Project Structure

```
academic-llm-assistant/
├── academic_assistant.py     # Main application code
├── models/                   # Directory for model files
│   └── tinyllama-1.1b-chat-v1.0.Q4_0.gguf
├── requirements.txt          # Python dependencies
├── run.sh                    # Launcher script
└── README.md                 # This documentation
```

## 📋 requirements.txt

Here's the content for your `requirements.txt` file:

```
torch==2.0.1
torchvision==0.15.2
torchaudio==2.0.2
transformers==4.31.0
gradio==3.38.0
llama-cpp-python==0.2.6
pymupdf==1.22.5
PyPDF2==3.0.1
```

## 📜 run.sh

To make launching the application easier, create a `run.sh` script:

```bash
#!/bin/bash

# Activate virtual environment
source llm_env/bin/activate

# Display menu
echo "========================================"
echo "      Academic LLM Assistant Launcher   "
echo "========================================"
echo "1. Run Academic Assistant"
echo "2. Exit"
echo "========================================"

# Get user choice
read -p "Enter your choice (1-2): " choice

case $choice in
    1)
        echo "Launching Academic Assistant..."
        python academic_assistant.py
        ;;
    2)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
```

Make it executable:

```bash
chmod +x run.sh
```

## 🚨 Limitations

- Context window constraints: Only processes first few pages of research papers
- No fine-tuning: Uses prompt engineering rather than model fine-tuning
- Limited mathematical understanding: Can detect but not comprehend complex formulas
- Performance: Takes ~20-30 seconds to analyze PDFs and ~15 seconds for chat responses

## 🛣️ Roadmap

- Improve runtime performance for faster analysis
- Expand PDF processing from 3-5 pages to 5-10 pages
- Add specialized handling for mathematical equations
- Implement LoRA fine-tuning for academic tasks

## ⚠️ Troubleshooting

### Context Window Errors
If you encounter "Requested tokens exceed context window" errors, try:
- Reducing the length of input text
- Processing smaller sections of papers
- Editing `academic_assistant.py` to further reduce `max_tokens` value

### Memory Issues
If the application crashes due to memory limitations:
- Try using a smaller model
- Reduce the number of CPU threads in the model loading section
- Close other applications to free up memory

### PDF Extraction Problems
If PDF extraction fails:
- Ensure the PDF is not encrypted/protected
- Try converting text-only PDFs (complex layouts with tables/formulas may not extract well)
- Check that PyMuPDF is properly installed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [llama.cpp](https://github.com/ggerganov/llama.cpp) for efficient CPU inference
- [Gradio](https://gradio.app/) for the web interface
- [Hugging Face](https://huggingface.co/) for model hosting
- [TinyLlama](https://github.com/jzhang38/TinyLlama) for the efficient base model
