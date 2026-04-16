const API = "http://localhost:8000";
let yearChart = null, typeChart = null;

// ── Navegação ──────────────────────────────────────────────
document.querySelectorAll("nav button[data-tab]").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll("nav button[data-tab]").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(btn.dataset.tab).classList.add("active");
    if (btn.dataset.tab === "tab-analytics") loadAnalytics();
  });
});

// ── Toast ──────────────────────────────────────────────────
function toast(msg, type = "info") {
  const icons = { success:"✅", error:"❌", info:"ℹ️", warning:"⚠️" };
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.innerHTML = `<span>${icons[type]||"•"}</span> ${msg}`;
  document.getElementById("toast-container").appendChild(el);
  setTimeout(() => el.remove(), 4500);
}

// ── Progress ───────────────────────────────────────────────
function setProgress(id, active, label = "") {
  const c = document.getElementById(id);
  const fill = c.querySelector(".progress-fill");
  c.classList.toggle("hidden", !active);
  if (active) { fill.classList.add("indeterminate"); c.querySelector(".progress-label").textContent = label; }
  else fill.classList.remove("indeterminate");
}

// ── Health check ───────────────────────────────────────────
(async () => {
  try {
    const data = await fetch(`${API}/health`).then(r => r.json());
    const badges = document.getElementById("health-badges");
    const mk = (label, ok) => `<span class="health-badge ${ok ? 'ok' : 'error'}">● ${label}</span>`;
    badges.innerHTML = mk("MongoDB", data.mongodb === "connected") + mk("PostgreSQL", data.postgresql === "connected");
  } catch {
    document.getElementById("health-badges").innerHTML = `<span class="health-badge error">● API offline</span>`;
  }
})();

// ══════════════════════════════════════════════════════════
// ABA BD — JSONL Pipeline
// ══════════════════════════════════════════════════════════
const slots = { producao: null, pessoa: null, equipe: null };

["producao", "pessoa", "equipe"].forEach(name => {
  const slot = document.getElementById(`slot-${name}`);
  const input = document.getElementById(`file-${name}`);
  slot.addEventListener("click", () => input.click());
  input.addEventListener("change", () => {
    if (input.files[0]) {
      slots[name] = input.files[0];
      slot.classList.add("filled");
      slot.querySelector(".slot-filename").textContent = `✓ ${input.files[0].name}`;
      checkBdReady();
    }
  });
});

function checkBdReady() {
  const ready = slots.producao && slots.pessoa && slots.equipe;
  document.getElementById("btn-run-bd").disabled = !ready;
}

document.getElementById("btn-run-bd").addEventListener("click", async () => {
  const btn = document.getElementById("btn-run-bd");
  btn.disabled = true;
  setProgress("progress-bd", true, "Executando pipeline completa...");
  document.getElementById("bd-results").classList.add("hidden");

  try {
    const form = new FormData();
    form.append("producao", slots.producao);
    form.append("pessoa",   slots.pessoa);
    form.append("equipe",   slots.equipe);

    const res  = await fetch(`${API}/pipeline/bd-producao-artistica`, { method: "POST", body: form });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Erro na pipeline");

    renderBdResults(data);
    toast("Pipeline completa executada com sucesso!", "success");
  } catch (err) {
    toast(err.message, "error");
  } finally {
    setProgress("progress-bd", false);
    btn.disabled = false;
  }
});

function renderBdResults(data) {
  const s = data.stages;
  document.getElementById("bd-results").classList.remove("hidden");

  // Qualidade
  const qGrid = document.getElementById("bd-quality-grid");
  qGrid.innerHTML = ["producao", "pessoa", "equipe"].map(key => {
    const q = s.quality?.[key] || {};
    const issues = (q.high_null_columns || []).length;
    return `
      <div class="quality-file-card">
        <h4>${key}.jsonl</h4>
        <div class="stat-row"><span class="label">Registros</span><span class="value">${(q.total_records||0).toLocaleString()}</span></div>
        <div class="stat-row"><span class="label">Duplicatas</span><span class="value">${q.duplicate_rows||0}</span></div>
        <div class="stat-row"><span class="label">Completude</span><span class="value">${q.completeness_pct||0}%</span></div>
        ${issues > 0 ? `<p style="color:var(--warning);font-size:0.75rem;margin-top:0.5rem">⚠️ ${issues} coluna(s) com >50% nulos</p>` : '<p style="color:var(--success);font-size:0.75rem;margin-top:0.5rem">✓ Sem colunas críticas</p>'}
      </div>`;
  }).join("");

  // Collections
  const colGrid = document.getElementById("bd-collections-grid");
  const collections = [
    { name: "raw_producao",  count: s.raw_load?.raw_producao?.inserted,  label: "RAW" },
    { name: "raw_pessoa",    count: s.raw_load?.raw_pessoa?.inserted,     label: "RAW" },
    { name: "raw_equipe",    count: s.raw_load?.raw_equipe?.inserted,     label: "RAW" },
    { name: "producao_clean",count: s.clean_load?.producao_clean?.inserted, label: "CLEAN" },
    { name: "pessoa_clean",  count: s.clean_load?.pessoa_clean?.inserted,   label: "CLEAN" },
    { name: "equipe_clean",  count: s.clean_load?.equipe_clean?.inserted,   label: "CLEAN" },
    { name: "producoes_com_participantes", count: s.enrichment?.producoes_enriquecidas, label: "RICO" },
  ];
  colGrid.innerHTML = collections.map(c => `
    <div class="collection-item">
      <div class="cname">${c.name}</div>
      <div class="ccount">${(c.count || 0).toLocaleString()}</div>
      <div class="clabel">${c.label}</div>
    </div>`).join("");

  // Enriquecimento
  const enr = s.enrichment || {};
  document.getElementById("bd-enrichment").innerHTML = `
    <div class="stat-row"><span class="label">Produções enriquecidas</span><span class="value" style="color:var(--success)">${enr.producoes_enriquecidas||0}</span></div>
    <div class="stat-row"><span class="label">Produções sem equipe</span><span class="value" style="color:var(--warning)">${enr.producoes_sem_equipe||0}</span></div>
    <div class="stat-row"><span class="label">Registros equipe órfãos</span><span class="value" style="color:var(--warning)">${enr.orphan_equipe_records||0}</span></div>
    <p style="margin-top:0.75rem;font-size:0.8rem;color:var(--text-muted)">
      Cada produção em <span class="collection-badge">producoes_com_participantes</span> traz os participantes aninhados — sem necessidade de JOIN.
    </p>`;

  // PostgreSQL
  const pg = s.postgresql || {};
  const pgEl = document.getElementById("bd-postgres");
  if (pg.status === "success") {
    pgEl.innerHTML = `
      <div class="stat-row"><span class="label">Produções inseridas</span><span class="value">${pg.producao_inserted||0}</span></div>
      <div class="stat-row"><span class="label">Pessoas inseridas</span><span class="value">${pg.pessoa_inserted||0}</span></div>
      <div class="stat-row"><span class="label">Equipe inserida</span><span class="value">${pg.equipe_inserted||0}</span></div>
      <p style="margin-top:0.75rem;font-size:0.8rem;color:var(--text-muted)">Dados espelhados para comparação na aba Analytics → Comparação MongoDB vs PostgreSQL.</p>`;
  } else {
    pgEl.innerHTML = `<p style="color:var(--warning);font-size:0.85rem">⚠️ ${pg.detail || "PostgreSQL não disponível."}</p>`;
  }
}

// ══════════════════════════════════════════════════════════
// ABA CSV
// ══════════════════════════════════════════════════════════
const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
let selectedFile = null;

dropZone.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("dragover", e => { e.preventDefault(); dropZone.classList.add("dragover"); });
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));
dropZone.addEventListener("drop", e => { e.preventDefault(); dropZone.classList.remove("dragover"); if (e.dataTransfer.files[0]) selectFile(e.dataTransfer.files[0]); });
fileInput.addEventListener("change", () => { if (fileInput.files[0]) selectFile(fileInput.files[0]); });

function selectFile(file) {
  if (!file.name.toLowerCase().endsWith(".csv")) { toast("Apenas arquivos .csv são aceitos.", "error"); return; }
  selectedFile = file;
  dropZone.querySelector(".filename").textContent = `📄 ${file.name} (${(file.size/1024).toFixed(1)} KB)`;
  document.getElementById("btn-run-csv").disabled = false;
}

document.getElementById("btn-run-csv").addEventListener("click", async () => {
  if (!selectedFile) return;
  const btn = document.getElementById("btn-run-csv");
  btn.disabled = true;
  setProgress("progress-csv", true, "Executando pipeline...");
  try {
    const form = new FormData();
    form.append("file", selectedFile);
    const res = await fetch(`${API}/pipeline/upload`, { method: "POST", body: form });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail);
    renderQualityReport(data.quality_report, "quality-csv", "quality-csv-card");
    renderLoadResult(data.load_result, "result-csv", "result-csv-placeholder", selectedFile.name);
    toast(`Pipeline concluída! Collection: ${data.collection_name}`, "success");
  } catch (err) {
    toast(err.message, "error");
    showError("result-csv", err.message);
  } finally { setProgress("progress-csv", false); btn.disabled = false; }
});

// ══════════════════════════════════════════════════════════
// ABA URL
// ══════════════════════════════════════════════════════════
document.querySelectorAll(".url-example-chip").forEach(c => {
  c.addEventListener("click", () => { document.getElementById("url-input").value = c.dataset.url; });
});

document.getElementById("btn-run-url").addEventListener("click", async () => {
  const url = document.getElementById("url-input").value.trim();
  if (!url) { toast("Informe uma URL.", "warning"); return; }
  const btn = document.getElementById("btn-run-url");
  btn.disabled = true;
  setProgress("progress-url", true, "Importando dados...");
  try {
    const res = await fetch(`${API}/pipeline/url`, { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({url}) });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail);
    renderQualityReport(data.quality_report, "quality-url", "quality-url-card");
    renderLoadResult(data.load_result, "result-url", "result-url-placeholder", "URL");
    toast(`Importação concluída! Collection: ${data.collection_name}`, "success");
  } catch (err) {
    toast(err.message, "error");
    showError("result-url", err.message);
  } finally { setProgress("progress-url", false); btn.disabled = false; }
});

// ══════════════════════════════════════════════════════════
// ABA ANALYTICS
// ══════════════════════════════════════════════════════════
async function loadAnalytics() {
  document.getElementById("btn-refresh").disabled = true;
  try {
    const [summary, byYear, byType, ranking] = await Promise.all([
      fetch(`${API}/analytics/summary?collection=producoes_com_participantes`).then(r => r.json()).catch(() => ({})),
      fetch(`${API}/analytics/bd/producoes-por-ano`).then(r => r.json()).catch(() => ({ data: [] })),
      fetch(`${API}/analytics/bd/producoes-por-tipo`).then(r => r.json()).catch(() => ({ data: [] })),
      fetch(`${API}/analytics/bd/ranking-pessoas`).then(r => r.json()).catch(() => ({ data: [] })),
    ]);

    document.getElementById("metric-total").textContent = (summary.total_records || 0).toLocaleString();

    // Participantes únicos e papéis via ranking
    const uniquePeople = (ranking.data || []).length;
    document.getElementById("metric-pessoas").textContent = uniquePeople > 0 ? `${uniquePeople}+` : "—";

    // Papéis via aggregação
    try {
      const papeis = await fetch(`${API}/analytics/bd/papeis-mais-frequentes`).then(r => r.json());
      document.getElementById("metric-papeis").textContent = (papeis.data || []).length || "—";
    } catch { document.getElementById("metric-papeis").textContent = "—"; }

    renderYearChart(byYear.data || []);
    renderTypeChart(byType.data || []);
    renderRankingTable(ranking.data || []);

    if ((summary.total_records || 0) === 0) toast("Execute a pipeline BD primeiro.", "info");
  } catch (err) {
    toast("Erro ao carregar analytics: " + err.message, "error");
  } finally {
    document.getElementById("btn-refresh").disabled = false;
  }
}

function renderYearChart(data) {
  const canvas = document.getElementById("chart-year");
  const empty  = document.getElementById("chart-year-empty");
  if (!data.length) { canvas.classList.add("hidden"); empty.classList.remove("hidden"); return; }
  canvas.classList.remove("hidden"); empty.classList.add("hidden");
  if (yearChart) yearChart.destroy();
  yearChart = new Chart(canvas.getContext("2d"), {
    type: "bar",
    data: { labels: data.map(d => d.ano), datasets: [{ label: "Produções", data: data.map(d => d.total), backgroundColor: "rgba(99,102,241,0.7)", borderColor: "rgba(99,102,241,1)", borderWidth: 1, borderRadius: 4 }] },
    options: { responsive: true, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: "#94a3b8" }, grid: { color: "#2e3250" } }, y: { ticks: { color: "#94a3b8" }, grid: { color: "#2e3250" } } } },
  });
}

function renderTypeChart(data) {
  const canvas = document.getElementById("chart-type");
  const empty  = document.getElementById("chart-type-empty");
  if (!data.length) { canvas.classList.add("hidden"); empty.classList.remove("hidden"); return; }
  canvas.classList.remove("hidden"); empty.classList.add("hidden");
  if (typeChart) typeChart.destroy();
  const colors = ["#6366f1","#22c55e","#f59e0b","#ef4444","#06b6d4","#a78bfa","#f472b6","#34d399","#fb923c","#818cf8"];
  typeChart = new Chart(canvas.getContext("2d"), {
    type: "doughnut",
    data: { labels: data.map(d => d.tipo), datasets: [{ data: data.map(d => d.total), backgroundColor: colors, borderWidth: 0 }] },
    options: { responsive: true, plugins: { legend: { position: "bottom", labels: { color: "#94a3b8", padding: 10, boxWidth: 10 } } } },
  });
}

function renderRankingTable(data) {
  const tbody = document.querySelector("#table-ranking tbody");
  tbody.innerHTML = "";
  if (!data.length) {
    tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;color:var(--text-muted)">Nenhum dado disponível. Execute a pipeline BD primeiro.</td></tr>`;
    return;
  }
  data.forEach((row, i) => {
    const papeis = (row.papeis || []).filter(p => p && p !== "N/A").slice(0, 3).join(", ");
    const tr = document.createElement("tr");
    tr.innerHTML = `<td style="color:var(--text-muted)">${i+1}</td><td>${row.nome}</td><td style="font-weight:600;color:var(--accent)">${row.total_participacoes}</td><td style="font-size:0.78rem;color:var(--text-muted)">${papeis || "—"}</td>`;
    tbody.appendChild(tr);
  });
}

document.getElementById("btn-refresh").addEventListener("click", loadAnalytics);

// Comparação SQL
document.getElementById("btn-comparacao").addEventListener("click", async () => {
  const el = document.getElementById("comparacao-result");
  el.textContent = "Executando consultas...";
  try {
    const res  = await fetch(`${API}/analytics/comparacao-sql`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail);
    const pg = data.postgresql_results || {};
    let html = `<p style="margin-bottom:0.75rem;color:var(--text)">${data.note || ""}</p>`;
    html += `<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;font-size:0.8rem">`;
    html += `<div><strong style="color:var(--accent)">MongoDB</strong><p style="color:var(--text-muted);margin-top:0.25rem">1 consulta em producoes_com_participantes — dados aninhados, sem JOIN</p></div>`;
    html += `<div><strong style="color:#22c55e">PostgreSQL</strong><p style="color:var(--text-muted);margin-top:0.25rem">JOIN entre producao + equipe + pessoa necessário para cada consulta</p></div>`;
    html += `</div>`;
    if (pg.top_pessoas?.data?.length) {
      html += `<p style="margin-top:0.75rem;font-size:0.78rem;color:var(--text-muted)">Top 5 no PostgreSQL (JOIN): ${pg.top_pessoas.data.slice(0,5).map(r=>`${r.nome} (${r.participacoes})`).join(", ")}</p>`;
    }
    if (pg.note) html += `<p style="margin-top:0.5rem;font-size:0.78rem;color:var(--warning)">💡 ${pg.note}</p>`;
    el.innerHTML = html;
  } catch (err) {
    el.innerHTML = `<p style="color:var(--error)">❌ ${err.message}</p>`;
  }
});

// ── Helpers ────────────────────────────────────────────────
function renderQualityReport(report, containerId, cardId) {
  const card = document.getElementById(cardId);
  const el   = document.getElementById(containerId);
  card.style.display = "block";
  el.innerHTML = "";
  const grid = document.createElement("div");
  grid.className = "quality-grid";
  grid.innerHTML = `
    <div class="quality-stat"><div class="val">${report.total_records.toLocaleString()}</div><div class="lbl">Registros</div></div>
    <div class="quality-stat"><div class="val">${report.total_columns}</div><div class="lbl">Colunas</div></div>
    <div class="quality-stat"><div class="val">${report.duplicate_rows}</div><div class="lbl">Duplicatas</div></div>
    <div class="quality-stat"><div class="val">${report.summary.overall_completeness_pct}%</div><div class="lbl">Completude</div></div>
  `;
  el.appendChild(grid);
  if (report.high_null_columns?.length > 0) {
    const w = document.createElement("p");
    w.style.cssText = "color:var(--warning);font-size:0.8rem;margin-bottom:0.75rem";
    w.textContent = `⚠️ Colunas com >50% nulos: ${report.high_null_columns.join(", ")}`;
    el.appendChild(w);
  }
  const acc = document.createElement("div");
  acc.className = "accordion";
  Object.entries(report.columns).forEach(([col, info]) => {
    const item = document.createElement("div");
    item.className = "accordion-item";
    item.innerHTML = `
      <div class="accordion-header">
        <span>${col} <span class="tag ${info.null_percentage > 10 ? 'tag-warn' : 'tag-ok'}">${info.dtype}</span></span>
        <span class="tag ${info.null_count > 0 ? 'tag-null' : 'tag-ok'}">${info.null_count} nulos (${info.null_percentage}%)</span>
      </div>
      <div class="accordion-body">
        <div class="stat-row"><span class="label">Valores únicos</span><span class="value">${info.unique_values}</span></div>
        ${info.mean !== undefined ? `<div class="stat-row"><span class="label">Média</span><span class="value">${info.mean}</span></div>` : ""}
        ${info.outliers ? `<div class="stat-row"><span class="label">Outliers IQR</span><span class="value">${info.outliers.count}</span></div>` : ""}
        ${info.sample_values ? `<div class="stat-row"><span class="label">Amostras</span><span class="value" style="font-size:0.72rem">${info.sample_values.slice(0,6).join(", ")}</span></div>` : ""}
      </div>`;
    item.querySelector(".accordion-header").addEventListener("click", () => item.querySelector(".accordion-body").classList.toggle("open"));
    acc.appendChild(item);
  });
  el.appendChild(acc);
}

function renderLoadResult(result, containerId, placeholderId, label) {
  const el = document.getElementById(containerId);
  const ph = document.getElementById(placeholderId);
  if (ph) ph.style.display = "none";
  el.className = `result-box ${result.errors === 0 ? "success" : "error"}`;
  el.innerHTML = `
    <div style="font-weight:600;margin-bottom:0.75rem">${result.errors===0?"✅":"⚠️"} ${label} → <span class="collection-badge">${result.collection_name}</span></div>
    <div class="stat-row"><span class="label">Total processado</span><span class="value">${result.total_processed.toLocaleString()}</span></div>
    <div class="stat-row"><span class="label">Inseridos</span><span class="value" style="color:var(--success)">${result.inserted}</span></div>
    <div class="stat-row"><span class="label">Atualizados</span><span class="value" style="color:var(--accent)">${result.updated}</span></div>
    <div class="stat-row"><span class="label">Erros</span><span class="value" style="color:${result.errors>0?'var(--error)':'var(--text-muted)'}">${result.errors}</span></div>`;
  el.classList.remove("hidden");
}

function showError(id, msg) {
  const el = document.getElementById(id);
  el.className = "result-box error";
  el.innerHTML = `<strong>❌ Erro:</strong> ${msg}`;
  el.classList.remove("hidden");
}
