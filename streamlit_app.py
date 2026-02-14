"""
Instagram Content Intelligence Agent - Streamlit Web Interface
Main application entry point for the web UI.
"""

import streamlit as st
from streamlit_option_menu import option_menu
import os
from pathlib import Path
import json
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Instagram Content Intelligence Agent",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 2rem;
        }
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .status-processing {
            background-color: #fff3cd;
            color: #856404;
        }
        .status-complete {
            background-color: #d4edda;
            color: #155724;
        }
        .status-error {
            background-color: #f8d7da;
            color: #721c24;
        }
        .result-card {
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
            background-color: #f8f9fa;
            margin-bottom: 1rem;
        }
        .result-card.transcription {
            border-left-color: #ff7f0e;
        }
        .result-card.summary {
            border-left-color: #2ca02c;
        }
        .result-card.research {
            border-left-color: #d62728;
        }
        .result-card.categorization {
            border-left-color: #9467bd;
        }
        .result-card.impact {
            border-left-color: #8c564b;
        }
        .result-card.validation {
            border-left-color: #17a2b8;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "analysis_in_progress" not in st.session_state:
    st.session_state.analysis_in_progress = False

# Sidebar
with st.sidebar:
    st.markdown("### 🎬 Instagram Content Agent")
    st.divider()
    
    # Navigation
    selected = option_menu(
        menu_title=None,
        options=["Upload & Analyze", "View Results", "History", "Settings"],
        icons=["upload", "chart-bar", "clock-history", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "icon": {"font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
        }
    )
    
    st.divider()
    st.markdown("""
    ### About
    Automated analysis of Instagram videos:
    - 📝 Transcription
    - 📋 Summaries
    - 🔍 Research
    - 🏷️ Categorization
    - 💡 Project Impact
    """)

# Main content
if selected == "Upload & Analyze":
    st.markdown('<div class="main-header">🎬 Upload & Analyze</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Upload an Instagram video for automated analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📹 Video Input")
        
        # Tabs for file upload vs URL input
        tab_file, tab_url = st.tabs(["📂 Upload File", "🔗 Download from URL"])
        
        with tab_file:
            uploaded_file = st.file_uploader(
                "Upload a video file",
                type=["mp4", "mov", "avi", "mkv", "webm"],
                help="Supported formats: MP4, MOV, AVI, MKV, WebM"
            )
            
            if uploaded_file is not None:
                st.session_state.uploaded_file = uploaded_file
                
                # Display video preview
                st.video(uploaded_file)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.info(f"**File:** {uploaded_file.name}")
                    st.info(f"**Size:** {uploaded_file.size / 1024 / 1024:.2f} MB")
                with col_b:
                    st.info(f"**Type:** {uploaded_file.type}")
                    st.info(f"**Uploaded:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        with tab_url:
            st.markdown("**Download from**:")
            st.markdown("- 🎥 YouTube videos")
            st.markdown("- 📱 Instagram videos, reels, posts")
            st.markdown("- 🎵 TikTok videos")
            st.markdown("- 🔗 Direct video URLs (MP4, WebM, etc.)")
            
            url_input = st.text_input(
                "Paste video URL:",
                placeholder="https://youtube.com/watch?v=... or https://instagram.com/reel/...",
                help="Paste a complete video URL",
                key="video_url_input"
            )
            
            if url_input:
                # Detect URL type
                from src.utils.video_downloader import VideoDownloader
                url_type = VideoDownloader.detect_url_type(url_input)
                
                # Show URL info
                col_url_a, col_url_b = st.columns([2, 1])
                with col_url_a:
                    if url_type == "unknown":
                        st.warning("⚠️ Unknown URL format")
                    else:
                        icon_map = {
                            "youtube": "🎥",
                            "instagram": "📱",
                            "tiktok": "🎵",
                            "direct": "🔗"
                        }
                        st.info(f"✓ {icon_map.get(url_type, '?')} {url_type.capitalize()} detected")
                with col_url_b:
                    if st.button("⬇️ Download", key="download_button", use_container_width=True):
                        download_placeholder = st.empty()
                        
                        def update_progress(msg: str):
                            download_placeholder.info(msg)
                        
                        downloader = VideoDownloader()
                        success, message, file_path = downloader.download(url_input, update_progress)
                        
                        if success:
                            download_placeholder.success(f"✓ {message}")
                            # Store the file path directly in session state
                            st.session_state.uploaded_file = {
                                'name': Path(file_path).name,
                                'size': Path(file_path).stat().st_size,
                                'type': 'video/' + Path(file_path).suffix.lstrip('.'),
                                'path': file_path,  # Store the actual file path
                                'is_downloaded': True
                            }
                            
                            # Display video preview
                            with open(file_path, "rb") as f:
                                video_bytes = f.read()
                            st.video(video_bytes)
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.info(f"**File:** {Path(file_path).name}")
                                st.info(f"**Size:** {Path(file_path).stat().st_size / 1024 / 1024:.2f} MB")
                            with col_b:
                                st.info(f"**Type:** video/{Path(file_path).suffix.lstrip('.')}")
                                st.info(f"**Downloaded:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        else:
                            download_placeholder.error(f"❌ {message}")
    
    with col2:
        st.subheader("⚙️ Analysis Options")
        
        st.markdown("**Enable Analysis Steps:**")
        enable_transcription = st.checkbox("📝 Transcription", value=True)
        enable_summary = st.checkbox("📋 Summary", value=True)
        enable_research = st.checkbox("🔍 Research", value=True)
        enable_categorization = st.checkbox("🏷️ Categorization", value=True)
        enable_proofreading = st.checkbox("✅ Quality Validation (Ollama)", value=False, help="Requires Ollama running - disabled by default")
        enable_impact = st.checkbox("💡 Project Impact", value=True)
        
        st.divider()
        
        st.markdown("**LLM Settings:**")
        llm_model = st.selectbox(
            "Model",
            ["ollama:llama2:13b", "openai:gpt-4", "openai:gpt-3.5-turbo"],
            help="Select the LLM to use for analysis"
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher = more creative, Lower = more deterministic"
        )
    
    st.divider()
    
    # Analysis pipeline
    if st.session_state.uploaded_file is not None:
        col_analyze, col_clear = st.columns([4, 1])
        
        with col_analyze:
            if st.button("🚀 Run Analysis", key="analyze_button", use_container_width=True):
                st.session_state.analysis_in_progress = True
                
                # Create progress placeholder
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Create analysis configuration
                analysis_config = {
                    "steps": {
                        "transcription": enable_transcription,
                        "summary": enable_summary,
                        "research": enable_research,
                        "categorization": enable_categorization,
                        "proofreading": enable_proofreading,
                        "impact": enable_impact
                    },
                    "llm_model": llm_model,
                    "temperature": temperature,
                    "ollama_host": "http://localhost:11434",
                    "ollama_model": "mistral",
                    "file_name": st.session_state.uploaded_file['name'] if isinstance(st.session_state.uploaded_file, dict) else st.session_state.uploaded_file.name,
                    "timestamp": datetime.now().isoformat()
                }
                
                try:
                    # Import analysis module
                    from src.analysis.pipeline import AnalysisPipeline
                    
                    # Determine file path
                    if isinstance(st.session_state.uploaded_file, dict) and st.session_state.uploaded_file.get('is_downloaded'):
                        # Downloaded video - use existing path
                        file_path = st.session_state.uploaded_file['path']
                    else:
                        # Uploaded file - save temporarily
                        temp_dir = Path("temp_uploads")
                        temp_dir.mkdir(exist_ok=True)
                        file_path = temp_dir / st.session_state.uploaded_file.name
                        
                        with open(file_path, "wb") as f:
                            f.write(st.session_state.uploaded_file.getbuffer())
                    
                    # Update progress
                    status_text.info("📝 Transcribing audio...")
                    progress_bar.progress(20)
                    
                    # Run pipeline
                    pipeline = AnalysisPipeline(config=analysis_config)
                    results = pipeline.run(str(file_path))
                    
                    st.session_state.analysis_results = results
                    st.session_state.analysis_in_progress = False
                    
                    # Final progress
                    status_text.empty()
                    progress_bar.progress(100)
                    st.markdown('<div style="background:#D4EDDA; padding:12px; border-radius:8px; border-left:4px solid #28A745;"><b>✅ Analysis Complete!</b> Results are ready below.</div>', unsafe_allow_html=True)
                    
                    import time
                    time.sleep(1)
                    progress_bar.empty()
                    
                except ImportError:
                    # Fallback: Create mock results for demonstration
                    status_text.empty()
                    progress_bar.progress(100)
                    st.markdown('<div style="background:#FFF3CD; padding:12px; border-radius:8px; border-left:4px solid #FFC107;"><b>⚠️ Demo Mode</b> Running with sample analysis.</div>', unsafe_allow_html=True)
                    file_name = st.session_state.uploaded_file['name'] if isinstance(st.session_state.uploaded_file, dict) else st.session_state.uploaded_file.name
                    st.session_state.analysis_results = create_demo_results(
                        file_name,
                        analysis_config
                    )
                    st.session_state.analysis_in_progress = False
                    import time
                    time.sleep(1)
                    progress_bar.empty()
                except Exception as e:
                    status_text.empty()
                    progress_bar.empty()
                    st.markdown(f'<div style="background:#F8D7DA; padding:12px; border-radius:8px; border-left:4px solid #DC3545;"><b>❌ Analysis Failed</b><br/>{str(e)}</div>', unsafe_allow_html=True)
                    st.session_state.analysis_in_progress = False
        
        with col_clear:
            if st.button("🗑️ Clear", key="clear_button", use_container_width=True):
                st.session_state.uploaded_file = None
                st.session_state.analysis_results = None
                st.rerun()
    
    # Display results if available
    if st.session_state.analysis_results is not None:
        st.divider()
        st.subheader("📊 Analysis Results")
        
        results = st.session_state.analysis_results
        
        if "transcription" in results and results["transcription"]:
            with st.expander("📝 Transcription", expanded=True):
                st.markdown('<div class="result-card transcription">', unsafe_allow_html=True)
                st.text_area(
                    "Transcribed Text",
                    value=results["transcription"],
                    height=200,
                    disabled=True,
                    label_visibility="collapsed"
                )
                st.markdown('</div>', unsafe_allow_html=True)
        
        if "summary" in results and results["summary"]:
            with st.expander("📋 Summary", expanded=True):
                st.markdown('<div class="result-card summary">', unsafe_allow_html=True)
                
                # Extract summary text and key takeaways
                summary_data = results["summary"]
                summary_text = summary_data.get("summary", "") if isinstance(summary_data, dict) else summary_data
                key_takeaways = summary_data.get("key_takeaways", []) if isinstance(summary_data, dict) else []
                
                # Display main summary
                if summary_text:
                    st.markdown("### 📄 Summary")
                    st.markdown(f"> {summary_text}")
                
                # Display key takeaways
                if key_takeaways:
                    st.markdown("### 🎯 Key Takeaways")
                    for idx, takeaway in enumerate(key_takeaways, 1):
                        st.markdown(f"{idx}. {takeaway}")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        if "research" in results and results["research"]:
            with st.expander("🔍 Research Findings", expanded=True):
                st.markdown('<div class="result-card research">', unsafe_allow_html=True)
                
                research_data = results["research"]
                
                # Display extracted topics
                topics = research_data.get("topics_extracted", [])
                if topics:
                    st.markdown("### 🏷️ Topics Identified")
                    topic_badges = " • ".join([f"`{topic}`" for topic in topics])
                    st.markdown(topic_badges)
                
                # Display findings
                findings = research_data.get("findings", [])
                if findings:
                    st.markdown("### 📌 Key Findings")
                    for idx, finding in enumerate(findings, 1):
                        st.markdown(f"**{idx}.** {finding}")
                
                # Display search terms used
                search_terms = research_data.get("search_terms_used", [])
                if search_terms:
                    st.markdown("### 🔎 Search Terms Used")
                    terms_str = ", ".join([f"`{term}`" for term in search_terms])
                    st.markdown(terms_str)
                
                if research_data.get("links"):
                    st.markdown("### 🔗 Useful Links")
                    for link in research_data["links"]:
                        st.markdown(f"- [{link['title']}]({link['url']})")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        if "categorization" in results and results["categorization"]:
            with st.expander("🏷️ Categorization", expanded=True):
                st.markdown('<div class="result-card categorization">', unsafe_allow_html=True)
                
                cat = results["categorization"]
                
                # Display primary category prominently
                primary = cat.get("primary_category")
                categories = cat.get("categories", [])
                
                if primary:
                    st.markdown(f"## 🎯 Primary Category: **{primary}**")
                
                # Display category confidence bars
                if categories:
                    st.markdown("### 📊 Category Confidence Scores")
                    for item in categories[:5]:  # Top 5
                        cat_name = item.get("name", "Unknown")
                        confidence = item.get("confidence", 0)
                        st.metric(cat_name, f"{confidence}%")
                
                # Display tags
                tags = cat.get("tags", [])
                if tags:
                    st.markdown("### 🏷️ Tags")
                    tag_chips = " ".join([f"<span style='display:inline-block; background:#E8F4F8; padding:6px 12px; border-radius:20px; margin:2px; font-size:0.9em;'>{tag}</span>" for tag in tags])
                    st.markdown(f"<div style='margin-top:10px;'>{tag_chips}</div>", unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        if "impact" in results and results["impact"]:
            with st.expander("💡 Project Impact", expanded=True):
                st.markdown('<div class="result-card impact">', unsafe_allow_html=True)
                impact = results["impact"]
                
                if impact.get("affected_projects"):
                    st.markdown("**Affected Projects:**")
                    for project in impact["affected_projects"]:
                        st.markdown(f"- **{project['name']}** ({project['impact_level']} impact)")
                        if project.get("skill_gaps"):
                            st.markdown(f"  - Skill gaps addressed: {', '.join(project['skill_gaps'][:3])}")
                
                if impact.get("actionable_insights"):
                    st.markdown("**Actionable Insights:**")
                    for idx, insight in enumerate(impact["actionable_insights"][:5], 1):
                        st.markdown(f"{idx}. {insight}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Display validation metadata if available
        if "validation_metadata" in results and results["validation_metadata"]:
            with st.expander("✅ Quality Validation", expanded=False):
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                validation = results["validation_metadata"]
                
                if validation.get("validated"):
                    st.success("✅ Results validated by Ollama proofreader")
                    
                    # Display validation timestamp
                    if validation.get("validation_timestamp"):
                        st.caption(f"Validated: {validation['validation_timestamp']}")
                    
                    # Display validation results by section
                    validation_results = validation.get("validation_results", {})
                    
                    if validation_results.get("transcription"):
                        trans_val = validation_results["transcription"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Transcription Quality", f"{trans_val.get('quality_score', 0)}%")
                        with col2:
                            st.metric("Word Count", trans_val.get('word_count', 0))
                        if trans_val.get("issues"):
                            with st.expander("Issues found"):
                                for issue in trans_val["issues"]:
                                    st.write(f"• {issue}")
                        if trans_val.get("ollama_assessment"):
                            st.info(f"**AI Assessment:** {trans_val['ollama_assessment']}")
                    
                    if validation_results.get("summary"):
                        summary_val = validation_results["summary"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Summary Quality", f"{summary_val.get('quality_score', 0)}%")
                        with col2:
                            st.metric("Key Takeaways", summary_val.get('takeaway_count', 0))
                        if summary_val.get("ollama_assessment"):
                            st.info(f"**AI Assessment:** {summary_val['ollama_assessment']}")
                    
                    if validation_results.get("research"):
                        research_val = validation_results["research"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Research Quality", f"{research_val.get('quality_score', 0)}%")
                        with col2:
                            st.metric("Findings", research_val.get('findings_count', 0))
                        if research_val.get("ollama_assessment"):
                            st.info(f"**AI Assessment:** {research_val['ollama_assessment']}")
                    
                    if validation_results.get("categorization"):
                        cat_val = validation_results["categorization"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Category Quality", f"{cat_val.get('quality_score', 0)}%")
                        with col2:
                            st.metric("Categories Found", cat_val.get('category_count', 0))
                        if cat_val.get("ollama_assessment"):
                            st.info(f"**AI Assessment:** {cat_val['ollama_assessment']}")
                else:
                    st.warning(f"⚠️ Validation unavailable: {validation.get('reason', validation.get('error', 'Unknown reason'))}")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Export options
        st.divider()
        col_export1, col_export2, col_export3 = st.columns(3)
        
        with col_export1:
            if st.button("💾 Export as JSON", key="export_json", use_container_width=True):
                json_str = json.dumps(st.session_state.analysis_results, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col_export2:
            if st.button("📄 Export as Markdown", key="export_md", use_container_width=True):
                md_content = format_results_as_markdown(st.session_state.analysis_results)
                st.download_button(
                    label="Download Markdown",
                    data=md_content,
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
        
        with col_export3:
            if st.button("🔗 Copy Share Link", key="share_link", use_container_width=True):
                st.info("Share link feature coming soon!")

elif selected == "View Results":
    st.markdown('<div class="main-header">📊 View Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Browse and manage analysis results</div>', unsafe_allow_html=True)
    
    # Load results from storage
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    result_files = list(results_dir.glob("*.json"))
    
    if result_files:
        st.subheader("Recent Analyses")
        
        # Create a list of results
        for result_file in sorted(result_files, reverse=True)[:10]:
            with open(result_file) as f:
                result_data = json.load(f)
            
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"**{result_data.get('file_name', 'Unknown')}**")
                st.caption(result_data.get('timestamp', 'Unknown date'))
            
            with col2:
                if "categorization" in result_data:
                    cat = result_data["categorization"]
                    st.markdown(f"Category: `{cat.get('primary', 'Unknown')}`")
            
            with col3:
                if st.button("📂 Open", key=f"open_{result_file.stem}"):
                    st.session_state.analysis_results = result_data
                    st.rerun()
            
            st.divider()
    else:
        st.info("No results yet. Upload and analyze a video to get started!")

elif selected == "History":
    st.markdown('<div class="main-header">🕐 Analysis History</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Track your analysis activities</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        results_dir = Path("results")
        result_files = list(results_dir.glob("*.json")) if results_dir.exists() else []
        st.metric("Total Analyses", len(result_files))
    
    with col2:
        st.metric("This Month", "3")  # Placeholder
    
    st.divider()
    
    st.subheader("Activity Timeline")
    
    if result_files:
        # Load and display recent activities
        activities_data = []
        for rf in sorted(result_files, reverse=True)[:20]:
            with open(rf) as f:
                data = json.load(f)
                activities_data.append({
                    "Date": data.get("timestamp", "Unknown"),
                    "File": data.get("file_name", "Unknown"),
                    "Category": data.get("categorization", {}).get("primary", "Unknown"),
                    "Status": "Complete" if data else "Error"
                })
        
        import pandas as pd
        df = pd.DataFrame(activities_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No history yet.")

elif selected == "Settings":
    st.markdown('<div class="main-header">⚙️ Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Configure the analysis agent</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 LLM Configuration")
        
        llm_provider = st.selectbox(
            "LLM Provider",
            ["Ollama (Local)", "OpenAI", "Anthropic"]
        )
        
        if llm_provider == "Ollama (Local)":
            ollama_model = st.text_input(
                "Ollama Model",
                value="llama2:13b",
                help="Model name available in local Ollama"
            )
            ollama_host = st.text_input(
                "Ollama Host",
                value="http://localhost:11434",
                help="Ollama API endpoint"
            )
        elif llm_provider == "OpenAI":
            openai_key = st.text_input(
                "OpenAI API Key",
                type="password",
                help="Your OpenAI API key"
            )
            openai_model = st.selectbox(
                "Model",
                ["gpt-4", "gpt-3.5-turbo"]
            )
        
        if st.button("💾 Save LLM Settings", use_container_width=True):
            st.success("Settings saved!")
    
    with col2:
        st.subheader("📁 Storage Configuration")
        
        results_path = st.text_input(
            "Results Directory",
            value="results",
            help="Where to store analysis results"
        )
        
        logs_path = st.text_input(
            "Logs Directory",
            value="logs",
            help="Where to store activity logs"
        )
        
        auto_cleanup = st.checkbox(
            "Auto-cleanup old results",
            value=False,
            help="Automatically delete results older than 30 days"
        )
        
        if st.button("💾 Save Storage Settings", use_container_width=True):
            st.success("Settings saved!")
    
    st.divider()
    
    st.subheader("🔧 Advanced Settings")
    
    col_adv1, col_adv2 = st.columns(2)
    
    with col_adv1:
        st.markdown("**Analysis Parameters**")
        st.slider("Max Transcription Length", 100, 10000, 5000)
        st.slider("Summary Length (words)", 50, 500, 200)
        st.number_input("Max Research Links", 3, 20, 10)
    
    with col_adv2:
        st.markdown("**Performance**")
        st.slider("Parallel Tasks", 1, 4, 2)
        st.number_input("API Timeout (seconds)", 10, 300, 60)
        st.checkbox("Enable Caching", value=True)


# Helper functions
def create_demo_results(filename: str, config: dict) -> dict:
    """Create demo results for testing without real pipeline."""
    return {
        "file_name": filename,
        "timestamp": datetime.now().isoformat(),
        "config": config,
        "transcription": """
This is a demonstration transcription of the uploaded video. In a real scenario, 
this would be the full transcribed text from the video using speech-to-text technology.

The transcription would include all spoken content, timestamps, speaker identification, 
and other relevant audio metadata extracted from the Instagram video.
        """.strip(),
        "summary": """
### Key Insights

This video discusses important advances in AI and machine learning technologies, 
focusing on:

- **Main Topic**: Recent developments in language model optimization
- **Key Points**: 
  - Performance improvements through fine-tuning
  - Cost reduction through model optimization
  - Practical applications in production environments

### Relevance
The content is highly relevant to ongoing project initiatives around AI/ML integration.
        """,
        "research": {
            "findings": [
                "Recent papers on model optimization show 30% performance gains",
                "Cost-effective fine-tuning approaches are gaining adoption",
                "Industry best practices are converging around similar architectures"
            ],
            "links": [
                {"title": "ArXiv: Model Optimization Techniques", "url": "https://arxiv.org"},
                {"title": "GitHub: Fine-tuning Library", "url": "https://github.com"},
                {"title": "Blog: Production ML Practices", "url": "https://example.com"}
            ]
        },
        "categorization": {
            "primary": "AI/ML",
            "secondary": ["Model Optimization", "Fine-tuning"],
            "confidence": 94,
            "relevance_score": 9,
            "tags": ["AI", "LLM", "Optimization", "Performance", "CostReduction"]
        },
        "impact": {
            "affected_projects": [
                {
                    "name": "main-ai-project",
                    "impact_level": "High",
                    "skill_gaps": ["Model Optimization", "Fine-tuning"]
                },
                {
                    "name": "ml-infrastructure",
                    "impact_level": "Medium",
                    "skill_gaps": ["Performance Monitoring"]
                }
            ],
            "actionable_insights": [
                "Implement fine-tuning pipeline for main models",
                "Investigate cost optimization techniques for production",
                "Evaluate identified architectural patterns",
                "Create team training session on new approaches",
                "Benchmark current performance against identified standards"
            ]
        }
    }


def format_results_as_markdown(results: dict) -> str:
    """Format analysis results as Markdown."""
    md = f"""# Analysis Report
**File**: {results.get('file_name', 'Unknown')}
**Date**: {results.get('timestamp', 'Unknown')}

---

## 📝 Transcription

{results.get('transcription', 'No transcription available')}

---

## 📋 Summary

{results.get('summary', 'No summary available')}

---

## 🔍 Research Findings

"""
    
    if "research" in results:
        for finding in results["research"].get("findings", []):
            md += f"- {finding}\n"
        
        md += "\n### Links\n"
        for link in results["research"].get("links", []):
            md += f"- [{link['title']}]({link['url']})\n"
    
    md += """
---

## 🏷️ Categorization

"""
    
    if "categorization" in results:
        cat = results["categorization"]
        md += f"- **Primary**: {cat.get('primary', 'Unknown')}\n"
        md += f"- **Tags**: {', '.join(cat.get('tags', []))}\n"
        md += f"- **Confidence**: {cat.get('confidence', 0)}%\n"
    
    md += """
---

## 💡 Project Impact

"""
    
    if "impact" in results:
        impact = results["impact"]
        md += "### Affected Projects\n"
        for project in impact.get("affected_projects", []):
            md += f"- **{project['name']}** ({project['impact_level']} impact)\n"
        
        md += "\n### Actionable Insights\n"
        for insight in impact.get("actionable_insights", []):
            md += f"- {insight}\n"
    
    return md


if __name__ == "__main__":
    pass
