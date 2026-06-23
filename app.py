import gradio as gr
from src.rag_pipeline import ComplaintRAG

rag = ComplaintRAG()


def ask_question(question):
    if not question or not question.strip():
        return (
            "⚠️ Please enter a valid question.",
            "<p style='color: #6b7280; font-style: italic;'>No sources to display.</p>"
        )

    try:
        result = rag.answer_question(question)

        answer = result["answer"]

        sources_md = "<div class='sources-container'>"

        for idx, source in enumerate(result["sources"], start=1):
            sources_md += f"""
<details class='source-accordion'>
<summary><b>📄 Source {idx}</b></summary>

<div class='source-text'>
{source["text"]}
</div>

</details>
"""

        sources_md += "</div>"

        return answer, sources_md

    except Exception as e:
        return f"❌ Error: {str(e)}", ""


custom_css = """
.gradio-container {
    max-width: 1300px !important;
    margin: 40px auto !important;
    font-family: 'Inter', system-ui, sans-serif;
}

.header-container {
    text-align: center;
    margin-bottom: 30px;
    padding: 24px;
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    border-radius: 12px;
    border: 1px solid #bfdbfe;
}

#title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #1e40af;
    margin-bottom: 8px;
}

#subtitle {
    font-size: 1.1rem;
    color: #4b5563;
}

.sources-container {
    max-height: 500px;
    overflow-y: auto;
}

.source-accordion {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 10px;
}

.source-accordion[open] {
    border-color: #3b82f6;
    box-shadow: 0 2px 8px rgba(59,130,246,0.15);
}

.source-accordion summary {
    cursor: pointer;
    font-weight: 600;
}

.source-text {
    margin-top: 10px;
    padding-left: 12px;
    border-left: 3px solid #3b82f6;
    color: #475569;
    line-height: 1.6;
}

footer {
    visibility: hidden !important;
}
"""

app_theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="slate"
)

with gr.Blocks() as demo:

    gr.HTML(
        """
        <div class="header-container">
            <div id="title">📋 Complaint Analysis RAG Assistant</div>
            <div id="subtitle">
                Analyze customer complaints and view supporting evidence.
            </div>
        </div>
        """
    )

    with gr.Row(equal_height=True):

        with gr.Column(scale=2):

            question_box = gr.Textbox(
                label="Ask a Question",
                placeholder="Why are customers disputing credit card charges?",
                lines=4
            )

            with gr.Row():
                clear_btn = gr.Button(
                    "🗑️ Clear",
                    variant="secondary"
                )

                ask_btn = gr.Button(
                    "🔍 Ask Assistant",
                    variant="primary"
                )

            gr.Examples(
                examples=[
                    ["Why are customers disputing credit card charges?"],
                    ["What mortgage servicing issues are common?"],
                    ["Why are customers unhappy with debt collection?"],
                    ["What billing problems appear frequently?"],
                    ["What complaints are made about loan payments?"]
                ],
                inputs=question_box,
                label="Example Questions"
            )

        with gr.Column(scale=3):

            answer_output = gr.Textbox(
                label="AI Response",
                lines=10,
                interactive=False,
                
            )

            with gr.Accordion(
                "📂 Sources Used for Answer Generation",
                open=True
            ):

                sources_output = gr.HTML(
                    value="""
                    <p style="color:#94a3b8;font-style:italic;">
                    Submit a question to view source documents.
                    </p>
                    """
                )

    ask_btn.click(
        fn=ask_question,
        inputs=question_box,
        outputs=[
            answer_output,
            sources_output
        ]
    )

    question_box.submit(
        fn=ask_question,
        inputs=question_box,
        outputs=[
            answer_output,
            sources_output
        ]
    )

    clear_btn.click(
        lambda: (
            "",
            "",
            """
            <p style="color:#94a3b8;font-style:italic;">
            Submit a question to view source documents.
            </p>
            """
        ),
        outputs=[
            question_box,
            answer_output,
            sources_output
        ]
    )

demo.launch()