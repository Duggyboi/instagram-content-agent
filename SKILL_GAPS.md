# Instagram Content Intelligence Agent - Skill Gaps

This file documents the specific skills and capabilities needed for the Instagram Content Intelligence Agent project. These represent gaps in the agentic-infrastructure-framework that this project will need to fill.

## Critical Skills (Must Build)

### 1. Instagram Integration Skill ⭐
**Purpose**: Connect to Instagram API and receive videos
- Authenticate with Instagram Business Account
- Fetch videos from direct messages
- Handle webhook events for new videos
- Manage rate limiting and errors
- Extract video metadata (URL, timestamp, sender)

**Status**: Not Started
**Estimated Effort**: 3-4 days
**Dependencies**: Instagram Business Account, valid API credentials
**Success Criteria**: Can authenticate and receive test video within 5 attempts

---

### 2. Video Transcription Skill ⭐
**Purpose**: Convert video audio to text transcriptions
- Download video files from Instagram
- Extract audio from video file
- Transcribe using Whisper API (or local model)
- Handle audio quality issues gracefully
- Return formatted transcript text

**Status**: Not Started
**Estimated Effort**: 3-4 days
**Dependencies**: Whisper API key OR local transcription model
**Success Criteria**: Produce 95%+ accurate transcripts on clear audio
**Cost Consideration**: Whisper API ~$0.02 per minute vs local (free but slower)

---

### 3. Content Brief Generator Skill ⭐
**Purpose**: Create concise summaries of video content
- Parse transcription text
- Extract key concepts and main points
- Synthesize into 150-250 word brief
- Highlight technical/actionable insights
- Format as structured brief with bullets

**Status**: Not Started
**Estimated Effort**: 2-3 days
**Dependencies**: Transcription skill  
**Success Criteria**: Generates 150-250 word summaries that capture video essence

---

### 4. Research & Link Discovery Skill ⭐
**Purpose**: Find high-quality resources for video topics
- Perform web searches for topic
- Filter for high-quality authoritative sources
- Validate links are still accessible  
- Extract metadata (title, description)
- Return top 5 most relevant links

**Status**: Not Started
**Estimated Effort**: 3-4 days
**Dependencies**: Search API (Google Custom Search, SerpAPI, or DuckDuckGo API)
**Success Criteria**: Find 5+ high-quality links per topic in under 30 seconds
**Cost Consideration**: Some APIs require payment; explore free tiers

---

### 5. Topic Categorizer Skill ⭐
**Purpose**: Classify videos into predefined categories
- Analyze brief and transcription
- Assign primary and secondary categories
- Provide confidence score (0-100%)
- Allow multiple category assignment

**Predefined Categories**:
- AI/ML Fundamentals
- LLM Models (Claude, GPT, Llama, etc.)
- Context Management Techniques
- Claude Features & Updates
- UI/UX Design Patterns
- Prompt Engineering
- Vector Databases & RAG
- Multi-Agent Systems
- Tools & Frameworks
- Developer Productivity
- Other / Uncategorized

**Status**: Not Started
**Estimated Effort**: 2-3 days
**Dependencies**: None (pure LLM reasoning)
**Success Criteria**: Correctly categorize 90%+ of test videos

---

### 6. Project Matcher Skill ⭐
**Purpose**: Cross-reference with existing projects' needs
- Load SKILL_GAPS.md from other projects (agentic-infrastructure-framework, pricewize-prd, etc.)
- Parse skill gap data
- Match video categories to project needs
- Rank projects by relevance
- Generate impact summary

**Status**: Not Started
**Estimated Effort**: 2-3 days
**Dependencies**: Access to other projects' SKILL_GAPS.md files
**Success Criteria**: Identify relevant projects with 80%+ accuracy
**Example Output**: 
  ```
  This video would benefit:
  1. agentic-infrastructure-framework (Agent Communication gap)
  2. pricewize-prd (LLM Integration gap)
  ```

---

### 7. Result Delivery Skill ⭐
**Purpose**: Send analysis back to user
- Format complete analysis report (transcript, brief, categories, links, matched projects)
- Deliver via Instagram DM
- Include metadata and formatting
- Handle delivery errors gracefully
- Log delivery status

**Status**: Not Started
**Estimated Effort**: 1-2 days
**Dependencies**: Instagram skill for sending messages
**Success Criteria**: Deliver formatted analysis within 5 minutes of completion

---

## Important Skills (Nice to Have)

### 8. Video Quality Assessment Skill
**Purpose**: Evaluate video quality before processing
- Check audio quality
- Detect language
- Assess relevance (is this actually about AI/tech?)
- Provide quality score
- Skip low-quality videos

**Status**: Not Started
**Estimated Effort**: 2 days
**Priority**: After MVP is working

---

### 9. Caching/Deduplication Skill
**Purpose**: Avoid reprocessing and research duplication
- Detect duplicate or similar videos
- Cache transcriptions and research results
- Retrieve cached results when available
- Prevent duplicate link searches

**Status**: Not Started
**Estimated Effort**: 1-2 days
**Priority**: After MVP, for efficiency
**Benefit**: Reduce API costs and processing time

---

## Agents That Will Use These Skills

```
📱 Main Orchestrator
├─ Receives video from Instagram
├─ Distributes to specialized agents
└─ Aggregates results

📝 Content Analysis Agent
├─ Instagram Integration skill
├─ Transcription skill
└─ Brief Generator skill

🔍 Research Agent
├─ Research & Link Discovery skill
└─ Logging skill

🏷️  Categorization Agent
├─ Topic Categorizer skill
├─ Project Matcher skill
└─ Logging skill

📤 Delivery Agent
├─ Result Delivery skill
└─ Instagram Integration skill
```

---

## Development Timeline

### Phase 1: Core Skills (Weeks 1-3)
- [ ] Instagram Integration - 3-4 days
- [ ] Video Transcription - 3-4 days
- [ ] Content Brief Generator - 2-3 days

### Phase 2: Intelligence Skills (Weeks 3-4)
- [ ] Research & Link Discovery - 3-4 days
- [ ] Topic Categorizer - 2-3 days
- [ ] Project Matcher - 2-3 days

### Phase 3: Agent Orchestration (Week 4)
- [ ] Agent architecture design - 2 days
- [ ] Result Delivery - 1-2 days
- [ ] End-to-end integration - 2-3 days

### Testing & Refinement (Week 4-5)
- [ ] MVP testing
- [ ] Accuracy improvements
- [ ] Cost optimization

---

## External Dependencies to Resolve

### Instagram API
- [ ] Business Account created
- [ ] API access approved
- [ ] Webhook configured
- [ ] Test credentials working

### Transcription Service
- [ ] **Option A**: Whisper API credentials
- [ ] **Option B**: Local model setup (ffmpeg + model)
- [ ] Test with sample video

### Search API
- [ ] **Option A**: Google Custom Search API key
- [ ] **Option B**: SerpAPI key
- [ ] **Option C**: DuckDuckGo free API
- [ ] Test searches working

### Data Access
- [ ] Access to other projects' SKILL_GAPS.md files
- [ ] Git setup for reading other project files
- [ ] Fallback if projects not available

---

## Success Metrics

| Skill | Metric | Target |
|-------|--------|--------|
| Instagram Integration | Auth success rate | 100% |
| Transcription | Accuracy on clear  audio | >95% |
| Brief Generator | Brief completeness | 150-250 words |
| Research Skill | Links found per topic | 5+ in <30s |
| Categorizer | Category accuracy | ≥90% |
| Project Matcher | Relevant matches | ≥80% accuracy |
| Delivery | Result delivery time | <5 minutes |
| **Overall** | End-to-end processing | <10 min per video |

---

## Estimated Cost & Resource Usage

### API Costs (Monthly, ~20 videos/month)
- Whisper API: ~$0.40/month (if using)
- Search API: Likely free tier sufficient
- Instagram API: Free
- **Total**: ~$0.50-1.00/month (minimal)

### Computation Resources  
- Video processing: 2-3 minutes per video
- Llama 2 13B inference: Runs locally (free)
- Storage: ~100MB per month

### Recommendations
1. Use **local transcription** if possible (free but slower)
2. Use **free search API** (DuckDuckGo or basic tier)
3. Cache heavily to avoid repeat searches
4. Monitor costs first month to validate estimates

---

Last Updated: 2026-02-14
Next Review: Once Phase 1 starts
