# Save this as test_model.py
import gradio as gr
from llama_cpp import Llama

# Path to the model
MODEL_PATH = "models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf"

# Initialize the model
print(f"Loading model from {MODEL_PATH}...")
try:
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,  # Context window size
        n_threads=4,  # Number of CPU threads to use
    )
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)


def process_prompt(prompt):
    formatted_prompt = f"""### Instruction:
{prompt}

### Response:
"""

    print("Generating response...")
    try:
        output = llm(
            formatted_prompt,
            max_tokens=512,
            temperature=0.1,
            top_p=0.9,
            repeat_penalty=1.1,
            stop=["### Instruction:", "### Input:"],
        )
        return output["choices"][0]["text"]
    except Exception as e:
        return f"Error generating response: {e}"


# Create the Gradio interface
with gr.Blocks(title="Simple LLM Assistant") as demo:
    gr.Markdown("# Simple LLM Assistant")

    with gr.Tab("Basic Interface"):
        prompt_input = gr.Textbox(
            label="Your Prompt",
            lines=5,
            placeholder="Enter your prompt here. For example: Explain recursion in programming.",
        )
        process_button = gr.Button("Generate Response")
        output = gr.Textbox(label="Generated Response", lines=10)

        process_button.click(process_prompt, inputs=prompt_input, outputs=output)

    gr.Markdown("## Notes")
    gr.Markdown("* This is a basic test of the model.")
    gr.Markdown(
        "* For academic purposes, you can add specialized prompts for grading or paper analysis."
    )

# Launch the interface
if __name__ == "__main__":
    demo.launch(share=False)
