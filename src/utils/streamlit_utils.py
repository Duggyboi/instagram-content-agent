"""
Streamlit utilities and helper functions.
"""

import streamlit as st
from pathlib import Path
import json
from typing import Dict, Any, List
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def initialize_session_state():
    """Initialize all session state variables."""
    state_defaults = {
        "analysis_results": None,
        "uploaded_file": None,
        "analysis_in_progress": False,
        "current_page": "Upload & Analyze",
        "settings_changed": False,
    }
    
    for key, default_value in state_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def save_analysis_to_file(results: Dict[str, Any]) -> Path:
    """Save analysis results to a JSON file."""
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = results_dir / f"analysis_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Analysis saved to {filename}")
    return filename


def load_results_from_disk(limit: int = 20) -> List[Dict[str, Any]]:
    """Load analysis results from disk."""
    results_dir = Path("results")
    if not results_dir.exists():
        return []
    
    result_files = sorted(results_dir.glob("*.json"), reverse=True)[:limit]
    results = []
    
    for rf in result_files:
        try:
            with open(rf) as f:
                results.append(json.load(f))
        except Exception as e:
            logger.error(f"Failed to load {rf}: {e}")
    
    return results


def create_results_dataframe(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert results list to DataFrame for display."""
    if not results:
        return pd.DataFrame()
    
    data = []
    for result in results:
        row = {
            "Date": result.get("timestamp", "Unknown"),
            "File": result.get("file_name", "Unknown"),
            "Category": result.get("categorization", {}).get("primary", "Unknown"),
            "Confidence": f"{result.get('categorization', {}).get('confidence', 0)}%",
            "Status": "Complete"
        }
        data.append(row)
    
    return pd.DataFrame(data)


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def display_status_badge(status: str):
    """Display a status badge with appropriate styling."""
    status_map = {
        "processing": ("⏳ Processing", "status-processing"),
        "complete": ("✅ Complete", "status-complete"),
        "error": ("❌ Error", "status-error"),
    }
    
    label, css_class = status_map.get(status, ("Unknown", ""))
    
    st.markdown(
        f'<span class="status-badge {css_class}">{label}</span>',
        unsafe_allow_html=True
    )


def export_results_as_json(results: Dict[str, Any]) -> str:
    """Convert results to JSON string for export."""
    return json.dumps(results, indent=2)


def export_results_as_markdown(results: Dict[str, Any]) -> str:
    """Convert results to Markdown format for export."""
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


def export_results_as_html(results: Dict[str, Any]) -> str:
    """Convert results to HTML format for export."""
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Analysis Report - {results.get('file_name', 'Unknown')}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2rem; }}
            h1 {{ color: #333; }}
            h2 {{ color: #666; margin-top: 2rem; }}
            .section {{ margin-bottom: 2rem; }}
            .metadata {{ background-color: #f0f0f0; padding: 1rem; border-radius: 4px; }}
            .findings {{ background-color: #f9f9f9; padding: 1rem; }}
            .tags {{ display: flex; gap: 0.5rem; flex-wrap: wrap; }}
            .tag {{ background-color: #e0e0e0; padding: 0.25rem 0.5rem; border-radius: 4px; }}
            a {{ color: #1f77b4; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>Analysis Report</h1>
        <div class="metadata">
            <p><strong>File:</strong> {results.get('file_name', 'Unknown')}</p>
            <p><strong>Date:</strong> {results.get('timestamp', 'Unknown')}</p>
        </div>
        
        <div class="section">
            <h2>Transcription</h2>
            <p>{results.get('transcription', 'No transcription available')}</p>
        </div>
        
        <div class="section">
            <h2>Summary</h2>
            <p>{results.get('summary', 'No summary available')}</p>
        </div>
    """
    
    if "research" in results:
        html += """
        <div class="section">
            <h2>Research Findings</h2>
            <div class="findings">
        """
        for finding in results["research"].get("findings", []):
            html += f"<p>- {finding}</p>\n"
        
        if results["research"].get("links"):
            html += "<h3>Useful Links</h3>\n"
            for link in results["research"]["links"]:
                html += f'<p><a href="{link["url"]}">{link["title"]}</a></p>\n'
        
        html += "</div>\n</div>\n"
    
    if "categorization" in results:
        cat = results["categorization"]
        html += f"""
        <div class="section">
            <h2>Categorization</h2>
            <p><strong>Primary:</strong> {cat.get('primary', 'Unknown')}</p>
            <p><strong>Confidence:</strong> {cat.get('confidence', 0)}%</p>
            <div class="tags">
        """
        for tag in cat.get("tags", []):
            html += f'<span class="tag">{tag}</span>\n'
        html += "</div>\n</div>\n"
    
    if "impact" in results:
        impact = results["impact"]
        html += """
        <div class="section">
            <h2>Project Impact</h2>
            <h3>Affected Projects</h3>
        """
        for project in impact.get("affected_projects", []):
            html += f"""
            <p><strong>{project['name']}</strong> ({project['impact_level']} impact)</p>
            """
        
        if impact.get("actionable_insights"):
            html += "<h3>Actionable Insights</h3>\n<ol>\n"
            for insight in impact["actionable_insights"]:
                html += f"<li>{insight}</li>\n"
            html += "</ol>\n"
        
        html += "</div>\n"
    
    html += """
    </body>
    </html>
    """
    
    return html


def cleanup_old_results(days: int = 30) -> int:
    """Delete analysis results older than specified days."""
    results_dir = Path("results")
    if not results_dir.exists():
        return 0
    
    import time
    cutoff_time = time.time() - (days * 24 * 60 * 60)
    deleted_count = 0
    
    for result_file in results_dir.glob("*.json"):
        if result_file.stat().st_mtime < cutoff_time:
            try:
                result_file.unlink()
                deleted_count += 1
                logger.info(f"Deleted old result: {result_file}")
            except Exception as e:
                logger.error(f"Failed to delete {result_file}: {e}")
    
    return deleted_count
