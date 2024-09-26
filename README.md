# LLM_playground
An educational playground for exploring and demonstrating various use cases and concepts of Large Language Models (LLMs). This repository provides examples of utilizing LLM APIs for different tasks, making it easier for developers to integrate LLMs into their projects.

## Installation

1. Clone the repository:
```sh
git clone https://github.com/marquezea/LLM_playground.git
```
2. Navigate to the project directory:
```sh
cd LLM_playground
```
3. Install the python libraries:
```sh
pip install -r requirements.txt
```

## Setting API Keys

This applications invokes LLM APIs from different providers. You must have API KEYs for all the services that you intend to use. The following API KEYs must be set as environment variables in your machine.

##### 1. Windows:
- Open Command Prompt or PowerShell.
- Use the following command to set the environment variable for the current session:
```sh
set OPENAI_API_KEY=<your api key>
set ANTHROPIC_API_KEY=<your api key>
set STABILITY_API_KEY=<your api key>
set LEONARDO_API_KEY=<your api key>
set GEMINI_API_KEY=<your api key>
set MISTRAL_API_KEY=<your api key>
set HFINF_API_KEY=<your api key>
set GROQ_API_KEY=<your api key>
```
- To make it persistent, add the variable to the system environment variables:
  - Search for "Environment Variables" in the start menu.
  - Click on "Edit the system environment variables."
  - In the System Properties window, click "Environment Variables."
  - Under "User variables" or "System variables," click "New" and add OPENAI_API_KEY as the name and your API key as the value.

##### 2. Linux:
- Open your terminal.
- Set the environment variable for the current session with:
```sh
export OPENAI_API_KEY=<your api key>
export ANTHROPIC_API_KEY=<your api key>
export STABILITY_API_KEY=<your api key>
export LEONARDO_API_KEY=<your api key>
export GEMINI_API_KEY=<your api key>
export MISTRAL_API_KEY=<your api key>
export HFINF_API_KEY=<your api key>
export GROQ_API_KEY=<your api key>
```
To make it permanent, add the following line to your shell configuration file (~/.bashrc, ~/.zshrc, etc.):
```sh
export OPENAI_API_KEY=<your api key>
export ANTHROPIC_API_KEY=<your api key>
export STABILITY_API_KEY=<your api key>
export LEONARDO_API_KEY=<your api key>
export GEMINI_API_KEY=<your api key>
export MISTRAL_API_KEY=<your api key>
export HFINF_API_KEY=<your api key>
export GROQ_API_KEY=<your api key>
```
- Save the file and run source ~/.bashrc (or the equivalent for your shell) to apply the changes.

##### 3. macOS:
- Open your terminal.
- Set the environment variable for the current session:
```sh
export OPENAI_API_KEY=<your api key>
export ANTHROPIC_API_KEY=<your api key>
export STABILITY_API_KEY=<your api key>
export LEONARDO_API_KEY=<your api key>
export GEMINI_API_KEY=<your api key>
export MISTRAL_API_KEY=<your api key>
export HFINF_API_KEY=<your api key>
export GROQ_API_KEY=<your api key>
```
- To make it permanent, add the following line to your shell configuration file (~/.bash_profile, ~/.zshrc, etc.):
```sh
export OPENAI_API_KEY=<your api key>
export ANTHROPIC_API_KEY=<your api key>
export STABILITY_API_KEY=<your api key>
export LEONARDO_API_KEY=<your api key>
export GEMINI_API_KEY=<your api key>
export MISTRAL_API_KEY=<your api key>
export HFINF_API_KEY=<your api key>
export GROQ_API_KEY=<your api key>
```
Save the file and run source ~/.bash_profile (or the equivalent for your shell) to apply the changes.


## Usage

To start the application use the following command:
```sh
streamlit run LLM_playground
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.


## Contact Information

Adriano Marqueze
adriano.marqueze@gmail.com