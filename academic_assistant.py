# Save this as academic_assistant.py
import gradio as gr
from llama_cpp import Llama
import os
import PyPDF2
import re
import fitz  # PyMuPDF for better PDF handling

# Path to the model
MODEL_PATH = "models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf"

# Initialize the model
print(f"Loading model from {MODEL_PATH}...")
try:
    llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=4)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)


def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file with better handling of elements"""
    if pdf_file is None:
        return "No PDF file uploaded."

    try:
        # Use PyMuPDF (fitz) for better extraction
        doc = fitz.open(pdf_file.name)

        # Extract text with better handling of layouts
        text = ""
        for page_num in range(
            min(5, len(doc))
        ):  # Limit to first 5 pages to avoid context issues
            page = doc[page_num]

            # Get text with preservation of layout
            text += page.get_text("text") + "\n\n"

            # Check for images
            image_list = page.get_images(full=True)
            if image_list:
                text += f"[Page {page_num+1} contains {len(image_list)} image(s)/figure(s)]\n\n"

        # Clean up text - remove excessive whitespace
        text = re.sub(r"\n\s*\n", "\n\n", text)

        # Limit text length to avoid context window issues - much more aggressive limit
        if len(text) > 3000:
            text = (
                text[:3000] + "...\n[Note: Text truncated to fit model context window]"
            )

        return text

    except Exception as e:
        # Fallback to PyPDF2 if PyMuPDF fails
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file.name)
            text = ""
            for page_num in range(
                min(3, len(pdf_reader.pages))
            ):  # Limit to first 3 pages
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n\n"

            if len(text) > 3000:
                text = (
                    text[:3000]
                    + "...\n[Note: Text truncated to fit model context window]"
                )

            return (
                text
                + "\n[Note: Using simplified extraction. Some elements like equations and figures may not be properly recognized.]"
            )

        except:
            return f"Error extracting text from PDF: {str(e)}"


def grade_assignment(rubric, assignment):
    # Limit the length of inputs to avoid exceeding context window
    if len(rubric) > 500:
        rubric = rubric[:500] + "...[truncated]"
    if len(assignment) > 1500:
        assignment = assignment[:1500] + "...[truncated]"

    prompt = f"""### Instruction:
You are an academic grading assistant. Grade the following assignment according to the provided rubric.

### Input:
RUBRIC:
{rubric}

ASSIGNMENT:
{assignment}

### Response:
"""

    print("Generating grading response...")
    try:
        output = llm(
            prompt,
            max_tokens=512,  # Reduced from 1024 to avoid context window issues
            temperature=0.1,
            top_p=0.9,
            repeat_penalty=1.1,
            stop=["### Instruction:", "### Input:"],
        )
        return output["choices"][0]["text"]
    except Exception as e:
        return f"Error generating response: {e}"


def analyze_paper(paper_text, domain, focus):
    # Trim text if it's too long - much more aggressive limit
    if len(paper_text) > 2000:
        paper_text = (
            paper_text[:2000]
            + "...\n[Note: Text truncated to fit model context window]"
        )

    prompt = f"""### Instruction:
You are a research paper analysis assistant. Analyze the following research paper in the field of {domain}, focusing on {focus}.
Provide a brief but insightful analysis.

### Input:
PAPER:
{paper_text}

### Response:
"""

    print("Generating paper analysis...")
    try:
        output = llm(
            prompt,
            max_tokens=512,  # Reduced from 1024 to avoid context window issues
            temperature=0.2,
            top_p=0.9,
            repeat_penalty=1.1,
            stop=["### Instruction:", "### Input:"],
        )
        return output["choices"][0]["text"]
    except Exception as e:
        return f"Error generating response: {e}"


def analyze_pdf_paper(pdf_file, domain, focus):
    # Extract text from PDF
    paper_text = extract_text_from_pdf(pdf_file)

    # Pass the extracted text to the paper analysis function
    return analyze_paper(paper_text, domain, focus)


def get_pdf_summary(pdf_file):
    """Get a summary of the PDF structure"""
    if pdf_file is None:
        return "No PDF file uploaded."

    try:
        doc = fitz.open(pdf_file.name)

        # Basic PDF information
        summary = f"PDF Information:\n"
        summary += f"- Pages: {len(doc)}\n"

        # Count images in first few pages
        image_count = 0
        for page_num in range(min(5, len(doc))):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            image_count += len(image_list)

        summary += f"- Images/Figures detected in first 5 pages: {image_count}\n"

        # Detect if there might be mathematical content
        math_detected = False
        for page_num in range(
            min(3, len(doc))
        ):  # Check first 3 pages only to save time
            page = doc[page_num]
            text = page.get_text("text")
            if "∑" in text or "∫" in text or "=" in text or "π" in text:
                math_detected = True
                break

        if math_detected:
            summary += f"- Mathematical content detected in the document\n"

        summary += f"- Note: Analysis limited to first {min(5, len(doc))} pages to fit model constraints"

        return summary

    except Exception as e:
        return f"Error analyzing PDF: {str(e)}"


# Create the Gradio interface
with gr.Blocks(title="Academic LLM Assistant") as demo:
    gr.Markdown("# Academic LLM Assistant")

    with gr.Tab("Assignment Grading"):
        with gr.Row():
            with gr.Column():
                rubric_input = gr.Textbox(
                    label="Grading Rubric",
                    lines=5,
                    placeholder="Enter the grading rubric here...",
                )
                assignment_input = gr.Textbox(
                    label="Assignment Submission",
                    lines=10,
                    placeholder="Enter the student's submission here...",
                )
                grade_button = gr.Button("Grade Assignment")

            with gr.Column():
                grading_output = gr.Textbox(label="Grading Result", lines=15)

        grade_button.click(
            grade_assignment,
            inputs=[rubric_input, assignment_input],
            outputs=grading_output,
        )

    with gr.Tab("Research Paper Analysis - Text"):
        with gr.Row():
            with gr.Column():
                paper_input = gr.Textbox(
                    label="Research Paper Text",
                    lines=15,
                    placeholder="Paste the research paper text here...",
                )
                with gr.Row():
                    domain_input1 = gr.Dropdown(
                        label="Domain",
                        choices=[
                            "Computer Science",
                            "Psychology",
                            "Biology",
                            "Economics",
                            "Physics",
                            "Engineering",
                            "Mathematics",
                            "Other",
                        ],
                        value="Computer Science",
                    )
                    focus_input1 = gr.Radio(
                        label="Analysis Focus",
                        choices=[
                            "Methodology",
                            "Results",
                            "Theoretical Framework",
                            "Implications",
                            "Literature Review",
                            "Overall Quality",
                        ],
                        value="Methodology",
                    )
                analyze_button = gr.Button("Analyze Paper")

            with gr.Column():
                analysis_output1 = gr.Textbox(label="Analysis Result", lines=15)

        analyze_button.click(
            analyze_paper,
            inputs=[paper_input, domain_input1, focus_input1],
            outputs=analysis_output1,
        )

    with gr.Tab("Research Paper Analysis - PDF Upload"):
        with gr.Row():
            with gr.Column():
                pdf_input = gr.File(
                    label="Upload Research Paper (PDF)", file_types=[".pdf"]
                )
                with gr.Row():
                    domain_input2 = gr.Dropdown(
                        label="Domain",
                        choices=[
                            "Computer Science",
                            "Psychology",
                            "Biology",
                            "Economics",
                            "Physics",
                            "Engineering",
                            "Mathematics",
                            "Other",
                        ],
                        value="Computer Science",
                    )
                    focus_input2 = gr.Radio(
                        label="Analysis Focus",
                        choices=[
                            "Methodology",
                            "Results",
                            "Theoretical Framework",
                            "Implications",
                            "Literature Review",
                            "Overall Quality",
                        ],
                        value="Methodology",
                    )
                pdf_analyze_button = gr.Button("Analyze PDF")

            with gr.Column():
                pdf_summary = gr.Textbox(
                    label="PDF Structure Summary", lines=5, visible=True
                )
                extracted_text = gr.Textbox(
                    label="Extracted Text (Preview)", lines=8, visible=True
                )
                analysis_output2 = gr.Textbox(label="Analysis Result", lines=15)

        # First analyze PDF structure and extract text
        pdf_input.change(get_pdf_summary, inputs=[pdf_input], outputs=[pdf_summary])

        pdf_input.change(
            extract_text_from_pdf, inputs=[pdf_input], outputs=[extracted_text]
        )

        # Then analyze the PDF content
        pdf_analyze_button.click(
            analyze_pdf_paper,
            inputs=[pdf_input, domain_input2, focus_input2],
            outputs=[analysis_output2],
        )

    gr.Markdown("## Notes")
    gr.Markdown("* This application runs entirely on your local machine.")
    gr.Markdown("* No data is sent to external servers.")
    gr.Markdown(
        "* Due to model constraints, only the first few pages of papers are analyzed."
    )
    gr.Markdown(
        "* This is a lightweight version designed to work with limited context windows."
    )
    gr.Markdown("* For larger papers, consider analyzing specific sections separately.")

# Launch the interface
if __name__ == "__main__":
    demo.launch(share=False)
