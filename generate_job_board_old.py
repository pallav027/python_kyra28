"""
Job Board Website Generator
Generates a complete, self-contained HTML job board website.
Run: python generate_job_board.py
Output: job_board.html
"""

import json
from datetime import datetime, timedelta
import random

# --- Sample job data ---
SAMPLE_JOBS = [
    {
        "id": 1,
        "title": "Senior Full-Stack Engineer",
        "company": "Nexora Labs",
        "location": "San Francisco, CA",
        "type": "Full-time",
        "salary": "$140k – $180k",
        "tags": ["React", "Node.js", "PostgreSQL"],
        "description": "Join our core product team to build scalable web applications. You'll own features end-to-end, from database design to pixel-perfect UI.",
        "posted_days_ago": 1,
        "logo_letter": "N",
        "apply_url": "https://nexoralabs.com/careers/senior-full-stack-engineer",
        "logo_color": "#0ea5e9",
    },
    {
        "id": 2,
        "title": "Product Designer",
        "company": "Drift Studio",
        "location": "Remote",
        "type": "Full-time",
        "salary": "$110k – $140k",
        "tags": ["Figma", "UX Research", "Design Systems"],
        "description": "Design elegant experiences for our SaaS platform used by 200k+ professionals. You'll define visual language, run user research, and partner with engineers.",
        "posted_days_ago": 2,
        "logo_letter": "D",
        "logo_color": "#f97316",
    },
    {
        "id": 3,
        "title": "Machine Learning Engineer",
        "company": "Verdant AI",
        "location": "New York, NY",
        "type": "Full-time",
        "salary": "$160k – $210k",
        "tags": ["Python", "PyTorch", "MLOps"],
        "description": "Build and deploy ML models powering our sustainability analytics platform. Work on real-world impact: carbon tracking, supply chain optimization.",
        "posted_days_ago": 3,
        "logo_letter": "V",
        "logo_color": "#22c55e",
    },
    {
        "id": 4,
        "title": "DevOps / Platform Engineer",
        "company": "Stackform",
        "location": "Austin, TX",
        "type": "Full-time",
        "salary": "$130k – $160k",
        "tags": ["Kubernetes", "Terraform", "AWS"],
        "description": "Architect and maintain cloud infrastructure for our rapidly scaling platform. Drive reliability, observability, and developer productivity.",
        "posted_days_ago": 5,
        "logo_letter": "S",
        "logo_color": "#8b5cf6",
    },
    {
        "id": 5,
        "title": "C++ Software Engineer - Critical Engineering",
        "company": "Optiver",
        "location": "Europe",
        "type": "Full-time",
        "salary": "$90k – $120k",
        "tags": ["C++", "Linux", "Python"],
        "description": "We are looking for experienced software engineers to join Critical Engineering APAC team in Sydney — the platform group that builds and operates the systems Optiver's trading stack runs on.",
        "posted_days_ago": 6,
        "logo_letter": "L",
        "logo_color": "#eab308",
    },
    {
        "id": 6,
        "title": "iOS Engineer",
        "company": "Petal Health",
        "location": "Boston, MA",
        "type": "Contract",
        "salary": "$90 – $120 / hr",
        "tags": ["Swift", "SwiftUI", "HealthKit"],
        "description": "Build privacy-first health tracking features on iOS. You'll work in a small, focused team shipping high-quality experiences to 500k active users.",
        "posted_days_ago": 7,
        "logo_letter": "P",
        "logo_color": "#ec4899",
    },
]


def posted_label(days_ago: int) -> str:
    if days_ago == 0:
        return "Today"
    elif days_ago == 1:
        return "Yesterday"
    else:
        return f"{days_ago} days ago"


def build_job_cards(jobs: list) -> str:
    cards = []
    for job in jobs:
        tags_html = "".join(
            f'<span class="tag">{t}</span>' for t in job["tags"]
        )
        cards.append(f"""
        <article class="job-card" data-type="{job['type']}" data-location="{job['location']}">
          <div class="card-left">
            <div class="logo" style="background:{job['logo_color']}">{job['logo_letter']}</div>
          </div>
          <div class="card-body">
            <div class="card-meta">
              <span class="company">{job['company']}</span>
              <span class="dot">·</span>
              <span class="posted">{posted_label(job['posted_days_ago'])}</span>
            </div>
            <h2 class="job-title">{job['title']}</h2>
            <p class="job-desc">{job['description']}</p>
            <div class="card-footer">
              <div class="tags">{tags_html}</div>
              <div class="meta-chips">
                <span class="chip chip-loc">📍 {job['location']}</span>
                <span class="chip chip-type">{job['type']}</span>
                <span class="chip chip-salary">{job['salary']}</span>
              </div>
            </div>
          </div>
          <div class="card-action">
            <button class="apply-btn" onclick="openModal({job['id']})">Apply</button>
          </div>
        </article>""")
    return "\n".join(cards)


def build_modal_data(jobs: list) -> str:
    return json.dumps({str(j["id"]): j for j in jobs}, indent=2)


def generate_html(jobs: list) -> str:
    job_cards_html = build_job_cards(jobs)
    modal_data_js = build_modal_data(jobs)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>WorkBoard — Find your next role</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap" rel="stylesheet" />
  <style>
    /* ── Reset & Variables ── */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --bg:        #0c0c0f;
      --surface:   #141418;
      --surface2:  #1c1c22;
      --border:    #2a2a35;
      --text:      #e8e8f0;
      --muted:     #7a7a99;
      --accent:    #7c6af7;
      --accent2:   #c084fc;
      --highlight: #f0ebff;
      --radius:    14px;
      --font-head: 'Syne', sans-serif;
      --font-body: 'DM Sans', sans-serif;
    }}

    body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-body);
      min-height: 100vh;
      line-height: 1.6;
    }}

    /* ── Hero Header ── */
    header {{
      position: relative;
      padding: 72px 24px 64px;
      text-align: center;
      overflow: hidden;
    }}

    header::before {{
      content: '';
      position: absolute;
      inset: 0;
      background:
        radial-gradient(ellipse 60% 50% at 30% 40%, rgba(124,106,247,.18) 0%, transparent 70%),
        radial-gradient(ellipse 50% 60% at 75% 60%, rgba(192,132,252,.12) 0%, transparent 70%);
      pointer-events: none;
    }}

    .wordmark {{
      font-family: var(--font-head);
      font-size: 13px;
      font-weight: 700;
      letter-spacing: .18em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 28px;
    }}

    header h1 {{
      font-family: var(--font-head);
      font-size: clamp(2.4rem, 6vw, 4rem);
      font-weight: 800;
      line-height: 1.1;
      letter-spacing: -.02em;
      color: var(--highlight);
      max-width: 640px;
      margin: 0 auto 20px;
    }}

    header h1 span {{
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    header p.subtitle {{
      color: var(--muted);
      font-size: 1.05rem;
      font-weight: 300;
      max-width: 420px;
      margin: 0 auto 40px;
    }}

    /* ── Search Bar ── */
    .search-wrap {{
      display: flex;
      gap: 10px;
      max-width: 540px;
      margin: 0 auto;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 50px;
      padding: 6px 6px 6px 20px;
      transition: border-color .2s;
    }}

    .search-wrap:focus-within {{
      border-color: var(--accent);
    }}

    .search-wrap input {{
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      color: var(--text);
      font-family: var(--font-body);
      font-size: .95rem;
    }}

    .search-wrap input::placeholder {{ color: var(--muted); }}

    .search-wrap button {{
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      border: none;
      border-radius: 50px;
      color: #fff;
      font-family: var(--font-head);
      font-size: .85rem;
      font-weight: 700;
      letter-spacing: .04em;
      padding: 10px 22px;
      cursor: pointer;
      transition: opacity .15s;
    }}

    .search-wrap button:hover {{ opacity: .88; }}

    /* ── Filters ── */
    .filters-bar {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: center;
      padding: 28px 24px 0;
    }}

    .filter-btn {{
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 50px;
      color: var(--muted);
      font-family: var(--font-body);
      font-size: .82rem;
      padding: 7px 16px;
      cursor: pointer;
      transition: all .15s;
    }}

    .filter-btn:hover, .filter-btn.active {{
      background: var(--accent);
      border-color: var(--accent);
      color: #fff;
    }}

    /* ── Main Layout ── */
    main {{
      max-width: 860px;
      margin: 0 auto;
      padding: 40px 24px 80px;
    }}

    .results-meta {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 22px;
    }}

    .results-meta span {{
      font-size: .85rem;
      color: var(--muted);
    }}

    .results-count strong {{
      color: var(--text);
      font-weight: 600;
    }}

    /* ── Job Cards ── */
    .jobs-list {{
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .job-card {{
      display: flex;
      align-items: flex-start;
      gap: 18px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 22px 22px 20px;
      transition: border-color .2s, transform .2s, box-shadow .2s;
      animation: slideUp .4s ease both;
    }}

    @keyframes slideUp {{
      from {{ opacity: 0; transform: translateY(14px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}

    .job-card:hover {{
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: 0 8px 32px rgba(124,106,247,.12);
    }}

    .logo {{
      width: 46px;
      height: 46px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-head);
      font-weight: 800;
      font-size: 1.2rem;
      color: #fff;
      flex-shrink: 0;
    }}

    .card-body {{ flex: 1; min-width: 0; }}

    .card-meta {{
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 5px;
    }}

    .company {{
      font-size: .82rem;
      font-weight: 600;
      color: var(--accent2);
    }}

    .dot {{ color: var(--border); }}

    .posted {{ font-size: .78rem; color: var(--muted); }}

    .job-title {{
      font-family: var(--font-head);
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--highlight);
      letter-spacing: -.01em;
      margin-bottom: 8px;
    }}

    .job-desc {{
      font-size: .86rem;
      color: var(--muted);
      font-weight: 300;
      margin-bottom: 14px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    .card-footer {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .tags {{ display: flex; gap: 6px; flex-wrap: wrap; }}

    .tag {{
      background: rgba(124,106,247,.12);
      border: 1px solid rgba(124,106,247,.25);
      border-radius: 6px;
      color: var(--accent2);
      font-size: .72rem;
      font-weight: 500;
      padding: 3px 9px;
    }}

    .meta-chips {{ display: flex; gap: 7px; flex-wrap: wrap; margin-left: auto; }}

    .chip {{
      background: var(--surface2);
      border-radius: 6px;
      font-size: .72rem;
      color: var(--muted);
      padding: 3px 9px;
    }}

    .card-action {{
      display: flex;
      align-items: center;
      flex-shrink: 0;
      padding-left: 6px;
    }}

    .apply-btn {{
      background: transparent;
      border: 1px solid var(--accent);
      border-radius: 8px;
      color: var(--accent);
      font-family: var(--font-head);
      font-size: .82rem;
      font-weight: 700;
      padding: 9px 18px;
      cursor: pointer;
      white-space: nowrap;
      transition: background .15s, color .15s;
    }}

    .apply-btn:hover {{
      background: var(--accent);
      color: #fff;
    }}

    .no-results {{
      text-align: center;
      padding: 60px 0;
      color: var(--muted);
      display: none;
    }}

    .no-results h3 {{
      font-family: var(--font-head);
      font-size: 1.2rem;
      color: var(--text);
      margin-bottom: 8px;
    }}

    /* ── Post Job CTA ── */
    .post-cta {{
      background: linear-gradient(135deg, rgba(124,106,247,.15), rgba(192,132,252,.1));
      border: 1px solid rgba(124,106,247,.3);
      border-radius: var(--radius);
      padding: 32px 28px;
      text-align: center;
      margin-top: 40px;
    }}

    .post-cta h3 {{
      font-family: var(--font-head);
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--highlight);
      margin-bottom: 8px;
    }}

    .post-cta p {{ color: var(--muted); font-size: .9rem; margin-bottom: 20px; }}

    .post-cta button {{
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      border: none;
      border-radius: 8px;
      color: #fff;
      font-family: var(--font-head);
      font-size: .9rem;
      font-weight: 700;
      padding: 12px 28px;
      cursor: pointer;
      transition: opacity .15s;
    }}

    .post-cta button:hover {{ opacity: .88; }}

    /* ── Modal ── */
    .modal-overlay {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,.7);
      backdrop-filter: blur(6px);
      z-index: 100;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}

    .modal-overlay.open {{ display: flex; }}

    .modal {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 18px;
      max-width: 520px;
      width: 100%;
      padding: 32px;
      animation: popIn .25s cubic-bezier(.34,1.56,.64,1) both;
    }}

    @keyframes popIn {{
      from {{ opacity: 0; transform: scale(.92); }}
      to   {{ opacity: 1; transform: scale(1); }}
    }}

    .modal-header {{
      display: flex;
      align-items: flex-start;
      gap: 14px;
      margin-bottom: 20px;
    }}

    .modal-logo {{
      width: 52px;
      height: 52px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-head);
      font-weight: 800;
      font-size: 1.3rem;
      color: #fff;
      flex-shrink: 0;
    }}

    .modal-header-info h2 {{
      font-family: var(--font-head);
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--highlight);
    }}

    .modal-header-info span {{
      font-size: .84rem;
      color: var(--accent2);
      font-weight: 500;
    }}

    .modal-desc {{
      color: var(--muted);
      font-size: .88rem;
      line-height: 1.65;
      margin-bottom: 22px;
    }}

    .modal label {{
      display: block;
      font-size: .8rem;
      font-weight: 600;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: .06em;
      margin-bottom: 6px;
    }}

    .modal input, .modal textarea {{
      width: 100%;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-family: var(--font-body);
      font-size: .9rem;
      padding: 10px 14px;
      margin-bottom: 14px;
      outline: none;
      transition: border-color .15s;
    }}

    .modal input:focus, .modal textarea:focus {{
      border-color: var(--accent);
    }}

    .modal textarea {{ resize: vertical; min-height: 90px; }}

    .modal-actions {{
      display: flex;
      gap: 10px;
      margin-top: 6px;
    }}

    .btn-cancel {{
      flex: 1;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--muted);
      font-family: var(--font-head);
      font-size: .85rem;
      font-weight: 700;
      padding: 11px;
      cursor: pointer;
    }}

    .btn-submit {{
      flex: 2;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      border: none;
      border-radius: 8px;
      color: #fff;
      font-family: var(--font-head);
      font-size: .85rem;
      font-weight: 700;
      padding: 11px;
      cursor: pointer;
      transition: opacity .15s;
    }}

    .btn-submit:hover {{ opacity: .88; }}

    .toast {{
      position: fixed;
      bottom: 28px;
      left: 50%;
      transform: translateX(-50%) translateY(20px);
      background: #22c55e;
      color: #fff;
      font-family: var(--font-head);
      font-size: .85rem;
      font-weight: 700;
      padding: 12px 24px;
      border-radius: 50px;
      opacity: 0;
      transition: opacity .3s, transform .3s;
      pointer-events: none;
      z-index: 200;
    }}

    .toast.show {{
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }}

    /* ── Post Job Modal ── */
    .post-modal {{ max-width: 560px; }}

    /* ── Responsive ── */
    @media (max-width: 600px) {{
      .card-action {{ display: none; }}
      .meta-chips {{ margin-left: 0; }}
      header h1 {{ font-size: 2rem; }}
    }}
  </style>
</head>
<body>

<!-- Header -->
<header>
  <p class="wordmark">WorkBoard</p>
  <h1>Find roles that <span>Your next move forward</span></h1>
  <p class="subtitle">Hand-picked opportunities at companies building something worth caring about.</p>
  <div class="search-wrap">
    <input type="text" id="searchInput" placeholder="Search job title, skill, or company…" oninput="filterJobs()" />
    <button onclick="filterJobs()">Search</button>
  </div>
</header>

<!-- Filters -->
<div class="filters-bar">
  <button class="filter-btn active" onclick="setFilter(this,'all')">All Roles</button>
  <button class="filter-btn" onclick="setFilter(this,'full-time')">Full-time</button>
  <button class="filter-btn" onclick="setFilter(this,'contract')">Contract</button>
  <button class="filter-btn" onclick="setFilter(this,'remote')">Remote</button>
</div>

<!-- Main -->
<main>
  <div class="results-meta">
    <span class="results-count"><strong id="jobCount">{len(SAMPLE_JOBS)}</strong> openings</span>
    <span>Updated today</span>
  </div>

  <div class="jobs-list" id="jobsList">
{job_cards_html}
  </div>

  <div class="no-results" id="noResults">
    <h3>No roles found</h3>
    <p>Try a different keyword or remove a filter.</p>
  </div>

  <!-- Post Job CTA -->
  <div class="post-cta">
    <h3>Hiring? Post your role here.</h3>
    <p>Reach thousands of qualified candidates looking for their next opportunity.</p>
    <button onclick="openPostModal()">Post a Job Opening</button>
  </div>
</main>

<!-- Apply Modal -->
<div class="modal-overlay" id="applyModal">
  <div class="modal">
    <div class="modal-header">
      <div class="modal-logo" id="modalLogo">N</div>
      <div class="modal-header-info">
        <h2 id="modalTitle">Job Title</h2>
        <span id="modalCompany">Company</span>
      </div>
    </div>
    <p class="modal-desc" id="modalDesc"></p>
    <label>Full Name</label>
    <input type="text" placeholder="Jane Smith" id="appName" />
    <label>Email Address</label>
    <input type="email" placeholder="jane@email.com" id="appEmail" />
    <label>LinkedIn / Portfolio URL</label>
    <input type="url" placeholder="https://…" id="appUrl" />
    <label>Cover Note (optional)</label>
    <textarea placeholder="Why are you excited about this role?" id="appNote"></textarea>
    <div class="modal-actions">
      <button class="btn-cancel" onclick="closeModal('applyModal')">Cancel</button>
      <button class="btn-submit" onclick="submitApplication()">Submit Application</button>
    </div>
  </div>
</div>

<!-- Post Job Modal -->
<div class="modal-overlay" id="postModal">
  <div class="modal post-modal">
    <h2 style="font-family:var(--font-head);font-size:1.2rem;color:var(--highlight);margin-bottom:20px;">Post a Job Opening</h2>
    <label>Job Title</label>
    <input type="text" placeholder="e.g. Senior Backend Engineer" id="postTitle" />
    <label>Company Name</label>
    <input type="text" placeholder="Acme Corp" id="postCompany" />
    <label>Location</label>
    <input type="text" placeholder="Remote / City, Country" id="postLocation" />
    <label>Salary Range</label>
    <input type="text" placeholder="e.g. $100k – $130k" id="postSalary" />
    <label>Job Description</label>
    <textarea placeholder="Describe the role, responsibilities, and ideal candidate…" id="postDesc"></textarea>
    <div class="modal-actions">
      <button class="btn-cancel" onclick="closeModal('postModal')">Cancel</button>
      <button class="btn-submit" onclick="submitPost()">Publish Listing</button>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
  const JOBS = {modal_data_js};
  let activeFilter = 'all';

  function openModal(id) {{
    const job = JOBS[id];
    if (!job) return;
    document.getElementById('modalLogo').textContent = job.logo_letter;
    document.getElementById('modalLogo').style.background = job.logo_color;
    document.getElementById('modalTitle').textContent = job.title;
    document.getElementById('modalCompany').textContent = job.company + ' · ' + job.location;
    document.getElementById('modalDesc').textContent = job.description;
    document.getElementById('applyModal').classList.add('open');
  }}

  function openPostModal() {{
    document.getElementById('postModal').classList.add('open');
  }}

  function closeModal(id) {{
    document.getElementById(id).classList.remove('open');
  }}

  document.querySelectorAll('.modal-overlay').forEach(el => {{
    el.addEventListener('click', e => {{ if (e.target === el) el.classList.remove('open'); }});
  }});

  function showToast(msg) {{
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3200);
  }}

  function submitApplication() {{
    const name = document.getElementById('appName').value.trim();
    const email = document.getElementById('appEmail').value.trim();
    if (!name || !email) {{ alert('Please fill in your name and email.'); return; }}
    closeModal('applyModal');
    showToast('✅ Application sent! Good luck, ' + name.split(' ')[0] + '.');
  }}

  function submitPost() {{
    const title = document.getElementById('postTitle').value.trim();
    const company = document.getElementById('postCompany').value.trim();
    if (!title || !company) {{ alert('Please fill in job title and company.'); return; }}
    closeModal('postModal');
    showToast('🎉 Your listing has been submitted for review!');
  }}

  function setFilter(btn, value) {{
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeFilter = value;
    filterJobs();
  }}

  function filterJobs() {{
    const query = document.getElementById('searchInput').value.toLowerCase();
    const cards = document.querySelectorAll('.job-card');
    let visible = 0;
    cards.forEach(card => {{
      const text = card.textContent.toLowerCase();
      const loc = card.dataset.location.toLowerCase();
      const type = card.dataset.type.toLowerCase();
      const matchesQuery = !query || text.includes(query);
      const matchesFilter =
        activeFilter === 'all' ||
        (activeFilter === 'remote' && loc.includes('remote')) ||
        type.includes(activeFilter);
      if (matchesQuery && matchesFilter) {{
        card.style.display = '';
        visible++;
      }} else {{
        card.style.display = 'none';
      }}
    }});
    document.getElementById('jobCount').textContent = visible;
    document.getElementById('noResults').style.display = visible ? 'none' : 'block';
  }}
</script>
</body>
</html>
"""


def main():
    html = generate_html(SAMPLE_JOBS)
    output_path = "job_board.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅  Generated: {output_path}")
    print(f"   {len(SAMPLE_JOBS)} job listings included.")
    print("   Open job_board.html in any browser to view the site.")
    print()
    print("To add your own jobs, edit the SAMPLE_JOBS list at the top of this script.")


if __name__ == "__main__":
    
    main()
