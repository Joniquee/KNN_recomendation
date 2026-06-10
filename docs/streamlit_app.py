import streamlit as st
import streamlit.components.v1 as components
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv('API_URL', 'http://localhost:8000')
DEFAULT_TRACK_ID = os.getenv('DEFAULT_TRACK_ID', '051006')

st.set_page_config(
    page_title="Music Recommender",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: #121212; }
    [data-testid="stHeader"] { background: transparent; }

    .track-card {
        background: #1e1e1e;
        border-radius: 20px;
        padding: 28px;
        display: flex;
        gap: 24px;
        align-items: center;
        margin-bottom: 20px;
    }
    .cover-wrap {
        flex-shrink: 0;
        width: 160px;
        height: 160px;
        border-radius: 12px;
        overflow: hidden;
        background: #2a2a2a;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 72px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.6);
    }
    .cover-wrap img { width: 100%; height: 100%; object-fit: cover; }
    .track-meta { flex: 1; min-width: 0; }
    .track-title {
        font-size: 1.5em;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 6px 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .track-artist { font-size: 1em; color: #aaaaaa; margin: 0 0 10px 0; }
    .track-id { font-size: 0.8em; color: #555; font-family: monospace; }

    div[data-testid="column"] > div > div > div > button {
        background: #2a2a2a !important;
        color: #fff !important;
        border: none !important;
        border-radius: 50px !important;
        font-size: 1.1em !important;
        padding: 10px !important;
        transition: background 0.2s !important;
    }
    div[data-testid="column"] > div > div > div > button:hover {
        background: #3a3a3a !important;
    }
    div[data-testid="column"] > div > div > div > button:disabled {
        opacity: 0.3 !important;
    }

    .queue-label {
        color: #666;
        font-size: 0.85em;
        text-align: center;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── API helpers ────────────────────────────────────────────────────────────────

def get_track_info(track_id: str) -> dict:
    try:
        r = requests.get(f"{API_URL}/track_info/{track_id}", timeout=5)
        return r.json() if r.ok else {}
    except Exception:
        return {}

def load_recommendations(track_id: str) -> list:
    try:
        r = requests.get(
            f"{API_URL}/next_track",
            params={"curent_track_id": track_id},
            timeout=20,
        )
        if r.ok:
            return [str(k).zfill(6) for k in r.json().keys()]
    except Exception:
        pass
    return []

# ── Session state ──────────────────────────────────────────────────────────────

if "queue" not in st.session_state:
    st.session_state.queue = [DEFAULT_TRACK_ID]
if "pos" not in st.session_state:
    st.session_state.pos = 0
if "prefetched_for" not in st.session_state:
    st.session_state.prefetched_for = None

current_id: str = st.session_state.queue[st.session_state.pos]

if (
    st.session_state.prefetched_for != current_id
    and st.session_state.pos == len(st.session_state.queue) - 1
):
    recs = load_recommendations(current_id)
    new = [t for t in recs if t not in st.session_state.queue]
    if new:
        st.session_state.queue.extend(new)
    st.session_state.prefetched_for = current_id

# ── Data ───────────────────────────────────────────────────────────────────────

info = get_track_info(current_id)
title  = info.get("title")  or f"Track {current_id}"
artist = info.get("artist") or "Unknown Artist"
img_url = info.get("image_url") or ""
audio_url = f"{API_URL}/audio/{current_id}"

# ── Track card ─────────────────────────────────────────────────────────────────

cover_html = (
    f'<img src="{img_url}" alt="cover">'
    if img_url
    else "🎵"
)

st.markdown(f"""
<div class="track-card">
  <div class="cover-wrap">{cover_html}</div>
  <div class="track-meta">
    <p class="track-title">{title}</p>
    <p class="track-artist">{artist}</p>
    <p class="track-id">id: {current_id}</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Audio player (play/pause via JS) ──────────────────────────────────────────

components.html(f"""
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: transparent; display: flex; justify-content: center; }}
  .player {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    padding: 8px 0;
  }}
  button {{
    background: none;
    border: none;
    cursor: pointer;
    color: #fff;
    border-radius: 50%;
    width: 52px;
    height: 52px;
    font-size: 1.6em;
    transition: background 0.15s;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  button:hover {{ background: rgba(255,255,255,0.08); }}
  #btn-pp {{
    background: #1db954;
    width: 60px;
    height: 60px;
    font-size: 1.8em;
  }}
  #btn-pp:hover {{ background: #1ed760; }}
  .progress-wrap {{
    width: 260px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  input[type=range] {{
    flex: 1;
    accent-color: #1db954;
    cursor: pointer;
    height: 4px;
  }}
  .time {{ color: #aaa; font-size: 0.75em; font-family: monospace; min-width: 36px; }}
</style>

<audio id="aud" src="{audio_url}" preload="auto"></audio>

<div class="player">
  <button id="btn-pp" onclick="togglePP()">▶</button>
  <div class="progress-wrap">
    <span class="time" id="cur">0:00</span>
    <input type="range" id="seek" value="0" min="0" step="0.1">
    <span class="time" id="dur">0:00</span>
  </div>
</div>

<script>
  const aud  = document.getElementById('aud');
  const pp   = document.getElementById('btn-pp');
  const seek = document.getElementById('seek');
  const cur  = document.getElementById('cur');
  const dur  = document.getElementById('dur');

  function fmt(s) {{
    const m = Math.floor(s / 60);
    return m + ':' + String(Math.floor(s % 60)).padStart(2, '0');
  }}

  function togglePP() {{
    aud.paused ? aud.play() : aud.pause();
  }}

  aud.addEventListener('play',  () => pp.textContent = '⏸');
  aud.addEventListener('pause', () => pp.textContent = '▶');

  aud.addEventListener('loadedmetadata', () => {{
    seek.max = aud.duration;
    dur.textContent = fmt(aud.duration);
  }});

  aud.addEventListener('timeupdate', () => {{
    seek.value = aud.currentTime;
    cur.textContent = fmt(aud.currentTime);
  }});

  seek.addEventListener('input', () => {{ aud.currentTime = seek.value; }});
</script>
""", height=90)

# ── Prev / Next controls ───────────────────────────────────────────────────────

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

col_prev, col_info, col_next = st.columns([1, 1.5, 1])

with col_prev:
    if st.button("⏮  Назад", disabled=(st.session_state.pos == 0), use_container_width=True):
        st.session_state.pos -= 1
        st.rerun()

with col_info:
    total = len(st.session_state.queue)
    pos   = st.session_state.pos + 1
    st.markdown(
        f"<div class='queue-label'>{pos} / {total}</div>",
        unsafe_allow_html=True,
    )

with col_next:
    if st.button("Далее  ⏭", use_container_width=True):
        queue = st.session_state.queue
        pos   = st.session_state.pos
        if pos < len(queue) - 1:
            st.session_state.pos += 1
        st.rerun()

# ── Queue preview ──────────────────────────────────────────────────────────────

with st.expander("Очередь треков"):
    for i, tid in enumerate(st.session_state.queue):
        marker = "▶" if i == st.session_state.pos else f"{i + 1}."
        color  = "#1db954" if i == st.session_state.pos else "#666"
        st.markdown(
            f"<span style='color:{color}'>{marker} <code>{tid}</code></span>",
            unsafe_allow_html=True,
        )
