const API = '/api';
let ingredients = [];
let lastResults = [];

async function doSearch() {
    const q = document.getElementById('query').value.trim();

    if (q)
    {
        ingredients = q.split(/[,\s]+/).map(s => s.trim().toLowerCase()).filter(Boolean);
        document.getElementById('query').value = '';
    } else if (ingredients.length === 0) {
        return;
    }
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    document.querySelector('.tab[onclick*="search"]').classList.add('active');
    document.getElementById('tab-search').classList.add('active');

    renderChips();


    const btn = document.getElementById('btn-search');
    btn.disabled = true;
    btn.textContent = 'Söker...';
    document.getElementById('results').innerHTML = loadingHTML();

    try {
        const searchQuery = ingredients.join(', ');
        const params = new URLSearchParams({ query: searchQuery, number: 5 }); // decides params for the search
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
    `<span class="chip chip-add" id="add-chip" onclick="showAddInput()">+ lägg till</span>
     <span class="chip chip-input" id="add-input-chip" style="display:none">
       <input id="add-input" type="text" placeholder="ingrediens..."
              style="border:none;background:transparent;outline:none;font-family:inherit;font-size:13px;width:100px;color:inherit"
              onkeydown="handleAddKey(event)" />
       <button onclick="confirmAdd()" aria-label="Lägg till">↵</button>
     </span>`;
}

function removeIngredient(name) {
  ingredients = ingredients.filter(i => i !== name);
  renderChips();
}


function showAddInput() {
  document.getElementById('add-chip').style.display = 'none';
  document.getElementById('add-input-chip').style.display = 'inline-flex';
  document.getElementById('add-input').focus();
}

function confirmAdd() {
  const input = document.getElementById('add-input');
  const val = input.value.trim();
  if (val)
   {
    ingredients.push(val.toLowerCase());
    renderChips();
    doSearch();
   } else{
   renderChips();
   }
}

function handleAddKey(e) {
  if (e.key === 'Enter') confirmAdd();
  if (e.key === 'Escape') renderChips(); // cancel
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

  lastResults = recipes.map(r => {
    const { matched, total } = computeMatch(r.ingredients || []);
    return { ...r, matched, total };
  }).sort((a, b) => (b.matched / (b.total || 1)) - (a.matched / (a.total || 1)));

  const cards = lastResults.map((r, index) => {
    const pct = r.total > 0 ? Math.round((r.matched / r.total) * 100) : 0;
    const cls = r.total > 0 ? pillCls(r.matched / r.total) : '';
    const time = r.cooking_minutes || r.ready_in_minutes || 0;
    return `
      <div class="recipe-card" onclick="openRecipe(lastResults[${index}].title)" style="cursor:pointer">
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
    const res = await fetch(`${API}/recipes/history?limit=20`); // TODO: add this route when history func is added later
    if (!res.ok) throw new Error(`Fel ${res.status}`);
    const data = await res.json();
    if (!data.length) {
      el.innerHTML = emptyHTML('📖', 'Du har inga sparade recept ännu.<br>Sök på ingredienser för att komma igång!');
      return;
    }
    el.innerHTML =
      `<div class="section-label" style="margin-bottom:10px">Senast sökta recept</div>` +
      data.map((r, i) => `
        <div class="history-item" onclick="openRecipe(this.dataset.title)" data-title="${r.title.replace(/"/g, '&quot;')}">
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
  if (name === 'stats') loadStats();
}


function loadingHTML() {
  return `<div class="loading"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>`;
}

function emptyHTML(icon, text) {
  return `<div class="empty"><div class="empty-icon">${icon}</div><p>${text}</p></div>`;
}

document.getElementById('results').innerHTML = emptyHTML('🍳', 'Sök på ingredienser du har hemma<br>så hittar vi recept åt dig.');

async function openRecipe(title) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.getElementById('tab-detail').classList.add('active');
  document.getElementById('detail-content').innerHTML = loadingHTML();

  try {
    const res = await fetch(`${API}/recipes/detail/${encodeURIComponent(title)}`);
    if (!res.ok) throw new Error(`Fel ${res.status}`);
    const r = await res.json();
    renderDetail(r);
  } catch (e) {
    document.getElementById('detail-content').innerHTML =
      `<div class="error">${e.message}</div>`;
  }
}


function renderDetail(r) {
  const ingredients = (r.ingredients_raw && r.ingredients_raw.length)
    ? r.ingredients_raw
    : r.ingredients_normalized || [];

  document.getElementById('detail-content').innerHTML = `
    <button class="btn-back" onclick="closeDetail()">← Tillbaka</button>
    ${r.image ? `<img src="${r.image}" alt="${r.title}" class="detail-img" />` : ''}
    <h2 class="detail-title">${r.title}</h2>
    <div class="rc-meta" style="margin-bottom:16px">
      ${r.cooking_minutes > 0 ? `<span>⏱ ${r.cooking_minutes} min</span>` : ''}
      ${r.servings > 0 ? `<span>👤 ${r.servings} portioner</span>` : ''}
    </div>
    <div class="section-label" style="margin-bottom:8px">Ingredienser</div>
    <ul class="ingredient-list">
      ${ingredients.map(i => `<li>${i}</li>`).join('')}
    </ul>
    <div class="section-label" style="margin-top:16px; margin-bottom:8px">Instruktioner</div>
    <div class="instructions">${r.instructions || 'Inga instruktioner tillgängliga.'}</div>
  `;
}

function closeDetail() {
  document.getElementById('tab-detail').classList.remove('active');
  document.getElementById('tab-search').classList.add('active');
}

async function loadStats() {
  const el = document.getElementById('stats-content');
  el.innerHTML = loadingHTML();

  try {
    const res = await fetch(`${API}/recipes/stats`);
    if (!res.ok) throw new Error(`Fel ${res.status}`);
    const data = await res.json();
    renderStats(data);
  } catch (e) {
    el.innerHTML = `<div class="error">${e.message}</div>`;
  }
}

function renderStats(data) {
  const el = document.getElementById('stats-content');

  el.innerHTML = `
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-value">${data.total_recipes}</div>
        <div class="stat-label">Recept i databasen</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${data.total_searches}</div>
        <div class="stat-label">Sökningar totalt</div>
      </div>
    </div>

    <div class="section-label" style="margin:18px 0 10px">Populära ingredienser</div>
    <canvas id="popular-chart" width="400" height="220"></canvas>
    <div id="chart-legend"></div>

    <div class="section-label" style="margin:20px 0 10px">Detaljerad graf</div>
    <img src="${API}/recipes/stats/plot" alt="Populära sökningar"
         style="width:100%; border-radius:var(--r-lg); border:0.5px solid var(--border);"
         onerror="this.style.display='none'" />

    <div class="section-label" style="margin:20px 0 10px">Senast visade recept</div>
    ${data.recent.map(r => `
      <div class="history-item" onclick="openRecipe(this.dataset.title)" data-title="${r.title.replace(/"/g, '&quot;')}">
        <div class="hi-left">
          <div class="hi-icon">${emojiFor(r.title)}</div>
          <div><div class="hi-title">${r.title}</div></div>
        </div>
        <div class="hi-arrow">›</div>
      </div>`).join('')}
  `;

  // Wait for DOM to render before drawing on canvas
  setTimeout(() => drawPieChart('popular-chart', data.popular), 0);
}

function drawPieChart(canvasId, data) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const total = data.reduce((sum, d) => sum + d.count, 0);

  const colors = [
    '#F07820','#D4661A','#F9BB8A','#1D9E75','#9FE1CB',
    '#0F6E56','#EF9F27','#E24B4A','#6b6b6b','#085041'
  ];

  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  const r = Math.min(cx, cy) - 10;
  let angle = -Math.PI / 2;

  data.forEach((d, i) => {
    const slice = (d.count / total) * 2 * Math.PI;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, r, angle, angle + slice);
    ctx.closePath();
    ctx.fillStyle = colors[i % colors.length];
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 2;
    ctx.stroke();

    const midAngle = angle + slice / 2;
    const lx = cx + (r * 0.65) * Math.cos(midAngle);
    const ly = cy + (r * 0.65) * Math.sin(midAngle);
    ctx.fillStyle = '#fff';
    ctx.font = '500 11px DM Sans, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(d.query, lx, ly);

    angle += slice;
  });

  // Legend in separate div so it doesn't interfere with canvas
  document.getElementById('chart-legend').innerHTML = `
    <div class="chart-legend">
      ${data.map((d, i) => `
        <div class="legend-item">
          <span class="legend-dot" style="background:${colors[i % colors.length]}"></span>
          ${d.query} (${d.count})
        </div>`).join('')}
    </div>`;
}