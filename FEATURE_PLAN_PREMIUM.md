# Premium Analysis Agents - Feature Plan

## Branch
`feature/premium-analysis-agents` 

## Overview
Implementing real analysis capabilities replacing placeholder/demo agents. This feature transforms the Streamlit MVP from a functional UI prototype into a fully operational video analysis system.

## Core Components

### 1. ✅ Local Whisper Transcription
**Purpose**: Extract audio from video and convert to text with timestamps (no API costs)

**Implementation**:
- Install `openai-whisper` package (handles audio extraction internally)
- Create `TranscriptionAgent` with real implementation
- Support video formats: mp4, mov, avi, mkv, webm
- Return: Full transcript with optional timestamps
- Error handling: Graceful fallback for unsupported audio codecs

**Files to modify**:
- `src/analysis/agents/transcription_agent.py` (NEW)
- `src/analysis/pipeline.py` (wire up agent)
- `requirements.txt` (add openai-whisper)

**Testing**:
- Test with downloaded Instagram reels
- Test with uploaded video files
- Verify timestamp accuracy

---

### 2. 🌐 Advanced Web Research Agent
**Purpose**: Search for related topics/people mentioned in transcription; find sources and links

**Implementation**:
- Use `requests` + BeautifulSoup or `duckduckgo-search` library (no API key needed) 
- Parse transcription to extract key topics/hashtags
- Perform 3-5 targeted searches
- Return: List of sources with titles, URLs, brief descriptions
- De-duplication to avoid redundant results

**Web Access**: Uses free search engines (DuckDuckGo or basic Google search)
- No authentication required
- No API rate limiting concerns for small projects
- Respects robots.txt

**Files to modify**:
- `src/analysis/agents/research_agent.py` (NEW)
- `src/analysis/pipeline.py` (wire up agent)
- `requirements.txt` (add requests, beautifulsoup4, duckduckgo-search)

**Output Format**:
```python
{
    "findings": [
        {
            "title": "Source Title",
            "url": "https://example.com",
            "snippet": "Brief description...",
            "relevance": 0.95
        }
    ],
    "search_terms_used": ["topic1", "topic2"]
}
```

---

### 3. 🏷️ ML-Based Categorization Agent
**Purpose**: Classify video content and assign relevant tags

**Implementation**:
- Use pre-trained Hugging Face transformers model (zero-shot classification)
- Classify into categories: Educational, Entertainment, News, Tutorial, etc.
- Extract hashtags from transcription
- Assign confidence scores (0-100)
- Return: Categories + tags + confidence levels

**Files to modify**:
- `src/analysis/agents/categorization_agent.py` (NEW)
- `src/analysis/pipeline.py` (wire up agent)
- `requirements.txt` (add transformers, torch)

**Output Format**:
```python
{
    "categories": [
        {"name": "Educational", "confidence": 95},
        {"name": "Tutorial", "confidence": 78}
    ],
    "tags": ["python", "coding", "open-source"],
    "primary_category": "Educational"
}
```

---

### 4. 🎯 Skill Gap Matching Agent
**Purpose**: Link video content to project skill gaps and recommend which projects benefit

**Implementation**:
- Load `project_brief.md` from agentic-infrastructure-framework
- Extract skill gaps from `.project/SKILL_GAPS.md`
- Compare video topics against skill list
- Calculate relevance score per project
- Return: List of affected projects with % matching and suggested learning path

**Files to modify**:
- `src/analysis/agents/matching_agent.py` (NEW)
- `src/analysis/pipeline.py` (wire up agent)
- `src/utils/project_loader.py` (NEW - load external project brief)

**Output Format**:
```python
{
    "matched_projects": [
        {
            "project_name": "Project Name",
            "skill_gaps": ["Skill1", "Skill2"],
            "relevance": 85,
            "learning_path": "Resource explains Skill1 and Skill2"
        }
    ]
}
```

---

### 5. 🧠 Summary Agent (via Ollama)
**Purpose**: Generate high-quality summaries using local LLM

**Implementation**:
- Wire `SummaryAgent` to use Ollama (`llama2:13b`)
- Input: Full transcription
- Output: Concise summary (2-3 sentences) + key takeaways (5-7 bullets)
- Prompt engineering for quality summaries

**Files to modify**:
- `src/analysis/agents/summary_agent.py` (wire up Ollama)
- `src/analysis/ollama_integration.py` (NEW)

**Note**: User prefers to pass detailed docs to other agents rather than multi-LLM setup

---

## Timeline & Dependencies

### Phase 1: Audio Transcription (30-45 min)
- [ ] Install openai-whisper
- [ ] Implement TranscriptionAgent
- [ ] Test with real videos
- [ ] Handle errors gracefully

### Phase 2: Research & Categorization (40-50 min)
- [ ] Implement ResearchAgent with web search
- [ ] Implement CategorizationAgent with ML model
- [ ] Wire both into pipeline
- [ ] Test with various content types

### Phase 3: Skill Matching & Summary (30-40 min)
- [ ] Load project brief system
- [ ] Implement MatchingAgent
- [ ] Wire up Ollama summarization
- [ ] Full end-to-end testing

### Total Time: 1.5-2.5 hours

---

## Technical Decisions

**Web Access**: Using free DuckDuckGo API
- ✅ No authentication
- ✅ No rate limiting for small projects
- ✅ Respects robots.txt
- ✅ No costs

**Transcription**: Local Whisper
- ✅ No API costs or rate limits
- ✅ Works completely offline
- ✅ Fast for typical video lengths
- ✅ Handles multiple audio codecs

**ML Models**: Pre-trained Hugging Face
- ✅ Zero-shot classification (no training needed)
- ✅ Works offline
- ✅ Fast inference on CPU
- ✅ Supports custom categories

**Summary Generation**: Ollama (local)
- ✅ Already running on system
- ✅ No API costs
- ✅ Low latency
- ✅ Portable

---

## Testing Strategy

1. **Unit Tests**: Each agent in isolation
2. **Integration Tests**: Full pipeline with real video
3. **UI Tests**: Streamlit interface displays results correctly
4. **Error Handling**: Graceful fallbacks when components fail

---

## Known Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Whisper slow on large videos | Implement timeout, show progress bar |
| Web search Rate-limited | Use cached results, implement backoff |
| ML Model download size | Pre-download on first run, show status |
| Memory usage high | Offload models after use, test on target system |

---

## Success Criteria

- ✅ Real transcription output (not placeholder text)
- ✅ Web research returns actual URLs with descriptions
- ✅ Categorization assigns relevant tags with confidence scores
- ✅ Skill matching correctly identifies affected projects
- ✅ All 5 result sections display real data (not placeholders)
- ✅ E2E test with real Instagram video succeeds
