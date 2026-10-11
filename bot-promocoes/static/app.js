const form = document.getElementById("filters");
const grid = document.getElementById("grid");
const empty = document.getElementById("empty");
const count = document.getElementById("count");
const tpl = document.getElementById("card-tpl");
const refreshBtn = document.getElementById("refresh-btn");
const statusText = document.getElementById("status-text");
const statusTable = document.getElementById("status-table");
const descontoOut = document.getElementById("desconto-out");

const brl = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });
const dateFmt = new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" });

function buildQuery() {
  const params = new URLSearchParams();
  for (const el of form.elements) {
    if (!el.name) continue;
    if (el.name === "so_promocoes" || el.name === "so_disponiveis") {
      params.set(el.name, el.checked ? "1" : "0");
    } else if (el.type === "checkbox") {
      if (el.checked) params.append(el.name, el.value);
    } else if (el.value !== "" && !(el.name === "desconto_min" && el.value === "0")) {
      params.set(el.name, el.value);
    }
  }
  return params;
}

// Mantém os filtros na URL para poder salvar/compartilhar a busca.
function restoreFromUrl() {
  const params = new URLSearchParams(location.search);
  if (![...params.keys()].length) return;
  for (const el of form.elements) {
    if (!el.name) continue;
    if (el.name === "so_promocoes" || el.name === "so_disponiveis") {
      if (params.has(el.name)) el.checked = params.get(el.name) === "1";
    } else if (el.type === "checkbox") {
      el.checked = params.getAll(el.name).includes(el.value);
      if (el.name === "loja" && !params.has("loja")) el.checked = true;
    } else if (params.has(el.name)) {
      el.value = params.get(el.name);
    }
  }
}

function timeLeft(iso) {
  const ms = new Date(iso) - Date.now();
  if (Number.isNaN(ms) || ms <= 0) return null;
  const h = Math.floor(ms / 3.6e6);
  if (h >= 48) return `${Math.floor(h / 24)} dias`;
  if (h >= 1) return `${h}h`;
  return `${Math.ceil(ms / 6e4)} min`;
}

function tag(text, cls = "") {
  const span = document.createElement("span");
  span.className = `tag ${cls}`;
  span.textContent = text;
  return span;
}

function render(deals) {
  grid.replaceChildren();
  count.textContent = `${deals.length} ${deals.length === 1 ? "oferta" : "ofertas"}`;
  empty.hidden = deals.length > 0;
  if (!deals.length) {
    empty.textContent = statusTable.children.length
      ? "Nenhuma oferta com esses filtros. Tente afrouxar o preço ou o desconto mínimo."
      : "Ainda não há dados. A primeira coleta pode levar alguns minutos.";
  }
  for (const d of deals) {
    const card = tpl.content.firstElementChild.cloneNode(true);
    const thumb = card.querySelector(".thumb");
    thumb.href = d.url;
    const img = card.querySelector("img");
    img.alt = d.title;
    if (d.image) {
      img.src = d.image;
    } else {
      img.remove();
      thumb.classList.add("noimg");
      thumb.textContent = "Sem imagem";
    }

    const tags = card.querySelector(".tags");
    tags.append(tag(d.store));
    tags.append(tag(window.CATEGORIES[d.category]?.label ?? d.category));
    if (d.effective_discount > 0) tags.append(tag(`-${Math.round(d.effective_discount)}%`, "off"));
    if (d.history_count > 1 && d.price <= d.lowest_price) tags.append(tag("Menor preço visto", "low"));
    const left = d.offer_ends_at && timeLeft(d.offer_ends_at);
    if (left) tags.append(tag(`Acaba em ${left}`, "timer"));

    const title = card.querySelector(".title");
    title.href = d.url;
    title.textContent = d.title;
    title.title = d.title;

    const ref = d.original_price || (d.previous_price > d.price ? d.previous_price : null);
    card.querySelector(".old").textContent = ref ? brl.format(ref) : "";
    card.querySelector(".price").textContent = brl.format(d.price);
    card.querySelector(".foot").textContent =
      `Visto desde ${dateFmt.format(new Date(d.first_seen))}`;
    grid.append(card);
  }
}

let pending;
async function loadDeals() {
  const params = buildQuery();
  history.replaceState(null, "", `?${params}`);
  pending?.abort();
  pending = new AbortController();
  try {
    const resp = await fetch(`/api/deals?${params}`, { signal: pending.signal });
    render((await resp.json()).deals);
  } catch (err) {
    if (err.name !== "AbortError") {
      empty.hidden = false;
      empty.textContent = "Não foi possível carregar as ofertas.";
    }
  }
}

let wasBusy = false;
let statusTimer;
async function loadStatus() {
  clearTimeout(statusTimer);
  let busy = false;
  try {
    const data = await (await fetch("/api/status")).json();
    busy = data.coletando;
    statusText.textContent = busy
      ? "Coletando ofertas…"
      : data.ultima_coleta
        ? `Última coleta: ${dateFmt.format(new Date(data.ultima_coleta))}`
        : "";
    refreshBtn.disabled = busy;
    statusTable.replaceChildren(
      ...data.lojas.map((s) => {
        const tr = document.createElement("tr");
        const label = window.CATEGORIES[s.category]?.label ?? s.category;
        const result = s.ok ? `${s.count} produtos` : `erro: ${s.message}`;
        for (const [text, cls] of [[s.store], [label], [result, s.ok ? "ok" : "err"]]) {
          const td = document.createElement("td");
          td.textContent = text;
          if (cls) td.className = cls;
          tr.append(td);
        }
        return tr;
      }),
    );
    if (wasBusy && !busy) loadDeals();
    wasBusy = busy;
  } catch {
    statusText.textContent = "Servidor indisponível";
  }
  statusTimer = setTimeout(loadStatus, busy ? 4000 : 60000);
}

let debounce;
form.addEventListener("input", (e) => {
  if (e.target.name === "desconto_min") descontoOut.textContent = `${e.target.value}%`;
  clearTimeout(debounce);
  debounce = setTimeout(loadDeals, e.target.type === "search" || e.target.type === "number" ? 350 : 0);
});
form.addEventListener("submit", (e) => e.preventDefault());

refreshBtn.addEventListener("click", async () => {
  refreshBtn.disabled = true;
  await fetch("/api/atualizar", { method: "POST" });
  wasBusy = true;
  setTimeout(loadStatus, 800);
});

restoreFromUrl();
descontoOut.textContent = `${form.elements.desconto_min.value}%`;
loadDeals();
loadStatus();
