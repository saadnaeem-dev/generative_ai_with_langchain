"""
CorpDocs with Citations: A Corporate Documentation Pipeline with RAG and Source Attribution
This single file contains the complete code to run a documentation generation system
using LangChain, LangGraph, and Gradio. In addition to generating and refining documentation,
this pipeline now retrieves and attaches citations to the final output.

Workflow Overview:
1. Generate an initial project documentation draft from a user's request.
2. Analyze the draft for compliance with corporate standards.
3. If issues are detected, prompt for human expert feedback.
4. Finalize the documentation (integrating any feedback).
5. Retrieve and append citations to the final document.
6. Output the fully revised document with inline source citations.

Note: More details on performance measurement and observability will be covered in Chapter 8.
"""

import gradio as gr             # For building the interactive web interface.
from langchain_core.messages import HumanMessage

from chapter4.rag import graph, config

# -------------------------------------------------------------------------------------------
# GRADIO INTERFACE: Build the interactive web UI.
CSS = """
.contain { display: flex; flex-direction: column; }
#component-0 { height: 100%; }
#chatbot { flex-grow: 1; overflow: auto;}
"""

def answer_question(message, history):
    """Answers the question from the user.

    Note: this ignores the previous messages

    There's some better way to stream this:
    for event in graph.stream(
            {"messages": HumanMessage(message)}, config=config
    ):
        print(event.key())
        if event.key == "doc_finalizer":
            for value in event.values():
                yield value["messages"][-1].content
.
    """
    response = graph.invoke({"messages": HumanMessage(message)}, config=config)
    return response["messages"][-1].content


with gr.Blocks(css=CSS, title="📄 CorpDocs with Citations") as demo:
    gr.Markdown("""
    # 📄 CorpDocs with Citations
    
    CorpDocs is your corporate documentation assistant. This tool generates detailed project documentation,
    verifies compliance with corporate standards, and integrates human feedback when necessary. Finally,
    it retrieves and attaches source citations to the final document.
    
    **Workflow:**
    1. **Generate Documentation:** Create an initial draft.
    2. **Compliance Check:** Automatically review for adherence to corporate guidelines.
    3. **Human Feedback:** If issues are detected, provide corrective feedback.
    4. **Finalize Document:** Produce the revised document.
    5. **Add Citations:** Append source citations to the document.
    
    If you like this application, please give us a 5-star review on [Amazon](https://amzn.to/3X1xQbn)!
    """)

    chatbot = gr.Chatbot(
        show_copy_button=False,
        show_share_button=True,
        label="Documentation Assistant",
        elem_id="chatbot",
        type="tuples"
    )
    msg = gr.Textbox(
        placeholder="Enter your documentation request...",
        container=False,
        scale=7
    )
    gr.ChatInterface(
        answer_question,
        type="messages",
        chatbot=chatbot,
        textbox=msg,
        title="Documentation Assistant",
        description="Ask any documentation request",
        theme="ocean",
    )

    # -------------------------------------------------------------------------------------------
    # EXAMPLE BUTTONS: Provide preset documentation scenarios.
    with gr.Row():
        example_button1 = gr.Button("Example 1: New Product Launch")
        example_button2 = gr.Button("Example 2: Quarterly Report")
        example_button3 = gr.Button("Example 3: Security Audit Summary")

    def load_example(example_num):
        if example_num == 1:
            return "Generate documentation for a new product launch outlining objectives, timelines, and KPIs."
        elif example_num == 2:
            return "Generate a detailed quarterly report for the marketing department."
        elif example_num == 3:
            return "Generate a security audit summary for our IT infrastructure."
        else:
            return None

    example_button1.click(fn=load_example, inputs=[gr.Number(value=1, visible=False)], outputs=[msg], show_progress="hidden")
    example_button2.click(fn=load_example, inputs=[gr.Number(value=2, visible=False)], outputs=[msg], show_progress="hidden")
    example_button3.click(fn=load_example, inputs=[gr.Number(value=3, visible=False)], outputs=[msg], show_progress="hidden")
    refresh_button = gr.Button("🔄 Refresh")
    refresh_button.click(fn=lambda: None, inputs=[], outputs=[chatbot], js="() => {window.location.reload()}")


if __name__ == "__main__":
    # Launch the Gradio application.
    # For hot-reloading run from the terminal from the top-level directory of the repository like this:
    # > gradio chapter4/app.py
    # If you run from the chapter4/ you can set the PYTHONPATH, for example, in Linux and macOS:
    # > PYTHONPATH=../ gradio app.py
    # Please make sure you are in the langchain_ai environment, for example by typing
    # conda activate langchain_ai
    demo.launch()


