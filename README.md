# Company Research

A powerful tool for automated company analysis using OpenAI's GPT models and Tavily's search capabilities. This tool helps you analyze company websites and generate comprehensive reports about their business, features, and market positioning.

## Features

- 🔍 Automated website analysis
- 🤖 AI-powered insights using OpenAI's GPT models
- 🌐 Intelligent web search using Tavily
- 📊 Structured JSON output reports
- 🎯 Detailed competitor insights

## Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Tavily API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nano-deep-research.git
cd nano-deep-research
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your API keys:
```
KEY_OPENAI=your_openai_api_key_here
KEY_TAVILY=your_tavily_api_key_here
```

## Usage

1. Run the main script:
```bash
python main.py
```

2. Enter the website URL you want to analyze when prompted
3. Provide a brief description of the company
4. Wait for the analysis to complete
5. Find your results in the `output` directory as JSON files

## How it Works

The tool uses a combination of advanced AI technologies:

### OpenAI Agents
- Utilizes GPT models for natural language understanding and generation
- Performs deep analysis of website content and company information
- Generates structured insights about the companies business model, features, and market positioning

### Tavily Integration
- Leverages Tavily's powerful search API for comprehensive web research
- Gathers additional context and information about the company
- Validates and enriches the analysis with real-time web data

## Output Format

The analysis results are saved in JSON format in the `output` directory. Each analysis creates a new file named `company_analysis_[domain].json` containing structured information about:

- Company overview
- Key features and offerings
- Market positioning
- Competitive advantages
- Target audience
- Technology stack
- And more...

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

