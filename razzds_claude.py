import os
import io
import re
import json
import datetime
from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic_error_handler import AnthropicErrorHandler
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import TerminalFormatter

load_dotenv()
client = Anthropic()
error_handler = AnthropicErrorHandler()
conversation_history = []

def sanitize_to_ascii(text):
    if text is None:
        return None
    return ''.join(char for char in text if ord(char) in [10] or (32 <= ord(char) <= 126))

def format_text(text):
    if text is None:
        return None
    code_blocks = {}
    code_block_count = 0
    def save_code_block(match):
        nonlocal code_block_count
        placeholder = f"__CODE_BLOCK_{code_block_count}__"
        code_blocks[placeholder] = match.group(0)
        code_block_count += 1
        return placeholder
    temp_text = re.sub(r'```(\w*)\n([\s\S]*?)\n```', save_code_block, text)
    temp_text = re.sub(r'^### (.*?)$', r'\033[01;32m\1\033[0m', temp_text, flags=re.MULTILINE)
    temp_text = re.sub(r'^## (.*?)$', r'\033[01;32m\1\033[0m', temp_text, flags=re.MULTILINE)
    temp_text = re.sub(r'^# (.*?)$', r'\033[01;32m\1\033[0m', temp_text, flags=re.MULTILINE)
    temp_text = re.sub(r'\*\*(.*?)\*\*', r'\033[38;5;153m\1\033[0m', temp_text)
    temp_text = re.sub(r'(?<![`\\])`([^`\n]+?)`(?![`])', r'\033[38;5;153m\1\033[0m', temp_text)
    for placeholder, code_block in code_blocks.items():
        code_content_match = re.match(r'```(\w*)\n([\s\S]*?)\n```', code_block)
        if code_content_match:
            language = code_content_match.group(1) or "text"
            code_content = code_content_match.group(2)
            try:
                lexer = get_lexer_by_name(language, stripall=True)
            except Exception:
                lexer = TextLexer(stripall=True)
            highlighted_code = highlight(code_content,lexer,TerminalFormatter(style='github-dark'))
            temp_text = temp_text.replace(placeholder, highlighted_code)
    return temp_text

def read_file(file_path):
    with open(file_path, 'r', encoding='ascii', errors='replace') as file:
        content = file.read()
        ascii_only = sanitize_to_ascii(content)
        return ascii_only

def save_conversation(history, filename=None):
    if not filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        filename = f"conversation_{timestamp}.json"
    sanitized_history = []
    for message in history:
        sanitized_message = {"role": message["role"],"content":sanitize_to_ascii(message["content"])}
        sanitized_history.append(sanitized_message)
    with open(filename, 'w', encoding='ascii') as f:
        json.dump(sanitized_history, f, indent=2)
    return filename

def load_conversation(filename):
    with open(filename, 'r', encoding='ascii') as f:
        loaded_data = json.load(f)
        for message in loaded_data:
            if "content" in message:
                message["content"] = sanitize_to_ascii(message["content"])
        return loaded_data

def print_history(history):
    for i, message in enumerate(history):
        role = message["role"]
        content = message["content"]
        if role == "user":
            role_display = "[Razzd83]"
        else:
            role_display = "[Claude37]"
        formatted_content = format_text(content)
        print(f"{i+1}. {role_display}\n\n{formatted_content}\n")

def print_raw_history(history):
    for i, message in enumerate(history):
        role = message["role"]
        content = message["content"]
        if role == "user":
            role_display = "[Razzd83]"
        else:
            role_display = "[Claude37]"
        print(f"{i+1}. {role_display}\n\n{content}\n")

def process_input(user_input):
    global conversation_history
    if user_input.startswith("/file "):
        file_path = user_input[6:].strip()
        file_content = read_file(file_path)
        print(f"File loaded: {file_path}")
        return file_content
    elif user_input.startswith("/save"):
        parts = user_input.split()
        filename = parts[1] if len(parts) > 1 else None
        saved_file = save_conversation(conversation_history, filename)
        print(f"Conversation saved to: {saved_file}")
        return None
    elif user_input.startswith("/load "):
        filename = user_input[6:].strip()
        conversation_history = load_conversation(filename)
        print(f"Loaded conversation from: {filename}")
        print(f"Conversation has {len(conversation_history)//2} exchanges")
        return None
    elif user_input == "/history":
        print_history(conversation_history)
        return None
    elif user_input == "/history-code":
        print_raw_history(conversation_history)
        return None
    elif user_input == "/response":
        if 'last_response' in globals():
            print("Last Response Object:")
            print(last_response)
        else:
            print("No response available yet")
        return None
    return user_input

def print_prompt():
    return "===== Razzd83 ======\n"

while True:
    user_input = input(print_prompt())
    user_input = sanitize_to_ascii(user_input)
    if user_input.lower() == "exit":
        print("Exit.")
        break

    processed_input = process_input(user_input)
    if processed_input is not None:
        processed_input = sanitize_to_ascii(processed_input)
        conversation_history.append({"role": "user", "content": processed_input})
        sanitized_history = []
        for message in conversation_history:
            sanitized_message = {"role": message["role"], "content": sanitize_to_ascii(message["content"])}
            sanitized_history.append(sanitized_message)

        response, error_message = error_handler.handle_request(
            client.messages.create,
            model="claude-3-7-sonnet-latest",
            tools=[{ "type":"text_editor_20250124" , "name":"str_replace_editor" }],
            system="",
            messages=sanitized_history,
            max_tokens=4096,
            temperature=0)

        if error_message:
            conversation_history.pop()
            print(f"===== Claude37 =====\n{error_message}")
            continue
        globals()['last_response'] = response
        assistant_response = response.content[0].text
        assistant_response = sanitize_to_ascii(assistant_response)
        conversation_history.append({"role": "assistant", "content": assistant_response})
        formatted_response = format_text(assistant_response)
        print(f"===== Claude37 =====\n{formatted_response}")
        print(f"\n[{response.usage.input_tokens}-{response.usage.output_tokens}]")
        print(last_response)