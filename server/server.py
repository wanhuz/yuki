import streamlit as st
import pandas as pd
import sqlite3

# ── Page config ────────────────────────────────────────────────────────────────
DB_PATH = "../history.db"

st.set_page_config(
    page_title="Yuki Transfer",
    page_icon="✦",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Epilogue:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --cream:   #faf8f4;
    --warm:    #f2ede4;
    --border:  #e0d9ce;
    --ink:     #1a1714;
    --muted:   #8a8078;
    --accent:  #c0622a;
    --accent2: #2a6b8a;
    --success: #3a7d5c;
    --display: 'Playfair Display', serif;
    --body:    'Epilogue', sans-serif;
    --mono:    'JetBrains Mono', monospace;
}

html, body, [class*="css"] {
    font-family: var(--body) !important;
    background-color: var(--cream) !important;
    color: var(--ink);
}

.main .block-container {
    padding: 3rem 3.5rem 5rem;
    max-width: 1300px;
}

/* ── Header ── */
.page-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 0.3rem;
}
.page-title {
    font-family: var(--display);
    font-size: 3rem;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: -0.02em;
    line-height: 1;
    margin: 0;
}
.page-title em { color: var(--accent); font-style: italic; }
.page-badge {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    border: 1px solid var(--border);
    padding: 0.3rem 0.75rem;
    border-radius: 2px;
    margin-bottom: 0.4rem;
}
.header-rule {
    height: 2px;
    background: linear-gradient(90deg, var(--accent) 0%, var(--border) 55%, transparent 100%);
    margin: 1rem 0 2.5rem;
}

/* ── Stat cards ── */
.stat-row {
    display: flex;
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 2.5rem;
}
.stat-card {
    flex: 1;
    background: var(--cream);
    padding: 1.25rem 1.6rem;
    position: relative;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
    opacity: 0;
    transition: opacity 0.2s;
}
.stat-card:hover::before { opacity: 1; }
.stat-card.b2::before { background: var(--accent2); }
.stat-card.b3::before { background: var(--success); }
.stat-label {
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.stat-value {
    font-family: var(--display);
    font-size: 2rem;
    font-weight: 600;
    color: var(--ink);
    line-height: 1;
}

/* ── Filter heading ── */
.filter-heading {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.75rem;
}

/* ── Table wrapper ── */
.table-shell {
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    background: white;
    margin-top: 1.5rem;
}
.table-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.9rem 1.4rem;
    background: var(--warm);
    border-bottom: 1px solid var(--border);
}
.table-name {
    font-family: var(--display);
    font-size: 1rem;
    font-weight: 600;
    color: var(--ink);
}
.row-pill {
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--accent);
    border: 1px solid var(--accent);
    padding: 0.18rem 0.65rem;
    border-radius: 20px;
    letter-spacing: 0.08em;
}

/* Streamlit widget labels */
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label {
    font-family: var(--mono) !important;
    font-size: 0.63rem !important;
    letter-spacing: 0.11em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}
div[data-testid="stTextInput"] input {
    font-family: var(--mono) !important;
    font-size: 0.85rem !important;
    border-color: var(--border) !important;
    background: var(--cream) !important;
}

/* ── Footer ── */
.footer {
    margin-top: 4rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--muted);
    letter-spacing: 0.08em;
}
.footer span { color: var(--accent); }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Data ───────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=5)
def load_data() -> pd.DataFrame:
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM record", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()
    
def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

df = load_data()

df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime('%d/%m/%Y %I:%M:%S %p')


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <h1 class="page-title">Yuki <em>Transfer</em></h1>
  <span class="page-badge">✦ Records Dashboard</span>
</div>
<div class="header-rule"></div>
""", unsafe_allow_html=True)

# ── Stats ──────────────────────────────────────────────────────────────────────
total_rows   = len(df)
total_cols   = len(df.columns)
numeric_cols = df.select_dtypes("number").columns.tolist()
total_sum    = f"{df[numeric_cols[0]].sum():,.0f}" if numeric_cols else "—"
sum_label    = numeric_cols[0].replace("_", " ").title() if numeric_cols else "Numeric Sum"

st.markdown(f"""
<div class="stat-row">
  <div class="stat-card">
    <div class="stat-label">Total Records</div>
    <div class="stat-value">{total_rows:,}</div>
  </div>
  <div class="stat-card b2">
    <div class="stat-label">Columns</div>
    <div class="stat-value">{total_cols}</div>
  </div>
  <div class="stat-card b3">
    <div class="stat-label">{sum_label}</div>
    <div class="stat-value">{total_sum}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Filters ────────────────────────────────────────────────────────────────────
if not df.empty:
    st.markdown('<div class="filter-heading">Filter Records</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        search = st.text_input("Search", placeholder="Type to search all columns…")

    cat_cols = [c for c in df.select_dtypes("object").columns if df[c].nunique() <= 50]
    with col2:
        filter_col = st.selectbox("Filter by column", ["— none —"] + cat_cols) if cat_cols else "— none —"

    with col3:
        if filter_col != "— none —":
            options  = sorted(df[filter_col].dropna().unique().tolist())
            selected = st.selectbox("Value", ["All"] + options)
        else:
            selected = "All"

    # Apply filters
    filtered = df.copy()
    if search:
        mask = filtered.apply(
            lambda col: col.astype(str).str.contains(search, case=False, na=False)
        ).any(axis=1)
        filtered = filtered[mask]
    if filter_col != "— none —" and selected != "All":
        filtered = filtered[filtered[filter_col] == selected]

    # ── Table ──────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="table-shell">
      <div class="table-topbar">
        <span class="table-name">Records</span>
        <span class="row-pill">{len(filtered):,} rows</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


    # st.dataframe(filtered, use_container_width=True, height=480)

    event = st.dataframe(
        df,
        on_select='rerun',
        selection_mode='single-row'
    )

    if len(event.selection['rows']):
        selected_row = event.selection['rows'][0]
        record_id = df.iloc[selected_row]['id']

        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("Delete", type="primary"):
                conn = get_db()
                conn.execute("DELETE FROM record WHERE id = ?", (int(record_id),))
                conn.commit()
                conn.close()
                st.cache_data.clear()
                st.rerun()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <span>Yuki Transfer · Records Dashboard</span>
  <span>db: <span>{DB_PATH}</span></span>
</div>
""", unsafe_allow_html=True)