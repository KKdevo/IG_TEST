#!/usr/bin/env python3
"""
Social Media Report Generator
Reads a Word document template and generates a beautiful HTML report.

Usage:
    python generate_report.py input.docx output.html
    python generate_report.py input.docx  (outputs to input_report.html)
"""

import sys
import os
import re
from docx import Document
from docx.table import Table
from datetime import datetime

def extract_tables(doc):
    """Extract all tables from the document."""
    tables = []
    for table in doc.tables:
        rows = []
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            rows.append(cells)
        tables.append(rows)
    return tables

def parse_config(tables):
    """Parse the config table (first table with Account Name/Date Created)."""
    config = {"AccountName": "", "DateCreated": ""}
    for table in tables:
        for row in table:
            if len(row) >= 2:
                key = row[0].strip().replace(" ", "")
                if key == "AccountName":
                    config["AccountName"] = row[1].strip()
                elif key == "DateCreated":
                    config["DateCreated"] = row[1].strip()
    # Clean placeholder text
    for k, v in config.items():
        if v.startswith("[") and v.endswith("]"):
            config[k] = ""
    return config

def parse_posts_table(table):
    """Parse the posting schedule table."""
    posts = []
    headers = ["Title", "PostDate", "Time", "Type", "Status", "Hashtags", "Notes"]
    
    for i, row in enumerate(table):
        if i == 0:  # Skip header row
            continue
        if len(row) >= 7 and row[0] and not row[0].startswith("["):
            post = {
                "Title": row[0],
                "PostDate": row[1],
                "Time": row[2],
                "Type": row[3].lower().replace("[", "").replace("]", ""),
                "Status": row[4].replace("[", "").replace("]", ""),
                "Hashtags": row[5],
                "Notes": row[6] if len(row) > 6 else ""
            }
            posts.append(post)
    return posts

def parse_post_blocks(tables):
    """Parse individual post detail blocks (Title/Caption/Hashtags/URL format)."""
    posts = []
    current_type = "post"
    
    for table in tables:
        # Check if this is a post detail block (has Title, Caption rows)
        row_labels = [row[0].strip().lower() if len(row) >= 2 else "" for row in table]
        
        if "title" in row_labels and ("caption" in row_labels or "description" in row_labels):
            post = {"Type": current_type, "Caption": "", "Hashtags": "", "MediaURL": ""}
            
            for row in table:
                if len(row) >= 2:
                    label = row[0].strip().lower()
                    value = row[1].strip()
                    
                    # Skip placeholder text
                    if value.startswith("[") and value.endswith("]"):
                        continue
                        
                    if label == "title":
                        post["Title"] = value
                    elif label in ["caption", "description"]:
                        post["Caption"] = value
                    elif label == "hashtags":
                        post["Hashtags"] = value
                    elif label in ["image url", "video url", "cover image url", "media url"]:
                        post["MediaURL"] = value
            
            if post.get("Title"):
                posts.append(post)
    
    return posts

def parse_stories_table(table):
    """Parse the stories table."""
    stories = []
    
    for i, row in enumerate(table):
        if i == 0:  # Skip header
            continue
        if len(row) >= 5 and row[0] and not row[0].startswith("["):
            story = {
                "Title": row[0],
                "PostDate": row[1],
                "Time": row[2],
                "InteractiveElements": row[3],
                "Notes": row[4],
                "MediaURL": row[5] if len(row) > 5 else ""
            }
            # Clean placeholder URLs
            if story["MediaURL"].startswith("["):
                story["MediaURL"] = ""
            stories.append(story)
    return stories

def parse_interactions_table(table):
    """Parse the interactions table."""
    interactions = []
    
    for i, row in enumerate(table):
        if i == 0:  # Skip header
            continue
        if len(row) >= 11 and row[0] and not row[0].startswith("["):
            interaction = {
                "AccountName": row[0].replace("@", "").replace("[", "").replace("]", ""),
                "Platform": row[1].replace("[", "").replace("]", ""),
                "InteractionType": row[2].replace("[", "").replace("]", ""),
                "DailyGoal": row[3].replace("[", "").replace("]", ""),
                "Mon": "TRUE" if row[4].strip().lower() in ["x", "✓", "✔", "true", "yes"] else "FALSE",
                "Tue": "TRUE" if row[5].strip().lower() in ["x", "✓", "✔", "true", "yes"] else "FALSE",
                "Wed": "TRUE" if row[6].strip().lower() in ["x", "✓", "✔", "true", "yes"] else "FALSE",
                "Thu": "TRUE" if row[7].strip().lower() in ["x", "✓", "✔", "true", "yes"] else "FALSE",
                "Fri": "TRUE" if row[8].strip().lower() in ["x", "✓", "✔", "true", "yes"] else "FALSE",
                "Sat": "TRUE" if row[9].strip().lower() in ["x", "✓", "✔", "true", "yes"] else "FALSE",
                "Sun": "TRUE" if row[10].strip().lower() in ["x", "✓", "✔", "true", "yes"] else "FALSE",
            }
            interactions.append(interaction)
    return interactions

def identify_tables(tables, doc):
    """Identify which table is which based on content/headers."""
    result = {
        "config": None,
        "posts_schedule": None,
        "post_blocks": [],
        "stories": None,
        "interactions": None
    }
    
    for table in tables:
        if not table or not table[0]:
            continue
            
        first_row = [c.lower().strip() for c in table[0]]
        
        # Config table (Account Name / Date Created)
        if any("account" in c for c in first_row):
            result["config"] = table
            
        # Posts schedule (has Title, Date, Time, Type columns)
        elif "title" in first_row and "date" in first_row and "type" in first_row:
            result["posts_schedule"] = table
            
        # Stories table (has Interactive Elements)
        elif any("interactive" in c for c in first_row):
            result["stories"] = table
            
        # Interactions table (has Daily Goal and day columns)
        elif any("goal" in c for c in first_row) and any("mon" in c for c in first_row):
            result["interactions"] = table
            
        # Post detail block (Title/Caption/Hashtags format)
        elif len(table) >= 3 and len(table[0]) == 2:
            labels = [row[0].lower().strip() if len(row) >= 2 else "" for row in table]
            if "title" in labels and ("caption" in labels or "description" in labels):
                result["post_blocks"].append(table)
    
    return result

def detect_post_type_from_context(tables, block_index):
    """Try to determine post type based on surrounding content."""
    # This is a simple heuristic - in practice you might need to parse paragraph text
    # For now, we'll look at the block's URL field
    if block_index < len(tables):
        table = tables[block_index]
        for row in table:
            if len(row) >= 2:
                label = row[0].lower().strip()
                value = row[1].lower()
                if "video" in label or "youtube" in value or "vimeo" in value:
                    return "reel"
                if "cover" in label:
                    return "highlight"
    return "post"

def generate_html(config, posts, stories, interactions):
    """Generate the final HTML report."""
    
    # Count posts by type
    posts_count = len([p for p in posts if p.get("Type", "").lower() == "post"])
    reels_count = len([p for p in posts if p.get("Type", "").lower() == "reel"])
    highlights_count = len([p for p in posts if p.get("Type", "").lower() == "highlight"])
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Content Schedule - {config.get("AccountName", "Report")}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Manrope:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #FAF9F7;
            --bg-secondary: #FFFFFF;
            --text-primary: #1A1A1A;
            --text-secondary: #6B6B6B;
            --text-muted: #9A9A9A;
            --accent: #2D2D2D;
            --accent-warm: #C4A484;
            --border: #E8E6E3;
            --border-light: #F0EFED;
            --shadow: rgba(0,0,0,0.04);
            --shadow-md: rgba(0,0,0,0.08);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Manrope', sans-serif; background: var(--bg-primary); color: var(--text-primary); line-height: 1.6; font-size: 15px; -webkit-font-smoothing: antialiased; }}
        
        .nav {{ position: fixed; top: 0; left: 0; width: 240px; height: 100vh; background: var(--bg-secondary); border-right: 1px solid var(--border); padding: 40px 24px; overflow-y: auto; z-index: 100; }}
        .nav-logo {{ font-family: 'Instrument Serif', serif; font-size: 22px; letter-spacing: -0.5px; margin-bottom: 8px; }}
        .nav-subtitle {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-muted); margin-bottom: 48px; }}
        .nav-section {{ font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-muted); margin: 32px 0 12px; }}
        .nav a {{ display: block; color: var(--text-secondary); text-decoration: none; padding: 10px 0; font-size: 14px; transition: all 0.2s ease; }}
        .nav a:hover {{ color: var(--text-primary); }}
        .nav .sub-link {{ padding-left: 16px; font-size: 13px; color: var(--text-muted); }}
        
        .main {{ margin-left: 240px; min-height: 100vh; }}
        section {{ scroll-margin-top: 20px; }}
        
        .title-page {{ min-height: 100vh; display: flex; flex-direction: column; position: relative; overflow: hidden; background: linear-gradient(165deg, #1A1A1A 0%, #2D2D2D 40%, #3D3D3D 100%); }}
        .title-page::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E"); opacity: 0.03; pointer-events: none; }}
        .title-header {{ padding: 48px 64px; display: flex; justify-content: space-between; align-items: flex-start; position: relative; z-index: 1; }}
        .title-badge {{ display: inline-flex; align-items: center; gap: 8px; padding: 10px 18px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12); border-radius: 100px; backdrop-filter: blur(10px); }}
        .title-badge-dot {{ width: 6px; height: 6px; background: #7FE5A2; border-radius: 50%; animation: pulse 2s ease-in-out infinite; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: 0.6; transform: scale(0.9); }} }}
        .title-badge span {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: rgba(255,255,255,0.7); font-weight: 500; }}
        .title-date {{ font-size: 13px; color: rgba(255,255,255,0.5); }}
        .title-content {{ flex: 1; display: flex; flex-direction: column; justify-content: center; padding: 0 64px; position: relative; z-index: 1; }}
        .title-eyebrow {{ font-size: 11px; text-transform: uppercase; letter-spacing: 3px; color: var(--accent-warm); margin-bottom: 24px; font-weight: 600; }}
        .title-main {{ font-family: 'Instrument Serif', serif; font-size: clamp(48px, 8vw, 86px); font-weight: 400; color: #FFFFFF; line-height: 1.05; letter-spacing: -2px; margin-bottom: 24px; max-width: 800px; }}
        .title-main em {{ font-style: italic; color: var(--accent-warm); }}
        .title-description {{ font-size: 17px; color: rgba(255,255,255,0.5); max-width: 500px; line-height: 1.7; font-weight: 300; }}
        .title-footer {{ padding: 48px 64px; display: flex; justify-content: space-between; align-items: flex-end; position: relative; z-index: 1; }}
        .title-meta {{ display: flex; gap: 64px; }}
        .title-meta-item {{ position: relative; }}
        .title-meta-label {{ font-size: 10px; text-transform: uppercase; letter-spacing: 2px; color: rgba(255,255,255,0.35); margin-bottom: 8px; font-weight: 500; }}
        .title-meta-value {{ font-size: 18px; color: #FFFFFF; font-weight: 500; }}
        .title-decoration {{ position: absolute; right: 64px; bottom: 50%; transform: translateY(50%); width: 320px; height: 320px; border: 1px solid rgba(255,255,255,0.08); border-radius: 50%; pointer-events: none; }}
        .title-decoration::before {{ content: ''; position: absolute; top: 40px; left: 40px; right: 40px; bottom: 40px; border: 1px solid rgba(255,255,255,0.05); border-radius: 50%; }}
        
        .content-section {{ padding: 80px 64px; border-bottom: 1px solid var(--border); }}
        .section-header {{ margin-bottom: 48px; max-width: 600px; }}
        .section-number {{ font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: var(--text-muted); margin-bottom: 16px; font-weight: 500; }}
        .section-title {{ font-family: 'Instrument Serif', serif; font-size: 38px; font-weight: 400; letter-spacing: -1px; margin-bottom: 12px; line-height: 1.2; }}
        .section-desc {{ font-size: 15px; color: var(--text-secondary); line-height: 1.7; }}
        
        .table-wrapper {{ background: var(--bg-secondary); border-radius: 16px; overflow: hidden; box-shadow: 0 1px 3px var(--shadow), 0 4px 20px var(--shadow); margin-bottom: 48px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: var(--bg-primary); padding: 16px 20px; text-align: left; font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-muted); font-weight: 600; border-bottom: 1px solid var(--border); }}
        td {{ padding: 20px; border-bottom: 1px solid var(--border-light); font-size: 14px; vertical-align: middle; }}
        tr:last-child td {{ border-bottom: none; }}
        tr:hover {{ background: var(--bg-primary); }}
        
        .status {{ display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 100px; font-size: 12px; font-weight: 600; }}
        .status::before {{ content: ''; width: 6px; height: 6px; border-radius: 50%; }}
        .status-draft {{ background: #FEF9E7; color: #9A7B2A; }}
        .status-draft::before {{ background: #F4C430; }}
        .status-approved {{ background: #E8F5E9; color: #2E7D32; }}
        .status-approved::before {{ background: #4CAF50; }}
        .status-posted {{ background: #E3F2FD; color: #1565C0; }}
        .status-posted::before {{ background: #2196F3; }}
        .status-needsrevision {{ background: #FFEBEE; color: #C62828; }}
        .status-needsrevision::before {{ background: #EF5350; }}
        
        .type-badge {{ display: inline-block; padding: 5px 12px; border-radius: 6px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }}
        .type-post {{ background: #F3F4F6; color: #374151; }}
        .type-reel {{ background: #FDF2F8; color: #BE185D; }}
        .type-highlight {{ background: #FEF3C7; color: #B45309; }}
        
        .posts-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 32px; margin-bottom: 48px; }}
        .post-card {{ background: var(--bg-secondary); border-radius: 20px; overflow: hidden; box-shadow: 0 1px 3px var(--shadow), 0 8px 32px var(--shadow); transition: all 0.3s ease; }}
        .post-card:hover {{ transform: translateY(-4px); box-shadow: 0 4px 12px var(--shadow-md), 0 16px 48px var(--shadow-md); }}
        .post-card-media {{ width: 100%; aspect-ratio: 1; object-fit: cover; background: var(--border-light); }}
        .post-card-media.video-container {{ position: relative; background: #000; }}
        .post-card-media iframe {{ width: 100%; height: 100%; border: none; }}
        .post-card-body {{ padding: 24px; }}
        .post-card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; gap: 12px; }}
        .post-card-title {{ font-size: 17px; font-weight: 600; color: var(--text-primary); line-height: 1.3; }}
        .post-card-caption {{ font-size: 14px; color: var(--text-secondary); margin-bottom: 16px; display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.6; }}
        .post-card-hashtags {{ font-size: 13px; color: var(--accent-warm); font-weight: 500; }}
        .no-media {{ width: 100%; aspect-ratio: 1; background: linear-gradient(135deg, var(--border-light) 0%, var(--border) 100%); display: flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 13px; }}
        
        .type-section {{ margin-bottom: 64px; }}
        .type-section:last-child {{ margin-bottom: 0; }}
        .type-section-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 28px; padding-bottom: 16px; border-bottom: 1px solid var(--border); }}
        .type-section-icon {{ width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; background: var(--bg-primary); border-radius: 10px; font-size: 18px; }}
        .type-section-title {{ font-size: 20px; font-weight: 600; }}
        .type-section-count {{ font-size: 13px; color: var(--text-muted); margin-left: auto; }}
        
        .stories-strip {{ display: flex; gap: 20px; overflow-x: auto; padding: 24px 0; }}
        .story-item {{ flex-shrink: 0; width: 140px; text-align: center; }}
        .story-thumb-wrapper {{ position: relative; width: 120px; height: 213px; margin: 0 auto 12px; border-radius: 16px; overflow: hidden; background: linear-gradient(135deg, #E1306C 0%, #F77737 50%, #FCAF45 100%); padding: 3px; }}
        .story-thumb {{ width: 100%; height: 100%; object-fit: cover; border-radius: 14px; background: var(--bg-secondary); }}
        .story-title {{ font-size: 13px; color: var(--text-primary); font-weight: 500; }}
        .story-date {{ font-size: 11px; color: var(--text-muted); margin-top: 2px; }}
        
        .interactions-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 24px; }}
        .interaction-card {{ background: var(--bg-secondary); border-radius: 16px; padding: 28px; box-shadow: 0 1px 3px var(--shadow); }}
        .interaction-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }}
        .interaction-account {{ font-weight: 600; font-size: 17px; margin-bottom: 4px; }}
        .interaction-platform {{ font-size: 13px; color: var(--text-muted); }}
        .interaction-goal-badge {{ display: inline-block; padding: 6px 14px; background: var(--bg-primary); border-radius: 100px; font-size: 12px; font-weight: 600; color: var(--text-secondary); }}
        .week-checklist {{ display: flex; gap: 8px; }}
        .day-check {{ flex: 1; text-align: center; }}
        .day-check label {{ display: block; font-size: 11px; color: var(--text-muted); margin-bottom: 8px; font-weight: 500; }}
        .day-check input[type="checkbox"] {{ appearance: none; width: 32px; height: 32px; border: 2px solid var(--border); border-radius: 8px; cursor: pointer; transition: all 0.2s ease; position: relative; }}
        .day-check input[type="checkbox"]:checked {{ background: var(--accent); border-color: var(--accent); }}
        .day-check input[type="checkbox"]:checked::after {{ content: '✓'; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #fff; font-size: 14px; font-weight: 600; }}
        
        .empty-state {{ text-align: center; padding: 48px; color: var(--text-muted); background: var(--bg-primary); border-radius: 16px; }}
        
        @media print {{ .nav {{ display: none; }} .main {{ margin-left: 0; }} .title-page {{ min-height: auto; padding: 60px; }} }}
        @media (max-width: 1024px) {{ .nav {{ display: none; }} .main {{ margin-left: 0; }} .content-section {{ padding: 48px 32px; }} .title-header, .title-content, .title-footer {{ padding-left: 32px; padding-right: 32px; }} .title-decoration {{ display: none; }} }}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-logo">Content Schedule</div>
        <div class="nav-subtitle">Social Media Report</div>
        <div class="nav-section">Overview</div>
        <a href="#title">Cover</a>
        <a href="#schedule">Posting Schedule</a>
        <div class="nav-section">Content</div>
        <a href="#posts">Draft Posts</a>
        <a href="#posts-posts" class="sub-link">Posts</a>
        <a href="#posts-reels" class="sub-link">Reels</a>
        <a href="#posts-highlights" class="sub-link">Highlights</a>
        <div class="nav-section">Engagement</div>
        <a href="#stories">Stories</a>
        <a href="#interactions">Interactions</a>
    </nav>

    <main class="main">
        <section id="title" class="title-page">
            <div class="title-decoration"></div>
            <header class="title-header">
                <div class="title-badge">
                    <span class="title-badge-dot"></span>
                    <span>Content Calendar</span>
                </div>
                <div class="title-date">{datetime.now().strftime("%A, %B %d, %Y")}</div>
            </header>
            <div class="title-content">
                <div class="title-eyebrow">Social Media Strategy</div>
                <h1 class="title-main">Content <em>Schedule</em> & Asset Review</h1>
                <p class="title-description">A comprehensive overview of planned content, posting schedule, and engagement strategy.</p>
            </div>
            <footer class="title-footer">
                <div class="title-meta">
                    <div class="title-meta-item">
                        <div class="title-meta-label">Account</div>
                        <div class="title-meta-value">{config.get("AccountName", "Not Set")}</div>
                    </div>
                    <div class="title-meta-item">
                        <div class="title-meta-label">Created</div>
                        <div class="title-meta-value">{config.get("DateCreated", "Not Set")}</div>
                    </div>
                    <div class="title-meta-item">
                        <div class="title-meta-label">Total Posts</div>
                        <div class="title-meta-value">{len(posts)}</div>
                    </div>
                </div>
            </footer>
        </section>

        <section id="schedule" class="content-section">
            <div class="section-header">
                <div class="section-number">01</div>
                <h2 class="section-title">Posting Schedule</h2>
                <p class="section-desc">Complete overview of all planned content.</p>
            </div>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Date</th>
                            <th>Time</th>
                            <th>Type</th>
                            <th>Status</th>
                            <th>Hashtags</th>
                            <th>Notes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join(f'''<tr>
                            <td><strong>{p.get("Title", "")}</strong></td>
                            <td>{p.get("PostDate", "")}</td>
                            <td>{p.get("Time", "")}</td>
                            <td><span class="type-badge type-{p.get("Type", "post").lower()}">{p.get("Type", "post")}</span></td>
                            <td><span class="status status-{p.get("Status", "Draft").lower().replace(" ", "")}">{p.get("Status", "Draft")}</span></td>
                            <td style="max-width: 200px; font-size: 13px; color: var(--text-muted);">{p.get("Hashtags", "")}</td>
                            <td style="max-width: 180px; font-size: 13px;">{p.get("Notes", "")}</td>
                        </tr>''' for p in posts) if posts else '<tr><td colspan="7" class="empty-state">No posts scheduled</td></tr>'}
                    </tbody>
                </table>
            </div>
        </section>

        <section id="posts" class="content-section">
            <div class="section-header">
                <div class="section-number">02</div>
                <h2 class="section-title">Draft Posts</h2>
                <p class="section-desc">Content previews organized by format.</p>
            </div>

            <div id="posts-posts" class="type-section">
                <div class="type-section-header">
                    <div class="type-section-icon">📷</div>
                    <div class="type-section-title">Feed Posts</div>
                    <div class="type-section-count">{posts_count} posts</div>
                </div>
                <div class="posts-grid">
                    {"".join(render_post_card(p, i) for i, p in enumerate(posts) if p.get("Type", "").lower() == "post") or '<div class="empty-state">No posts scheduled</div>'}
                </div>
            </div>

            <div id="posts-reels" class="type-section">
                <div class="type-section-header">
                    <div class="type-section-icon">🎬</div>
                    <div class="type-section-title">Reels</div>
                    <div class="type-section-count">{reels_count} reels</div>
                </div>
                <div class="posts-grid">
                    {"".join(render_post_card(p, i) for i, p in enumerate(posts) if p.get("Type", "").lower() == "reel") or '<div class="empty-state">No reels scheduled</div>'}
                </div>
            </div>

            <div id="posts-highlights" class="type-section">
                <div class="type-section-header">
                    <div class="type-section-icon">⭐</div>
                    <div class="type-section-title">Highlights</div>
                    <div class="type-section-count">{highlights_count} highlights</div>
                </div>
                <div class="posts-grid">
                    {"".join(render_post_card(p, i) for i, p in enumerate(posts) if p.get("Type", "").lower() == "highlight") or '<div class="empty-state">No highlights scheduled</div>'}
                </div>
            </div>
        </section>

        <section id="stories" class="content-section">
            <div class="section-header">
                <div class="section-number">03</div>
                <h2 class="section-title">Stories Schedule</h2>
                <p class="section-desc">Ephemeral content planned for the period.</p>
            </div>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Date</th>
                            <th>Time</th>
                            <th>Interactive Elements</th>
                            <th>Notes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join(f'''<tr>
                            <td><strong>{s.get("Title", "")}</strong></td>
                            <td>{s.get("PostDate", "")}</td>
                            <td>{s.get("Time", "")}</td>
                            <td>{s.get("InteractiveElements", "")}</td>
                            <td>{s.get("Notes", "")}</td>
                        </tr>''' for s in stories) if stories else '<tr><td colspan="5" class="empty-state">No stories scheduled</td></tr>'}
                    </tbody>
                </table>
            </div>
            
            <div class="type-section-header" style="margin-top: 48px;">
                <div class="type-section-icon">📱</div>
                <div class="type-section-title">Story Assets</div>
            </div>
            <div class="stories-strip">
                {"".join(f'''<div class="story-item">
                    <div class="story-thumb-wrapper">
                        <img class="story-thumb" src="{s.get("MediaURL", "")}" alt="{s.get("Title", "")}" onerror="this.style.background='#f5f5f5'">
                    </div>
                    <div class="story-title">{s.get("Title", "")}</div>
                    <div class="story-date">{s.get("PostDate", "")}</div>
                </div>''' for s in stories if s.get("MediaURL")) or '<div class="empty-state" style="width: 100%;">No story assets uploaded</div>'}
            </div>
        </section>

        <section id="interactions" class="content-section">
            <div class="section-header">
                <div class="section-number">04</div>
                <h2 class="section-title">Account Interactions</h2>
                <p class="section-desc">Daily engagement targets and tracking.</p>
            </div>
            <div class="interactions-grid">
                {"".join(render_interaction_card(i) for i in interactions) if interactions else '<div class="empty-state">No interaction targets configured</div>'}
            </div>
        </section>
    </main>
</body>
</html>'''
    
    return html

def render_post_card(post, index):
    """Render a single post card."""
    media_url = post.get("MediaURL", "")
    is_video = any(x in media_url.lower() for x in ["youtube.com", "youtu.be", "vimeo.com"])
    
    if is_video:
        embed_url = get_embed_url(media_url)
        media_html = f'<div class="post-card-media video-container"><iframe src="{embed_url}" allowfullscreen></iframe></div>'
    elif media_url:
        media_html = f'<img class="post-card-media" src="{media_url}" alt="{post.get("Title", "")}" onerror="this.outerHTML=\'<div class=\\\'no-media\\\'>Image not available</div>\'">'
    else:
        media_html = '<div class="no-media">No media uploaded</div>'
    
    return f'''<div class="post-card" id="post-{index}">
        {media_html}
        <div class="post-card-body">
            <div class="post-card-header">
                <span class="post-card-title">{post.get("Title", "Untitled")}</span>
                <span class="type-badge type-{post.get("Type", "post").lower()}">{post.get("Type", "post")}</span>
            </div>
            <p class="post-card-caption">{post.get("Caption", "No caption provided")}</p>
            <div class="post-card-hashtags">{post.get("Hashtags", "")}</div>
        </div>
    </div>'''

def render_interaction_card(interaction):
    """Render a single interaction card."""
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    checkboxes = "".join(f'''<div class="day-check">
        <label>{day}</label>
        <input type="checkbox" {"checked" if interaction.get(day) == "TRUE" else ""}>
    </div>''' for day in days)
    
    return f'''<div class="interaction-card">
        <div class="interaction-header">
            <div>
                <div class="interaction-account">@{interaction.get("AccountName", "")}</div>
                <div class="interaction-platform">{interaction.get("Platform", "")} · {interaction.get("InteractionType", "")}</div>
            </div>
            <div class="interaction-goal-badge">{interaction.get("DailyGoal", "0")}/day</div>
        </div>
        <div class="week-checklist">{checkboxes}</div>
    </div>'''

def get_embed_url(url):
    """Convert video URLs to embed format."""
    if "youtube.com/watch" in url:
        video_id = url.split("v=")[1].split("&")[0] if "v=" in url else ""
        return f"https://www.youtube.com/embed/{video_id}"
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0]
        return f"https://www.youtube.com/embed/{video_id}"
    elif "vimeo.com/" in url:
        video_id = url.split("vimeo.com/")[1].split("?")[0]
        return f"https://player.vimeo.com/video/{video_id}"
    return url

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py input.docx [output.html]")
        print("\nThis script reads a Word document and generates an HTML report.")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace(".docx", "_report.html")
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    print(f"📄 Reading: {input_file}")
    
    # Load document
    doc = Document(input_file)
    tables = extract_tables(doc)
    
    print(f"   Found {len(tables)} tables")
    
    # Identify and parse tables
    identified = identify_tables(tables, doc)
    
    config = parse_config(tables)
    print(f"   Config: {config}")
    
    # Parse posts from schedule table
    posts = []
    if identified["posts_schedule"]:
        posts = parse_posts_table(identified["posts_schedule"])
        print(f"   Posts from schedule: {len(posts)}")
    
    # Merge with post detail blocks (for captions/media)
    post_blocks = []
    for block in identified["post_blocks"]:
        block_data = {}
        post_type = "post"
        for row in block:
            if len(row) >= 2:
                label = row[0].strip().lower()
                value = row[1].strip()
                if value.startswith("[") and value.endswith("]"):
                    continue
                if label == "title":
                    block_data["Title"] = value
                elif label in ["caption", "description"]:
                    block_data["Caption"] = value
                elif label == "hashtags":
                    block_data["Hashtags"] = value
                elif "video" in label:
                    block_data["MediaURL"] = value
                    post_type = "reel"
                elif "cover" in label:
                    block_data["MediaURL"] = value
                    post_type = "highlight"
                elif "image" in label or "url" in label:
                    block_data["MediaURL"] = value
        if block_data.get("Title"):
            block_data["Type"] = post_type
            post_blocks.append(block_data)
    
    # Merge post blocks with schedule
    for block in post_blocks:
        title = block.get("Title", "")
        matched = False
        for post in posts:
            if post.get("Title") == title:
                post.update({k: v for k, v in block.items() if v})
                matched = True
                break
        if not matched:
            posts.append(block)
    
    print(f"   Total posts after merge: {len(posts)}")
    
    # Parse stories
    stories = []
    if identified["stories"]:
        stories = parse_stories_table(identified["stories"])
    print(f"   Stories: {len(stories)}")
    
    # Parse interactions
    interactions = []
    if identified["interactions"]:
        interactions = parse_interactions_table(identified["interactions"])
    print(f"   Interactions: {len(interactions)}")
    
    # Generate HTML
    html = generate_html(config, posts, stories, interactions)
    
    # Write output
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\n✅ Report generated: {output_file}")
    print(f"   Open in any browser to view!")

if __name__ == "__main__":
    main()
