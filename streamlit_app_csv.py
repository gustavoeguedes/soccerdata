"""
Dashboard Interativo - FBref Assists Analysis
Versão com dados pré-carregados (CSV)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="FBref Assists Analysis",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    [data-testid="stMetricValue"] {
        color: #1f77b4 !important;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        color: #262730 !important;
        font-weight: 500;
    }
    
    [data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carregar dados do CSV pré-processado"""
    try:
        csv_file = Path('fbref_data.csv')
        if not csv_file.exists():
            st.error("❌ Arquivo fbref_data.csv não encontrado!")
            st.info("💡 Execute: `python generate_data.py` localmente e faça upload do CSV gerado")
            return None
        
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return None

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Interface
st.title("⚽ FBref Assists Analysis Dashboard")
st.markdown("**Análise de Assists vs Expected Assists (xAG) - Big 5 Leagues 2017-2025**")
st.markdown("---")

# Carregar dados
with st.spinner("🔄 Carregando dados..."):
    stats_pd = load_data()

if stats_pd is None or len(stats_pd) == 0:
    st.stop()

# Filtros
st.sidebar.header("🔍 Filtros")

all_leagues = sorted(stats_pd['league'].unique().tolist())
selected_leagues = st.sidebar.multiselect(
    "Liga:",
    options=all_leagues,
    default=all_leagues
)

stats_filtered = stats_pd[stats_pd['league'].isin(selected_leagues)].copy() if selected_leagues else stats_pd.copy()

if len(stats_filtered) == 0:
    st.warning("⚠️ Nenhum dado com os filtros selecionados.")
    st.stop()

all_teams = sorted(stats_filtered['team'].unique().tolist())
selected_teams = st.sidebar.multiselect("Equipa:", options=all_teams, default=[])
if selected_teams:
    stats_filtered = stats_filtered[stats_filtered['team'].isin(selected_teams)]

player_search = st.sidebar.text_input("🔎 Procurar Jogador:", "")
if player_search:
    stats_filtered = stats_filtered[stats_filtered['player'].str.contains(player_search, case=False, na=False)]

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Filtros Avançados")

max_matches = int(stats_pd['matches'].max())
min_matches = st.sidebar.slider("Mínimo de Jogos:", 0, max_matches, 5)

max_xag = float(stats_pd['xAG'].max())
min_xag = st.sidebar.slider("Mínimo xAG:", 0.0, max_xag, 0.0, 0.5)

stats_filtered = stats_filtered[
    (stats_filtered['matches'] >= min_matches) &
    (stats_filtered['xAG'] >= min_xag)
]

st.sidebar.markdown("---")
st.sidebar.info(f"📊 **{len(stats_filtered):,}** jogadores")

if len(stats_filtered) == 0:
    st.warning("⚠️ Nenhum jogador encontrado.")
    st.stop()

# Métricas
st.header("📊 Métricas Gerais")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Jogadores", f"{len(stats_filtered):,}")
with col2:
    st.metric("Total Assists", f"{stats_filtered['assists'].sum():,.0f}")
with col3:
    st.metric("Total xAG", f"{stats_filtered['xAG'].sum():,.2f}")
with col4:
    avg_diff = stats_filtered['assists_minus_xag'].mean()
    st.metric("Média Assists - xAG", f"{avg_diff:.2f}")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔺 Overperformers", "🔻 Subperformers", "⚡ Per 90", "📈 Gráficos"])

with tab1:
    st.subheader("🔺 TOP 100 Overperformers")
    top100 = stats_filtered.sort_values('assists_minus_xag', ascending=False).head(100)
    
    if len(top100) > 0:
        display_cols = ['player', 'team', 'league', 'position', 'matches', 'assists', 'xAG', 'assists_minus_xag', 'assists_minus_xag_90']
        df_display = top100[display_cols].copy()
        df_display.columns = ['Jogador', 'Equipa', 'Liga', 'Posição', 'Jogos', 'Assists', 'xAG', 'Diff', 'Diff/90']
        
        numeric_cols = df_display.select_dtypes(include=['float64', 'float32']).columns
        df_display[numeric_cols] = df_display[numeric_cols].round(2)
        
        st.dataframe(df_display, use_container_width=True, height=600)
        
        csv = convert_df_to_csv(df_display)
        st.download_button("📥 Download CSV", csv, "top100_overperformers.csv", "text/csv")

with tab2:
    st.subheader("🔻 TOP 100 Subperformers")
    top100 = stats_filtered.sort_values('assists_minus_xag', ascending=True).head(100)
    
    if len(top100) > 0:
        display_cols = ['player', 'team', 'league', 'position', 'matches', 'assists', 'xAG', 'assists_minus_xag', 'assists_minus_xag_90']
        df_display = top100[display_cols].copy()
        df_display.columns = ['Jogador', 'Equipa', 'Liga', 'Posição', 'Jogos', 'Assists', 'xAG', 'Diff', 'Diff/90']
        
        numeric_cols = df_display.select_dtypes(include=['float64', 'float32']).columns
        df_display[numeric_cols] = df_display[numeric_cols].round(2)
        
        st.dataframe(df_display, use_container_width=True, height=600)
        
        csv = convert_df_to_csv(df_display)
        st.download_button("📥 Download CSV", csv, "top100_subperformers.csv", "text/csv")

with tab3:
    st.subheader("⚡ TOP 100 Por 90 Minutos")
    top100 = stats_filtered[stats_filtered['xAG'] >= 5].sort_values('assists_minus_xag_90', ascending=False).head(100)
    
    if len(top100) > 0:
        display_cols = ['player', 'team', 'league', 'position', 'matches', 'assists', 'xAG', 'assists_minus_xag', 'assists_minus_xag_90']
        df_display = top100[display_cols].copy()
        df_display.columns = ['Jogador', 'Equipa', 'Liga', 'Posição', 'Jogos', 'Assists', 'xAG', 'Diff', 'Diff/90']
        
        numeric_cols = df_display.select_dtypes(include=['float64', 'float32']).columns
        df_display[numeric_cols] = df_display[numeric_cols].round(2)
        
        st.dataframe(df_display, use_container_width=True, height=600)
        
        csv = convert_df_to_csv(df_display)
        st.download_button("📥 Download CSV", csv, "top100_per90.csv", "text/csv")

with tab4:
    st.subheader("📈 Visualizações")
    
    if len(stats_filtered) > 0:
        # Scatter
        st.markdown("### 🎯 Scatter: xAG vs Assists")
        scatter_df = stats_filtered[['player', 'team', 'league', 'xAG', 'assists', 'assists_minus_xag']].copy()
        
        fig1 = px.scatter(
            scatter_df, x='xAG', y='assists', color='assists_minus_xag',
            hover_data=['player', 'team', 'league'],
            color_continuous_scale='RdYlGn', color_continuous_midpoint=0,
            title='Assists vs xAG', height=600
        )
        
        max_val = max(scatter_df['xAG'].max(), scatter_df['assists'].max())
        fig1.add_trace(go.Scatter(x=[0, max_val], y=[0, max_val], mode='lines', 
                                  line=dict(color='red', dash='dash'), name='y=x'))
        
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown("---")
        
        # Top 30 Overperformers
        st.markdown("### 🔺 Top 30 Overperformers")
        top30 = stats_filtered.sort_values('assists_minus_xag', ascending=False).head(30)
        
        fig2 = go.Figure(go.Bar(
            y=top30['player'], x=top30['assists_minus_xag'], orientation='h',
            marker=dict(color=top30['assists_minus_xag'], colorscale='Greens'),
            text=top30['assists_minus_xag'].round(2), textposition='outside'
        ))
        fig2.update_layout(title='TOP 30 Overperformers', height=900, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        
        # Boxplot por Liga
        st.markdown("### 📊 Distribuição por Liga")
        fig3 = px.box(stats_filtered, x='league', y='assists_minus_xag', color='league',
                      title='Distribuição por Liga', height=600)
        st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>📊 Dados: FBref via soccerdata | ⚽ Big 5 Leagues 2017-2025</p>
</div>
""", unsafe_allow_html=True)
