# Terminal LLM Utilities

I built simple terminal tools that let me ask cli-related questions and generate files in natural language—without having to leave the terminal.

## Tools

- **ask**: Get concise answers
- **create**: Generate files

## Installation

1. Install the required Python package:
   ```bash
   pip install google-genai
   ```

2. Set up your Gemini API key:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```
   Add this to your shell profile (~/.bashrc, ~/.zshrc, etc.) to make it permanent.

3. Make the CLI tool executable and move it to your system bin:
   ```bash
   chmod +x create.py
   sudo mv create.py /usr/local/bin/cli

   chmod +x ask.py
   sudo mv ask.py /usr/local/bin/cli
   ```

## Usage

### Ask Questions

Use the `ask` command to get quick answers:

```bash
ask how do i create a next project

npx create-next-app@latest

Follow the prompts to configure your project.

```

### Generate Files 

Use the `create` command to generate files with natural language instructions:

```bash
create "write a python script that prints hello world"
create "make an html template for a landing page"
```

## Requirements

- Python 3.8+
- llm api key (you can customize this to use any, used gemini since its free and quick)
- Unix-like environment (Linux/macOS)

## Project Structure

- `ask.py`: Question-answering interface
- `create.py`: File generation interface 
- `client.py`: LLM client configuration

## Next Steps

- Currently exploring MCP, and how it can be applied to this project to safely read and write documents directly.

## License

MIT License