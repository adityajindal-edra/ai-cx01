import anthropic
import os
import json
from datetime import datetime
import base64

# Configuration class for easy management
class Config:
    def __init__(self):
        self.USER_PROMPT_FILE = "user_prompt.txt"
        self.OUTPUT_DIR = "outputs"
        self.MODEL = "claude-sonnet-4-20250514"

        # Thinking mode configuration
        self.ENABLE_THINKING = True
        self.MAX_TOKENS = 54000  # Total max tokens for response
        self.THINKING_BUDGET_TOKENS = 44000  # Budget tokens for thinking process

        # Streaming configuration
        self.ENABLE_STREAMING = True  # Enable streaming for long requests

        # System prompt
        self.SYSTEM_PROMPT = """Role: You are a professional customer support agent designed to resolve technical tickets for customers.

Goal:
- Generate or suggest a relevant root cause to the customer's problem.

Context/Input:
You will receive a support ticket that includes:
- A user-submitted issue
- All available context (logs, session IDs, screenshots, error codes, documentation, infromation from user, capabilities, etc.)

Task:
- Analyze the provided information.
- Determine the root cause of the issue user is facing

Output:
- Always respond in the following JSON format:
{
  "root cause": "<your root cause here, or empty string if not ready>",
  "reason/chain_of_thought": "<explain your reasoning on how you arrived at this root cause>",
}

Constraints:
- Be concise and professional in your root causes.
- Always check for completeness of information before proceeding.
- Only provide causes relevant to the ticket / product, backed by sound logical reasoning.
- If root cause/answer is not possible to any query, just say there is no such information available to do that, but strictly do not hallucinate or give any recommended solutions.

---

Example Outputs:

```json
{
  "root cause": "There is no invoice generated for this customer last month. Confirm if the customer made any purchases during this period, or if further assistance is needed.",
  "reason/chain_of_thought": "After checking the list of invoices for last month and searching for the customer's email id, I concluded that there is no invoice generated for this customer last month because their ",
}
```"""

# Load user prompt from file
def load_user_prompt(file_path):
    """Load user prompt from a text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: User prompt file '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading user prompt file: {e}")
        return None

# Load markdown file as text
def load_markdown_file(md_path):
    """Load markdown file and return as text"""
    try:
        with open(md_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Markdown file '{md_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading markdown file '{md_path}': {e}")
        return None

# Load and encode PDF file
def load_pdf_as_base64(pdf_path):
    """Load PDF file and return as base64 encoded string"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_content = file.read()
            return base64.b64encode(pdf_content).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading PDF file '{pdf_path}': {e}")
        return None

# Parse file paths from user prompt
def extract_file_paths(user_prompt):
    """Extract PDF and MD file paths from user prompt"""
    file_paths = []
    lines = user_prompt.split('\n')

    for line in lines:
        line = line.strip()
        if line.endswith('.pdf') or line.endswith('.md'):
            # Extract just the filename or path
            if '(' in line and ')' in line:
                # Extract from parentheses like (browserstack_product_suite.pdf)
                start = line.find('(') + 1
                end = line.find(')')
                file_path = line[start:end]
            else:
                # Direct file path
                file_path = line
            file_paths.append(file_path)

    return file_paths

# Generate output filename
def generate_output_filename():
    """Generate unique output filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"claude_output_{timestamp}.json"

# Handle streaming response
def handle_streaming_response(stream):
    """Handle streaming response from Claude API"""
    thinking_content = ""
    response_content = ""
    usage_info = None

    print("Processing streaming response...")

    try:
        for chunk in stream:
            if hasattr(chunk, 'type'):
                if chunk.type == 'message_start':
                    print("✓ Message started")
                    if hasattr(chunk, 'message') and hasattr(chunk.message, 'usage'):
                        usage_info = chunk.message.usage

                elif chunk.type == 'content_block_start':
                    if hasattr(chunk, 'content_block'):
                        block_type = getattr(chunk.content_block, 'type', 'unknown')
                        if block_type == 'thinking':
                            print("✓ Thinking block started")
                        elif block_type == 'text':
                            print("✓ Text block started")

                elif chunk.type == 'content_block_delta':
                    if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text'):
                        text = chunk.delta.text
                        # Simple heuristic to separate thinking from response
                        if hasattr(chunk, 'index') and chunk.index == 0:
                            thinking_content += text
                        else:
                            response_content += text

                        # Print progress indicator
                        print(".", end="", flush=True)

                elif chunk.type == 'content_block_stop':
                    block_type = getattr(chunk, 'content_block', {}).get('type', 'unknown')
                    if block_type == 'thinking':
                        print("\n✓ Thinking block completed")
                    elif block_type == 'text':
                        print("\n✓ Text block completed")

                elif chunk.type == 'message_delta':
                    if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'stop_reason'):
                        print(f"\n✓ Message completed: {chunk.delta.stop_reason}")

                elif chunk.type == 'message_stop':
                    print("✓ Streaming completed")

    except Exception as e:
        print(f"\nError processing stream: {e}")
        return "", "", None

    print("\n")
    return thinking_content, response_content, usage_info

# Handle non-streaming response
def handle_non_streaming_response(response):
    """Handle non-streaming response from Claude API"""
    thinking_content = ""
    response_content = ""

    if hasattr(response, 'content') and response.content:
        for content_block in response.content:
            if hasattr(content_block, 'type'):
                if content_block.type == 'thinking':
                    thinking_content = content_block.text
                elif content_block.type == 'text':
                    response_content = content_block.text
            else:
                # Fallback for different response structure
                response_content = content_block.text if hasattr(content_block, 'text') else str(content_block)

    return thinking_content, response_content

# Main function
def main():
    # Load configuration
    config = Config()

    # Create output directory if it doesn't exist
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    # Load API key from environment variable
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Please set it with: export ANTHROPIC_API_KEY='your-api-key-here'")
        return

    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=api_key)

    # Load user prompt
    user_prompt = load_user_prompt(config.USER_PROMPT_FILE)
    if not user_prompt:
        return

    # Extract file paths from user prompt
    file_paths = extract_file_paths(user_prompt)
    print(f"Found {len(file_paths)} files to process: {file_paths}")

    # Prepare message content
    message_content = []
    processed_files = []

    # Start building the complete prompt text
    complete_prompt = user_prompt + "\n\n"

    # Process each file
    for file_path in file_paths:
        if file_path.endswith('.md'):
            # Handle markdown files
            md_content = load_markdown_file(file_path)
            if md_content:
                complete_prompt += f"\n\n--- Content from {file_path} ---\n\n"
                complete_prompt += md_content
                processed_files.append(file_path)
                print(f"Added Markdown: {file_path}")
            else:
                print(f"Skipping Markdown: {file_path} (could not load)")

        elif file_path.endswith('.pdf'):
            # Handle PDF files (as before)
            pdf_base64 = load_pdf_as_base64(file_path)
            if pdf_base64:
                # Add PDF as document attachment
                message_content.append({
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_base64
                    }
                })
                processed_files.append(file_path)
                print(f"Added PDF: {file_path}")
            else:
                print(f"Skipping PDF: {file_path} (could not load)")

    # Add the complete prompt (including markdown content) as the main text
    message_content.insert(0, {
        "type": "text",
        "text": complete_prompt
    })

    try:
        # Prepare API call parameters
        api_params = {
            "model": config.MODEL,
            "max_tokens": config.MAX_TOKENS,
            "system": config.SYSTEM_PROMPT,
            "messages": [
                {
                    "role": "user",
                    "content": message_content
                }
            ]
        }

        # Add thinking mode parameters if enabled
        if config.ENABLE_THINKING:
            api_params["thinking"] = {
                "type": "enabled",
                "budget_tokens": config.THINKING_BUDGET_TOKENS
            }

        # Add streaming parameter
        if config.ENABLE_STREAMING:
            api_params["stream"] = True

        print("Sending request to Claude...")
        print(f"Configuration:")
        print(f"  - Model: {config.MODEL}")
        print(f"  - Max Tokens: {config.MAX_TOKENS}")
        print(f"  - Thinking Mode: {config.ENABLE_THINKING}")
        print(f"  - Streaming: {config.ENABLE_STREAMING}")
        if config.ENABLE_THINKING:
            print(f"  - Thinking Budget Tokens: {config.THINKING_BUDGET_TOKENS}")

        # Make API call to Claude
        if config.ENABLE_STREAMING:
            # Streaming response
            stream = client.messages.create(**api_params)
            thinking_content, response_content, usage_info = handle_streaming_response(stream)

            # Create a mock usage object if we don't have one
            if usage_info is None:
                usage_info = type('Usage', (), {
                    'input_tokens': 0,
                    'output_tokens': 0
                })()
        else:
            # Non-streaming response
            response = client.messages.create(**api_params)
            thinking_content, response_content = handle_non_streaming_response(response)
            usage_info = response.usage

        print("Response received from Claude.")

        # Prepare output data
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "model": config.MODEL,
            "configuration": {
                "max_tokens": config.MAX_TOKENS,
                "thinking_enabled": config.ENABLE_THINKING,
                "thinking_budget_tokens": config.THINKING_BUDGET_TOKENS if config.ENABLE_THINKING else None,
                "streaming_enabled": config.ENABLE_STREAMING
            },
            "user_prompt_file": config.USER_PROMPT_FILE,
            "processed_files": processed_files,
            "thinking_content": thinking_content if config.ENABLE_THINKING else None,
            "response": response_content,
            "usage": {
                "input_tokens": getattr(usage_info, 'input_tokens', 0),
                "output_tokens": getattr(usage_info, 'output_tokens', 0)
            }
        }

        # Generate output filename and save
        output_filename = generate_output_filename()
        output_path = os.path.join(config.OUTPUT_DIR, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"Response saved to: {output_path}")
        print(f"Token usage - Input: {getattr(usage_info, 'input_tokens', 0)}, Output: {getattr(usage_info, 'output_tokens', 0)}")

        # Print thinking process if available
        if config.ENABLE_THINKING and thinking_content:
            print("\nClaude's Thinking Process:")
            print("=" * 50)
            print(thinking_content)
            print("=" * 50)

        # Print the final response
        print("\nClaude's Final Response:")
        print("=" * 50)
        print(response_content)
        print("=" * 50)

    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return

if __name__ == "__main__":
    main()
