import os
import pandas as pd
import taipy.gui.builder as tgb
from taipy.gui import Gui, notify, State
from pathlib import Path

# Initialize variables
UPLOAD_FOLDER = "./uploaded_files"
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)

# Initialize dataframes for file tracking
uploaded_files = pd.DataFrame(columns=["Filename"])
removed_files = pd.DataFrame(columns=["Filename"])

# Initialize messages
messages = []
messages_dict = {}
query_message = ""

def on_init(state):
    """Initialize the chat state"""
    state.messages = [
        {
            "style": "assistant_message",
            "content": "Welcome to the Corporate Documentation System! How can I help you?",
        },
    ]
    new_conv = create_conv(state)
    state.conv.update_content(state, new_conv)

def create_conv(state):
    """Create the conversation display"""
    messages_dict = {}
    with tgb.Page() as conversation:
        for i, message in enumerate(state.messages):
            text = message["content"].replace("<br>", "\n").replace('"', "'")
            messages_dict[f"message_{i}"] = text
            tgb.text(
                f"{{messages_dict.get('message_{i}') or ''}}",
                class_name=f"message_base {message['style']}",
                mode="md",
            )
    state.messages_dict = messages_dict
    return conversation

def send_message(state):
    """Handle sending messages in chat"""
    if state.query_message.strip():
        state.messages.append(
            {
                "style": "user_message",
                "content": state.query_message,
            }
        )
        # Simulate response - replace with your actual response function
        response = f"Received your message: {state.query_message}"
        state.messages.append(
            {
                "style": "assistant_message",
                "content": response,
            }
        )
        state.conv.update_content(state, create_conv(state))
        state.query_message = ""

def handle_file_upload(state, file):
    """Handle file upload"""
    if file and file.name:
        # Save file
        file_path = os.path.join(UPLOAD_FOLDER, file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())

        # Update uploaded files list
        global uploaded_files
        if file.name not in uploaded_files['Filename'].values:
            uploaded_files.loc[len(uploaded_files)] = [file.name]
        state.uploaded_files = uploaded_files
        notify(state, "success", f"File uploaded: {file.name}")

def remove_file(state, filename):
    """Handle file removal"""
    global uploaded_files, removed_files

    # Remove from uploaded files
    if filename in uploaded_files['Filename'].values:
        uploaded_files = uploaded_files[uploaded_files['Filename'] != filename]

        # Add to removed files
        if filename not in removed_files['Filename'].values:
            removed_files.loc[len(removed_files)] = [filename]

        # Remove file from disk
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        state.uploaded_files = uploaded_files
        state.removed_files = removed_files
        notify(state, "info", f"File removed: {filename}")

def reset_chat(state):
    """Reset the chat history"""
    state.query_message = ""
    on_init(state)

# Create the main page
with tgb.Page() as page:
    # Documentation header
    tgb.text("""
    # Corporate Documentation Management System
    
    Welcome to our documentation management platform. This system allows you to:
    - Chat with our documentation assistant
    - Upload and manage corporate documents
    - Track document changes and removals
    
    Use the sidebar to manage your files and the chat interface below to ask questions.
    """, mode="md")

    with tgb.layout(columns="350px 1"):
        # Sidebar
        with tgb.part(class_name="sidebar"):
            tgb.text("## Document Management", mode="md")
            tgb.button(
                "New Chat",
                class_name="fullwidth plain",
                on_action=reset_chat,
            )

            # File upload
            tgb.file_selector("Upload File", on_action=handle_file_upload)

            # Display current files
            tgb.text("### Current Files", mode="md")
            tgb.table("{uploaded_files}", show_all=True)

            # Display removed files
            tgb.text("### Removed Files", mode="md")
            tgb.table("{removed_files}", show_all=True)

        # Main chat area
        with tgb.part(class_name="p1"):
            tgb.part(partial="{conv}", height="600px", class_name="card card_chat")
            with tgb.part("card mt1"):
                tgb.input(
                    "{query_message}",
                    on_action=send_message,
                    change_delay=-1,
                    label="Write your message:",
                    class_name="fullwidth",
                )

# Run the application
if __name__ == "__main__":
    gui = Gui(page)
    conv = gui.add_partial("")

    # Add custom CSS for styling
    stylekit = {
        "color_primary": "#2563eb",
        "color_secondary": "#4b5563",
        "color_background_dark": "#1f2937",
        "color_background_light": "#ffffff",
    }

    gui.run(
        title="Corporate Documentation System",
        dark_mode=False,
        margin="0px",
        styles=stylekit,
        debug=True,
        uploaded_files=uploaded_files,
        removed_files=removed_files,
    )