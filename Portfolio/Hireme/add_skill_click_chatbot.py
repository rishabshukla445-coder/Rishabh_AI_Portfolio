import re

file_path = r"c:\MLAI_ANON\AIML_ANON\Week2\day10\Hireme\frontend\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update CSS for skill pills to indicate clickability
pill_css_old = """.skill-view-pill {
      font-size: 11px;
      font-weight: 600;
      padding: 4px 9px;
      border-radius: 7px;
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.08);
      color: var(--text2);
      transition: all 0.15s;
    }"""

pill_css_new = """.skill-view-pill {
      font-size: 11px;
      font-weight: 600;
      padding: 5px 11px;
      border-radius: 8px;
      background: rgba(139, 92, 246, 0.08);
      border: 1px solid rgba(139, 92, 246, 0.2);
      color: var(--text);
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .skill-view-pill:hover {
      background: rgba(139, 92, 246, 0.25);
      border-color: rgba(167, 139, 250, 0.6);
      color: #ffffff;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    }"""

html = html.replace(pill_css_old, pill_css_new)

# Function to transform span tags into interactive askQuestion triggers
def make_interactive_pill(match):
    text = match.group(1).strip()
    # Remove emoji prefix for clean question
    clean_skill = re.sub(r'^[^\w\s]+', '', text).strip()
    return f'<span class="skill-view-pill" onclick="askQuestion(\'Tell me about Rishabh\\\'s experience with {clean_skill}\')" title="Ask AI Chat about {clean_skill}">{text} 💬</span>'

# Replace skill pills in skillsView
html = re.sub(r'<span class="skill-view-pill">(.*?)</span>', make_interactive_pill, html)

# Replace skill pills in main skills section if any
def make_main_pill(match):
    text = match.group(1).strip()
    clean_skill = re.sub(r'^[^\w\s]+', '', text).strip()
    return f'<span class="skill-pill" onclick="askQuestion(\'Tell me about Rishabh\\\'s experience with {clean_skill}\')" style="cursor:pointer;" title="Ask AI Chat about {clean_skill}">{text} 💬</span>'

html = re.sub(r'<span class="skill-pill">(.*?)</span>', make_main_pill, html)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated skill pills with askQuestion chatbot popup triggers.")
