import streamlit as st
import pandas as pd
import sqlite3
from os import getenv

# ── Page config ────────────────────────────────────────────────────────────────
DB_NAME = getenv("RECORD_PATH")
DB_PATH = "../" + DB_NAME


st.set_page_config(
    page_title="Yuki Transfer",
    page_icon="✦",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600&family=Epilogue:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --cream:   #f2eff7;
    --warm:    #e8e2f2;
    --border:  #cfc6e4;
    --ink:     #1a1520;
    --muted:   #9088a0;
    --accent:  #6b5b95;
    --accent2: #4a7a8a;
    --success: #7a4a6a;
    --display: 'Cormorant Garamond', serif;
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

.page-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 0.3rem;
}
.page-title {
    font-family: var(--display);
    font-size: 3.2rem;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: -0.02em;
    line-height: 1;
    margin: 0;
}
.page-title em { color: var(--accent2); font-style: italic; }
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
    background: linear-gradient(90deg, var(--accent2) 0%, var(--accent) 40%, var(--border) 70%, transparent 100%);
    margin: 1rem 0 2.5rem;
}

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
    font-size: 2.2rem;
    font-weight: 600;
    color: var(--ink);
    line-height: 1;
}

.filter-heading {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.75rem;
}

.table-shell {
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    background: #f7f4f0;
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
    color: var(--accent2);
    border: 1px solid var(--accent2);
    padding: 0.18rem 0.65rem;
    border-radius: 20px;
    letter-spacing: 0.08em;
}

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

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent2) !important;
    border-bottom-color: var(--accent2) !important;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--warm); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 99px; }

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
.footer span { color: var(--accent2); }

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
    tab1, tab2 = st.tabs(["Records", "Logs"])

    with tab1:
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
            selection_mode='multi-row'
        )

        if len(event.selection['rows']):
            selected_rows = event.selection['rows']
            record_ids = df.iloc[selected_rows]['id'].tolist()

            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button(f"Delete ({len(record_ids)})", type="primary"):
                    conn = get_db()
                    conn.execute(f"DELETE FROM record WHERE id IN ({','.join('?' * len(record_ids))})", record_ids)
                    conn.commit()
                    conn.close()
                    st.cache_data.clear()
                    st.rerun()
    with tab2:
        if st.button("Refresh"):
            st.cache_data.clear()
        log_path = "../yuki.log"  # change this
        try:
            with open(log_path, "r") as f:
                logs = f.readlines()

            last_100 = "".join(logs[-100:][::-1])
            st.code(last_100, language="log")
        except FileNotFoundError:
            st.warning(f"Log file not found: {log_path}")


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <span>Yuki Transfer · Records Dashboard</span>
  <span>db: <span>{DB_PATH}</span></span>
</div>
""", unsafe_allow_html=True)