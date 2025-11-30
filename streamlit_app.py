"""
Dashboard Interativo - FBref Assists Analysis
Análise de Assists vs Expected Assists (xAG)
"""

import streamlit as st
import soccerdata as sd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
from pathlib import Path

# Suprimir warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

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
    
    /* Métricas com fundo escuro e texto visível */
    [data-testid="stMetricValue"] {
        color: #1f77b4 !important;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        color: #262730 !important;
        font-weight: 500;
    }
    
    [data-testid="stMetricDelta"] {
        color: #262730 !important;
    }
    
    /* Container das métricas */
    [data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        [data-testid="metric-container"] {
            background-color: #262730;
            border-color: #464646;
        }
        
        [data-testid="stMetricLabel"] {
            color: #fafafa !important;
        }
        
        [data-testid="stMetricDelta"] {
            color: #fafafa !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

@st.cache_data(show_spinner=False, ttl=3600)  # Cache por 1 hora
def load_data():
    """Carregar e processar dados do FBref"""
    
    # Configuração completa - Big 5 Leagues
    LEAGUES = [
        'ENG-Premier League',
        'ESP-La Liga',
        'FRA-Ligue 1',
        'GER-Bundesliga',
        'ITA-Serie A'
    ]
    SEASONS = ['1718', '1819', '1920', '2021', '2122', '2223', '2324', '2425']
    
    try:
        # Configurar com no_cache=False para usar cache local
        fbref = sd.FBref(
            leagues=LEAGUES,
            seasons=SEASONS,
            no_cache=False
        )
        
        player_season_stats = fbref.read_player_season_stats(stat_type="standard")
        
        # Validar se não está vazio
        if len(player_season_stats) == 0:
            st.error("❌ Nenhum dado foi carregado do FBref. Verifique a conexão.")
            return None
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        st.info("💡 Tente recarregar a página (F5) ou aguarde alguns minutos.")
        return None
    
    # Processar colunas (com fallback robusto)
    try:
        all_columns = player_season_stats.columns.tolist()
        column_mapping = {}
        
        for idx, col in enumerate(all_columns):
            col_str = str(col)
            col_lower = col_str.lower()
            
            # Posição
            if ('pos' in col_lower and 'position' not in column_mapping and 
                'composed' not in col_lower and 'deposit' not in col_lower):
                column_mapping['position'] = idx
            
            # Matches/Jogos (MP = Matches Played)
            elif (('mp' == col_lower or 'matches' in col_lower) and 'matches' not in column_mapping):
                column_mapping['matches'] = idx
            
            # Minutos (Min)
            elif ('min' in col_lower and 'minute' not in column_mapping and 
                  'per' not in col_lower and '90' not in col_lower):
                column_mapping['minutes'] = idx
            
            # Assists (Ast)
            elif ((col_lower == 'ast' or 'assist' in col_lower) and 
                  'assists' not in column_mapping and 'xag' not in col_lower):
                column_mapping['assists'] = idx
            
            # xAG (Expected Assisted Goals)
            elif ('xag' in col_lower and 'xAG' not in column_mapping):
                column_mapping['xAG'] = idx
        
        if len(column_mapping) < 5:
            # Fallback: usar índices conhecidos
            selected_indices = [1, 4, 6, 9, 18]
            df = player_season_stats.iloc[:, selected_indices].copy()
            df.columns = ['position', 'matches', 'minutes', 'assists', 'xAG']
        else:
            selected_indices = [
                column_mapping['position'],
                column_mapping['matches'],
                column_mapping['minutes'],
                column_mapping['assists'],
                column_mapping['xAG']
            ]
            df = player_season_stats.iloc[:, selected_indices].copy()
            df.columns = ['position', 'matches', 'minutes', 'assists', 'xAG']
        
        # Resetar index para ter acesso a league, team, player
        df = df.reset_index()
        
        # Agregar dados usando pandas
        stats = df.groupby(['league', 'team', 'player']).agg({
            'matches': 'sum',
            'assists': 'sum',
            'xAG': 'sum',
            'minutes': 'sum',
            'position': 'first'
        }).reset_index()
        
        # Calcular métricas derivadas
        stats['assists_minus_xag'] = stats['assists'] - stats['xAG']
        stats['assists_minus_xag_90'] = (stats['assists'] - stats['xAG']) / stats['minutes'] * 90
        
        # Filtrar
        stats = stats[
            (stats['minutes'] > 450) &
            (stats['xAG'] > 0)
        ]
        
        return stats
        
    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")
        return None

def format_dataframe(df_pd, columns_to_show):
    """Formatar DataFrame para exibição"""
    df_display = df_pd[columns_to_show].copy()
    
    # Arredondar valores numéricos
    numeric_cols = df_display.select_dtypes(include=['float64', 'float32']).columns
    df_display[numeric_cols] = df_display[numeric_cols].round(2)
    
    return df_display

@st.cache_data
def convert_df_to_csv(df):
    """Converter DataFrame para CSV para download"""
    return df.to_csv(index=False).encode('utf-8')

# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

# Cabeçalho
st.title("⚽ FBref Assists Analysis Dashboard")
st.markdown("**Análise de Assists vs Expected Assists (xAG) - Big 5 Leagues 2017-2025**")
st.markdown("---")

# Carregar dados
with st.spinner("🔄 A carregar dados do FBref... (pode demorar alguns minutos)"):
    stats = load_data()

if stats is None or len(stats) == 0:
    st.error("❌ Não foi possível carregar os dados. Verifique a conexão e tente novamente.")
    st.info("💡 Tente recarregar a página (F5) ou limpar o cache.")
    st.stop()

# Usar dados diretamente (já é pandas)
try:
    stats_pd = stats.copy()
    
    # Validar se tem dados
    if len(stats_pd) == 0:
        st.error("❌ DataFrame vazio após conversão.")
        st.stop()
        
except Exception as e:
    st.error(f"❌ Erro ao converter dados: {e}")
    st.stop()

# ============================================================================
# SIDEBAR - FILTROS
# ============================================================================

st.sidebar.header("🔍 Filtros")

# Filtro de Liga
all_leagues = sorted(stats_pd['league'].unique().tolist()) if 'league' in stats_pd.columns else []

if len(all_leagues) == 0:
    st.error("❌ Nenhuma liga encontrada nos dados.")
    st.stop()

selected_leagues = st.sidebar.multiselect(
    "Liga:",
    options=all_leagues,
    default=all_leagues
)

# Filtrar dados por liga
if selected_leagues:
    stats_filtered = stats_pd[stats_pd['league'].isin(selected_leagues)].copy()
else:
    stats_filtered = stats_pd.copy()

# Validar se tem dados após filtro
if len(stats_filtered) == 0:
    st.warning("⚠️ Nenhum dado disponível com os filtros selecionados.")
    st.stop()

# Filtro de Equipa
all_teams = sorted(stats_filtered['team'].unique().tolist()) if 'team' in stats_filtered.columns else []
selected_teams = st.sidebar.multiselect(
    "Equipa:",
    options=all_teams,
    default=[]
)

if selected_teams:
    stats_filtered = stats_filtered[stats_filtered['team'].isin(selected_teams)].copy()

# Filtro de Jogador (search box)
player_search = st.sidebar.text_input("🔎 Procurar Jogador:", "")

if player_search and 'player' in stats_filtered.columns:
    stats_filtered = stats_filtered[
        stats_filtered['player'].str.contains(player_search, case=False, na=False)
    ].copy()

# Filtros numéricos
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Filtros Avançados")

# Calcular max values com fallback para evitar NaN
max_matches = stats_pd['matches'].max() if 'matches' in stats_pd.columns else 100
max_matches = int(max_matches) if pd.notna(max_matches) and max_matches > 0 else 100

max_xag_val = stats_pd['xAG'].max() if 'xAG' in stats_pd.columns else 50.0
max_xag_val = float(max_xag_val) if pd.notna(max_xag_val) and max_xag_val > 0 else 50.0

min_matches = st.sidebar.slider(
    "Mínimo de Jogos:",
    min_value=0,
    max_value=max_matches,
    value=min(5, max_matches)
)

min_xag = st.sidebar.slider(
    "Mínimo xAG:",
    min_value=0.0,
    max_value=max_xag_val,
    value=0.0,
    step=0.5
)

# Aplicar filtros numéricos com validação
if 'matches' in stats_filtered.columns and 'xAG' in stats_filtered.columns:
    stats_filtered = stats_filtered[
        (stats_filtered['matches'] >= min_matches) &
        (stats_filtered['xAG'] >= min_xag)
    ].copy()

st.sidebar.markdown("---")
st.sidebar.info(f"📊 **{len(stats_filtered):,}** jogadores no filtro atual")

# Validar se ainda tem dados
if len(stats_filtered) == 0:
    st.warning("⚠️ Nenhum jogador encontrado com os filtros aplicados. Tente ajustar os filtros.")
    st.stop()

# ============================================================================
# MÉTRICAS PRINCIPAIS
# ============================================================================

st.header("📊 Métricas Gerais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Jogadores",
        value=f"{len(stats_filtered):,}"
    )

with col2:
    st.metric(
        label="Total Assists",
        value=f"{stats_filtered['assists'].sum():,.0f}"
    )

with col3:
    st.metric(
        label="Total xAG",
        value=f"{stats_filtered['xAG'].sum():,.2f}"
    )

with col4:
    avg_diff = stats_filtered['assists_minus_xag'].mean()
    st.metric(
        label="Média Assists - xAG",
        value=f"{avg_diff:.2f}",
        delta=f"{'Overperformance' if avg_diff > 0 else 'Underperformance'}"
    )

st.markdown("---")

# ============================================================================
# TABS PRINCIPAIS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🔺 Overperformers",
    "🔻 Subperformers",
    "⚡ Per 90 Minutes",
    "📈 Gráficos"
])

# ============================================================================
# TAB 1: OVERPERFORMERS
# ============================================================================

with tab1:
    st.subheader("🔺 TOP 100 Overperformers (Assists acima do esperado)")
    
    top100_over = (
        stats_filtered
        .sort_values('assists_minus_xag', ascending=False)
        .head(100)
    )
    
    if len(top100_over) > 0:
        # Selecionar colunas para exibição
        display_cols = [
            'player', 'team', 'league', 'position',
            'matches', 'assists', 'xAG', 'assists_minus_xag', 'assists_minus_xag_90'
        ]
        
        df_display = top100_over[display_cols].copy()
        
        # Arredondar
        numeric_cols = df_display.select_dtypes(include=['float64', 'float32']).columns
        df_display[numeric_cols] = df_display[numeric_cols].round(2)
        
        # Renomear colunas para português
        df_display.columns = [
            'Jogador', 'Equipa', 'Liga', 'Posição',
            'Jogos', 'Assists', 'xAG', 'Diff', 'Diff/90'
        ]
        
        st.dataframe(
            df_display,
            use_container_width=True,
            height=600
        )
        
        # Botão de download
        csv = convert_df_to_csv(df_display)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="top100_overperformers.csv",
            mime="text/csv"
        )
    else:
        st.warning("Nenhum jogador encontrado com os filtros atuais.")

# ============================================================================
# TAB 2: SUBPERFORMERS
# ============================================================================

with tab2:
    st.subheader("🔻 TOP 100 Subperformers (Assists abaixo do esperado)")
    
    top100_sub = (
        stats_filtered
        .sort_values('assists_minus_xag', ascending=True)
        .head(100)
    )
    
    if len(top100_sub) > 0:
        display_cols = [
            'player', 'team', 'league', 'position',
            'matches', 'assists', 'xAG', 'assists_minus_xag', 'assists_minus_xag_90'
        ]
        
        df_display = top100_sub[display_cols].copy()
        numeric_cols = df_display.select_dtypes(include=['float64', 'float32']).columns
        df_display[numeric_cols] = df_display[numeric_cols].round(2)
        
        df_display.columns = [
            'Jogador', 'Equipa', 'Liga', 'Posição',
            'Jogos', 'Assists', 'xAG', 'Diff', 'Diff/90'
        ]
        
        st.dataframe(
            df_display,
            use_container_width=True,
            height=600
        )
        
        csv = convert_df_to_csv(df_display)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="top100_subperformers.csv",
            mime="text/csv"
        )
    else:
        st.warning("Nenhum jogador encontrado com os filtros atuais.")

# ============================================================================
# TAB 3: PER 90 MINUTES
# ============================================================================

with tab3:
    st.subheader("⚡ TOP 100 Por 90 Minutos (mínimo 5 xAG)")
    
    top100_p90 = (
        stats_filtered[stats_filtered['xAG'] >= 5]
        .sort_values('assists_minus_xag_90', ascending=False)
        .head(100)
    )
    
    if len(top100_p90) > 0:
        display_cols = [
            'player', 'team', 'league', 'position',
            'matches', 'assists', 'xAG', 'assists_minus_xag', 'assists_minus_xag_90'
        ]
        
        df_display = top100_p90[display_cols].copy()
        numeric_cols = df_display.select_dtypes(include=['float64', 'float32']).columns
        df_display[numeric_cols] = df_display[numeric_cols].round(2)
        
        df_display.columns = [
            'Jogador', 'Equipa', 'Liga', 'Posição',
            'Jogos', 'Assists', 'xAG', 'Diff', 'Diff/90'
        ]
        
        st.dataframe(
            df_display,
            use_container_width=True,
            height=600
        )
        
        csv = convert_df_to_csv(df_display)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="top100_per90.csv",
            mime="text/csv"
        )
    else:
        st.warning("Nenhum jogador encontrado com os filtros atuais (mínimo 5 xAG).")

# ============================================================================
# TAB 4: GRÁFICOS
# ============================================================================

with tab4:
    st.subheader("📈 Visualizações Interativas")
    
    if len(stats_filtered) > 0:
        
        # ---- GRÁFICO 1: Scatter xAG vs Assists (Plotly) ----
        st.markdown("### 🎯 Scatter: xAG vs Assists")
        st.markdown("*Passe o rato sobre os pontos para ver detalhes*")
        
        # Criar DataFrame com informações completas para hover
        scatter_df = stats_filtered[['player', 'team', 'league', 'xAG', 'assists', 'assists_minus_xag']].copy()
        
        fig1 = px.scatter(
            scatter_df,
            x='xAG',
            y='assists',
            hover_data={
                'player': True,
                'team': True,
                'league': True,
                'xAG': ':.2f',
                'assists': ':.0f',
                'assists_minus_xag': ':.2f'
            },
            labels={
                'xAG': 'Expected Assisted Goals (xAG)',
                'assists': 'Assists',
                'assists_minus_xag': 'Diferença'
            },
            title='Assists vs Expected Assists (xAG)',
            color='assists_minus_xag',
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=0
        )
        
        # Adicionar linha de referência (assists = xAG)
        max_val = max(scatter_df['xAG'].max(), scatter_df['assists'].max())
        fig1.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            name='Assists = xAG',
            line=dict(color='red', width=2, dash='dash'),
            showlegend=True
        ))
        
        fig1.update_layout(
            height=600,
            hovermode='closest',
            template='plotly_white'
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown("---")
        
        # ---- GRÁFICO 2: Bar Chart Top 30 Overperformers (Plotly) ----
        st.markdown("### 🔺 Top 30 Overperformers")
        st.markdown("*Clique nas barras para interagir*")
        
        top30_over = stats_filtered.sort_values('assists_minus_xag', ascending=False).head(30)
        
        fig2 = go.Figure()
        
        fig2.add_trace(go.Bar(
            y=top30_over['player'],
            x=top30_over['assists_minus_xag'],
            orientation='h',
            marker=dict(
                color=top30_over['assists_minus_xag'],
                colorscale='Greens',
                showscale=True,
                colorbar=dict(title="Diff")
            ),
            text=top30_over['assists_minus_xag'].round(2),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>' +
                         'Assists - xAG: %{x:.2f}<br>' +
                         'Team: %{customdata[0]}<br>' +
                         'League: %{customdata[1]}<br>' +
                         '<extra></extra>',
            customdata=top30_over[['team', 'league']].values
        ))
        
        fig2.update_layout(
            title='TOP 30 Overperformers: Assists acima do Esperado',
            xaxis_title='Assists - xAG',
            yaxis_title='',
            height=900,
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        
        # ---- GRÁFICO 3: Bar Chart Top 30 Subperformers (Plotly) ----
        st.markdown("### 🔻 Top 30 Subperformers")
        st.markdown("*Clique nas barras para interagir*")
        
        top30_sub = stats_filtered.sort_values('assists_minus_xag', ascending=True).head(30)
        
        fig3 = go.Figure()
        
        fig3.add_trace(go.Bar(
            y=top30_sub['player'],
            x=top30_sub['assists_minus_xag'],
            orientation='h',
            marker=dict(
                color=top30_sub['assists_minus_xag'],
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Diff"),
                reversescale=True
            ),
            text=top30_sub['assists_minus_xag'].round(2),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>' +
                         'Assists - xAG: %{x:.2f}<br>' +
                         'Team: %{customdata[0]}<br>' +
                         'League: %{customdata[1]}<br>' +
                         '<extra></extra>',
            customdata=top30_sub[['team', 'league']].values
        ))
        
        fig3.update_layout(
            title='TOP 30 Subperformers: Assists abaixo do Esperado',
            xaxis_title='Assists - xAG',
            yaxis_title='',
            height=900,
            template='plotly_white',
            yaxis={'categoryorder': 'total descending'}
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("---")
        
        # ---- GRÁFICO 4: Distribuição por Liga (Boxplot) ----
        st.markdown("### 📊 Distribuição por Liga")
        st.markdown("*Compare a performance entre diferentes ligas*")
        
        fig4 = px.box(
            stats_filtered,
            x='league',
            y='assists_minus_xag',
            color='league',
            title='Distribuição de Assists - xAG por Liga',
            labels={
                'league': 'Liga',
                'assists_minus_xag': 'Assists - xAG'
            },
            hover_data=['player', 'team']
        )
        
        fig4.update_layout(
            height=600,
            template='plotly_white',
            showlegend=False
        )
        
        st.plotly_chart(fig4, use_container_width=True)
        
        st.markdown("---")
        
        # ---- GRÁFICO 5: Top 20 por 90 minutos ----
        st.markdown("### ⚡ Top 20 por 90 Minutos")
        st.markdown("*Performance normalizada (mínimo 5 xAG)*")
        
        top20_p90 = (
            stats_filtered[stats_filtered['xAG'] >= 5]
            .sort_values('assists_minus_xag_90', ascending=False)
            .head(20)
        )
        
        if len(top20_p90) > 0:
            fig5 = go.Figure()
            
            fig5.add_trace(go.Bar(
                y=top20_p90['player'],
                x=top20_p90['assists_minus_xag_90'],
                orientation='h',
                marker=dict(
                    color=top20_p90['assists_minus_xag_90'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Diff/90")
                ),
                text=top20_p90['assists_minus_xag_90'].round(3),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>' +
                             'Diff per 90: %{x:.3f}<br>' +
                             'Team: %{customdata[0]}<br>' +
                             'Minutes: %{customdata[1]:.0f}<br>' +
                             '<extra></extra>',
                customdata=top20_p90[['team', 'minutes']].values
            ))
            
            fig5.update_layout(
                title='TOP 20 Assists - xAG por 90 Minutos',
                xaxis_title='(Assists - xAG) / 90 min',
                yaxis_title='',
                height=600,
                template='plotly_white',
                yaxis={'categoryorder': 'total ascending'}
            )
            
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.info("Nenhum jogador com mínimo 5 xAG nos dados filtrados.")
        
    else:
        st.warning("Nenhum dado disponível para gerar gráficos.")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>📊 Dados: FBref via soccerdata | ⚽ Big 5 Leagues 2017-2025</p>
    <p>Desenvolvido com Streamlit + Plotly 🚀</p>
</div>
""", unsafe_allow_html=True)
