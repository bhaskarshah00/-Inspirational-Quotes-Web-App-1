const $ = (s) => document.querySelector(s);
const qs = (k) => encodeURIComponent(k || 'auto');

async function fetchJSON(url) {
  const r = await fetch(url, { headers: { 'Accept': 'application/json' } });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

function setQuoteCard(payload) {
  const { quote, provider, fetched_at, cached, offline } = payload;
  $('#quoteText').textContent = quote.text || '—';
  $('#quoteAuthor').textContent = quote.author || 'Unknown';
  $('#provider').textContent = (provider || 'auto').toUpperCase();
  const when = new Date(fetched_at || Date.now());
  $('#timestamp').textContent = when.toLocaleString();
  const status = cached ? ' (cached)' : offline ? ' (offline fallback)' : '';
  $('#statusLine').textContent = `Source: ${provider}${status}`;
}

function setImage() {
  const src = $('#imageSource').value;
  // Ask backend to proxy image bytes to sidestep CORS/hotlink issues
  const url = `/api/image?source=${qs(src)}&ts=${Date.now()}`;
  $('#heroImage').src = url;
}

async function loadRandom() {
  try {
    const src = $('#randomSource').value;
    const data = await fetchJSON(`/api/random?source=${qs(src)}`);
    if (data.ok) setQuoteCard(data);
  } catch (e) {
    $('#statusLine').textContent = 'Failed to load random quote.';
  }
}

async function loadToday() {
  try {
    const src = $('#todaySource').value;
    const data = await fetchJSON(`/api/today?source=${qs(src)}`);
    if (data.ok) setQuoteCard(data);
  } catch (e) {
    $('#statusLine').textContent = 'Failed to load today quote.';
  }
}

function copyQuote() {
  const text = `"${$('#quoteText').textContent}" — ${$('#quoteAuthor').textContent}`;
  navigator.clipboard.writeText(text).then(() => {
    const btn = $('#btnCopy');
    btn.textContent = 'Copied!';
    setTimeout(() => (btn.textContent = 'Copy'), 1200);
  });
}

function tweetQuote() {
  const text = encodeURIComponent(`"${$('#quoteText').textContent}" — ${$('#quoteAuthor').textContent}`);
  window.open(`https://twitter.com/intent/tweet?text=${text}`, '_blank');
}

function downloadCard() {
  const card = document.getElementById('quoteCard');
  html2canvas(card).then((canvas) => {
    const link = document.createElement('a');
    link.download = `quotewave-${Date.now()}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
  });
}

function toggleTheme() {
  document.documentElement.classList.toggle('light');
}

function init() {
  $('#year').textContent = new Date().getFullYear();
  $('#btnRandom').addEventListener('click', loadRandom);
  $('#btnToday').addEventListener('click', loadToday);
  $('#btnImage').addEventListener('click', setImage);
  $('#btnCopy').addEventListener('click', copyQuote);
  $('#btnTweet').addEventListener('click', tweetQuote);
  $('#btnRefresh').addEventListener('click', () => { loadRandom(); setImage(); });
  $('#btnDownload').addEventListener('click', downloadCard);
  $('#themeToggle').addEventListener('click', toggleTheme);

  // Initial content
  setImage();
  loadToday().catch(loadRandom);
}

document.addEventListener('DOMContentLoaded', init);

// REMOVE this function
function applyDarkMode(isDark) {
  document.body.classList.toggle("dark-mode", isDark);
  const quoteText = document.getElementById("quote-text");
  const quoteAuthor = document.getElementById("quote-author");
  const quoteProvider = document.getElementById("quote-provider");
  if (isDark) {
    if (quoteText) quoteText.style.color = "#f5f5f5";
    if (quoteAuthor) quoteAuthor.style.color = "#f5f5f5";
    if (quoteProvider) quoteProvider.style.color = "#f5f5f5";
  } else {
    if (quoteText) quoteText.style.color = "#222";
    if (quoteAuthor) quoteAuthor.style.color = "#555";
    if (quoteProvider) quoteProvider.style.color = "#555";
  }
}


function preloadImage(url, callback) {
  const img = new Image();
  img.src = url;
  img.onload = () => callback(img);
  img.onerror = () => callback(null); // fallback
}

// Example usage for image loading with spinner
const img = document.getElementById("quote-img");
const spinner = document.querySelector(".spinner");
const imageUrl = "/static/sample-image.jpg"; // Replace with your dynamic image URL

spinner.style.display = "block";
preloadImage(imageUrl, (loadedImg) => {
  if (loadedImg) {
    img.src = loadedImg.src;
    img.style.display = "block";
  }
  spinner.style.display = "none";
});
