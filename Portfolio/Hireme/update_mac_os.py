import re

file_path = r"c:\MLAI_ANON\AIML_ANON\Week2\day10\Hireme\frontend\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Body CSS for Desktop locking
html = html.replace(
    "body {\n      background: linear-gradient(135deg, #020617 0%, #0b132b 30%, #1c2541 65%, #0b0d1b 100%) !important;\n      position: relative;\n    }",
    "body {\n      background: linear-gradient(135deg, #020617 0%, #0b132b 30%, #1c2541 65%, #0b0d1b 100%) !important;\n      position: relative;\n      height: 100vh;\n      overflow: hidden;\n    }"
)

# 2. Update macOS Top Menu Bar
menubar_old = """<!-- ═══════════ macOS TOP MENU BAR ═══════════ -->
<div class="mac-menubar">
  <div class="mac-menu-left">
    <span class="mac-apple-logo" onclick="window.scrollTo({top:0, behavior:'smooth'})"></span>
    <span class="mac-menu-title" style="cursor:pointer;" onclick="window.scrollTo({top:0, behavior:'smooth'})">Rishabh's Portfolio</span>
    <a href="#projects" class="mac-menu-item" onclick="event.preventDefault(); document.getElementById('projects').scrollIntoView({behavior:'smooth'})">Projects</a>
    <a href="#about" class="mac-menu-item" onclick="event.preventDefault(); document.getElementById('about').scrollIntoView({behavior:'smooth'})">Experience</a>
    <a href="#skills" class="mac-menu-item" onclick="event.preventDefault(); document.getElementById('skills').scrollIntoView({behavior:'smooth'})">Skills</a>
    <button class="mac-menu-item" onclick="openMacAIWindow('jd')">HR Matcher</button>
    <button class="mac-menu-item" onclick="openMacAIWindow('chat')">Rishabh.AI</button>
    <a href="/resume/download" class="mac-menu-item" target="_blank">Resume.pdf</a>
  </div>
  <div class="mac-menu-right">
    <span class="mac-status-icon" title="Wi-Fi Connected">📡</span>
    <span class="mac-status-icon" title="Battery 100%">🔋 100%</span>
    <span id="mac-clock" class="mac-clock">Wed, Aug 9, 4:17 PM</span>
  </div>
</div>"""

menubar_new = """<!-- ═══════════ macOS TOP MENU BAR ═══════════ -->
<div class="mac-menubar">
  <div class="mac-menu-left">
    <span class="mac-apple-logo" onclick="openMacAIWindow('chat')"></span>
    <span class="mac-menu-title" style="cursor:pointer;" onclick="openMacAIWindow('chat')">Rishabh's Portfolio</span>
    <button class="mac-menu-item" onclick="openMacAIWindow('projects')">Projects</button>
    <button class="mac-menu-item" onclick="openMacAIWindow('experience')">Experience</button>
    <button class="mac-menu-item" onclick="openMacAIWindow('skills')">Skills</button>
    <button class="mac-menu-item" onclick="openMacAIWindow('jd')">HR Matcher</button>
    <button class="mac-menu-item" onclick="openMacAIWindow('chat')">Rishabh.AI</button>
    <a href="/resume/download" class="mac-menu-item" target="_blank" download="Rishabh_Shukla_Resume.pdf">Resume.pdf</a>
  </div>
  <div class="mac-menu-right">
    <span class="mac-status-icon" title="Wi-Fi Connected">📡</span>
    <span class="mac-status-icon" title="Battery 100%">🔋 100%</span>
    <span id="mac-clock" class="mac-clock">Wed, Aug 9, 4:17 PM</span>
  </div>
</div>"""

if menubar_old in html:
    html = html.replace(menubar_old, menubar_new)
else:
    # Pattern replace if whitespace differs
    pattern = r'<!-- ═══════════ macOS TOP MENU BAR ═══════════ -->.*?<div class="mac-desktop-grid">'
    html = re.sub(pattern, menubar_new + "\n\n<!-- ═══════════ macOS DESKTOP APP ICONS (Left Grid) ═══════════ -->\n<div class=\"mac-desktop-grid\">", html, flags=re.DOTALL)

# 3. Update macOS Dock actions
dock_old = """    <div class="mac-dock-item" title="Finder — Portfolio Home" onclick="window.scrollTo({top:0, behavior:'smooth'})">
      <div class="dock-icon-box" style="background:linear-gradient(180deg,#5eb5f7 0%,#2196f3 100%); color:#fff;">😊</div>
      <span class="dock-dot"></span>
    </div>
    <div class="mac-dock-item" title="Safari — Projects" onclick="document.getElementById('projects').scrollIntoView({behavior:'smooth'})">
      <div class="dock-icon-box" style="background:linear-gradient(180deg,#5db8fe 0%,#1976d2 100%); color:#fff;">🧭</div>
      <span class="dock-dot"></span>
    </div>
    <div class="mac-dock-item" title="Photos — Skills" onclick="document.getElementById('skills').scrollIntoView({behavior:'smooth'})">
      <div class="dock-icon-box">🌸</div>
      <span class="dock-dot"></span>
    </div>
    <div class="mac-dock-item" title="Contacts — Experience" onclick="document.getElementById('about').scrollIntoView({behavior:'smooth'})">
      <div class="dock-icon-box" style="background:linear-gradient(180deg,#ffb74d 0%,#f57c00 100%); color:#fff;">👤</div>
      <span class="dock-dot"></span>
    </div>"""

dock_new = """    <div class="mac-dock-item" title="Finder — Projects" onclick="openMacAIWindow('projects')">
      <div class="dock-icon-box" style="background:linear-gradient(180deg,#5eb5f7 0%,#2196f3 100%); color:#fff;">😊</div>
      <span class="dock-dot"></span>
    </div>
    <div class="mac-dock-item" title="Safari — The Anon Tech" onclick="window.open('https://the-anon-tech-uv5o.vercel.app/','_blank')">
      <div class="dock-icon-box" style="background:linear-gradient(180deg,#5db8fe 0%,#1976d2 100%); color:#fff;">🧭</div>
      <span class="dock-dot"></span>
    </div>
    <div class="mac-dock-item" title="Photos — Skills" onclick="openMacAIWindow('skills')">
      <div class="dock-icon-box">🌸</div>
      <span class="dock-dot"></span>
    </div>
    <div class="mac-dock-item" title="Contacts — Experience" onclick="openMacAIWindow('experience')">
      <div class="dock-icon-box" style="background:linear-gradient(180deg,#ffb74d 0%,#f57c00 100%); color:#fff;">👤</div>
      <span class="dock-dot"></span>
    </div>"""

if dock_old in html:
    html = html.replace(dock_old, dock_new)

# 4. Update Tab Bar inside Window Modal to include all 5 tabs
tabbar_old = """        <!-- Tab Bar -->
        <div class="tab-nav-bar">
          <button class="tab-btn active" id="tabChatBtn" onclick="switchTab('chat')">
            💬 AI Chat Assistant
          </button>
          <button class="tab-btn" id="tabJdBtn" onclick="switchTab('jd')">
            📄 HR JD Matcher & Multi-Line Charts
          </button>
        </div>"""

tabbar_new = """        <!-- Tab Bar -->
        <div class="tab-nav-bar" style="display:flex; gap:8px; overflow-x:auto; padding-bottom:6px; margin-bottom:16px;">
          <button class="tab-btn active" id="tabChatBtn" onclick="switchTab('chat')">
            💬 AI Chat Assistant
          </button>
          <button class="tab-btn" id="tabJdBtn" onclick="switchTab('jd')">
            🎯 HR JD Matcher & Charts
          </button>
          <button class="tab-btn" id="tabProjectsBtn" onclick="switchTab('projects')">
            📁 Projects
          </button>
          <button class="tab-btn" id="tabSkillsBtn" onclick="switchTab('skills')">
            🛠️ Skills
          </button>
          <button class="tab-btn" id="tabExperienceBtn" onclick="switchTab('experience')">
            🏆 Experience
          </button>
        </div>"""

if tabbar_old in html:
    html = html.replace(tabbar_old, tabbar_new)

# 5. Update switchTab function in JavaScript
switchtab_old = """  // ─── TAB SWITCHER ──────────────────────────────────────────
  function switchTab(tab) {
    const chatBtn = document.getElementById('tabChatBtn');
    const jdBtn = document.getElementById('tabJdBtn');
    const chatView = document.getElementById('chatView');
    const jdView = document.getElementById('jdView');

    if (tab === 'chat') {
      chatBtn.classList.add('active');
      jdBtn.classList.remove('active');
      chatView.style.display = 'flex';
      jdView.style.display = 'none';
    } else {
      jdBtn.classList.add('active');
      chatBtn.classList.remove('active');
      chatView.style.display = 'none';
      jdView.style.display = 'flex';
    }
  }"""

switchtab_new = """  // ─── TAB SWITCHER ──────────────────────────────────────────
  function switchTab(tab) {
    const tabs = ['chat', 'jd', 'projects', 'skills', 'experience'];
    tabs.forEach(t => {
      const btnName = 'tab' + t.charAt(0).toUpperCase() + t.slice(1) + 'Btn';
      const viewName = t + 'View';
      const btn = document.getElementById(btnName);
      const view = document.getElementById(viewName);
      if (btn) {
        if (t === tab) btn.classList.add('active');
        else btn.classList.remove('active');
      }
      if (view) {
        if (t === tab) view.style.display = (t === 'chat' || t === 'jd') ? 'flex' : 'block';
        else view.style.display = 'none';
      }
    });
  }"""

if switchtab_old in html:
    html = html.replace(switchtab_old, switchtab_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)

print("macOS OS layout script finished successfully.")
