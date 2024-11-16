# AI Web Research Assistant 🔍

An intelligent web research tool that combines web scraping, AI-powered analysis, and structured data processing to automate research tasks. Built with Streamlit, this application allows users to process bulk queries, perform web searches, and generate AI-enhanced analysis reports.

## 🌟 Features

- **Bulk Data Processing**: Upload CSV files containing multiple research queries
- **Automated Web Search**: Utilizes DuckDuckGo for gathering recent information
- **AI-Powered Analysis**: Leverages Groq's Mixtral-8x7b model for intelligent information extraction
- **Structured Output**: Generates organized reports in both JSON and CSV formats
- **Interactive Dashboard**: User-friendly Streamlit interface with progress tracking
- **Customizable Search Templates**: Flexible query formatting for different use cases

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-web-research-assistant.git
cd ai-web-research-assistant
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Environment Setup

1. Create a `.env` file in the project root directory
2. Add your API keys and configurations:
```env
GROQ_API_KEY=your_groq_api_key_here
```

## 📊 Usage Guide

### Starting the Application

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically `http://localhost:8501`)

### Using the Dashboard

1. **Upload Data**:
   - Prepare a CSV file with your research queries
   - Click "Upload your dataset (CSV)" and select your file
   - Preview your data in the dashboard

2. **Configure Search**:
   - Select the column containing your search queries
   - Customize the search template using the `{entity}` placeholder
   - Example template: "Latest developments and news about {entity}"

3. **Run Analysis**:
   - Click "Start Analysis" to begin processing
   - Monitor progress through the progress bar
   - View results in either Summary or Detailed view

4. **Export Results**:
   - Download results in CSV format for spreadsheet analysis
   - Download results in JSON format for structured data processing

## 🔑 API Keys and Environment Variables

### Required API Keys

1. **Groq API Key**:
   - Sign up at [Groq's website](https://www.groq.com)
   - Generate an API key from your dashboard
   - Add to `.env` file as `GROQ_API_KEY`

## 📦 Dependencies

- `streamlit`: Web application framework
- `pandas`: Data processing and analysis
- `requests`: HTTP requests for web scraping
- `beautifulsoup4`: HTML parsing
- `groq`: Groq API client
- `python-dotenv`: Environment variable management

## ⚠️ Rate Limiting and Performance Notes

- The application includes a 2-second delay between requests to prevent rate limiting
- Processing time depends on the number of entries and API response times
- Large datasets may take several minutes to process

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Bug Reports

If you discover any bugs, please create an issue in the GitHub repository including:
- Detailed description of the problem
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)

## 🎥 Project Walkthrough

Watch a brief demonstration of the AI Web Research Assistant in action:

[Project Demo Video](https://www.loom.com/share/c595ae32c805420ea65f2972cf221426?sid=6da40b5e-8158-4266-9b30-5d96c60e3512)

In this video, you'll learn:
- Overview of project purpose and capabilities
- Live demonstration of the dashboard
- Technical implementation highlights
- Key challenges and solutions

The video provides a quick way to understand the project's functionality and get started with your own research tasks.
