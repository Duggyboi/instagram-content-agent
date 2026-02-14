# Streamlit MVP - Instagram Content Intelligence Agent

## Overview

This is a web-based interface for the Instagram Content Intelligence Agent, built with Streamlit. It provides an intuitive UI for uploading videos, running analysis, and viewing results.

## Features

### 📹 Upload & Analyze
- Upload Instagram videos (MP4, MOV, AVI, MKV, WebM)
- Configure which analysis steps to run:
  - 📝 Transcription: Extract dialogue and speech from video
  - 📋 Summary: Generate concise content summary
  - 🔍 Research: Find relevant sources and citations
  - 🏷️ Categorization: Tag content with relevant categories
  - 💡 Project Impact: Assess relevance to existing projects
- Configure LLM settings (model, temperature)
- Real-time analysis progress tracking

### 📊 View Results
- Browse all past analyses
- Quick preview of categorization and confidence scores
- Open detailed results for review

### 🕐 History
- View activity timeline
- Track analysis volume over time
- Export analysis history

### ⚙️ Settings
- Configure LLM provider (Ollama, OpenAI, Anthropic)
- Set storage locations
- Adjust analysis parameters
- Enable/disable features

## Getting Started

### Prerequisites
- Python 3.8+
- Virtual environment activated with dependencies installed
- Ollama running locally (if using Ollama as LLM provider)

### Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment** (optional):
   An `.env` file is provided with default settings. Customize as needed:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and preferences
   ```

### Running the App

#### Option 1: Using the batch file (Windows)
```bash
run_streamlit.bat
```

#### Option 2: Direct command
```bash
# Activate environment first
C:\Users\Keagan\anaconda3\envs\pm-agent\Scripts\activate.bat

# Run Streamlit
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

### Usage Workflow

1. **Navigate to "Upload & Analyze"**
   - Click the upload area and select a video file
   - Video preview will display automatically
   - Choose which analysis steps to run
   - Configure LLM settings (model, temperature)

2. **Start Analysis**
   - Click "🚀 Run Analysis" button
   - Monitor progress with the spinner
   - Results will appear in expandable sections

3. **Review Results**
   - **Transcription**: Full transcript of video audio
   - **Summary**: Key points and insights
   - **Research**: Related findings and useful links
   - **Categorization**: Content tags and confidence scores
   - **Project Impact**: Which projects are affected and actionable insights

4. **Export Results**
   - JSON: Machine-readable format
   - Markdown: For documentation and sharing
   - HTML: Standalone view-only report (coming soon)

5. **Track History**
   - Navigate to "History" tab to view all analyses
   - Search and filter past results
   - View statistics on analysis patterns

## Project Structure

```
instagram-content-agent/
├── streamlit_app.py           # Main Streamlit application
├── requirements.txt           # Python dependencies
├── run_streamlit.bat         # Windows startup script
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── src/
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── pipeline.py       # Core analysis pipeline
│   ├── config/
│   │   ├── __init__.py
│   │   └── app_config.py     # Configuration management
│   ├── utils/
│   │   ├── __init__.py
│   │   └── streamlit_utils.py # Helper functions
│   └── agents/               # Agent implementations (to be built)
├── results/                  # Saved analysis results
├── logs/                     # Application logs
├── temp_uploads/             # Temporary video storage
└── .env                      # Environment configuration
```

## Architecture

### Analysis Pipeline
The `AnalysisPipeline` class orchestrates the analysis workflow:

1. **Transcription**: Converts video audio to text
2. **Summary**: Extracts key points from transcription
3. **Research**: Finds relevant sources and citations
4. **Categorization**: Classifies content and assigns tags
5. **Impact Analysis**: Maps findings to existing projects

Each step is modular and can be skipped independently.

### Agents
Placeholder agent classes are included:
- `TranscriptionAgent`: Video to text conversion
- `SummaryAgent`: Text summarization
- `ResearchAgent`: Topic research
- `CategorizationAgent`: Content classification
- `ImpactAgent`: Project impact assessment

These should be extended with actual implementations using CrewAI.

## Demo Mode

The app runs in **demo mode** by default (agents not yet implemented). It shows:
- Full working UI with all features
- Mock analysis results for demonstration
- Realistic data flows and interactions

To enable real analysis:
1. Implement agent classes in `src/agents/`
2. Point `AnalysisPipeline` to actual agent implementations
3. Configure credentials in `.env`

## Configuration

### Via UI (Settings Tab)
- Select LLM provider
- Configure model selection
- Set storage locations
- Adjust analysis parameters

### Via File (src/config/app_config.py)
Configuration defaults are in `AppConfig` dataclass:
- `LLMConfig`: Model, provider, API keys
- `StorageConfig`: Directory locations, cleanup rules
- `AnalysisConfig`: Feature toggles, parameter limits

Configuration is auto-loaded from `~/.instagram_agent/config.json` if it exists.

## Troubleshooting

### App won't start
```bash
# Verify Streamlit is installed
pip show streamlit

# Check Python version
python --version

# Verify dependencies
pip install -r requirements.txt
```

### "Module not found" errors
```bash
# Ensure you're in the right directory
cd c:\Users\Keagan\projects\instagram-content-agent

# Verify environment is activated
python -c "import streamlit; print(streamlit.__version__)"
```

### Port already in use (error: Address already in use)
```bash
# Use a different port
streamlit run streamlit_app.py --server.port 8502
```

## Next Steps

### Phase 1: Streamlit UI ✅
- [x] Web interface created
- [x] Analysis pipeline skeleton
- [x] Demo mode for testing
- [x] Export functionality

### Phase 2: Agent Implementation
- [ ] Transcription agent (Whisper API)
- [ ] Summary agent (LLM-based)
- [ ] Research agent (Web search)
- [ ] Categorization agent (ML-based)
- [ ] Impact agent (Skill gap matching)

### Phase 3: Integration & Polish
- [ ] Connect real agents
- [ ] Add error handling
- [ ] Performance optimization
- [ ] User testing & feedback
- [ ] Production deployment

## Technology Stack

- **Framework**: Streamlit (web UI)
- **Agent Orchestration**: CrewAI
- **LLMs**: Ollama (local), OpenAI (cloud), Anthropic (alternative)
- **Video Processing**: OpenCV, moviepy
- **Data Export**: pandas, openpyxl
- **Configuration**: Pydantic
- **Logging**: Python json-logger

## Contributing

To extend the app:

1. **Add new analysis step**:
   - Create agent in `src/agents/`
   - Add to `AnalysisPipeline`
   - Add UI section in `streamlit_app.py`

2. **Add new export format**:
   - Create function in `src/utils/streamlit_utils.py`
   - Add button to export section in UI

3. **Modify configuration**:
   - Update dataclasses in `src/config/app_config.py`
   - Configuration is automatically loaded/saved

## License

Proprietary - Internal project

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs in `logs/` directory
3. Contact project owner: Keagan
