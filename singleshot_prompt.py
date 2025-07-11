import anthropic
import google.generativeai as genai
import os
import json
from datetime import datetime
import base64
from dotenv import load_dotenv
import argparse
from pathlib import Path
import concurrent.futures
import threading

load_dotenv()

# Configuration class for easy management
class Config:
    def __init__(self, user_prompt_file):
        self.USER_PROMPT_FILE = user_prompt_file
        self.OUTPUT_DIR = "outputs"

        # Claude configuration
        self.CLAUDE_MODEL = "claude-sonnet-4-20250514"
        self.CLAUDE_ENABLE_THINKING = True
        self.CLAUDE_MAX_TOKENS = 54000
        self.CLAUDE_THINKING_BUDGET_TOKENS = 44000
        self.CLAUDE_ENABLE_STREAMING = True

        # Gemini configuration
        self.GEMINI_MODEL = "gemini-2.5-pro"
        self.GEMINI_MAX_TOKENS = 50000
        self.GEMINI_ENABLE_STREAMING = True

        # Model selection
        self.ENABLE_CLAUDE = True
        self.ENABLE_GEMINI = True

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

# Parse command line arguments
def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run dual AI model analysis on support tickets')
    parser.add_argument(
        'prompt_file',
        nargs='?',
        default='user_prompt.txt',
        help='Path to the user prompt file (default: user_prompt.txt)'
    )
    parser.add_argument(
        '--claude-only',
        action='store_true',
        help='Run only Claude model'
    )
    parser.add_argument(
        '--gemini-only',
        action='store_true',
        help='Run only Gemini model'
    )
    parser.add_argument(
        '--output-dir',
        default='outputs',
        help='Output directory for results (default: outputs)'
    )
    parser.add_argument(
        '--no-streaming',
        action='store_true',
        help='Disable streaming for both models'
    )
    parser.add_argument(
        '--no-thinking',
        action='store_true',
        help='Disable Claude thinking mode'
    )

    return parser.parse_args()

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

# Upload file to Gemini
def upload_file_to_gemini(file_path):
    """Upload file to Gemini and return file object"""
    try:
        print(f"Uploading {file_path} to Gemini...")
        file_obj = genai.upload_file(file_path)
        return file_obj
    except Exception as e:
        print(f"Error uploading {file_path} to Gemini: {e}")
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

# Generate output filename based on prompt file
def generate_output_filename(prompt_file_path):
    """Generate output filename based on prompt file name and timestamp"""
    # Extract filename without extension
    prompt_file_name = Path(prompt_file_path).stem
    timestamp = datetime.now().strftime("%d-%m_%H-%M")
    return f"{prompt_file_name}_{timestamp}.json"

# Handle Claude streaming response
def handle_claude_streaming_response(stream):
    """Handle streaming response from Claude API"""
    thinking_content = ""
    response_content = ""
    usage_info = None

    print("Processing Claude streaming response...")

    try:
        for chunk in stream:
            if hasattr(chunk, 'type'):
                if chunk.type == 'message_start':
                    print("✓ Claude message started")
                    if hasattr(chunk, 'message') and hasattr(chunk.message, 'usage'):
                        usage_info = chunk.message.usage

                elif chunk.type == 'content_block_start':
                    if hasattr(chunk, 'content_block'):
                        block_type = getattr(chunk.content_block, 'type', 'unknown')
                        if block_type == 'thinking':
                            print("✓ Claude thinking block started")
                        elif block_type == 'text':
                            print("✓ Claude text block started")

                elif chunk.type == 'content_block_delta':
                    if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text'):
                        text = chunk.delta.text
                        # Simple heuristic to separate thinking from response
                        if hasattr(chunk, 'index') and chunk.index == 0:
                            thinking_content += text
                        else:
                            response_content += text
                        print(".", end="", flush=True)

                elif chunk.type == 'content_block_stop':
                    block_type = getattr(chunk, 'content_block', {}).get('type', 'unknown')
                    if block_type == 'thinking':
                        print("\n✓ Claude thinking block completed")
                    elif block_type == 'text':
                        print("\n✓ Claude text block completed")

                elif chunk.type == 'message_stop':
                    print("✓ Claude streaming completed")

    except Exception as e:
        print(f"\nError processing Claude stream: {e}")
        return "", "", None

    print("\n")
    return thinking_content, response_content, usage_info

# Handle Claude non-streaming response
def handle_claude_non_streaming_response(response):
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
                response_content = content_block.text if hasattr(content_block, 'text') else str(content_block)

    return thinking_content, response_content

# Handle Gemini streaming response
def handle_gemini_streaming_response(stream):
    """Handle streaming response from Gemini API"""
    response_content = ""
    usage_info = None

    print("Processing Gemini streaming response...")

    try:
        for chunk in stream:
            if hasattr(chunk, 'text'):
                response_content += chunk.text
                print(".", end="", flush=True)
            elif hasattr(chunk, 'candidates') and chunk.candidates:
                for candidate in chunk.candidates:
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'text'):
                                response_content += part.text
                                print(".", end="", flush=True)

        print("\n✓ Gemini streaming completed")

    except Exception as e:
        print(f"\nError processing Gemini stream: {e}")
        return "", None

    print("\n")
    return response_content, usage_info

# Call Claude API
def call_claude_api(client, config, message_content):
    """Call Claude API and return response"""
    try:
        print("🔵 Calling Claude API...")

        # Prepare API call parameters
        api_params = {
            "model": config.CLAUDE_MODEL,
            "max_tokens": config.CLAUDE_MAX_TOKENS,
            "system": config.SYSTEM_PROMPT,
            "messages": [
                {
                    "role": "user",
                    "content": message_content
                }
            ]
        }

        # Add thinking mode parameters if enabled
        if config.CLAUDE_ENABLE_THINKING:
            api_params["thinking"] = {
                "type": "enabled",
                "budget_tokens": config.CLAUDE_THINKING_BUDGET_TOKENS
            }

        # Add streaming parameter
        if config.CLAUDE_ENABLE_STREAMING:
            api_params["stream"] = True

        # Make API call to Claude
        if config.CLAUDE_ENABLE_STREAMING:
            stream = client.messages.create(**api_params)
            thinking_content, response_content, usage_info = handle_claude_streaming_response(stream)

            if usage_info is None:
                usage_info = type('Usage', (), {'input_tokens': 0, 'output_tokens': 0})()
        else:
            response = client.messages.create(**api_params)
            thinking_content, response_content = handle_claude_non_streaming_response(response)
            usage_info = response.usage

        return {
            "success": True,
            "thinking_content": thinking_content,
            "response_content": response_content,
            "usage": {
                "input_tokens": getattr(usage_info, 'input_tokens', 0),
                "output_tokens": getattr(usage_info, 'output_tokens', 0)
            }
        }

    except Exception as e:
        print(f"❌ Error calling Claude API: {e}")
        return {
            "success": False,
            "error": str(e),
            "thinking_content": "",
            "response_content": "",
            "usage": {"input_tokens": 0, "output_tokens": 0}
        }

# Call Gemini API
def call_gemini_api(config, complete_prompt, gemini_files):
    """Call Gemini API and return response"""
    try:
        print("🟢 Calling Gemini API...")

        # Create the model
        model = genai.GenerativeModel(config.GEMINI_MODEL)

        # Prepare content for Gemini
        content_parts = [config.SYSTEM_PROMPT + "\n\n" + complete_prompt]

        # Add uploaded files
        for file_obj in gemini_files:
            if file_obj:
                content_parts.append(file_obj)

        # Generate response
        if config.GEMINI_ENABLE_STREAMING:
            response = model.generate_content(
                content_parts,
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=config.GEMINI_MAX_TOKENS
                )
            )
            response_content, usage_info = handle_gemini_streaming_response(response)
        else:
            response = model.generate_content(
                content_parts,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=config.GEMINI_MAX_TOKENS
                )
            )
            response_content = response.text if hasattr(response, 'text') else str(response)
            usage_info = None

        return {
            "success": True,
            "response_content": response_content,
            "usage": {
                "input_tokens": getattr(usage_info, 'prompt_token_count', 0) if usage_info else 0,
                "output_tokens": getattr(usage_info, 'candidates_token_count', 0) if usage_info else 0
            }
        }

    except Exception as e:
        print(f"❌ Error calling Gemini API: {e}")
        return {
            "success": False,
            "error": str(e),
            "response_content": "",
            "usage": {"input_tokens": 0, "output_tokens": 0}
        }

# Main function
def main():
    # Parse command line arguments
    args = parse_arguments()

    # Load configuration
    config = Config(args.prompt_file)
    config.OUTPUT_DIR = args.output_dir

    # Apply command line overrides
    if args.claude_only:
        config.ENABLE_CLAUDE = True
        config.ENABLE_GEMINI = False
    elif args.gemini_only:
        config.ENABLE_CLAUDE = False
        config.ENABLE_GEMINI = True

    if args.no_streaming:
        config.CLAUDE_ENABLE_STREAMING = False
        config.GEMINI_ENABLE_STREAMING = False

    if args.no_thinking:
        config.CLAUDE_ENABLE_THINKING = False

    # Create output directory if it doesn't exist
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    # Initialize API clients
    claude_client = None
    if config.ENABLE_CLAUDE:
        claude_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not claude_api_key:
            print("❌ Error: ANTHROPIC_API_KEY environment variable not set.")
            config.ENABLE_CLAUDE = False
        else:
            claude_client = anthropic.Anthropic(api_key=claude_api_key)

    if config.ENABLE_GEMINI:
        gemini_api_key = os.getenv('GOOGLE_API_KEY')
        if not gemini_api_key:
            print("❌ Error: GOOGLE_API_KEY environment variable not set.")
            config.ENABLE_GEMINI = False
        else:
            genai.configure(api_key=gemini_api_key)

    if not config.ENABLE_CLAUDE and not config.ENABLE_GEMINI:
        print("❌ No API keys configured. Please set ANTHROPIC_API_KEY and/or GOOGLE_API_KEY")
        return

    # Load user prompt
    user_prompt = load_user_prompt(config.USER_PROMPT_FILE)
    if not user_prompt:
        return

    # Extract file paths from user prompt
    file_paths = extract_file_paths(user_prompt)
    print(f"Found {len(file_paths)} files to process: {file_paths}")

    # Prepare content for both models
    message_content = []  # For Claude
    processed_files = []
    gemini_files = []  # For Gemini

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
            # Handle PDF files
            pdf_base64 = load_pdf_as_base64(file_path)
            if pdf_base64:
                # For Claude: Add PDF as document attachment
                if config.ENABLE_CLAUDE:
                    message_content.append({
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_base64
                        }
                    })

                # For Gemini: Upload file
                if config.ENABLE_GEMINI:
                    gemini_file = upload_file_to_gemini(file_path)
                    gemini_files.append(gemini_file)

                processed_files.append(file_path)
                print(f"Added PDF: {file_path}")
            else:
                print(f"Skipping PDF: {file_path} (could not load)")

    # Add the complete prompt as the main text for Claude
    if config.ENABLE_CLAUDE:
        message_content.insert(0, {
            "type": "text",
            "text": complete_prompt
        })

    print("\n" + "="*50)
    print("STARTING PARALLEL DUAL MODEL ANALYSIS")
    print("="*50)

    # Store results
    results = {
        "timestamp": datetime.now().isoformat(),
        "user_prompt_file": config.USER_PROMPT_FILE,
        "processed_files": processed_files,
        "claude_result": None,
        "gemini_result": None,
        "execution_mode": "parallel"
    }

    # Run both API calls in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Submit both tasks
        future_to_model = {}

        if config.ENABLE_CLAUDE and claude_client:
            future_claude = executor.submit(call_claude_api, claude_client, config, message_content)
            future_to_model[future_claude] = "claude"

        if config.ENABLE_GEMINI:
            future_gemini = executor.submit(call_gemini_api, config, complete_prompt, gemini_files)
            future_to_model[future_gemini] = "gemini"

        # Wait for both to complete and collect results
        for future in concurrent.futures.as_completed(future_to_model):
            model_name = future_to_model[future]
            try:
                result = future.result()
                if model_name == "claude":
                    results["claude_result"] = result
                    print(f"✅ Claude completed: {result['success']}")
                elif model_name == "gemini":
                    results["gemini_result"] = result
                    print(f"✅ Gemini completed: {result['success']}")
            except Exception as e:
                print(f"❌ Error with {model_name}: {e}")
                if model_name == "claude":
                    results["claude_result"] = {"success": False, "error": str(e)}
                elif model_name == "gemini":
                    results["gemini_result"] = {"success": False, "error": str(e)}

    # Save combined results
    output_filename = generate_output_filename(config.USER_PROMPT_FILE)
    output_path = os.path.join(config.OUTPUT_DIR, output_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Combined results saved to: {output_path}")

    # Display results
    print("\n" + "="*50)
    print("RESULTS SUMMARY")
    print("="*50)

    if config.ENABLE_CLAUDE and results["claude_result"]:
        claude_result = results["claude_result"]
        print(f"\n🔵 CLAUDE RESULTS:")
        print(f"Status: {'✅ Success' if claude_result['success'] else '❌ Failed'}")
        if claude_result['success']:
            print(f"Tokens: {claude_result['usage']['input_tokens']} in, {claude_result['usage']['output_tokens']} out")

            if claude_result.get('thinking_content'):
                print(f"\n🧠 Claude's Thinking:")
                print("-" * 30)
                thinking_preview = claude_result['thinking_content'][:500]
                print(thinking_preview + "..." if len(claude_result['thinking_content']) > 500 else thinking_preview)

            print(f"\n💬 Claude's Response:")
            print("-" * 30)
            print(claude_result['response_content'])
        else:
            print(f"Error: {claude_result.get('error', 'Unknown error')}")

    if config.ENABLE_GEMINI and results["gemini_result"]:
        gemini_result = results["gemini_result"]
        print(f"\n🟢 GEMINI RESULTS:")
        print(f"Status: {'✅ Success' if gemini_result['success'] else '❌ Failed'}")
        if gemini_result['success']:
            print(f"Tokens: {gemini_result['usage']['input_tokens']} in, {gemini_result['usage']['output_tokens']} out")
            print(f"\n💬 Gemini's Response:")
            print("-" * 30)
            print(gemini_result['response_content'])
        else:
            print(f"Error: {gemini_result.get('error', 'Unknown error')}")

    print("\n" + "="*50)
    print("PARALLEL ANALYSIS COMPLETE")
    print("="*50)

if __name__ == "__main__":
    main()
