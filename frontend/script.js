// ════════════════════════════════════════
// Theme Toggle (Light ↔ Dark)
// ════════════════════════════════════════
(function initThemeToggle() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) return;

    toggleBtn.addEventListener('click', () => {
        const html = document.documentElement;

        // Enable smooth transition
        html.classList.add('theme-transition');

        // Toggle dark class
        html.classList.toggle('dark');

        // Save preference
        const isDark = html.classList.contains('dark');
        localStorage.setItem('recruitai_theme', isDark ? 'dark' : 'light');

        // Remove transition class after animation completes
        setTimeout(() => html.classList.remove('theme-transition'), 500);
    });
})();


// ════════════════════════════════════════
// Tab Navigation
// ════════════════════════════════════════
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPages = document.querySelectorAll('.tab-page');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        tabPages.forEach(p => p.classList.remove('active'));

        btn.classList.add('active');
        const target = document.getElementById(btn.dataset.tab);
        if (target) target.classList.add('active');

        if (btn.dataset.tab === 'tab-history') renderHistory();
        if (btn.dataset.tab === 'tab-insights') renderInsights();
    });
});


// ════════════════════════════════════════
// Character Counters
// ════════════════════════════════════════
function updateCounts() {
    document.getElementById('screen-resume-count').textContent =
        document.getElementById('screen-resume').value.length;
    document.getElementById('screen-jd-count').textContent =
        document.getElementById('screen-jd').value.length;
}
document.getElementById('screen-resume').addEventListener('input', updateCounts);
document.getElementById('screen-jd').addEventListener('input', updateCounts);


// ════════════════════════════════════════
// Sample Data — Domain-Aware System (55 Industries × 3 Levels)
// ════════════════════════════════════════

function populateDomainSelector() {
    const sel = document.getElementById('domain-selector');
    if (!sel || typeof DOMAIN_LIST === 'undefined') return;
    DOMAIN_LIST.forEach(domain => {
        const opt = document.createElement('option');
        opt.value = domain;
        opt.textContent = domain;
        sel.appendChild(opt);
    });
    // Wire up level radio buttons to reload data when changed
    document.querySelectorAll('input[name="exp-level"]').forEach(radio => {
        radio.addEventListener('change', () => {
            const sel = document.getElementById('domain-selector');
            if (sel && sel.value && sel.value !== '') loadDomainSample();
        });
    });
}

function getSelectedLevel() {
    const checked = document.querySelector('input[name="exp-level"]:checked');
    return checked ? checked.value : 'mid';
}

function loadDomainSample() {
    if (typeof SAMPLE_DATA === 'undefined') return;

    const sel = document.getElementById('domain-selector');
    let domain = sel ? sel.value : '';
    if (!domain) return;

    // Random domain
    if (domain === '__random__') {
        const keys = Object.keys(SAMPLE_DATA);
        domain = keys[Math.floor(Math.random() * keys.length)];
        sel.value = domain;
    }

    const data = SAMPLE_DATA[domain];
    if (!data) return;

    const level = getSelectedLevel();
    const resume = data[level] || data.mid || '';
    const jd = data.jd || '';

    document.getElementById('screen-resume').value = resume.trim();
    document.getElementById('screen-jd').value = jd.trim();
    updateCounts();
}

function loadSampleData() {
    if (typeof SAMPLE_DATA === 'undefined' || typeof DOMAIN_LIST === 'undefined') {
        document.getElementById('screen-resume').value = 'Sample data not available.';
        return;
    }
    const randomDomain = DOMAIN_LIST[Math.floor(Math.random() * DOMAIN_LIST.length)];
    const sel = document.getElementById('domain-selector');
    if (sel) sel.value = randomDomain;
    loadDomainSample();
}

// Auto-populate domain dropdown on load
populateDomainSelector();



// ════════════════════════════════════════
// Helpers — show / hide sections
// ════════════════════════════════════════
const inputSec = document.getElementById('screen-input-section');
const loader = document.getElementById('screen-loader');
const errorBox = document.getElementById('screen-error');
const errorMsg = document.getElementById('screen-error-msg');
const resultsWrap = document.getElementById('screen-results');

function showLoader() {
    inputSec.classList.add('hidden');
    hideError();
    resultsWrap.classList.remove('visible');
    loader.classList.add('visible');
}
function hideLoader() {
    loader.classList.remove('visible');
}
function showError(msg) {
    errorMsg.textContent = msg;
    errorBox.classList.add('visible');
    inputSec.classList.remove('hidden');
}
function hideError() {
    errorBox.classList.remove('visible');
}
function showResults() {
    resultsWrap.classList.add('visible');
}


// ════════════════════════════════════════
// Single Screen
// ════════════════════════════════════════
let lastScreenResult = null;

document.getElementById('screen-btn').addEventListener('click', async () => {
    const resumeText = document.getElementById('screen-resume').value.trim();
    const jdText = document.getElementById('screen-jd').value.trim();

    if (!resumeText || !jdText) {
        alert('Please provide both a Resume and a Job Description.');
        return;
    }

    showLoader();

    try {
        const settings = getSettings();
        const res = await fetch('/api/screen', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                resume: resumeText,
                job_description: jdText,
                match_threshold: settings.matchThreshold,
                ai_threshold: settings.aiThreshold
            })
        });
        const data = await res.json();
        console.log('FULL RESPONSE:', data);
        console.log('SENTENCE DATA:', data.sentence_analysis);

        if (!res.ok || !data.success) throw new Error(data.error || 'Analysis failed.');

        renderResults(data);
        lastScreenResult = { ...data, timestamp: new Date().toISOString() };

        // Auto-track shortlisted candidate
        if (data.decision === 'SHORTLISTED') {
            recordShortlist();
        }

        // Store insights data for the Insights tab
        lastInsightsData = {
            tips: data.tips || [],
            general_advice: data.general_advice || [],
            match_score: data.match_score,
            ai_score: data.ai_score,
            decision: data.decision,
            skill_analysis: data.skill_analysis || {}
        };

    } catch (err) {
        showError(err.message);
    } finally {
        hideLoader();
    }
});


// ════════════════════════════════════════
// Render Results
// ════════════════════════════════════════
function renderResults(data) {
    const pass = data.decision === 'SHORTLISTED';

    // Decision banner
    const iconWrap = document.getElementById('res-icon-wrap');
    const iconEl = document.getElementById('res-icon');
    iconWrap.className = 'decision-icon w-14 h-14 rounded-full flex items-center justify-center flex-shrink-0 ' + (pass ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-600');
    iconEl.textContent = pass ? 'task_alt' : 'cancel';

    const decisionEl = document.getElementById('res-decision');
    decisionEl.textContent = data.decision;
    decisionEl.className = 'text-2xl font-extrabold tracking-tight ' + (pass ? 'text-emerald-600' : 'text-red-600');

    document.getElementById('res-reason').textContent = data.reason || '';

    // Confidence badge
    const confEl = document.getElementById('res-confidence');
    if (confEl && data.confidence) {
        confEl.textContent = data.confidence + ' Confidence';
        const confColors = {
            'High': 'bg-emerald-100 text-emerald-700 border border-emerald-300',
            'Medium': 'bg-amber-100 text-amber-700 border border-amber-300',
            'Low': 'bg-red-100 text-red-700 border border-red-300',
        };
        confEl.className = 'text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full ' + (confColors[data.confidence] || confColors['Medium']);
    }

    // Scores
    const matchEl = document.getElementById('res-match-val');
    matchEl.textContent = data.match_score.toFixed(1) + '%';
    matchEl.className = 'score-value text-3xl font-extrabold leading-none ' + scoreClass(data.match_score, 60, 40);

    const aiEl = document.getElementById('res-ai-val');
    aiEl.textContent = data.ai_score.toFixed(1) + '%';
    aiEl.className = 'score-value text-3xl font-extrabold leading-none ' + (data.ai_score < 40 ? 'good' : data.ai_score < 70 ? 'warn' : 'bad');

    // Vacancies from settings
    const settings = getSettings();
    const totalVac = settings.jobVacancies;
    const filledVac = settings.filledVacancies;
    const remainingVac = Math.max(0, totalVac - filledVac);
    const vacEl = document.getElementById('res-vacancies-val');
    const vacDivider = document.getElementById('res-vacancies-divider');
    const vacWrap = document.getElementById('res-vacancies-wrap');
    const vacStatus = document.getElementById('res-vacancies-status');
    if (vacEl) {
        vacEl.textContent = remainingVac + '/' + totalVac;
        if (vacDivider) vacDivider.style.display = '';
        if (vacWrap) vacWrap.style.display = '';

        // Color code: green = plenty, amber = few left, red = none left
        if (remainingVac === 0) {
            vacEl.className = 'text-3xl font-extrabold leading-none text-red-600';
            if (vacStatus) { vacStatus.textContent = 'ALL FILLED'; vacStatus.className = 'text-[10px] font-semibold mt-1 tracking-wide text-red-600'; }
        } else if (remainingVac <= Math.ceil(totalVac * 0.25)) {
            vacEl.className = 'text-3xl font-extrabold leading-none text-amber-600';
            if (vacStatus) { vacStatus.textContent = 'FEW LEFT'; vacStatus.className = 'text-[10px] font-semibold mt-1 tracking-wide text-amber-600'; }
        } else {
            vacEl.className = 'text-3xl font-extrabold leading-none text-primary';
            if (vacStatus) { vacStatus.textContent = 'OPEN'; vacStatus.className = 'text-[10px] font-semibold mt-1 tracking-wide text-emerald'; }
        }
    }

    // ── Domain Badge ──
    const domainBadge = document.getElementById('res-domain-badge');
    const domainRow = document.getElementById('res-domain-row');
    const methodBadge = document.getElementById('res-match-method');
    const mismatchEl = document.getElementById('res-domain-mismatch');
    const mismatchDiv = document.getElementById('res-domain-mismatch-divider');
    const mismatchText = document.getElementById('res-domain-mismatch-text');

    if (domainBadge && data.domain) {
        const d = data.domain.primary || {};
        domainBadge.textContent = (d.icon || '📄') + ' ' + (d.label || 'General');
        if (domainRow) domainRow.style.display = '';

        // Domain mismatch warning
        if (data.domain.domain_mismatch && data.domain.mismatch_note) {
            if (mismatchEl) mismatchEl.style.display = 'flex';
            if (mismatchDiv) mismatchDiv.style.display = '';
            if (mismatchText) mismatchText.textContent = data.domain.mismatch_note;
        } else {
            if (mismatchEl) mismatchEl.style.display = 'none';
            if (mismatchDiv) mismatchDiv.style.display = 'none';
        }
    }

    if (methodBadge && data.match_method) {
        const methodLabels = {
            'sentence-bert': '🧠 Sentence-BERT',
            'tfidf-fallback': '📊 TF-IDF',
            'tfidf': '📊 TF-IDF',
        };
        methodBadge.textContent = methodLabels[data.match_method] || data.match_method;
    }

    // Skills
    renderChips('res-matched-skills', data.skill_analysis?.matched_skills || [], 'chip chip-green', 'No matched skills detected.');
    renderChips('res-missing-skills', data.skill_analysis?.missing_skills || [], 'chip chip-gray', 'All required skills matched! ✅');

    // AI Bar — use classification from API if available, else derive from score
    const pct = Math.min(100, Math.max(0, data.ai_score));
    const bar = document.getElementById('res-ai-bar');
    const aiClassification = data.details?.ai?.classification || '';
    const aiExplanation = data.details?.ai?.explanation || '';
    const aiDisclaimer = data.details?.ai?.disclaimer || 'This is a probabilistic estimate and may not be fully accurate.';
    const aiObservations = data.details?.ai?.observations || [];

    document.getElementById('res-ai-bar-lbl').textContent = pct.toFixed(1) + '% likelihood';
    setTimeout(() => { bar.style.width = pct + '%'; }, 60);

    if (pct >= 70) {
        bar.style.background = '#dc2626';
        setVerdict('res-ai-verdict',
            aiExplanation || 'Several indicators suggest this content may have been generated or heavily assisted by AI tools. Manual review is recommended.',
            '#dc2626');
    } else if (pct >= 40) {
        bar.style.background = '#d97706';
        setVerdict('res-ai-verdict',
            aiExplanation || 'The content contains mixed characteristics. Some patterns suggest possible AI assistance, but this is not conclusive.',
            '#d97706');
    } else {
        bar.style.background = '#059669';
        setVerdict('res-ai-verdict',
            aiExplanation || 'The writing patterns in this resume are consistent with human-authored content. Natural variation in structure and vocabulary was observed.',
            '#059669');
    }

    // AI Stats
    const statsEl = document.getElementById('res-ai-stats');
    const d = data.details?.ai;
    if (d) {
        const sb = d.signal_breakdown || {};
        statsEl.innerHTML = `
            <div class="stat-box">
                <div class="stat-box-label">Sentences</div>
                <div class="stat-box-val">${d.sentence_count || 0}</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-label">Avg Length</div>
                <div class="stat-box-val">${d.avg_sentence_length ? Number(d.avg_sentence_length).toFixed(1) : 0}</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-label">Length Variance</div>
                <div class="stat-box-val">${d.sentence_length_variance ? Number(d.sentence_length_variance).toFixed(1) : 0}</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-label">Lex. Diversity</div>
                <div class="stat-box-val">${d.lexical_diversity_ttr ? (d.lexical_diversity_ttr * 100).toFixed(1) + '%' : '—'}</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-label">Opener Variety</div>
                <div class="stat-box-val">${d.opener_diversity != null ? (d.opener_diversity * 100).toFixed(0) + '%' : '—'}</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-label">Transition Density</div>
                <div class="stat-box-val">${d.transition_density != null ? (d.transition_density * 100).toFixed(0) + '%' : '—'}</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-label">Buzzword Score</div>
                <div class="stat-box-val">${d.buzzword_score != null ? Number(d.buzzword_score).toFixed(0) : '—'}</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-label">Punct. Diversity</div>
                <div class="stat-box-val">${d.punctuation_diversity != null ? (d.punctuation_diversity * 100).toFixed(0) + '%' : '—'}</div>
            </div>`;

        // Add signal breakdown bars if available
        if (Object.keys(sb).length) {
            const signalNames = {
                buzzword_score: 'AI Buzzwords',
                fingerprint_score: 'ChatGPT Fingerprints',
                hyper_polish_score: 'Hyper-Polish',
                generic_score: 'Generic Claims',
                transition_score: 'Transition Overuse',
                variance_score: 'Length Uniformity',
                diversity_score: 'Vocab Repetition',
                punct_score: 'Punct Simplicity',
                burstiness_score: 'Burstiness',
                predictability_score: 'Predictability',
            };
            let barsHtml = '<div style="grid-column:1/-1;margin-top:8px"><div class="stat-box-label" style="margin-bottom:8px">🔬 Per-Signal AI Scores</div>';
            for (const [key, label] of Object.entries(signalNames)) {
                const val = sb[key] ?? 0;
                const color = val >= 60 ? '#dc2626' : val >= 35 ? '#d97706' : '#059669';
                barsHtml += `
                    <div class="section-score-row" style="margin-bottom:4px">
                        <span class="section-score-name" style="min-width:130px;font-size:11px">${label}</span>
                        <div class="section-score-bar-track">
                            <div class="section-score-bar-fill" style="width:${val}%;background:${color}"></div>
                        </div>
                        <span class="section-score-val" style="font-size:11px">${val.toFixed(0)}%</span>
                    </div>`;
            }
            barsHtml += '</div>';
            statsEl.innerHTML += barsHtml;
        }
    } else {
        statsEl.innerHTML = '<div class="text-on-surface-variant text-sm" style="grid-column:1/-1">Insufficient data for detailed analysis.</div>';
    }

    // ── AI Explanation + Observations + Disclaimer block ──
    const aiExpWrap = document.getElementById('res-ai-explanation');
    if (aiExpWrap) {
        const obsHtml = aiObservations.length
            ? '<ul style="margin:8px 0 0 0;padding-left:16px;font-size:12px;color:#475569">' +
            aiObservations.map(o => `<li style="margin-bottom:4px">${esc(o)}</li>`).join('') +
            '</ul>'
            : '';
        aiExpWrap.innerHTML = `
            <div style="margin-top:12px;padding:12px 14px;background:#f8fafc;border-radius:8px;border-left:3px solid ${pct >= 70 ? '#dc2626' : pct >= 40 ? '#d97706' : '#059669'}">
                <div style="font-size:12px;font-weight:700;color:#334155;margin-bottom:4px">AI Likelihood: ${pct.toFixed(1)}% &nbsp;·&nbsp; Category: ${aiClassification || (pct >= 70 ? 'Likely AI' : pct >= 40 ? 'Uncertain' : 'Likely Human')}</div>
                ${obsHtml}
                <div style="font-size:11px;color:#94a3b8;margin-top:8px;font-style:italic">&#9432; ${esc(aiDisclaimer)}</div>
            </div>`;
        aiExpWrap.style.display = '';
    }

    // Keywords
    const kwEl = document.getElementById('res-keywords');
    const kws = data.top_keywords || [];
    const kwColors = ['chip-purple', 'chip-indigo', 'chip-cyan', 'chip-green'];
    kwEl.innerHTML = kws.length
        ? kws.map((kw, i) => `<span class="chip kw-chip ${kwColors[i % kwColors.length]}">${kw}</span>`).join('')
        : '<span class="chip chip-none">No keywords generated.</span>';

    // ── Sentence-Level AI Analysis ──────────────────────────────────────
    console.log('FULL RESPONSE:', data);
    console.log('SENTENCE DATA:', data.sentence_analysis);

    // STEP 6 hard-test override: set window.SA_FORCE_TEST = true in console to verify UI
    if (window.SA_FORCE_TEST) {
        console.warn('[HARD TEST MODE] Overriding sentence_analysis with synthetic data');
        renderSentences([
            { text: 'This is definitely AI generated sentence.', label: 'ai', score: 72 },
            { text: 'This looks somewhat structured and polished.', label: 'uncertain', score: 28 },
            { text: 'I built this project myself from scratch.', label: 'human', score: 5 }
        ]);
    } else {
        renderSentences(data.sentence_analysis || []);
    }

    // ── Resume AI Heatmap ──
    renderHeatmap(data.ai_sections || [], data.details?.ai || {}, data.ai_score || 0);

    // ── Parsed Resume Profile ──
    renderParsedResume(data.parsed_resume || {});

    // ── Charts ──
    renderCharts(data);

    // Reset Save button
    const saveBtn = document.getElementById('btn-save-hist');
    saveBtn.innerHTML = '<span class="material-symbols-outlined">bookmark</span> Save to History';
    saveBtn.disabled = false;

    showResults();
}

function scoreClass(val, goodThresh, warnThresh) {
    if (val >= goodThresh) return 'good';
    if (val >= warnThresh) return 'warn';
    return 'bad';
}

function renderChips(elId, items, cls, emptyMsg) {
    const el = document.getElementById(elId);
    el.innerHTML = items.length
        ? items.map(s => `<span class="${cls}">${s}</span>`).join('')
        : `<span class="chip chip-none">${emptyMsg}</span>`;
}

function setVerdict(elId, text, color) {
    const el = document.getElementById(elId);
    el.textContent = text;
    el.style.color = color;
}


// ════════════════════════════════════════════════════════════════════════
// Sentence-Level AI Detection
//   level: "HIGH" → 🔴 RED (bg-red-100)  |  "MEDIUM" → 🟡 YELLOW (bg-yellow-100)
//   NON-NEGOTIABLE: if AI score > 0, at least one sentence MUST be colored.
//   Frontend renders ALL sentences returned by the backend — no filtering.
// ════════════════════════════════════════════════════════════════════════
function renderSentences(sentenceData) {
    const container = document.getElementById('sentence-analysis');
    if (!container) {
        console.error('renderSentences: #sentence-analysis div NOT FOUND in DOM!');
        return;
    }

    console.log('renderSentences called with', sentenceData ? sentenceData.length : 0, 'sentences');

    // Only show the green "no patterns" state when the backend genuinely
    // returned nothing (i.e. AI score == 0 on a clean document).
    if (!sentenceData || !sentenceData.length) {
        container.innerHTML =
            '<div style="padding:12px;background:#ecfdf5;border-radius:8px;' +
            'border-left:4px solid #10b981;font-size:13px;color:#065f46">' +
            '🟢 <strong>No AI patterns detected.</strong> ' +
            'This document scored 0% AI likelihood — no sentences to highlight.</div>';
        return;
    }

    container.innerHTML = '';

    // ── Resolve level from item.level or fall back to item.label ────────
    function resolveLevel(item) {
        if (item.level) return item.level;
        const lbl = item.label || 'human';
        if (lbl === 'ai')        return 'HIGH';
        if (lbl === 'uncertain') return 'MEDIUM';
        return 'LOW';
    }

    const highCount = sentenceData.filter(s => resolveLevel(s) === 'HIGH').length;
    const midCount  = sentenceData.filter(s => resolveLevel(s) === 'MEDIUM').length;
    const lowCount  = sentenceData.filter(s => resolveLevel(s) === 'LOW').length;

    // ── Legend / stats bar ───────────────────────────────────────────────
    const statsBar = document.createElement('div');
    statsBar.style.cssText =
        'display:flex;gap:14px;flex-wrap:wrap;align-items:center;' +
        'margin-bottom:14px;padding:10px 16px;' +
        'background:#f8fafc;border-radius:10px;' +
        'border:1px solid #e2e8f0;font-size:12px;font-weight:600;';
    statsBar.innerHTML =
        (highCount ? `<span style="color:#dc2626;">🔴 <strong>${highCount}</strong> High AI likelihood</span>` : '') +
        (midCount  ? `<span style="color:#d97706;">🟡 <strong>${midCount}</strong> Medium indicators</span>` : '') +
        (lowCount  ? `<span style="color:#059669;">🟢 <strong>${lowCount}</strong> Human-like</span>` : '') +
        `<span style="margin-left:auto;color:#64748b;font-weight:400;">${sentenceData.length} sentence${sentenceData.length !== 1 ? 's' : ''} highlighted</span>`;
    container.appendChild(statsBar);

    // ── Render ALL returned sentences (no client-side filtering) ─────────
    const textWrap = document.createElement('div');
    textWrap.style.cssText = 'line-height:2.6;font-size:0.875rem;word-break:break-word;';
    container.appendChild(textWrap);

    // COLOR RULES:
    //   HIGH   → RED    (bg-red-200  / text-red-800)
    //   MEDIUM → YELLOW (bg-yellow-200 / text-yellow-800)
    //   LOW    → GREEN  (subtle, rarely returned)
    const palette = {
        HIGH: {
            bg:      '#fee2e2',            // red-100
            bgHover: '#fecaca',            // red-200
            border:  '2px solid #ef4444', // red-500
            text:    '#991b1b',            // red-800
            tip:     '🔴 High AI likelihood',
        },
        MEDIUM: {
            bg:      '#fef9c3',            // yellow-100
            bgHover: '#fef08a',            // yellow-200
            border:  '2px solid #eab308', // yellow-500
            text:    '#713f12',            // yellow-900
            tip:     '🟡 Medium AI indicators',
        },
        LOW: {
            bg:      'rgba(5,150,105,0.10)',
            bgHover: 'rgba(5,150,105,0.20)',
            border:  '2px solid rgba(5,150,105,0.50)',
            text:    '#065f46',
            tip:     '🟢 Human-like writing',
        },
    };

    sentenceData.forEach(item => {
        if (!item.text || !item.text.trim()) return;

        const level  = resolveLevel(item);
        const score  = Number(item.score || 0).toFixed(1);
        const cfg    = palette[level] || palette.MEDIUM;
        const tipTxt = `${cfg.tip} — AI Score: ${score}%`;

        const span = document.createElement('span');
        span.style.backgroundColor = cfg.bg;
        span.style.borderBottom    = cfg.border;
        span.style.borderRadius    = '4px';
        span.style.padding         = '3px 7px';
        span.style.margin          = '0 3px 6px 0';
        span.style.display         = 'inline';
        span.style.cursor          = 'help';
        span.style.transition      = 'background-color 0.15s ease';
        span.style.color           = cfg.text;
        span.style.fontWeight      = level === 'HIGH' ? '600' : 'inherit';
        span.title                 = tipTxt;
        span.textContent           = item.text.trim() + ' ';

        span.addEventListener('mouseenter', () => { span.style.backgroundColor = cfg.bgHover; });
        span.addEventListener('mouseleave',  () => { span.style.backgroundColor = cfg.bg; });

        textWrap.appendChild(span);
    });

    // ── Explanation disclaimer ────────────────────────────────────────────
    const disclaimer = document.createElement('p');
    disclaimer.style.cssText =
        'margin-top:14px;padding:10px 14px;font-size:11.5px;' +
        'color:#64748b;font-style:italic;' +
        'background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0;';
    disclaimer.textContent =
        'ℹ Only sentences with meaningful AI patterns are highlighted. ' +
        'When overall AI score is moderate, top contributing sentences are highlighted ' +
        'even if individual scores are not very high.';
    container.appendChild(disclaimer);

    console.log(`renderSentences COMPLETE: HIGH=${highCount} / MEDIUM=${midCount} / LOW=${lowCount}`);
}



// ════════════════════════════════════════
// Resume AI Heatmap
// ════════════════════════════════════════
function renderHeatmap(sections, aiDetails, overallScore) {
    aiDetails = aiDetails || {};
    overallScore = overallScore || 0;

    const heatmapEl = document.getElementById('res-heatmap');
    const summaryEl = document.getElementById('res-heatmap-summary');
    const flaggedListEl = document.getElementById('res-flagged-lines');

    if (!sections || !sections.length) {
        heatmapEl.innerHTML = '<span style="color:var(--muted)">No sentence-level data available.</span>';
        summaryEl.innerHTML = '';
        if (flaggedListEl) flaggedListEl.innerHTML = '';
        return;
    }

    // Escape HTML to prevent XSS
    function esc(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    let aiCount = 0, maybeCount = 0, humanCount = 0;
    const flaggedLines = [];   // High + Medium sentences for the detail panel
    const allScored = [];   // All non-excluded sentences with their scores (for fallback)

    // ── classMap: keys match backend labels ('High'/'Medium'/'Low') ──
    const classMap = {
        'High': 'sent-ai-yes',    // Red   — definite AI signal
        'Medium': 'sent-ai-maybe',  // Amber — suspicious
        'Low': 'sent-ai-no',     // Green — appears human
    };

    const html = sections.map((s, i) => {
        const label = s.label || 'Low';
        const cls = classMap[label] || 'sent-ai-no';
        const score = (s.score || 0).toFixed(1);
        const lineNum = s.sentence_number || (i + 1);
        const excluded = s.is_excluded || false;
        const flags = (s.flags && s.flags.length) ? s.flags.join(' · ') : 'No AI signals detected';
        const tip = excluded
            ? `Line ${lineNum}: Personal info / section header — excluded from AI analysis (always Human-Written)`
            : `Line ${lineNum} | AI Score: ${score}% — ${flags}`;

        if (!excluded) allScored.push({ lineNum, score: parseFloat(score), flags, label, sentence: s.sentence });

        if (label === 'High') { aiCount++; if (!excluded) flaggedLines.push({ lineNum, score, flags, label, sentence: s.sentence }); }
        else if (label === 'Medium') { maybeCount++; if (!excluded) flaggedLines.push({ lineNum, score, flags, label, sentence: s.sentence }); }
        else humanCount++;

        return `<span class="${cls}" title="${esc(tip)}" data-line="${lineNum}"><sup style="font-size:9px;opacity:0.55;vertical-align:super;margin-right:1px">${lineNum}</sup>${esc(s.sentence)}</span> `;
    }).join('');

    heatmapEl.innerHTML = html;

    summaryEl.innerHTML = `
        <span style="color:#ef4444;font-weight:700">&#9679; <strong>${aiCount}</strong> Indicators observed (High)</span>
        <span style="color:#d97706;font-weight:600">&#9679; <strong>${maybeCount}</strong> Patterns noted (Medium)</span>
        <span style="color:#10b981;font-weight:500">&#9679; <strong>${humanCount}</strong> Appears human-written</span>
        <span style="margin-left:auto;font-weight:600">Total: <strong>${sections.length}</strong> sentences</span>
    `;

    if (!flaggedListEl) return;

    // ── Helper: render a flagged-line card ──
    function flagCard(f, note) {
        const isHigh = f.label === 'High';
        const borderColor = isHigh ? '#ef4444' : '#f59e0b';
        const bgColor = isHigh ? '#fef2f2' : '#fffbeb';
        const textColor = isHigh ? '#991b1b' : '#92400e';
        const badgeBg = isHigh ? '#ef4444' : '#f59e0b';
        const badgeLabel = isHigh ? 'Indicators Observed' : 'Patterns Noted';
        const scoreColor = isHigh ? '#dc2626' : '#d97706';
        return `
            <div style="border-left:4px solid ${borderColor};background:${bgColor};border-radius:0 10px 10px 0;padding:14px 18px;margin-bottom:10px">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap">
                    <span style="font-size:11px;font-weight:800;color:#64748b;letter-spacing:0.5px">LINE ${f.lineNum}</span>
                    <span style="background:${badgeBg};color:#fff;font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;text-transform:uppercase;letter-spacing:0.5px">${badgeLabel}</span>
                    <span style="font-size:11px;font-weight:700;color:${scoreColor};margin-left:auto">AI Score: ${f.score}%</span>
                </div>
                <div style="font-size:13px;color:${textColor};font-style:italic;line-height:1.5;margin-bottom:8px;border-left:2px solid ${borderColor};padding-left:10px">"${esc(f.sentence)}"</div>
                <div style="font-size:11px;color:#64748b;display:flex;align-items:flex-start;gap:6px">
                    <span style="flex-shrink:0;font-weight:700">🔍 Why flagged:</span>
                    <span>${esc(f.flags)}</span>
                </div>
                ${note ? `<div style="font-size:11px;color:#94a3b8;margin-top:6px;font-style:italic">${note}</div>` : ''}
            </div>`;
    }

    const introNote = `
        <div style="font-size:12px;color:#64748b;margin-bottom:12px;padding:10px 14px;background:#fffbeb;border-radius:8px;border-left:3px solid #f59e0b">
            <strong>ℹ️ Note:</strong> Names, emails, phone numbers, LinkedIn/GitHub links, and section headers
            are <strong>automatically excluded</strong> from AI analysis — they always show as Human-Written (green).
            Only the <em>written content</em> of your resume is analyzed.
        </div>`;

    if (flaggedLines.length > 0) {
        // ── Standard case: show flagged lines ──
        flaggedListEl.innerHTML = introNote + flaggedLines.map(f => flagCard(f, '')).join('');

    } else if (overallScore > 5) {
        // ── Statistical-signal case: overall AI score exists but no per-line patterns ──
        // The score comes from DOCUMENT-LEVEL statistical signals (sentence variance,
        // vocabulary uniformity, repetition patterns). No sentence reached the
        // flagging threshold, so we explain this clearly without showing low-score lines.

        const sb = aiDetails.signal_breakdown || {};
        const sigLabels = {
            predictability_score: 'Word Predictability (common word density)',
            burstiness_score: 'Burstiness (uniform AI-phrase distribution)',
            variance_score: 'Sentence Length Uniformity',
            diversity_score: 'Vocabulary Repetition (low TTR)',
            punct_score: 'Punctuation Simplicity',
            buzzword_score: 'AI Buzzwords',
            fingerprint_score: 'ChatGPT Fingerprint Phrases',
            transition_score: 'Transition Word Overuse',
        };

        const topSignals = Object.entries(sigLabels)
            .map(([k, label]) => ({ label, val: sb[k] ?? 0 }))
            .filter(s => s.val >= 15)
            .sort((a, b) => b.val - a.val);

        const signalBarsHtml = topSignals.length ? `
            <div style="margin-top:14px;margin-bottom:8px;font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.6px">📊 Document-Level Signals Driving the ${overallScore.toFixed(1)}% AI Score:</div>
            ${topSignals.map(s => {
            const color = s.val >= 60 ? '#dc2626' : s.val >= 35 ? '#d97706' : '#64748b';
            return `
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
                        <span style="font-size:11px;color:#475569;min-width:220px">${esc(s.label)}</span>
                        <div style="flex:1;height:8px;background:#e2e8f0;border-radius:8px;overflow:hidden">
                            <div style="height:100%;width:${s.val}%;background:${color};border-radius:8px;transition:width 1s ease"></div>
                        </div>
                        <span style="font-size:11px;font-weight:700;color:${color};min-width:32px;text-align:right">${s.val.toFixed(0)}</span>
                    </div>`;
        }).join('')}
        ` : '';

        flaggedListEl.innerHTML = `
            <div style="padding:14px 16px;background:#fff7ed;border:1px solid #fed7aa;border-radius:10px;margin-bottom:14px">
                <div style="font-size:13px;font-weight:700;color:#9a3412;margin-bottom:4px">
                    📈 ${overallScore.toFixed(1)}% AI Score — Driven by Statistical Document Patterns
                </div>
                <div style="font-size:12px;color:#92400e;line-height:1.6">
                    No individual sentences crossed the AI flagging threshold. The score reflects
                    <strong>whole-document statistical signals</strong> — things like how predictable the vocabulary is,
                    how uniformly sentences are structured, and the density of formal language.
                    Only sentences with meaningful AI patterns are highlighted. Low overall AI scores may come
                    from weak statistical signals across the document rather than specific sentences.
                </div>
                ${signalBarsHtml}
            </div>
            ${introNote}`;
    } else {
        // ── Clean case: score is low and no lines flagged ──
        flaggedListEl.innerHTML = `
            <div style="display:flex;align-items:center;gap:10px;padding:14px 16px;background:#ecfdf5;border:1px solid #a7f3d0;border-radius:10px;color:#065f46;font-size:13px;font-weight:600">
                <span style="font-size:18px">&#10003;</span>
                No significant AI indicators detected in individual lines. Content appears consistent with human authorship.
            </div>`;
    }
}


// ════════════════════════════════════════
// Parsed Resume Profile
// ════════════════════════════════════════
function renderParsedResume(parsed) {
    const card = document.getElementById('res-parsed-resume-card');
    if (!parsed || !parsed.stats) {
        if (card) card.style.display = 'none';
        return;
    }
    if (card) card.style.display = '';

    // Reset collapse state
    const detailsWrap = document.getElementById('parsed-details-wrap');
    const toggleIcon = document.getElementById('toggle-parsed-icon');
    const toggleBtn = document.getElementById('toggle-parsed-btn');
    if (detailsWrap) detailsWrap.style.display = 'none';
    if (toggleIcon) toggleIcon.textContent = 'expand_more';
    if (toggleBtn) toggleBtn.innerHTML = '<span class="material-symbols-outlined text-sm" id="toggle-parsed-icon">expand_more</span> Show Details';

    // ── Contact Info ──
    const contactEl = document.getElementById('res-contact-info');
    const c = parsed.contact || {};
    const contactLines = [];
    if (c.name) contactLines.push(`<div class="flex items-center gap-2"><span class="material-symbols-outlined text-sm text-primary">person</span><strong>${esc(c.name)}</strong></div>`);
    if (c.email) contactLines.push(`<div class="flex items-center gap-2"><span class="material-symbols-outlined text-sm text-primary">mail</span>${esc(c.email)}</div>`);
    if (c.phone) contactLines.push(`<div class="flex items-center gap-2"><span class="material-symbols-outlined text-sm text-primary">phone</span>${esc(c.phone)}</div>`);
    if (c.linkedin) contactLines.push(`<div class="flex items-center gap-2"><span class="material-symbols-outlined text-sm text-primary">link</span>${esc(c.linkedin)}</div>`);
    if (c.github) contactLines.push(`<div class="flex items-center gap-2"><span class="material-symbols-outlined text-sm text-primary">code</span>${esc(c.github)}</div>`);
    contactEl.innerHTML = contactLines.length
        ? contactLines.join('')
        : '<span class="text-xs text-on-surface-variant">No contact info detected</span>';

    // ── Quick Stats ──
    const statsEl = document.getElementById('res-resume-stats');
    const s = parsed.stats || {};
    statsEl.innerHTML = `
        <div class="stat-box" style="padding:10px">
            <div class="stat-box-label">Words</div>
            <div class="stat-box-val" style="font-size:16px">${s.total_words || 0}</div>
        </div>
        <div class="stat-box" style="padding:10px">
            <div class="stat-box-label">Sections</div>
            <div class="stat-box-val" style="font-size:16px">${s.section_count || 0}</div>
        </div>
        <div class="stat-box" style="padding:10px">
            <div class="stat-box-label">Exp. Years</div>
            <div class="stat-box-val" style="font-size:16px">${s.exp_years_est || 0}${s.exp_years_est ? '+' : ''}</div>
        </div>
        <div class="stat-box" style="padding:10px">
            <div class="stat-box-label">Certs</div>
            <div class="stat-box-val" style="font-size:16px">${s.cert_count || 0}</div>
        </div>
    `;

    // ── Section Scores ──
    const scoresEl = document.getElementById('res-section-scores');
    const scoresWrap = document.getElementById('res-section-scores-wrap');
    const scores = parsed.section_scores || {};
    const scoreKeys = Object.keys(scores);
    if (scoreKeys.length) {
        scoresWrap.style.display = '';
        scoresEl.innerHTML = scoreKeys.map(key => {
            const val = scores[key];
            const color = val >= 60 ? '#059669' : val >= 30 ? '#d97706' : '#dc2626';
            return `
                <div class="section-score-row">
                    <span class="section-score-name">${esc(key)}</span>
                    <div class="section-score-bar-track">
                        <div class="section-score-bar-fill" style="width:0%;background:${color}"></div>
                    </div>
                    <span class="section-score-val">${val.toFixed(1)}%</span>
                </div>`;
        }).join('');
        // Animate bars
        setTimeout(() => {
            scoresEl.querySelectorAll('.section-score-bar-fill').forEach((bar, i) => {
                bar.style.width = scores[scoreKeys[i]] + '%';
            });
        }, 100);
    } else {
        scoresWrap.style.display = 'none';
    }

    // ── Education ──
    const eduEl = document.getElementById('res-education');
    const eduWrap = document.getElementById('res-education-wrap');
    const edu = parsed.education || [];
    if (edu.length) {
        eduWrap.style.display = '';
        eduEl.innerHTML = edu.map(e => `
            <div class="parsed-entry">
                <div class="parsed-entry-body">${esc(e.raw || '')}</div>
                <div class="parsed-entry-meta" style="margin-top:4px">
                    ${e.year ? `<span>📅 ${esc(e.year)}</span>` : ''}
                    ${e.gpa ? ` · <span>📊 GPA: ${esc(e.gpa)}</span>` : ''}
                </div>
            </div>
        `).join('');
    } else {
        eduWrap.style.display = 'none';
    }

    // ── Experience ──
    const expEl = document.getElementById('res-experience');
    const expWrap = document.getElementById('res-experience-wrap');
    const exp = parsed.experience || [];
    if (exp.length) {
        expWrap.style.display = '';
        expEl.innerHTML = exp.map(e => `
            <div class="parsed-entry">
                <div class="parsed-entry-title">${esc(e.title || '')}</div>
                ${e.dates ? `<div class="parsed-entry-meta">📅 ${esc(e.dates)}</div>` : ''}
                <div class="parsed-entry-body">${esc((e.raw || '').substring(0, 300))}${(e.raw || '').length > 300 ? '…' : ''}</div>
            </div>
        `).join('');
    } else {
        expWrap.style.display = 'none';
    }

    // ── Projects ──
    const projEl = document.getElementById('res-projects');
    const projWrap = document.getElementById('res-projects-wrap');
    const proj = parsed.projects || [];
    if (proj.length) {
        projWrap.style.display = '';
        projEl.innerHTML = proj.map(p => `
            <div class="parsed-entry">
                <div class="parsed-entry-title">${esc(p.name || '')}</div>
                ${(p.technologies || []).length ? `<div class="chip-wrap" style="margin:6px 0">${p.technologies.map(t => `<span class="chip chip-cyan">${esc(t)}</span>`).join('')}</div>` : ''}
                <div class="parsed-entry-body">${esc((p.raw || '').substring(0, 250))}${(p.raw || '').length > 250 ? '…' : ''}</div>
            </div>
        `).join('');
    } else {
        projWrap.style.display = 'none';
    }

    // ── Certifications ──
    const certsEl = document.getElementById('res-certs');
    const certsWrap = document.getElementById('res-certs-wrap');
    const certs = parsed.certifications || [];
    if (certs.length) {
        certsWrap.style.display = '';
        certsEl.innerHTML = certs.map(c => `<span class="chip chip-purple">${esc(c)}</span>`).join('');
    } else {
        certsWrap.style.display = 'none';
    }

    // ── Detected Sections ──
    const sectionsEl = document.getElementById('res-sections-list');
    const sectionNames = parsed.stats?.sections_found || [];
    sectionsEl.innerHTML = sectionNames.length
        ? sectionNames.map(s => `<span class="chip chip-indigo">${esc(s)}</span>`).join('')
        : '<span class="chip chip-none">No named sections detected</span>';
}

function toggleParsedResume() {
    const wrap = document.getElementById('parsed-details-wrap');
    const icon = document.getElementById('toggle-parsed-icon');
    const btn = document.getElementById('toggle-parsed-btn');
    if (!wrap) return;

    const isHidden = wrap.style.display === 'none';
    wrap.style.display = isHidden ? '' : 'none';
    if (icon) icon.textContent = isHidden ? 'expand_less' : 'expand_more';
    if (btn) {
        btn.innerHTML = `<span class="material-symbols-outlined text-sm" id="toggle-parsed-icon">${isHidden ? 'expand_less' : 'expand_more'}</span> ${isHidden ? 'Hide Details' : 'Show Details'}`;
    }
}

// HTML escape helper (global)
function esc(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}


// ════════════════════════════════════════
// Reset
// ════════════════════════════════════════
function resetScreen() {
    resultsWrap.classList.remove('visible');
    hideError();
    inputSec.classList.remove('hidden');
}


// ════════════════════════════════════════
// Download PDF Report
// ════════════════════════════════════════
async function downloadPdfReport() {
    if (!lastScreenResult) {
        alert('No screening results available. Run a screen first.');
        return;
    }

    try {
        const res = await fetch('/api/export/pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(lastScreenResult),
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.error || 'PDF generation failed.');
        }

        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = res.headers.get('Content-Disposition')?.split('filename=')[1] || 'screening_report.pdf';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (err) {
        alert('PDF download error: ' + err.message);
    }
}

// ════════════════════════════════════════
// Batch Processing
// ════════════════════════════════════════
const batchBtn = document.getElementById('batch-btn');
const batchProg = document.getElementById('batch-progress');
const batchRes = document.getElementById('batch-results');
const batchTb = document.getElementById('batch-table-body');

batchBtn.addEventListener('click', async () => {
    const jdText = document.getElementById('batch-jd').value.trim();
    const resumesRaw = document.getElementById('batch-resumes').value.trim();

    if (!jdText || !resumesRaw) { alert('Provide a Job Description and at least one resume.'); return; }

    const resumes = resumesRaw.split('---NEXT CANDIDATE---').map(s => s.trim()).filter(s => s.length > 5);
    if (!resumes.length) { alert('No valid resumes found. Check the separator.'); return; }

    batchProg.classList.add('visible');
    batchRes.classList.remove('visible');
    batchTb.innerHTML = '';
    document.getElementById('batch-total').textContent = resumes.length;
    batchBtn.disabled = true;

    try {
        const results = [];
        for (let i = 0; i < resumes.length; i++) {
            document.getElementById('batch-curr-idx').textContent = i + 1;
            document.getElementById('batch-bar').style.width = `${(i / resumes.length) * 100}%`;

            try {
                const batchSettings = getSettings();
                const r = await fetch('/api/screen', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ resume: resumes[i], job_description: jdText, match_threshold: batchSettings.matchThreshold, ai_threshold: batchSettings.aiThreshold })
                });
                const data = await r.json();
                results.push(data.success
                    ? { id: `Candidate ${i + 1}`, ...data }
                    : { id: `Candidate ${i + 1}`, error: data.error });
            } catch {
                results.push({ id: `Candidate ${i + 1}`, error: 'Network Error' });
            }
        }

        document.getElementById('batch-bar').style.width = '100%';
        document.getElementById('batch-status-text').textContent = 'Complete!';

        results.sort((a, b) => (b.match_score || 0) - (a.match_score || 0));

        // Track shortlisted candidates for vacancy tracking
        let batchShortlisted = 0;
        results.forEach(r => {
            if (r.error) {
                batchTb.innerHTML += `
                    <tr>
                        <td style="color:#fff;font-weight:600">${r.id}</td>
                        <td colspan="3" style="color:#ef4444">Failed: ${r.error}</td>
                    </tr>`;
            } else {
                const dec = r.decision === 'SHORTLISTED';
                if (dec) batchShortlisted++;
                batchTb.innerHTML += `
                    <tr>
                        <td style="color:#fff;font-weight:600">${r.id}</td>
                        <td style="color:#a5b4fc;font-weight:700">${r.match_score.toFixed(1)}%</td>
                        <td style="color:#f59e0b">${r.ai_score.toFixed(1)}%</td>
                        <td><span class="badge ${dec ? 'badge-green' : 'badge-red'}">${r.decision}</span></td>
                    </tr>`;
            }
        });

        // Record all shortlisted candidates for vacancy tracking
        if (batchShortlisted > 0) {
            const s = getSettings();
            const newFilled = s.filledVacancies + batchShortlisted;
            const remaining = Math.max(0, s.jobVacancies - newFilled);
            localStorage.setItem('recruitai_settings', JSON.stringify({
                matchThreshold: s.matchThreshold,
                aiThreshold: s.aiThreshold,
                jobVacancies: s.jobVacancies,
                filledVacancies: newFilled,
            }));
            updateVacancyTracker();

            // Add vacancy summary row to batch table
            const vacColor = remaining === 0 ? '#ef4444' : remaining <= Math.ceil(s.jobVacancies * 0.25) ? '#f59e0b' : '#10b981';
            batchTb.innerHTML += `
                <tr style="background:rgba(37,99,235,0.08)">
                    <td colspan="2" style="font-weight:700;font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px">
                        📊 Vacancy Summary
                    </td>
                    <td style="font-weight:800;font-size:13px;color:#10b981">
                        ${batchShortlisted} Shortlisted
                    </td>
                    <td style="font-weight:800;font-size:13px;color:${vacColor}">
                        ${remaining}/${s.jobVacancies} Remaining
                    </td>
                </tr>`;
        }

        batchRes.style.display = 'block';

    } catch (err) {
        alert('Batch error: ' + err.message);
    } finally {
        setTimeout(() => {
            batchProg.classList.remove('visible');
            document.getElementById('batch-bar').style.width = '0%';
            batchBtn.disabled = false;
        }, 1800);
    }
});


// ════════════════════════════════════════
// Compare
// ════════════════════════════════════════
document.getElementById('comp-btn').addEventListener('click', async () => {
    const jd = document.getElementById('comp-jd').value.trim();
    const resA = document.getElementById('comp-res-a').value.trim();
    const resB = document.getElementById('comp-res-b').value.trim();

    if (!jd || !resA || !resB) { alert('Provide the Job Description and both resumes.'); return; }

    const btn = document.getElementById('comp-btn');
    const loader = document.getElementById('comp-loader');
    const res = document.getElementById('comp-results');

    btn.disabled = true;
    loader.classList.remove('hidden');
    res.classList.add('hidden');

    try {
        const compSettings = getSettings();
        const [a, b] = await Promise.all([
            fetch('/api/screen', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ resume: resA, job_description: jd, match_threshold: compSettings.matchThreshold, ai_threshold: compSettings.aiThreshold }) }).then(r => r.json()),
            fetch('/api/screen', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ resume: resB, job_description: jd, match_threshold: compSettings.matchThreshold, ai_threshold: compSettings.aiThreshold }) }).then(r => r.json())
        ]);

        if (!a.success || !b.success) throw new Error('One or both analyses failed.');

        let winner = 'It\'s a Tie!';
        if (a.match_score > b.match_score) winner = '🏆 Candidate A';
        else if (b.match_score > a.match_score) winner = '🏆 Candidate B';

        document.getElementById('comp-winner-text').textContent = winner;
        document.getElementById('comp-card-a').innerHTML = buildCompCard(a, 'Candidate A', '#3b82f6');
        document.getElementById('comp-card-b').innerHTML = buildCompCard(b, 'Candidate B', '#ec4899');

        res.classList.remove('hidden');

    } catch (err) {
        alert('Comparison error: ' + err.message);
    } finally {
        btn.disabled = false;
        loader.classList.add('hidden');
    }
});

function buildCompCard(data, name, color) {
    const pass = data.decision === 'SHORTLISTED';
    const skills = (data.skill_analysis?.matched_skills || []).slice(0, 6);
    return `
        <div style="border-bottom:1px solid #e2e8f0;padding-bottom:14px;margin-bottom:16px">
            <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:${color};margin-bottom:4px">${name}</div>
            <div style="font-size:48px;font-weight:800;line-height:1;color:${pass ? '#059669' : '#dc2626'}">${data.match_score.toFixed(1)}<span style="font-size:24px">%</span></div>
            <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:#64748b;margin-top:4px">Match Score</div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px">
            <div class="stat-box">
                <div class="stat-box-label">AI Signal</div>
                <div class="stat-box-val" style="font-size:16px;color:#d97706">${data.ai_score.toFixed(1)}%</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-label">Decision</div>
                <div style="margin-top:4px"><span class="badge ${pass ? 'badge-green' : 'badge-red'}">${data.decision}</span></div>
            </div>
        </div>
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:12px">
            <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#64748b;margin-bottom:8px">Matched Skills</div>
            <div class="chip-wrap">
                ${skills.length
            ? skills.map(s => `<span class="chip chip-indigo">${s}</span>`).join('')
            : '<span class="chip chip-none">None detected</span>'}
            </div>
        </div>`;
}


// ════════════════════════════════════════
// History
// ════════════════════════════════════════
function saveToHistory() {
    if (!lastScreenResult) return;
    try {
        let hist = JSON.parse(localStorage.getItem('ai_recruit_history') || '[]');
        hist.unshift(lastScreenResult);
        if (hist.length > 20) hist = hist.slice(0, 20);
        localStorage.setItem('ai_recruit_history', JSON.stringify(hist));

        const btn = document.getElementById('btn-save-hist');
        btn.innerHTML = '<span class="material-symbols-outlined">check</span> Saved!';
        btn.disabled = true;
    } catch (e) {
        console.error('Storage error', e);
    }
}

function renderHistory() {
    const listEl = document.getElementById('history-list');
    const emptyEl = document.getElementById('history-empty');
    listEl.innerHTML = '';

    let hist = [];
    try { hist = JSON.parse(localStorage.getItem('ai_recruit_history') || '[]'); } catch { }

    if (!hist.length) {
        emptyEl.classList.remove('hidden');
        listEl.classList.add('hidden');
        return;
    }

    emptyEl.classList.add('hidden');
    listEl.classList.remove('hidden');

    hist.forEach(h => {
        const pass = h.decision === 'SHORTLISTED';
        const d = h.timestamp ? new Date(h.timestamp).toLocaleString() : 'Unknown';
        listEl.innerHTML += `
            <div class="card flex items-center gap-5 p-5 flex-wrap" style="border-left:3px solid ${pass ? '#059669' : '#dc2626'}">
                <div class="flex-1 min-w-[200px]">
                    <div class="text-[11px] text-on-surface-variant mb-1">${d}</div>
                    <div class="flex items-center gap-3 flex-wrap">
                        <span class="badge ${pass ? 'badge-green' : 'badge-red'}">${h.decision}</span>
                        <span class="text-xl font-extrabold text-on-surface">${(h.match_score || 0).toFixed(1)}% Match</span>
                    </div>
                    <div class="text-sm text-on-surface-variant mt-1.5">${h.reason || ''}</div>
                </div>
                <div class="flex-shrink-0 bg-surface-container border border-outline-variant/30 rounded-xl px-4 py-2.5 text-center">
                    <div class="text-[10px] font-bold uppercase tracking-wider text-outline">AI Risk</div>
                    <div class="text-lg font-extrabold text-amber-600">${(h.ai_score || 0).toFixed(1)}%</div>
                </div>
            </div>`;
    });
}

function clearHistory() {
    if (confirm('Clear all saved history?')) {
        localStorage.removeItem('ai_recruit_history');
        renderHistory();
    }
}


// ════════════════════════════════════════
// Insights Tab
// ════════════════════════════════════════
let lastInsightsData = null;

function renderInsights() {
    const emptyEl = document.getElementById('insights-empty');
    const contentEl = document.getElementById('insights-content');
    const summaryEl = document.getElementById('insights-summary');
    const adviceEl = document.getElementById('insights-advice');
    const tipsEl = document.getElementById('insights-tips');

    if (!lastInsightsData || !lastInsightsData.tips) {
        emptyEl.classList.remove('hidden');
        contentEl.classList.add('hidden');
        return;
    }

    emptyEl.classList.add('hidden');
    contentEl.classList.remove('hidden');

    const d = lastInsightsData;
    const matched = d.skill_analysis?.matched_skills || [];
    const missing = d.skill_analysis?.missing_skills || [];
    const total = matched.length + missing.length;
    const coverage = total ? ((matched.length / total) * 100).toFixed(0) : 100;

    const highCount = d.tips.filter(t => t.priority.includes('High')).length;
    const medCount = d.tips.filter(t => t.priority.includes('Medium')).length;
    const lowCount = d.tips.filter(t => !t.priority.includes('High') && !t.priority.includes('Medium')).length;

    // Summary stats
    summaryEl.innerHTML = `
        <div class="card p-5 text-center">
            <div class="text-3xl font-extrabold text-primary leading-none">${d.match_score.toFixed(1)}%</div>
            <div class="text-[11px] font-semibold uppercase tracking-wider text-outline mt-2">Match Score</div>
        </div>
        <div class="card p-5 text-center">
            <div class="text-3xl font-extrabold text-amber-600 leading-none">${d.ai_score.toFixed(1)}%</div>
            <div class="text-[11px] font-semibold uppercase tracking-wider text-outline mt-2">AI Score</div>
        </div>
        <div class="card p-5 text-center">
            <div class="text-3xl font-extrabold text-emerald-600 leading-none">${coverage}%</div>
            <div class="text-[11px] font-semibold uppercase tracking-wider text-outline mt-2">Skill Coverage</div>
        </div>
        <div class="card p-5 text-center">
            <div class="text-3xl font-extrabold text-on-surface leading-none">${d.tips.length}</div>
            <div class="text-[11px] font-semibold uppercase tracking-wider text-outline mt-2">Suggestions</div>
        </div>
    `;

    // General advice
    if (d.general_advice.length) {
        adviceEl.classList.remove('hidden');
        adviceEl.innerHTML = `
            <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-primary mb-3">
                <span class="material-symbols-outlined text-lg">auto_awesome</span>
                General Recommendations
            </div>
            ${d.general_advice.map(a => `<div class="text-sm text-on-surface leading-relaxed py-1.5">${a}</div>`).join('')}
        `;
    } else {
        adviceEl.classList.add('hidden');
    }

    // Tip cards
    if (!d.tips.length) {
        tipsEl.innerHTML = `
            <div class="card p-10 text-center text-on-surface-variant">
                <span class="material-symbols-outlined text-4xl block mb-3 text-emerald-500">verified</span>
                <strong class="text-on-surface">All skills matched!</strong><br>No improvement tips needed for this job description.
            </div>
        `;
        return;
    }

    tipsEl.innerHTML = d.tips.map(tip => {
        const isHigh = tip.priority.includes('High');
        const isMed = tip.priority.includes('Medium');
        const pClass = isHigh ? 'high' : isMed ? 'medium' : 'low';
        const pIcon = isHigh ? 'priority_high' : isMed ? 'trending_up' : 'check_circle';
        const pLabel = isHigh ? 'High Priority' : isMed ? 'Medium Priority' : 'Nice to Have';

        return `
            <div class="card tip-card priority-${pClass}">
                <div class="tip-icon">
                    <span class="material-symbols-outlined">${pIcon}</span>
                </div>
                <div class="tip-body">
                    <div class="tip-skill">
                        ${tip.skill}
                        <span class="tip-priority ${pClass}">${pLabel}</span>
                    </div>
                    <div class="tip-text">${tip.tip}</div>
                </div>
            </div>
        `;
    }).join('');
}


// ════════════════════════════════════════
// File Upload
// ════════════════════════════════════════
(function initFileUpload() {
    const zone = document.getElementById('upload-zone');
    const fileIn = document.getElementById('resume-file-input');
    const content = document.getElementById('upload-zone-content');
    const fileLbl = document.getElementById('upload-zone-file');
    const loading = document.getElementById('upload-zone-loading');
    const fnameEl = document.getElementById('upload-filename');
    const removeBtn = document.getElementById('upload-remove-btn');
    if (!zone || !fileIn) return;

    // Click to browse
    zone.addEventListener('click', (e) => {
        if (e.target === removeBtn || e.target.closest('#upload-remove-btn')) return;
        fileIn.click();
    });

    // Remove button
    if (removeBtn) {
        removeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            fileIn.value = '';
            fileLbl.style.display = 'none';
            content.style.display = '';
        });
    }

    // Drag & drop
    zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag-over'); });
    zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
    zone.addEventListener('drop', e => {
        e.preventDefault();
        zone.classList.remove('drag-over');
        if (e.dataTransfer.files.length) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    // File input change
    fileIn.addEventListener('change', () => {
        if (fileIn.files.length) handleFileUpload(fileIn.files[0]);
    });

    async function handleFileUpload(file) {
        const allowed = ['pdf', 'docx', 'doc', 'txt'];
        const ext = file.name.split('.').pop().toLowerCase();
        if (!allowed.includes(ext)) { alert('Unsupported file type. Use PDF, DOCX or TXT.'); return; }

        content.style.display = 'none';
        fileLbl.style.display = 'none';
        loading.style.display = 'flex';

        try {
            const formData = new FormData();
            formData.append('file', file);

            const res = await fetch('/api/upload', { method: 'POST', body: formData });
            const data = await res.json();

            if (!res.ok || !data.success) throw new Error(data.error || 'Upload failed.');

            document.getElementById('screen-resume').value = data.text;
            updateCounts();

            fnameEl.textContent = data.filename || file.name;
            loading.style.display = 'none';
            fileLbl.style.display = 'flex';

        } catch (err) {
            alert('Upload error: ' + err.message);
            loading.style.display = 'none';
            content.style.display = '';
        }
    }
})();

function removeUploadedFile() {
    document.getElementById('resume-file-input').value = '';
    document.getElementById('upload-zone-file').style.display = 'none';
    document.getElementById('upload-zone-content').style.display = '';
}


// ════════════════════════════════════════
// JD File Upload
// ════════════════════════════════════════
(function initJdFileUpload() {
    const zone = document.getElementById('jd-upload-zone');
    const fileIn = document.getElementById('jd-file-input');
    const content = document.getElementById('jd-upload-zone-content');
    const fileLbl = document.getElementById('jd-upload-zone-file');
    const loading = document.getElementById('jd-upload-zone-loading');
    const fnameEl = document.getElementById('jd-upload-filename');
    const removeBtn = document.getElementById('jd-upload-remove-btn');
    if (!zone || !fileIn) return;

    // Click to browse
    zone.addEventListener('click', (e) => {
        if (e.target === removeBtn || e.target.closest('#jd-upload-remove-btn')) return;
        fileIn.click();
    });

    // Remove button
    if (removeBtn) {
        removeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            fileIn.value = '';
            fileLbl.style.display = 'none';
            content.style.display = '';
        });
    }

    // Drag & drop
    zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag-over'); });
    zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
    zone.addEventListener('drop', e => {
        e.preventDefault();
        zone.classList.remove('drag-over');
        if (e.dataTransfer.files.length) {
            handleJdFileUpload(e.dataTransfer.files[0]);
        }
    });

    // File input change
    fileIn.addEventListener('change', () => {
        if (fileIn.files.length) handleJdFileUpload(fileIn.files[0]);
    });

    async function handleJdFileUpload(file) {
        const allowed = ['pdf', 'docx', 'doc', 'txt'];
        const ext = file.name.split('.').pop().toLowerCase();
        if (!allowed.includes(ext)) { alert('Unsupported file type. Use PDF, DOCX or TXT.'); return; }

        content.style.display = 'none';
        fileLbl.style.display = 'none';
        loading.style.display = 'flex';

        try {
            const formData = new FormData();
            formData.append('file', file);

            const res = await fetch('/api/upload', { method: 'POST', body: formData });
            const data = await res.json();

            if (!res.ok || !data.success) throw new Error(data.error || 'Upload failed.');

            document.getElementById('screen-jd').value = data.text;
            updateCounts();

            fnameEl.textContent = data.filename || file.name;
            loading.style.display = 'none';
            fileLbl.style.display = 'flex';

        } catch (err) {
            alert('Upload error: ' + err.message);
            loading.style.display = 'none';
            content.style.display = '';
        }
    }
})();

function removeJdUploadedFile() {
    document.getElementById('jd-file-input').value = '';
    document.getElementById('jd-upload-zone-file').style.display = 'none';
    document.getElementById('jd-upload-zone-content').style.display = '';
}

// ════════════════════════════════════════
// Email Results
// ════════════════════════════════════════

function extractCandidateName(resumeText) {
    if (!resumeText) return '';
    const lines = resumeText.split('\n').map(l => l.trim()).filter(l => l.length > 0);
    if (!lines.length) return '';

    // 1. Check for "Name: ..." pattern anywhere in the first 10 lines
    for (let i = 0; i < Math.min(lines.length, 10); i++) {
        const nameMatch = lines[i].match(/^name\s*[:—–-]\s*(.+)/i);
        if (nameMatch) {
            const name = nameMatch[1].replace(/[|•·].*$/, '').replace(/[^a-zA-Z\s.'-]/g, '').trim();
            if (name.length > 1) return name;
        }
    }

    // 2. First line is usually the candidate's name
    let firstLine = lines[0]
        .replace(/^(candidate|resume|cv|profile|curriculum vitae)\s*[:—–-]?\s*/i, '')
        .replace(/\s*[—–|•·]\s*.*/g, '')   // Remove " — Software Engineer" etc.
        .replace(/[^a-zA-Z\s.'-]/g, '')     // Keep letters, spaces, dots, hyphens, apostrophes
        .trim();

    const words = firstLine.split(/\s+/).filter(w => w.length > 0);
    if (words.length >= 1 && words.length <= 5 && words.every(w => /^[A-Z]/.test(w))) {
        return firstLine;
    }
    return '';
}

function extractCandidateEmail(resumeText) {
    if (!resumeText) return '';
    const lines = resumeText.split('\n').map(l => l.trim());

    // 1. Look for labeled email on any line: "Email:", "E-mail:", "Mail:", "Contact:" etc.
    for (const line of lines) {
        const labeledMatch = line.match(/(?:e[-.]?mail|mail|contact)\s*[:—–\-]\s*([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})/i);
        if (labeledMatch) return labeledMatch[1].toLowerCase();
    }

    // 2. Find ANY email address anywhere in the full resume text
    const anyEmail = resumeText.match(/[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/);
    if (anyEmail) return anyEmail[0].toLowerCase();

    return '';
}

function buildEmailPreview(candidateName, data) {
    if (!data) return '<span style="color:#94a3b8">No screening results available.</span>';

    const pass = data.decision === 'SHORTLISTED';
    const statusColor = pass ? '#059669' : '#dc2626';
    const statusIcon = pass ? '✅' : '❌';
    const statusMsg = pass
        ? 'Congratulations! Your profile has been shortlisted for the next round.'
        : 'Thank you for your application. Unfortunately, your profile was not shortlisted at this time.';

    const matchedSkills = data.skill_analysis?.matched_skills || [];
    const missingSkills = data.skill_analysis?.missing_skills || [];
    const tips = data.tips || lastInsightsData?.tips || [];
    const advice = data.general_advice || lastInsightsData?.general_advice || [];

    const matchedChips = matchedSkills.length
        ? matchedSkills.map(s => `<span style="display:inline-block;background:#ecfdf5;color:#059669;border:1px solid #a7f3d0;border-radius:20px;padding:3px 10px;margin:2px;font-size:11px;font-weight:600">${s}</span>`).join('')
        : '<span style="color:#94a3b8;font-size:12px">None detected</span>';

    const missingChips = missingSkills.length
        ? missingSkills.map(s => `<span style="display:inline-block;background:#fef2f2;color:#dc2626;border:1px solid #fecaca;border-radius:20px;padding:3px 10px;margin:2px;font-size:11px;font-weight:600">${s}</span>`).join('')
        : '<span style="color:#059669;font-size:12px">All skills matched! ✅</span>';

    let tipsHtml = '';
    if (tips.length) {
        tipsHtml = `<div style="margin-top:14px"><strong style="font-size:12px;color:#1e293b">📋 Improvement Tips:</strong>`;
        tips.slice(0, 4).forEach(t => {
            tipsHtml += `<div style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:8px 12px;margin-top:6px">
                <strong style="color:#1e293b;font-size:12px">${t.skill || ''}</strong>
                <span style="font-size:9px;background:#fffbeb;color:#d97706;border-radius:8px;padding:1px 5px;margin-left:4px">${t.priority || ''}</span>
                <div style="color:#64748b;font-size:11px;margin-top:2px">${t.tip || ''}</div>
            </div>`;
        });
        tipsHtml += '</div>';
    }

    let adviceHtml = '';
    if (advice.length) {
        adviceHtml = `<div style="margin-top:14px"><strong style="font-size:12px;color:#1e293b">💡 General Advice:</strong>`;
        advice.forEach(a => {
            adviceHtml += `<div style="color:#475569;font-size:12px;padding:4px 0;border-bottom:1px solid #f1f5f9">${a}</div>`;
        });
        adviceHtml += '</div>';
    }

    return `
        <div style="text-align:center;margin-bottom:16px">
            <div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px">Subject Line</div>
            <div style="font-size:14px;font-weight:700;color:#1e293b">Resume Screening Result: ${data.decision}</div>
        </div>
        <div style="border-top:1px solid #e2e8f0;padding-top:14px">
            <p style="margin:0 0 8px">Dear <strong>${candidateName || 'Candidate'}</strong>,</p>
            <p style="margin:0 0 14px">${statusMsg}</p>

            <div style="background:${statusColor};color:#fff;border-radius:10px;padding:14px;text-align:center;margin-bottom:14px">
                <div style="font-size:20px;font-weight:800;letter-spacing:0.5px">${data.decision} ${statusIcon}</div>
                <div style="font-size:11px;opacity:0.9;margin-top:3px">${data.reason || ''}</div>
            </div>

            <div style="display:flex;gap:10px;margin-bottom:14px">
                <div style="flex:1;background:#f0f9ff;border:1px solid #bae6fd;border-radius:10px;padding:12px;text-align:center">
                    <div style="font-size:10px;font-weight:700;color:#0369a1;text-transform:uppercase">Match Score</div>
                    <div style="font-size:24px;font-weight:800;color:#2563eb">${data.match_score.toFixed(1)}%</div>
                </div>
                <div style="flex:1;background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:12px;text-align:center">
                    <div style="font-size:10px;font-weight:700;color:#92400e;text-transform:uppercase">AI Content</div>
                    <div style="font-size:24px;font-weight:800;color:#d97706">${data.ai_score.toFixed(1)}%</div>
                </div>
            </div>

            <div style="margin-bottom:12px">
                <strong style="font-size:12px;color:#1e293b">✅ Matched Skills:</strong>
                <div style="margin-top:4px">${matchedChips}</div>
            </div>
            <div style="margin-bottom:12px">
                <strong style="font-size:12px;color:#1e293b">⚠️ Skills to Improve:</strong>
                <div style="margin-top:4px">${missingChips}</div>
            </div>
            ${tipsHtml}
            ${adviceHtml}
        </div>
        <div style="border-top:1px solid #e2e8f0;padding-top:10px;margin-top:14px;text-align:center;color:#94a3b8;font-size:11px">
            Sent by AI Driven Resume Screening — Intelligent Screening Engine
        </div>
    `;
}

function openEmailModal() {
    const modal = document.getElementById('email-modal');
    modal.style.display = 'flex';
    document.getElementById('email-status').style.display = 'none';

    // Auto-extract candidate name and email from resume
    const resumeText = document.getElementById('screen-resume')?.value || '';
    const detectedName = extractCandidateName(resumeText);
    const detectedEmail = extractCandidateEmail(resumeText);

    if (detectedName) document.getElementById('email-candidate-name').value = detectedName;
    if (detectedEmail) document.getElementById('email-to').value = detectedEmail;

    // Build auto-generated email preview
    updateEmailPreview();

    // Live-update preview when name changes
    document.getElementById('email-candidate-name').addEventListener('input', updateEmailPreview);
}

function updateEmailPreview() {
    const name = document.getElementById('email-candidate-name').value.trim();
    const previewEl = document.getElementById('email-preview');
    if (previewEl && lastScreenResult) {
        previewEl.innerHTML = buildEmailPreview(name, lastScreenResult);
    }
}

function closeEmailModal() {
    document.getElementById('email-modal').style.display = 'none';
    document.getElementById('email-candidate-name').removeEventListener('input', updateEmailPreview);
}

async function sendEmailResults() {
    const toEmail = document.getElementById('email-to').value.trim();
    const candidateName = document.getElementById('email-candidate-name').value.trim() || 'Candidate';
    const sendBtn = document.getElementById('btn-send-email');

    if (!toEmail) { showEmailStatus('❌ Please enter the candidate email.', false); return; }
    if (!lastScreenResult) { showEmailStatus('❌ No screening results to send.', false); return; }

    sendBtn.disabled = true;
    sendBtn.innerHTML = '<div class="spinner-ring" style="width:20px;height:20px;border-width:2px"></div> Sending...';

    try {
        const payload = {
            to_email: toEmail,
            candidate_name: candidateName,
            decision: lastScreenResult.decision,
            match_score: lastScreenResult.match_score,
            ai_score: lastScreenResult.ai_score,
            reason: lastScreenResult.reason,
            matched_skills: lastScreenResult.skill_analysis?.matched_skills || [],
            missing_skills: lastScreenResult.skill_analysis?.missing_skills || [],
            tips: lastScreenResult.tips || lastInsightsData?.tips || [],
            general_advice: lastScreenResult.general_advice || lastInsightsData?.general_advice || []
        };

        const res = await fetch('/api/send-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (!res.ok || !data.success) throw new Error(data.error || 'Failed to send email.');

        showEmailStatus(`✅ Email sent successfully to ${toEmail}`, true);
        setTimeout(() => closeEmailModal(), 2500);

    } catch (err) {
        showEmailStatus('❌ ' + err.message, false);
    } finally {
        sendBtn.disabled = false;
        sendBtn.innerHTML = '<span class="material-symbols-outlined text-lg">send</span> Send Email';
    }
}

function showEmailStatus(msg, success) {
    const el = document.getElementById('email-status');
    el.style.display = 'block';
    el.textContent = msg;
    el.style.background = success ? '#ecfdf5' : '#fef2f2';
    el.style.color = success ? '#059669' : '#dc2626';
    el.style.border = `1px solid ${success ? '#a7f3d0' : '#fecaca'}`;
}


// ════════════════════════════════════════
// Chart Rendering
// ════════════════════════════════════════
let chartInstances = {};

function destroyChart(key) {
    if (chartInstances[key]) { chartInstances[key].destroy(); delete chartInstances[key]; }
}

function renderCharts(data) {
    const isDark = document.documentElement.classList.contains('dark');
    const textColor = isDark ? '#94a3b8' : '#64748b';
    const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';

    // ── 1. Score Overview Doughnut ──
    destroyChart('scores');
    const scoresCtx = document.getElementById('chart-scores');
    if (scoresCtx) {
        chartInstances.scores = new Chart(scoresCtx, {
            type: 'doughnut',
            data: {
                labels: ['Match Score', 'AI Score', 'Remaining'],
                datasets: [{
                    data: [data.match_score, data.ai_score, Math.max(0, 100 - data.match_score - data.ai_score)],
                    backgroundColor: ['#2563eb', '#f59e0b', isDark ? '#1e293b' : '#e2e8f0'],
                    borderWidth: 0,
                    borderRadius: 4,
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                cutout: '65%',
                plugins: {
                    legend: { position: 'bottom', labels: { color: textColor, padding: 12, usePointStyle: true, pointStyleWidth: 8, font: { size: 11, weight: 600 } } }
                }
            }
        });
    }

    // ── 2. Skills Doughnut ──
    destroyChart('skills');
    const skillsCtx = document.getElementById('chart-skills');
    const matched = (data.skill_analysis?.matched_skills || []).length;
    const missing = (data.skill_analysis?.missing_skills || []).length;
    if (skillsCtx) {
        chartInstances.skills = new Chart(skillsCtx, {
            type: 'doughnut',
            data: {
                labels: ['Matched Skills', 'Missing Skills'],
                datasets: [{
                    data: [matched, missing || 0],
                    backgroundColor: ['#059669', isDark ? '#991b1b' : '#fca5a5'],
                    borderWidth: 0,
                    borderRadius: 4,
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                cutout: '65%',
                plugins: {
                    legend: { position: 'bottom', labels: { color: textColor, padding: 12, usePointStyle: true, pointStyleWidth: 8, font: { size: 11, weight: 600 } } }
                }
            }
        });
    }

    // ── 3. AI Breakdown Bar ──
    destroyChart('ai');
    const aiCtx = document.getElementById('chart-ai');
    const aiD = data.details?.ai || {};
    if (aiCtx) {
        const labels = ['Uniformity', 'Sent. Length', 'Lex. Diversity', 'Overall'];
        const vals = [
            aiD.sentence_length_variance != null ? Math.max(0, 100 - aiD.sentence_length_variance) : 0,
            aiD.avg_sentence_length || 0,
            aiD.lexical_diversity_ttr ? (aiD.lexical_diversity_ttr * 100) : 0,
            data.ai_score
        ];
        chartInstances.ai = new Chart(aiCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Score',
                    data: vals,
                    backgroundColor: [
                        'rgba(99,102,241,0.7)',
                        'rgba(6,182,212,0.7)',
                        'rgba(16,185,129,0.7)',
                        data.ai_score >= 70 ? 'rgba(239,68,68,0.7)' : data.ai_score >= 40 ? 'rgba(245,158,11,0.7)' : 'rgba(16,185,129,0.7)'
                    ],
                    borderRadius: 6,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { color: gridColor }, ticks: { color: textColor, font: { size: 10 } }, max: 100 },
                    y: { grid: { display: false }, ticks: { color: textColor, font: { size: 11, weight: 600 } } }
                }
            }
        });
    }
}


// ════════════════════════════════════════
// Settings Tab
// ════════════════════════════════════════
const DEFAULT_MATCH_THRESHOLD = 60;
const DEFAULT_AI_THRESHOLD = 80;

function getSettings() {
    try {
        const saved = JSON.parse(localStorage.getItem('recruitai_settings') || '{}');
        return {
            matchThreshold: saved.matchThreshold ?? DEFAULT_MATCH_THRESHOLD,
            aiThreshold: saved.aiThreshold ?? DEFAULT_AI_THRESHOLD,
            jobVacancies: saved.jobVacancies ?? 1,
            filledVacancies: saved.filledVacancies ?? 0,
        };
    } catch {
        return { matchThreshold: DEFAULT_MATCH_THRESHOLD, aiThreshold: DEFAULT_AI_THRESHOLD, jobVacancies: 1, filledVacancies: 0 };
    }
}

function updateSettingsUI() {
    const s = getSettings();
    const matchSlider = document.getElementById('match-threshold-slider');
    const aiSlider = document.getElementById('ai-threshold-slider');
    const vacSlider = document.getElementById('vacancies-slider');
    const vacInput = document.getElementById('vacancies-input');
    if (matchSlider) matchSlider.value = s.matchThreshold;
    if (aiSlider) aiSlider.value = s.aiThreshold;
    if (vacSlider) vacSlider.value = Math.min(50, s.jobVacancies);
    if (vacInput) vacInput.value = s.jobVacancies;
    document.getElementById('match-threshold-val').textContent = s.matchThreshold;
    document.getElementById('ai-threshold-val').textContent = s.aiThreshold;
    document.getElementById('summary-match').textContent = s.matchThreshold + '%';
    document.getElementById('summary-ai').textContent = s.aiThreshold + '%';
    const sumVacEl = document.getElementById('summary-vacancies');
    if (sumVacEl) sumVacEl.textContent = s.jobVacancies;

    updateVacancyTracker();

    // Compute strictness
    const matchStrictness = s.matchThreshold / 100;
    const aiStrictness = (100 - s.aiThreshold) / 100;
    const avg = (matchStrictness + aiStrictness) / 2;
    let label, color;
    if (avg >= 0.7) { label = 'Very Strict'; color = '#dc2626'; }
    else if (avg >= 0.5) { label = 'Strict'; color = '#d97706'; }
    else if (avg >= 0.3) { label = 'Balanced'; color = '#2563eb'; }
    else { label = 'Lenient'; color = '#059669'; }
    const el = document.getElementById('summary-strictness');
    el.textContent = label;
    el.style.color = color;
}

function saveSettings() {
    const matchVal = parseInt(document.getElementById('match-threshold-slider').value);
    const aiVal = parseInt(document.getElementById('ai-threshold-slider').value);
    const vacInput = document.getElementById('vacancies-input');
    const vacVal = Math.max(1, parseInt(vacInput?.value || document.getElementById('vacancies-slider').value));
    const currentSettings = getSettings();
    localStorage.setItem('recruitai_settings', JSON.stringify({
        matchThreshold: matchVal,
        aiThreshold: aiVal,
        jobVacancies: vacVal,
        filledVacancies: currentSettings.filledVacancies,
    }));
    updateSettingsUI();

    // Visual feedback
    const btn = event.target.closest('button');
    const orig = btn.innerHTML;
    btn.innerHTML = '<span class="material-symbols-outlined text-lg">check</span> Saved!';
    btn.disabled = true;
    setTimeout(() => { btn.innerHTML = orig; btn.disabled = false; }, 1500);
}

function resetSettings() {
    localStorage.removeItem('recruitai_settings');
    updateSettingsUI();
}

// Wire up sliders
(function initSettingsSliders() {
    const matchSlider = document.getElementById('match-threshold-slider');
    const aiSlider = document.getElementById('ai-threshold-slider');
    const vacSlider = document.getElementById('vacancies-slider');

    if (matchSlider) {
        matchSlider.addEventListener('input', () => {
            document.getElementById('match-threshold-val').textContent = matchSlider.value;
            document.getElementById('summary-match').textContent = matchSlider.value + '%';
            updateStrictnessPreview();
        });
    }
    if (aiSlider) {
        aiSlider.addEventListener('input', () => {
            document.getElementById('ai-threshold-val').textContent = aiSlider.value;
            document.getElementById('summary-ai').textContent = aiSlider.value + '%';
            updateStrictnessPreview();
        });
    }
    if (vacSlider) {
        vacSlider.addEventListener('input', () => {
            const v = parseInt(vacSlider.value);
            const vacInput = document.getElementById('vacancies-input');
            const sumEl = document.getElementById('summary-vacancies');
            if (vacInput) vacInput.value = v;
            if (sumEl) sumEl.textContent = v;
            updateTrackerPreview(v);
        });
    }

    updateSettingsUI();
})();

function adjustVacancies(delta) {
    const slider = document.getElementById('vacancies-slider');
    const vacInput = document.getElementById('vacancies-input');
    const sumEl = document.getElementById('summary-vacancies');
    if (!vacInput) return;
    let current = parseInt(vacInput.value) || 1;
    let newVal = Math.max(1, current + delta);
    vacInput.value = newVal;
    if (slider) slider.value = Math.min(50, newVal);
    if (sumEl) sumEl.textContent = newVal;
    updateTrackerPreview(newVal);
}

function setVacanciesFromInput() {
    const vacInput = document.getElementById('vacancies-input');
    const slider = document.getElementById('vacancies-slider');
    const sumEl = document.getElementById('summary-vacancies');
    if (!vacInput) return;
    let val = Math.max(1, parseInt(vacInput.value) || 1);
    vacInput.value = val;
    if (slider) slider.value = Math.min(50, val);
    if (sumEl) sumEl.textContent = val;
    updateTrackerPreview(val);
}

function updateTrackerPreview(previewTotal) {
    const s = getSettings();
    const filled = s.filledVacancies;
    const remaining = Math.max(0, previewTotal - filled);
    const pct = previewTotal > 0 ? Math.min(100, (filled / previewTotal) * 100) : 0;

    const totalEl = document.getElementById('tracker-total');
    const remainingEl = document.getElementById('tracker-remaining');
    const barEl = document.getElementById('tracker-bar');
    const statusEl = document.getElementById('tracker-status-text');

    if (totalEl) totalEl.textContent = previewTotal;
    if (remainingEl) remainingEl.textContent = remaining;
    if (barEl) barEl.style.width = pct + '%';

    if (statusEl) {
        if (filled === 0) {
            statusEl.textContent = 'No positions filled yet';
            statusEl.className = 'text-center mt-2 text-xs font-semibold text-outline';
        } else if (remaining === 0) {
            statusEl.textContent = '⚠️ All vacancies filled — consider increasing positions or starting a new cycle';
            statusEl.className = 'text-center mt-2 text-xs font-semibold text-red-600';
            if (barEl) barEl.className = 'h-full rounded-full transition-all duration-500 ease-out bg-red-500';
        } else if (remaining <= Math.ceil(previewTotal * 0.25)) {
            statusEl.textContent = `${filled} filled, ${remaining} remaining — almost full`;
            statusEl.className = 'text-center mt-2 text-xs font-semibold text-amber-600';
            if (barEl) barEl.className = 'h-full rounded-full transition-all duration-500 ease-out bg-amber-500';
        } else {
            statusEl.textContent = `${filled} filled, ${remaining} remaining`;
            statusEl.className = 'text-center mt-2 text-xs font-semibold text-emerald';
            if (barEl) barEl.className = 'h-full rounded-full transition-all duration-500 ease-out bg-emerald';
        }
    }
}

function recordShortlist() {
    const s = getSettings();
    const newFilled = s.filledVacancies + 1;
    localStorage.setItem('recruitai_settings', JSON.stringify({
        matchThreshold: s.matchThreshold,
        aiThreshold: s.aiThreshold,
        jobVacancies: s.jobVacancies,
        filledVacancies: newFilled,
    }));
    updateVacancyTracker();
}

function resetFilledVacancies() {
    const s = getSettings();
    localStorage.setItem('recruitai_settings', JSON.stringify({
        matchThreshold: s.matchThreshold,
        aiThreshold: s.aiThreshold,
        jobVacancies: s.jobVacancies,
        filledVacancies: 0,
    }));
    updateVacancyTracker();
}

function updateVacancyTracker() {
    const s = getSettings();
    const total = s.jobVacancies;
    const filled = s.filledVacancies;
    const remaining = Math.max(0, total - filled);
    const pct = total > 0 ? Math.min(100, (filled / total) * 100) : 0;

    const totalEl = document.getElementById('tracker-total');
    const filledEl = document.getElementById('tracker-filled');
    const remainingEl = document.getElementById('tracker-remaining');
    const barEl = document.getElementById('tracker-bar');
    const statusEl = document.getElementById('tracker-status-text');

    if (totalEl) totalEl.textContent = total;
    if (filledEl) filledEl.textContent = filled;
    if (remainingEl) remainingEl.textContent = remaining;
    if (barEl) barEl.style.width = pct + '%';

    if (statusEl) {
        if (filled === 0) {
            statusEl.textContent = 'No positions filled yet';
            statusEl.className = 'text-center mt-2 text-xs font-semibold text-outline';
        } else if (remaining === 0) {
            statusEl.textContent = '⚠️ All vacancies filled — consider increasing positions or starting a new cycle';
            statusEl.className = 'text-center mt-2 text-xs font-semibold text-red-600';
            if (barEl) barEl.className = 'h-full rounded-full transition-all duration-500 ease-out bg-red-500';
        } else if (remaining <= Math.ceil(total * 0.25)) {
            statusEl.textContent = `${filled} filled, ${remaining} remaining — almost full`;
            statusEl.className = 'text-center mt-2 text-xs font-semibold text-amber-600';
            if (barEl) barEl.className = 'h-full rounded-full transition-all duration-500 ease-out bg-amber-500';
        } else {
            statusEl.textContent = `${filled} filled, ${remaining} remaining`;
            statusEl.className = 'text-center mt-2 text-xs font-semibold text-emerald';
            if (barEl) barEl.className = 'h-full rounded-full transition-all duration-500 ease-out bg-emerald';
        }
    }
}

function updateStrictnessPreview() {
    const matchVal = parseInt(document.getElementById('match-threshold-slider').value);
    const aiVal = parseInt(document.getElementById('ai-threshold-slider').value);
    const matchStrictness = matchVal / 100;
    const aiStrictness = (100 - aiVal) / 100;
    const avg = (matchStrictness + aiStrictness) / 2;
    let label, color;
    if (avg >= 0.7) { label = 'Very Strict'; color = '#dc2626'; }
    else if (avg >= 0.5) { label = 'Strict'; color = '#d97706'; }
    else if (avg >= 0.3) { label = 'Balanced'; color = '#2563eb'; }
    else { label = 'Lenient'; color = '#059669'; }
    const el = document.getElementById('summary-strictness');
    el.textContent = label;
    el.style.color = color;
}
