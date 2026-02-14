# Instagram Content Intelligence Agent - Project Brief

## 1. Problem Statement

As a busy professional working on multiple AI projects, Keagan encounters valuable short-form video content on Instagram related to AI tools, models, and services. However, he lacks the time to thoroughly investigate these videos and extract actionable insights. This leads to missed opportunities to discover improvements or new features that could benefit ongoing projects.

**The Challenge**: Manually reviewing, transcribing, researching, and categorizing Instagram videos is time-prohibitive while the potential value is high.

## 2. Target Users

- **Primary**: Keagan (project developer and decision-maker)
- **Secondary**: Team members working on Keagan's projects who need to understand how discovered improvements apply to their work

## 3. Desired Outcomes

After implementing this project, the user should be able to:

1. Send Instagram videos to a dedicated agent profile
2. Receive automated analysis including:
   - Full video transcription
   - Comprehensive brief summary
   - In-depth research/investigation of the topic
   - Curated links for further reading
   - Topic categorization (AI/ML, context management, Claude features, UI/UX design, etc.)
   - Project impact assessment (which existing projects would benefit)
3. Make informed decisions about investigating topics further based on automated summaries
4. Track which improvements match existing project skill gaps
5. Reduce time spent on manual content research from hours to minutes

## 4. Success Metrics

- **Efficiency**: Time to resolve one Instagram video from hours → 5-10 minutes of analysis time
- **Quality**: Video transcriptions are >95% accurate
- **Relevance**: Categorization correctly matches video topics to project improvement areas ≥90% of the time
- **Coverage**: Agent successfully processes and analyzes 95%+ of received videos
- **Impact**: Insights from analyzed videos result in at least 2-3 actionable improvements for projects per month
- **Usability**: User can send a video via Instagram and receive analysis within 5 minutes

## 5. Scope & Features

### In Scope
- Instagram API integration (read-only access for agent profiles)
- Video transcription (via Whisper API or similar)
- Topic extraction and categorization
- Brief summary generation
- Research and link discovery for topics
- Skill gap matching against existing projects
- Analysis delivery back via Instagram DM or email
- Support for multiple video formats/quality

### Out of Scope
- Video editing or enhancement
- Creating new content based on videos
- Real-time video monitoring (batch processing is fine)
- Building a video database/archive (though optional logging)
- Multi-language support (English videos only initially)

## 6. Constraints & Requirements

### Technical Constraints
- Must work with Instagram's current API limitations (cost-effective approach)
- Transcription quality dependent on audio quality
- Research phase limited to reliable sources (avoid misinformation)
- Rate limiting on Instagram API calls

### Budget Constraints
- Minimize API costs (prefer free/low-cost services where possible)
- Whisper API or free alternatives for transcription
- Free or low-cost research tools

### Timeline
- Initial MVP: 4-6 weeks
- Milestone 1 (2 weeks): Instagram integration + transcription
- Milestone 2 (2 weeks): Brief generation + categorization
- Milestone 3 (2 weeks): Research engine + project matching

### Team/Skill Constraints
- One developer (Keagan)
- Access to existing agentic infrastructure framework
- Knowledge of CrewAI agents and project structure

## 7. Dependencies

- LinkedIn/Twitter/news APIs for research (assuming Instagram provides basic video metadata)
- Working Instagram Business Account for agent profile
- Whisper API or similar transcription service
- Access to existing project skill gap documentation
- Existing project structure with skill gaps files in place

## 8. Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| Instagram API changes limit functionality | High | Medium | Build abstraction layer, monitor API docs closely |
| Poor transcription quality on noisy videos | Medium | High | Implement quality checks, fall back to manual review option |
| Inaccurate categorization/matching | Medium | Medium | Create categorization rubric, fine-tune with examples |
| High API costs for transcription/research | High | Medium | Test with free tier first, implement caching |
| Difficulty matching to skill gaps | Medium | Medium | Build flexible matcher, allow manual adjustment |
| Instagram bot detection/blocks | High | Low | Use official API, implement responsible usage patterns |

## 9. Assumptions

- Instagram will allow a bot account with proper API credentials
- Video transcription accuracy will be 90%+ for clear audio
- Existing project skill gaps are well-documented
- User wants analysis delivered via Instagram DM or email (not both)
- Video volume is moderate (5-20 videos per week)

## 10. Next Steps

1. **Phase 2**: Decompose into specific agents and components
   - Content Analyzer Agent
   - Researcher Agent
   - Categorizer Agent
   - Project Matcher Agent

2. **Phase 3**: Define technical architecture
   - Agent structure
   - Required skills
   - Integration points
   - Data flow

3. **Implementation**: Build and test each component
