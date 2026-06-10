# Brug Agent
* Legally distinct grug AI agent
* Not secure for real world use, just MVP style
* Calculator folder is demo codebase for local testing
* Things I should extend this for:
    * Other Gemini models, Other LLM providers and local models(using ollama probably)
    * Giving it more functions to call
    * Other codebases (commit your changes before running the agent on a codebase, so you can always revert)

# Usage
* `uv run main.py "describe the task you want the agent to perform here"`
* `uv run main.py --verbose "describe the task you want the agent to perform here"` to see the process the agent is taking to complete its task

# Setup
* Clone repo from github and install the required packages from uv
* Add a .env file with `GEMINI_API_KEY='gemini_key_should_be_placed_here'`

# Configuration
* Read config.py file to see if all the value there are suitable for your use:
    * MAX_CHARS (for limiting agent from reading very large files)
    * WORKING_DIR (current working directory, agent can only operate on files in this directory)
    * MAX_ITERS (for limiting number of requests made to LLM provider for one)
