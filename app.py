

import sys, os, json, io, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))


from resume_screener import compute_match_score, get_top_matching_terms
from ai_detector import detect_ai_content, detect_ai_sections
from skill_extractor import compare_skills, extract_skills, TECH_SKILLS, SOFT_SKILLS
from decision_engine import get_decision_summary
from tips_generator import generate_tips, get_general_advice

st.set_page_config(page_title="AI Driven Resume Screening", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    * { box-sizing: border-box; }
    html, body, [class*="css"], .stMarkdown, h1, h2, h3, h4, h5, h6, label, p, span, div {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e2e8f0;
    }
    
    .stApp {
        background: #0f172a !important;
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(99, 102, 241, 0.08) 0%, transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(168, 85, 247, 0.08) 0%, transparent 25%) !important;
        background-attachment: fixed !important;
    }
    

    #MainMenu, footer, header, [data-testid="stHeader"] { visibility: hidden; }
    [data-testid="stSidebar"] { background-color: rgba(30, 41, 59, 0.4) !important; border-right: 1px solid rgba(255,255,255,0.05); }
    

    h1 { 
        font-weight: 800 !important; 
        font-size: 2.2rem !important; 
        background: linear-gradient(135deg, #fff 0%, #cbd5e1 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        letter-spacing: -0.02em !important;
        text-transform: uppercase;
    }
    h2 { font-weight: 700 !important; font-size: 1.5rem !important; letter-spacing: -0.01em; }
    h3 { font-weight: 600 !important; font-size: 1.2rem !important; }
    

    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-radius: 16px; padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: rgba(99, 102, 241, 0.4); 
    }


    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(30, 41, 59, 0.5) !important; 
        color: #f8fafc !important;
        border: 1px solid rgba(255,255,255,0.1) !important; 
        border-radius: 12px !important;
        transition: all 0.2s ease;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #8b5cf6 !important; 
        box-shadow: 0 0 0 3px rgba(139,92,246,0.15) !important;
        background-color: rgba(30, 41, 59, 0.8) !important;
    }


    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important; border: none !important; border-radius: 12px !important;
        padding: 0.6rem 1.4rem !important; font-weight: 600 !important;
        box-shadow: 0 4px 6px -1px rgba(99,102,241,0.3) !important; 
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button:hover { 
        transform: translateY(-2px) !important; 
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.4) !important;
        filter: brightness(1.1); 
    }


    .stTabs [data-baseweb="tab-list"] { background-color: rgba(30,41,59,0.5); border-radius: 14px; padding: 4px; gap: 4px; }
    .stTabs [data-baseweb="tab"] { color: #94a3b8 !important; border-radius: 10px; font-weight: 600; padding: 8px 16px; border:none !important; }
    .stTabs [aria-selected="true"] { background-color: rgba(99,102,241,0.2) !important; color: #f8fafc !important; }


    [data-testid="stMetric"] { background-color: rgba(30,41,59,0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 1rem; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.1); }
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #f8fafc !important; text-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    [data-testid="stMetricLabel"] { font-size: 0.85rem !important; color: #94a3b8 !important; font-weight: 500 !important; letter-spacing: 0.02em; }
    

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


defaults = {'history': [], 'result': None, 'screened': False, 'resume_input': '', 'jd_input': '', 'email_sent': False, 'email_msg': ''}
for k, v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v


def load_sample():
    try:
        with open("sample_resume.txt", "r", encoding="utf-8") as f: st.session_state["resume_input"] = f.read()
        with open("sample_job_description.txt", "r", encoding="utf-8") as f: st.session_state["jd_input"] = f.read()
    except: st.error("Sample files missing.")

def run_pipeline_wrapper(resume_text, jd_text, match_thr, ai_thr):
    try:
        match_score, match_details = compute_match_score(resume_text, jd_text)
        ai_score, ai_details       = detect_ai_content(resume_text)
        skill_data                 = compare_skills(resume_text, jd_text)
        top_terms                  = get_top_matching_terms(resume_text, jd_text, top_n=12)
        ai_sections                = detect_ai_sections(resume_text)
        r = get_decision_summary(match_score, ai_score, match_details, ai_details, skill_data, match_thr, ai_thr)
        r['top_terms']   = top_terms
        r['ai_sections'] = ai_sections
        missing = skill_data.get('missing_skills', [])
        r['tips'] = generate_tips(missing, match_score)
        jd_skills = skill_data.get('jd_skills', [])
        skill_coverage = (len(skill_data.get('matched_skills', [])) / len(jd_skills) * 100) if jd_skills else 100
        r['general_advice'] = get_general_advice(match_score, ai_score, skill_coverage)
        return r
    except: return None


def build_email_html(candidate_name, decision, match_score, ai_score, reason, matched_skills, missing_skills, tips, general_advice):
    is_accepted = decision == "SHORTLISTED"
    status_color = "#059669" if is_accepted else "#dc2626"
    status_label = "SHORTLISTED ✅" if is_accepted else "NOT SHORTLISTED ❌"
    status_msg = "Congratulations! Your profile has been shortlisted for the next round." if is_accepted else "Thank you for your application. Unfortunately, your profile was not shortlisted at this time."

    matched_html = "".join(f'<span style="display:inline-block;background:#ecfdf5;color:#059669;border:1px solid #a7f3d0;border-radius:20px;padding:4px 12px;margin:3px;font-size:12px;font-weight:600">{s}</span>' for s in matched_skills) or '<span style="color:#94a3b8;font-size:13px">None detected</span>'
    missing_html = "".join(f'<span style="display:inline-block;background:#fef2f2;color:#dc2626;border:1px solid #fecaca;border-radius:20px;padding:4px 12px;margin:3px;font-size:12px;font-weight:600">{s}</span>' for s in missing_skills) or '<span style="color:#059669;font-size:13px">All skills matched! ✅</span>'

    tips_html = ""
    for tip in (tips or [])[:5]:
        tips_html += f'''
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:14px 18px;margin-bottom:8px">
            <strong style="color:#1e293b">{tip.get("skill","")}</strong>
            <span style="font-size:10px;background:#fffbeb;color:#d97706;border-radius:10px;padding:2px 6px;margin-left:6px">{tip.get("priority","")}</span>
            <div style="color:#64748b;font-size:13px;margin-top:4px">{tip.get("tip","")}</div>
        </div>'''

    advice_html = ""
    for a in (general_advice or []):
        advice_html += f'<div style="color:#334155;font-size:14px;padding:6px 0">{a}</div>'

    return f"""
    <div style="max-width:600px;margin:0 auto;font-family:'Segoe UI',Arial,sans-serif;background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;overflow:hidden">
        <div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);padding:32px 28px;text-align:center">
            <h1 style="color:#ffffff;margin:0;font-size:24px;font-weight:800">AI Resume Screener</h1>
            <p style="color:rgba(255,255,255,0.8);margin:8px 0 0;font-size:14px">Screening Results Notification</p>
        </div>
        <div style="padding:28px">
            <p style="color:#334155;font-size:15px;line-height:1.6;margin:0 0 20px">Dear <strong>{candidate_name}</strong>,</p>
            <p style="color:#334155;font-size:15px;line-height:1.6;margin:0 0 24px">{status_msg}</p>

            <div style="background:{status_color};color:#fff;border-radius:12px;padding:20px;text-align:center;margin-bottom:24px">
                <div style="font-size:28px;font-weight:800;letter-spacing:1px">{status_label}</div>
                <div style="font-size:13px;opacity:0.9;margin-top:4px">{reason}</div>
            </div>

            <div style="display:flex;gap:12px;margin-bottom:24px">
                <div style="flex:1;background:#f0f9ff;border:1px solid #bae6fd;border-radius:12px;padding:16px;text-align:center">
                    <div style="font-size:11px;font-weight:700;color:#0369a1;text-transform:uppercase;letter-spacing:1px">Match Score</div>
                    <div style="font-size:32px;font-weight:800;color:#2563eb;margin-top:4px">{match_score:.1f}%</div>
                </div>
                <div style="flex:1;background:#fffbeb;border:1px solid #fde68a;border-radius:12px;padding:16px;text-align:center">
                    <div style="font-size:11px;font-weight:700;color:#92400e;text-transform:uppercase;letter-spacing:1px">AI Content</div>
                    <div style="font-size:32px;font-weight:800;color:#d97706;margin-top:4px">{ai_score:.1f}%</div>
                </div>
            </div>

            <h3 style="color:#1e293b;font-size:15px;margin:0 0 10px;border-bottom:1px solid #e2e8f0;padding-bottom:8px">✅ Matched Skills</h3>
            <div style="margin-bottom:20px">{matched_html}</div>

            <h3 style="color:#1e293b;font-size:15px;margin:0 0 10px;border-bottom:1px solid #e2e8f0;padding-bottom:8px">⚠️ Skills to Improve</h3>
            <div style="margin-bottom:20px">{missing_html}</div>

            {"<h3 style='color:#1e293b;font-size:15px;margin:0 0 10px;border-bottom:1px solid #e2e8f0;padding-bottom:8px'>📋 Improvement Tips</h3>" + tips_html + "<div style='margin-bottom:20px'></div>" if tips_html else ""}

            {"<h3 style='color:#1e293b;font-size:15px;margin:0 0 10px;border-bottom:1px solid #e2e8f0;padding-bottom:8px'>💡 General Advice</h3>" + advice_html + "<div style='margin-bottom:20px'></div>" if advice_html else ""}
        </div>
        <div style="background:#f8fafc;border-top:1px solid #e2e8f0;padding:16px 28px;text-align:center">
            <p style="color:#94a3b8;font-size:12px;margin:0">Sent by AI Resume Screener — Intelligent Screening Engine</p>
        </div>
    </div>
    """


def send_notification_email(to_email, candidate_name, smtp_email, smtp_password, result):
    decision       = result['decision']
    match_score    = result['match_score']
    ai_score       = result['ai_score']
    reason         = result['reason']
    matched_skills = result['skill_analysis'].get('matched_skills', [])
    missing_skills = result['skill_analysis'].get('missing_skills', [])
    tips           = result.get('tips', [])
    general_advice = result.get('general_advice', [])

    html_body = build_email_html(
        candidate_name, decision, match_score, ai_score, reason,
        matched_skills, missing_skills, tips, general_advice
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Resume Screening Result: {decision}"
    msg["From"]    = smtp_email
    msg["To"]      = to_email
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, to_email, msg.as_string())


def create_radar_chart(result):
    s = result['skill_analysis']
    cats = s.get('categories', {})
    jd_tech = [k for k in s['jd_skills'] if k in TECH_SKILLS]
    jd_soft = [k for k in s['jd_skills'] if k in SOFT_SKILLS]
    tech_match = (len(cats.get('matched_tech', [])) / len(jd_tech) * 100) if jd_tech else 0
    soft_match = (len(cats.get('matched_soft', [])) / len(jd_soft) * 100) if jd_soft else 0
    values = [tech_match, soft_match, result['match_score'], max(0, 100 - result['ai_score']), min(100, result['match_score'] * 1.1)]
    categories = ['Technical Skills', 'Soft Skills', 'Overall Match', 'Content Quality', 'Keyword Relevance']
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values, theta=categories, fill='toself',
        fillcolor='rgba(99, 102, 241, 0.3)', line=dict(color='#8b5cf6', width=2), marker=dict(size=4)
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='#64748b'), gridcolor='rgba(255,255,255,0.1)'),
            bgcolor='rgba(0,0,0,0)',
            angularaxis=dict(tickfont=dict(color='#cbd5e1', size=11), gridcolor='rgba(255,255,255,0.1)')
        ),
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=20, l=40, r=40), height=300
    )
    return fig


st.markdown("""
<div style='text-align: center; margin-bottom: 2.5rem; display: flex; flex-direction: column; align-items: center;'>
    <svg width="60" height="60" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 0.5rem; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));">
      <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#6366f1;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#a855f7;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect x="10" y="10" width="80" height="80" rx="20" ry="20" fill="url(#grad1)" opacity="0.9" />
      <path d="M35 50 C 35 30, 65 30, 65 50 C 65 70, 35 70, 35 50 Z M 50 35 L 50 20 M 50 65 L 50 80 M 20 50 L 35 50 M 65 50 L 80 50" 
            stroke="white" stroke-width="4" fill="none" stroke-linecap="round" />
      <circle cx="50" cy="50" r="8" fill="white" />
      <circle cx="35" cy="50" r="4" fill="white" />
      <circle cx="65" cy="50" r="4" fill="white" />
    </svg>
    <div style='padding-top:4px;'>
        <h1 style='margin:0;font-size:2.4rem!important;'>AI DRIVEN RESUME SCREENING</h1>
        <p style='margin:4px 0 0 0;color:#94a3b8;font-size:1.05rem;font-weight:400;'>Intelligent Recruitment Analytics Dashboard</p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Global Settings")
    st.markdown("<p style='font-size:0.85rem;color:#64748b;margin-bottom:1rem;'>Tune your analysis thresholds for the engine.</p>", unsafe_allow_html=True)
    mt = st.slider("Min Match %", 0, 100, 60, help="Minimum competency score to shortlist a candidate.")
    at = st.slider("Max AI %", 0, 100, 80, help="Maximum allowed AI content probability before raising a flag.")
    
    st.markdown("---")
    st.markdown("### 🧪 Actions")
    st.button("📂 Load Sample Data", on_click=load_sample, use_container_width=True, help="Fills inputs with sample testing data.")
    st.markdown("<div style='margin-top:2rem;text-align:center;color:#475569;font-size:0.75rem;'>v5.3 Dashboard</div>", unsafe_allow_html=True)


tab_dash, tab_screen, tab_batch, tab_compare, tab_tips = st.tabs(["📊 Dashboard", "🔍 Screen", "📁 Batch", "⚡ Compare", "💡 Insights"])


with tab_dash:
    hist = st.session_state['history']
    total, short = len(hist), len([r for r in hist if r['decision'] == 'SHORTLISTED'])
    avg = sum(r['match_score'] for r in hist)/total if total else 0
    ai_risk = len([r for r in hist if r['ai_score'] > 80])

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Candidates", total)
    k2.metric("Shortlisted", short, delta=f"{short/total*100:.0f}%" if total else None)
    k3.metric("Avg Match", f"{avg:.1f}%", delta=f"{avg-60:.1f}%" if total else None)
    k4.metric("AI Risk", ai_risk, delta=f"-{ai_risk}" if ai_risk else "Clean", delta_color="inverse")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    if not hist:
        st.info("👋 No data yet. Start by screening a resume in the **Screen** tab.")
    else:
        c_l, c_r = st.columns(2)
        with c_l:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### Match Distribution")
            dist = [len([r for r in hist if r['match_score'] >= 75]),
                    len([r for r in hist if 50 <= r['match_score'] < 75]),
                    len([r for r in hist if r['match_score'] < 50])]
            fig = go.Figure(data=[go.Pie(labels=['Top (75%+)', 'Mid (50-75%)', 'Low (<50%)'], values=dist, hole=.65, marker_colors=['#8b5cf6', '#6366f1', '#334155'])])
            fig.update_layout(showlegend=True, height=220, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#94a3b8"))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_r:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### Top Skills")
            all_s = [s for r in hist for s in r.get('matched_skills', [])]
            if all_s:
                cnt = Counter(all_s).most_common(6)
                fig_b = go.Figure(go.Bar(x=[v for k,v in cnt], y=[k for k,v in cnt], orientation='h', marker_color='#6366f1'))
                fig_b.update_layout(height=220, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#94a3b8"), yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig_b, use_container_width=True)
            else: st.caption("No skills extracted.")
            st.markdown('</div>', unsafe_allow_html=True)


with tab_screen:
    c_in1, c_in2 = st.columns(2)
    with c_in1:
        st.markdown("<h3 style='font-size:1.1rem;margin-bottom:0.5rem;'>📄 Candidate Resume</h3>", unsafe_allow_html=True)
        rf = st.file_uploader("Upload Resume", type=["txt"], key="rf", label_visibility="collapsed")
        rt = st.text_area("Or paste text", height=250, key="rt", placeholder="Paste resume text here...", label_visibility="collapsed")
        if rf: rt = rf.read().decode("utf-8")
        st.caption(f"{len(rt) if rt else 0} characters")
    with c_in2:
        st.markdown("<h3 style='font-size:1.1rem;margin-bottom:0.5rem;'>📋 Job Description</h3>", unsafe_allow_html=True)
        jf = st.file_uploader("Upload JD", type=["txt"], key="jf", label_visibility="collapsed")
        jt = st.text_area("Or paste text", height=250, key="jt", placeholder="Paste Job Description here...", label_visibility="collapsed")
        if jf: jt = jf.read().decode("utf-8")
        st.caption(f"{len(jt) if jt else 0} characters")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    if st.button("🚀 Analyze Candidate", type="primary", use_container_width=True):
        if rt and jt:
            with st.spinner("Analyzing profile... (Skill Matching, Competency, AI Detetion)"):
                res = run_pipeline_wrapper(rt, jt, mt, at)
                if res:
                    st.session_state['result'] = res
                    st.session_state['screened'] = True
                    st.session_state['history'].append({'name': f"Candidate #{len(st.session_state['history'])+1}",
                        'match_score': res['match_score'], 'ai_score': res['ai_score'], 'decision': res['decision'],
                        'matched_skills': res['skill_analysis'].get('matched_skills', [])})
        else: st.warning("Please provide both Resume and Job Description input.")

    if st.session_state['screened'] and st.session_state['result']:
        r = st.session_state['result']
        ok = r['decision'] == "SHORTLISTED"
        color = "#10b981" if ok else "#ef4444"
        
        st.markdown(f"""
        <div style="background:rgba({'16,185,129' if ok else '239,68,68'}, 0.08); border:1px solid {color}; border-radius:12px; padding:1.2rem; margin:1.5rem 0; display:flex; align-items:center;">
            <div style="font-size:2rem; margin-right:1rem;">{'✨' if ok else '⚠️'}</div>
            <div>
                <div style="font-size:1.4rem; font-weight:700; color:{color};">{r['decision']}</div>
                <div style="color:#94a3b8; font-size:0.9rem;">{r['reason']}</div>
            </div>
            <div style="margin-left:auto; text-align:right; display:flex; gap:2rem; align-items:center;">
                <div style="text-align:center;">
                    <div style="font-size:2.2rem; font-weight:800; color:{color};">{r['match_score']:.1f}%</div>
                    <div style="font-size:0.75rem; color:{color}; opacity:0.8; letter-spacing:0.05em;">MATCH SCORE</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:2.2rem; font-weight:800; color:#f59e0b;">{r['ai_score']:.1f}%</div>
                    <div style="font-size:0.75rem; color:#f59e0b; opacity:0.8; letter-spacing:0.05em;">AI SCORE</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── v2: Classification badge ──
        ai_classification = r.get('ai_details', {}).get('classification', '')
        if ai_classification:
            cls_colors = {"Likely Human": ("#10b981", "#ecfdf5"), "Uncertain": ("#f59e0b", "#fffbeb"), "Likely AI": ("#ef4444", "#fef2f2")}
            cls_color, cls_bg = cls_colors.get(ai_classification, ("#94a3b8", "#f8fafc"))
            st.markdown(f"""
            <div style="text-align:center;margin:-0.5rem 0 1rem 0;">
                <span style="background:{cls_bg};color:{cls_color};border:1px solid {cls_color}40;padding:6px 18px;border-radius:20px;font-weight:700;font-size:0.95rem;">
                    {'🟢' if 'Human' in ai_classification else '🟡' if 'Uncertain' in ai_classification else '🔴'} {ai_classification}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        g1, g2 = st.columns([1, 1.2])
        with g1:
            st.markdown("### 🕸️ Competency Radar")
            st.plotly_chart(create_radar_chart(r), use_container_width=True)
            
        with g2:
            st.markdown("### 🧬 Skill DNA")
            s = r['skill_analysis']
            cats = s.get('categories', {})
            def pills(title, items, col):
                if not items: return ""
                h = "".join([f"<span style='background:{col}15;color:{col};border:1px solid {col}30;padding:4px 10px;border-radius:20px;font-size:0.8rem;margin:2px 4px 4px 0;display:inline-block;'>{i}</span>" for i in items])
                return f"<div style='margin-bottom:12px;'><div style='font-size:0.8rem;color:#64748b;margin-bottom:4px;text-transform:uppercase;'>{title}</div>{h}</div>"
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            content = pills("Technical Matched", cats.get('matched_tech', []), "#10b981") + pills("Soft Skills Matched", cats.get('matched_soft', []), "#6366f1") + pills("Missing Critical", s.get('missing_skills', [])[:8], "#f59e0b")
            if not content: st.info("No sufficient skill data found.")
            else: st.markdown(content, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("### 🏷️ Keyword Cloud")
        top_terms = r.get('top_terms', [])
        if top_terms:
            cloud_html = "<div style='display:flex;flex-wrap:wrap;gap:12px;justify-content:flex-start;padding:1.5rem;background:rgba(255,255,255,0.02);border-radius:16px;border:1px dashed rgba(255,255,255,0.1);'>"
            sizes = ["1.4rem", "1.2rem", "1.1rem", "1.0rem", "0.9rem", "0.85rem"]
            colors = ["#a855f7", "#8b5cf6", "#6366f1", "#06b6d4", "#10b981", "#cbd5e1"]
            for i, term in enumerate(top_terms):
                sz = sizes[i] if i < len(sizes) else "0.8rem"
                cl = colors[i % len(colors)]
                cloud_html += f"<span style='font-size:{sz};color:{cl};opacity:0.9;padding:2px 6px;'>{term}</span>"
            cloud_html += "</div>"
            st.markdown(cloud_html, unsafe_allow_html=True)

        ai_sections = r.get('ai_sections', [])
        if ai_sections:
            st.markdown("### 🤖 AI Content Breakdown")
            st.markdown(
                "<p style='color:#64748b;font-size:0.88rem;margin-bottom:1rem;'>Sentences highlighted by AI likelihood — "
                "<span style='color:#ef4444;'>■</span> High &nbsp;"
                "<span style='color:#f59e0b;'>■</span> Medium &nbsp;"
                "<span style='color:#10b981;'>■</span> Clean</p>",
                unsafe_allow_html=True
            )
            _color_map = {"High": ("#ef444420", "#ef4444"), "Medium": ("#f59e0b18", "#f59e0b"), "Low": ("#10b98112", "#10b981")}
            high_sents = [s for s in ai_sections if s['label'] == 'High']
            med_sents  = [s for s in ai_sections if s['label'] == 'Medium']
            clean_sents = len(ai_sections) - len(high_sents) - len(med_sents)
            st.markdown(f"<p style='color:#94a3b8;font-size:0.82rem;margin-bottom:0.5rem;'>🔴 {len(high_sents)} high-risk &nbsp;·&nbsp; 🟡 {len(med_sents)} medium-risk &nbsp;·&nbsp; 🟢 {clean_sents} clean sentences</p>", unsafe_allow_html=True)
            html_parts = ["<div style='line-height:2.2;padding:1rem;background:rgba(255,255,255,0.02);border-radius:16px;border:1px solid rgba(255,255,255,0.06);'>"]
            for s in ai_sections:
                lbl = s.get('label', 'Low')
                bg, border = _color_map.get(lbl, ("#10b98112", "#10b981"))
                tooltip = ' | '.join(s['flags']) if s['flags'] else 'No AI signals detected'
                html_parts.append(
                    f"<span title='{tooltip}' style='background:{bg};border:1px solid {border}40;"
                    f"border-radius:4px;padding:2px 5px;margin:2px;display:inline;cursor:default;'"
                    f">{s['sentence']}</span> "
                )
            html_parts.append("</div>")
            st.markdown("".join(html_parts), unsafe_allow_html=True)

            flagged = [s for s in ai_sections if s['label'] == 'High']
            if flagged:
                with st.expander(f"⚠️ {len(flagged)} High-Risk Sentence(s) — Click to Review"):
                    for s in flagged:
                        st.markdown(
                            f"<div style='border-left:3px solid #ef4444;padding:8px 12px;margin:6px 0;background:rgba(239,68,68,0.06);border-radius:0 8px 8px 0;'>"
                            f"<div style='color:#f8fafc;font-size:0.92rem;'>{s['sentence']}</div>"
                            f"<div style='color:#ef4444;font-size:0.78rem;margin-top:4px;'>Score: {s['score']}% &nbsp;·&nbsp; {' · '.join(s['flags'])}</div>"
                            f"</div>",
                            unsafe_allow_html=True
                        )

        # ── Email Notification Section ──────────────────────────────────────
        st.markdown("---")
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.5rem;">
            <span style="font-size:1.5rem;">📧</span>
            <h3 style="margin:0;font-size:1.2rem;">Email Notification to Candidate</h3>
        </div>
        <p style="color:#94a3b8;font-size:0.88rem;margin-bottom:1rem;">Send the screening results directly to the candidate's inbox.</p>
        """, unsafe_allow_html=True)

        with st.expander("✉️ Send Email Notification", expanded=False):
            # Try to auto-extract candidate name from original resume text if possible
            default_cname = "Candidate"
            import re
            lines = [l.strip() for l in uploaded_text.split('\n') if l.strip()]
            if lines:
                first_line = re.sub(r'^(candidate|resume|cv|profile)\s*[:—–-]?\s*', '', lines[0], flags=re.I)
                first_line = re.sub(r'[^a-zA-Z\s\.\'-]', '', first_line).strip()
                if 1 <= len(first_line.split()) <= 5:
                    default_cname = first_line

            candidate_name = st.text_input("Candidate Name", value=default_cname, key="email_cand_name")
            candidate_email = st.text_input("Candidate Email *", placeholder="candidate@email.com", key="email_cand_addr")

            if st.button("📨 Send Screening Result Email", type="primary", use_container_width=True, key="send_email_btn"):
                if not candidate_email:
                    st.error("❌ Candidate email is required.")
                elif not getattr(config, 'SMTP_EMAIL', None) or config.SMTP_EMAIL == "your-email@gmail.com":
                    st.error("❌ Server SMTP credentials not configured in config.py.")
                else:
                    cname = candidate_name if candidate_name else "Candidate"
                    try:
                        with st.spinner("Sending email..."):
                            send_notification_email(candidate_email, cname, config.SMTP_EMAIL, config.SMTP_PASSWORD, r)
                        st.success(f"✅ Email sent successfully to **{candidate_email}**!")
                        st.balloons()
                    except smtplib.SMTPAuthenticationError:
                        st.error("❌ Server SMTP authentication failed. Check config.py credentials.")
                    except Exception as e:
                        st.error(f"❌ Failed to send email: {str(e)}")


with tab_batch:
    st.markdown("### 📁 Batch Screening")
    st.info("Uses Global Settings (Sidebar) for Match & AI Thresholds.")

    bjd = st.text_area("Paste Job Description", height=100, key="bjd")
    bfs = st.file_uploader("Upload Resumes (.txt)", accept_multiple_files=True, type=["txt"], key="bfs")

    if st.button("🚀 Run Batch Analysis", type="primary", use_container_width=True):
        if bjd and bfs:
            rows = []
            prog = st.progress(0)
            for i, f in enumerate(bfs):
                res = run_pipeline_wrapper(f.read().decode("utf-8"), bjd, mt, at)
                if res:
                    rows.append({'Candidate': f.name, 'Match Score': res['match_score'], 
                                 'AI Score': res['ai_score'], 'Decision': res['decision']})
                    st.session_state['history'].append({'name': f.name, 'match_score': res['match_score'], 
                                                        'ai_score': res['ai_score'], 'decision': res['decision']})
                prog.progress((i+1)/len(bfs))
            prog.empty()
            st.dataframe(pd.DataFrame(rows).sort_values('Match Score', ascending=False).style.background_gradient(subset=['Match Score'], cmap='Purples'), use_container_width=True)
            

with tab_compare:
    st.markdown("### ⚡ Comparison")
    cjd = st.text_area("Comparsion Job Description", height=80, key="cjd")
    c1, c2 = st.columns(2)
    with c1: t1 = st.text_area("Resume A", height=150, key="t1")
    with c2: t2 = st.text_area("Resume B", height=150, key="t2")
    
    if st.button("⚡ Compare Candidates", type="primary", use_container_width=True):
        if cjd and t1 and t2:
            r1 = run_pipeline_wrapper(t1, cjd, 60, 80)
            r2 = run_pipeline_wrapper(t2, cjd, 60, 80)
            win = 'A' if r1['match_score'] >= r2['match_score'] else 'B'
            
            st.markdown(f"<div style='text-align:center;padding:1rem;background:linear-gradient(90deg,#6366f1,#8b5cf6);border-radius:12px;margin:1rem 0;font-weight:700;font-size:1.2rem;'>🏆 Winner: Candidate {win}</div>", unsafe_allow_html=True)
            
            m1, m2 = st.columns(2)
            for col, r, lbl in [(m1,r1,"A"), (m2,r2,"B")]:
                with col:
                    bord = "2px solid #a855f7" if lbl == win else "1px solid rgba(255,255,255,0.1)"
                    st.markdown(f"<div class='glass-card' style='border:{bord};text-align:center;'><h3>{lbl}</h3><h1>{r['match_score']:.1f}%</h1><p>{len(r['skill_analysis']['matched_skills'])} skills</p></div>", unsafe_allow_html=True)


with tab_tips:
    if st.session_state['result']:
        r = st.session_state['result']
        tips = generate_tips(r['skill_analysis'].get('missing_skills', []), r['match_score'])
        for tip in tips:
            col = "#ef4444" if "High" in tip['priority'] else "#f59e0b"
            st.markdown(f"<div class='glass-card' style='border-left:4px solid {col}'><b>{tip['skill']}</b>: {tip['tip']}</div>", unsafe_allow_html=True)
    else: st.info("Run analysis first.")

st.markdown("<div style='text-align:center;margin-top:3rem;color:#475569;font-size:0.8rem;'>AI Screener Pro v5.3 · 2026</div>", unsafe_allow_html=True)
