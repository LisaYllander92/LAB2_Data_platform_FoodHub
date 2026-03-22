const API = '/api';
let ingredients = [];

async function doSearch() {
    const q = document.getElementById('query').value.trim();
    if (!q) return;

    ingredients = q.split(/[,\s]+/).map(s => s.trim().toLowerCase()).filter(Boolean);
    renderChips();


    const btn = document.getElementById('btn-search');
    btn.disabled = true;
    btn.textContent = 'Söker...';
    document.getElementById('results').innerHTML = loadingHTML();
    try {
        const params = new URLSearchParams({ query: q, number: 5 });
        const res = await fetch(`${API}/recipes/search?${params}`);
        if (!res.ok) throw new Error(`Fel ${res.status}`);
        const data = await res.json();
        renderResults(data.recipes || [], data.totalResults || 0);
    } catch (e) {
        document.getElementById('results').innerHTML = `<div class="error">${e.message}</div>`;
    } finally {
        btn.disabled = false;
        btn.textContent = 'Sök';
    }
}

document.getElementById('query').addEventListener('keydown', e => {
  if (e.key === 'Enter') doSearch();
});


function renderChips() {
    const section = document.getElementById('chips-section');
    const container = document.getElementById('chips');

    if (!ingredients.length) { section.style.display = 'none'; return; }
    section.style.display = 'block';
    container.innerHTML =
    ingredients.map(ing =>
      `<span class="chip">${ing}
        <button onclick="removeIngredient('${ing}')" aria-label="Ta bort ${ing}">×</button>
      </span>`
    ).join('') +
    `<span class="chip chip-add" onclick="addIngredient()">+ lägg till</span>`;
}

function removeIngredient(name) {
  ingredients = ingredients.filter(i => i !== name);
  renderChips();
}

function addIngredient() {
  const name = prompt('Lägg till ingrediens:');
  if (name && name.trim()) {
    ingredients.push(name.trim().toLowerCase());
    renderChips();
  }
}

function computeMatch(list) {
  if (!list || !list.length) return { matched: 0, total: 0 };
  const norm = list.map(i => (typeof i === 'string' ? i : i.name || '').toLowerCase());
  let matched = 0;
  for (const term of ingredients) {
    if (norm.some(ri => ri.includes(term) || term.includes(ri))) matched++;
  }
  return { matched, total: norm.length };
}

function pillCls(ratio) {
  return ratio >= 0.75 ? 'high' : ratio >= 0.5 ? 'mid' : 'low';
}

function renderResults(recipes, total) {
  const el = document.getElementById('results');
  if (!recipes.length) {
    el.innerHTML = emptyHTML('🥦', 'Inga recept matchade.<br>Prova andra ingredienser.');
    return;
  }

  const enriched = recipes.map(r => {
    const { matched, total } = computeMatch(r.ingredients || []);
    return { ...r, matched, total };
  }).sort((a, b) => (b.matched / (b.total || 1)) - (a.matched / (a.total || 1)));

  const cards = enriched.map(r => {
    const pct = r.total > 0 ? Math.round((r.matched / r.total) * 100) : 0;
    const cls = r.total > 0 ? pillCls(r.matched / r.total) : '';
    const time = r.cooking_minutes || r.ready_in_minutes || 0;
    return `
      <div class="recipe-card">
        <div class="rc-top">
          <div class="rc-title">${r.title}</div>
          ${r.total > 0 ? `<span class="pill ${cls}">${r.matched}/${r.total}</span>` : ''}
        </div>
        <div class="rc-meta">
          ${time > 0 ? `<span>⏱ ${time} min</span>` : ''}
          ${r.servings > 0 ? `<span>👤 ${r.servings} port.</span>` : ''}
        </div>
        ${r.total > 0 ? `
          <div class="bar-labels">
            <span>Du har ${r.matched}/${r.total} ingredienser hemma</span>
            <span>${pct}%</span>
          </div>
          <div class="bar-bg">
            <div class="bar-fill ${cls === 'mid' ? 'mid' : cls === 'low' ? 'low' : ''}"
                 style="width:${pct}%"></div>
          </div>` : ''}
      </div>`;
  }).join('');

  el.innerHTML = `
    <div class="section-label" style="margin-bottom:10px">${total} recept hittade</div>
    <div class="recipe-list">${cards}</div>`;
}


const EMOJIS = ['🍝','🍗','🥗','🍲','🍛','🥘','🫕','🍜','🥩','🫔'];

function emojiFor(title) {
  let h = 0;
  for (const c of title) h = (h * 31 + c.charCodeAt(0)) & 0xffff;
  return EMOJIS[h % EMOJIS.length];
}

function formatDate(str) {
  if (!str) return '';
  const d = new Date(str), now = new Date();
  const days = Math.floor((now - d) / 86400000);
  if (days === 0) return 'idag';
  if (days === 1) return 'igår';
  if (days < 7)  return `${days} dagar sedan`;
  if (days < 14) return 'förra veckan';
  return d.toLocaleDateString('sv-SE', { day: 'numeric', month: 'short' });
}

async function loadHistory() {
  const el = document.getElementById('history');
  el.innerHTML = loadingHTML();
  try {
    const res = await fetch(`${API}/recipes/history?limit=20`);
    if (!res.ok) throw new Error(`Fel ${res.status}`);
    const data = await res.json();
    if (!data.length) {
      el.innerHTML = emptyHTML('📖', 'Du har inga sparade recept ännu.<br>Sök på ingredienser för att komma igång!');
      return;
    }
    el.innerHTML =
      `<div class="section-label" style="margin-bottom:10px">Senast sökta recept</div>` +
      data.map(r => `
        <div class="history-item">
          <div class="hi-left">
            <div class="hi-icon">${emojiFor(r.title)}</div>
            <div>
              <div class="hi-title">${r.title}</div>
              <div class="hi-date">${formatDate(r.created_at)}</div>
            </div>
          </div>
          <div class="hi-arrow">›</div>
        </div>`).join('');
  } catch (e) {
    el.innerHTML = `<div class="error">${e.message}</div>`;
  }
}


function switchTab(name, btn) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('tab-' + name).classList.add('active');
  if (name === 'history') loadHistory();
}


function loadingHTML() {
  return `<div class="loading"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>`;
}

function emptyHTML(icon, text) {
  return `<div class="empty"><div class="empty-icon">${icon}</div><p>${text}</p></div>`;
}

document.getElementById('results').innerHTML = emptyHTML('🍳', 'Sök på ingredienser du har hemma<br>så hittar vi recept åt dig.');