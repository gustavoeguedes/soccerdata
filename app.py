"""
FBref Data Analysis - Assists vs Expected Assists (xAG)
Análise completa de jogadores das Big 5 Leagues (2017-2025)
"""

import soccerdata as sd
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import warnings
from pathlib import Path

# Suprimir warnings do pandas e soccerdata
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# Configurar matplotlib para não precisar de display
matplotlib.use('Agg')

# Criar diretório de outputs
OUTPUT_DIR = Path("out")
OUTPUT_DIR.mkdir(exist_ok=True)

print("🔄 Iniciando análise de dados FBref...")
print("=" * 60)

# ============================================================================
# 1. CARREGAR DADOS DO FBREF
# ============================================================================

# Verificar ligas disponíveis
print("\n🔍 Verificando ligas disponíveis no FBref...")
try:
    available_leagues = sd.FBref.available_leagues()
    print(f"✅ Ligas disponíveis: {available_leagues}")
except Exception as e:
    print(f"⚠️  Não foi possível listar ligas: {e}")
    available_leagues = []

# Configuração de ligas e temporadas
# Formato de temporadas aceite: '1718', '2017-18', '2017-2018', 2017, etc.
LEAGUES_PRIMARY = ['Big 5 European Leagues Combined']
LEAGUES_FALLBACK = [
    'ENG-Premier League',
    'ESP-La Liga',
    'FRA-Ligue 1',
    'GER-Bundesliga',
    'ITA-Serie A'
]
SEASONS = ['1718', '1819', '1920', '2021', '2122', '2223', '2324', '2425']

print(f"\n⚙️  Configuração:")
print(f"   Liga principal: {LEAGUES_PRIMARY}")
print(f"   Liga fallback: {LEAGUES_FALLBACK}")
print(f"   Temporadas: {SEASONS}")

# Tentativa 1: Big 5 Combined
player_season_stats = None
leagues_used = None

try:
    print("\n📡 Tentativa 1: Carregar 'Big 5 European Leagues Combined'...")
    fbref = sd.FBref(
        leagues=LEAGUES_PRIMARY,
        seasons=SEASONS
    )
    
    print("✅ Objeto FBref criado")
    
    # Tentar ler ligas e temporadas (pode falhar)
    try:
        leagues_df = fbref.read_leagues()
        print(f"   Ligas: {leagues_df['league'].unique().tolist() if 'league' in leagues_df.columns else 'N/A'}")
    except Exception as e:
        print(f"   ⚠️  Não foi possível ler ligas: {e}")
    
    try:
        seasons_df = fbref.read_seasons()
        print(f"   Temporadas: {seasons_df['season'].unique().tolist() if 'season' in seasons_df.columns else 'N/A'}")
    except Exception as e:
        print(f"   ⚠️  Não foi possível ler temporadas: {e}")
    
    print("📥 A ler dados de jogadores...")
    player_season_stats = fbref.read_player_season_stats(stat_type="standard")
    
    print(f"✅ Dados carregados: {len(player_season_stats)} registos")
    
    # Validar se não está vazio
    if len(player_season_stats) == 0:
        print("⚠️  DataFrame vazio! Tentando fallback...")
        player_season_stats = None
    else:
        leagues_used = LEAGUES_PRIMARY
        print(f"✅ Sucesso com {LEAGUES_PRIMARY[0]}")
        
except Exception as e:
    print(f"❌ Erro na tentativa 1: {e}")
    print(f"   Tipo: {type(e).__name__}")
    import traceback
    print("   Stack trace:")
    traceback.print_exc()
    player_season_stats = None

# Tentativa 2: Ligas individuais (fallback)
if player_season_stats is None or len(player_season_stats) == 0:
    try:
        print("\n📡 Tentativa 2: Carregar ligas individualmente (fallback)...")
        fbref = sd.FBref(
            leagues=LEAGUES_FALLBACK,
            seasons=SEASONS
        )
        
        print("✅ Objeto FBref criado com ligas individuais")
        
        # Tentar ler ligas e temporadas (pode falhar)
        try:
            leagues_df = fbref.read_leagues()
            print(f"   Ligas: {leagues_df['league'].unique().tolist() if 'league' in leagues_df.columns else leagues_df.columns.tolist()}")
        except Exception as e:
            print(f"   ⚠️  Não foi possível ler ligas: {e}")
        
        try:
            seasons_df = fbref.read_seasons()
            print(f"   Temporadas: {seasons_df['season'].unique().tolist() if 'season' in seasons_df.columns else seasons_df.columns.tolist()}")
        except Exception as e:
            print(f"   ⚠️  Não foi possível ler temporadas: {e}")
        
        print("📥 A ler dados de jogadores...")
        player_season_stats = fbref.read_player_season_stats(stat_type="standard")
        
        print(f"✅ Dados carregados: {len(player_season_stats)} registos")
        
        if len(player_season_stats) == 0:
            print("❌ DataFrame ainda está vazio!")
            raise ValueError("Nenhum jogador foi carregado mesmo após fallback")
        else:
            leagues_used = LEAGUES_FALLBACK
            print(f"✅ Sucesso com ligas individuais")
            
    except Exception as e:
        print(f"❌ Erro na tentativa 2 (fallback): {e}")
        print(f"   Tipo: {type(e).__name__}")
        import traceback
        print("   Stack trace completo:")
        traceback.print_exc()
        print("\n❌ ERRO CRÍTICO: Não foi possível carregar dados do FBref")
        print("   Possíveis causas:")
        print("   • Mudança na estrutura do FBref")
        print("   • Problema de conexão")
        print("   • Ligas ou temporadas não disponíveis")
        print(f"   • Versão do soccerdata: {sd.__version__ if hasattr(sd, '__version__') else 'desconhecida'}")
        exit(1)

# Diagnóstico final
print("\n" + "=" * 60)
print("📊 DIAGNÓSTICO DOS DADOS CARREGADOS")
print("=" * 60)

if player_season_stats is not None and len(player_season_stats) > 0:
    print(f"\n✅ DataFrame válido!")
    print(f"   • Total de registos: {len(player_season_stats)}")
    print(f"   • Ligas usadas: {leagues_used}")
    print(f"   • Colunas disponíveis ({len(player_season_stats.columns)}): {player_season_stats.columns.tolist()[:10]}...")
    print(f"   • Index levels: {player_season_stats.index.names}")
    print(f"\n📋 Primeiras 5 linhas:")
    print(player_season_stats.head())
    print(f"\n📊 Info do DataFrame:")
    print(player_season_stats.info())
else:
    print("❌ Nenhum jogador carregado. Verifique liga, temporada ou mudança no FBref.")
    exit(1)

# ============================================================================
# 2. PROCESSAR E SELECIONAR COLUNAS
# ============================================================================

print("\n" + "=" * 60)
print("🔧 PROCESSAMENTO DE COLUNAS")
print("=" * 60)

# Tentar encontrar as colunas corretas (fallback para diferentes estruturas)
try:
    # Verificar quais colunas temos
    all_columns = player_season_stats.columns.tolist()
    print(f"\n📋 Total de colunas disponíveis: {len(all_columns)}")
    print(f"   Primeiras 30 colunas: {all_columns[:30]}")
    
    # Mapeamento robusto de colunas (aceita variações de nomes)
    column_mapping = {}
    
    # Procurar colunas por padrões
    print("\n🔍 A procurar colunas necessárias...")
    for idx, col in enumerate(all_columns):
        col_str = str(col)
        col_lower = col_str.lower() if isinstance(col, str) else str(col).lower()
        
        # Posição
        if ('pos' in col_lower and 'position' not in column_mapping and 
            'composed' not in col_lower and 'deposit' not in col_lower):
            column_mapping['position'] = idx
            print(f"   ✓ Posição encontrada: coluna {idx} = '{col_str}'")
        
        # Matches/Jogos (MP = Matches Played)
        elif (('mp' == col_lower or 'matches' in col_lower) and 'matches' not in column_mapping):
            column_mapping['matches'] = idx
            print(f"   ✓ Jogos encontrados: coluna {idx} = '{col_str}'")
        
        # Minutos (Min)
        elif ('min' in col_lower and 'minute' not in column_mapping and 
              'per' not in col_lower and '90' not in col_lower):
            column_mapping['minutes'] = idx
            print(f"   ✓ Minutos encontrados: coluna {idx} = '{col_str}'")
        
        # Assists (Ast)
        elif ((col_lower == 'ast' or 'assist' in col_lower) and 
              'assists' not in column_mapping and 'xag' not in col_lower):
            column_mapping['assists'] = idx
            print(f"   ✓ Assists encontrados: coluna {idx} = '{col_str}'")
        
        # xAG (Expected Assisted Goals)
        elif ('xag' in col_lower and 'xAG' not in column_mapping):
            column_mapping['xAG'] = idx
            print(f"   ✓ xAG encontrado: coluna {idx} = '{col_str}'")
    
    print(f"\n📊 Colunas mapeadas: {len(column_mapping)}/5")
    
    # Se não encontrou todas, usar índices fixos como fallback
    if len(column_mapping) < 5:
        print("⚠️  Mapeamento incompleto! A usar índices fixos (fallback)...")
        print(f"   Colunas encontradas: {list(column_mapping.keys())}")
        print(f"   Colunas faltando: {set(['position', 'matches', 'minutes', 'assists', 'xAG']) - set(column_mapping.keys())}")
        
        # Tentar índices conhecidos
        selected_indices = [1, 4, 6, 9, 18]  # posição, matches, minutos, assists, xAG
        print(f"   Tentando índices: {selected_indices}")
        
        df = player_season_stats.iloc[:, selected_indices].copy()
        df.columns = ['position', 'matches', 'minutes', 'assists', 'xAG']
        
        print(f"   Colunas extraídas por índice: {df.columns.tolist()}")
    else:
        print("✅ Todas as colunas identificadas automaticamente!")
        selected_indices = [
            column_mapping['position'],
            column_mapping['matches'],
            column_mapping['minutes'],
            column_mapping['assists'],
            column_mapping['xAG']
        ]
        print(f"   Índices selecionados: {selected_indices}")
        
        df = player_season_stats.iloc[:, selected_indices].copy()
        df.columns = ['position', 'matches', 'minutes', 'assists', 'xAG']
    
    # Validar dados antes de converter
    print(f"\n📊 DataFrame processado:")
    print(f"   • Linhas: {len(df)}")
    print(f"   • Colunas: {df.columns.tolist()}")
    print(f"   • Index: {df.index.names}")
    print(f"\n   Primeiras 3 linhas:")
    print(df.head(3))
    
    # Verificar valores nulos
    null_counts = df.isnull().sum()
    print(f"\n   Valores nulos por coluna:")
    for col, count in null_counts.items():
        print(f"      {col}: {count}")
    
    # Converter para Polars mantendo o index (league, season, team, player)
    print("\n🔄 Convertendo para Polars...")
    df_polars = pl.from_pandas(df, include_index=True)
    
    print(f"✅ DataFrame Polars criado com {len(df_polars)} linhas")
    print(f"   Colunas: {df_polars.columns}")
    
except Exception as e:
    print(f"\n❌ ERRO no processamento: {e}")
    print(f"   Tipo: {type(e).__name__}")
    
    # Debug detalhado
    import traceback
    print("\n🔍 Stack trace completo:")
    traceback.print_exc()
    
    print("\n📋 Informação adicional:")
    print(f"   Colunas disponíveis: {player_season_stats.columns.tolist()[:20]}")
    print(f"   Tipos das colunas: {player_season_stats.dtypes.head(20)}")
    
    exit(1)

# ============================================================================
# 3. AGREGAR DADOS POR JOGADOR
# ============================================================================

print("\n📊 A calcular estatísticas agregadas...")

try:
    stats = (
        df_polars
        .group_by("league", "team", "player")
        .agg([
            pl.col("matches").sum().alias("matches"),
            pl.col("assists").sum().alias("assists"),
            pl.col("xAG").sum().alias("xAG"),
            pl.col("minutes").sum().alias("minutes"),
            pl.col("position").first().alias("position")
        ])
        .with_columns([
            (pl.col("assists") - pl.col("xAG")).alias("assists_minus_xag"),
            ((pl.col("assists") - pl.col("xAG")) / pl.col("minutes") * 90).alias("assists_minus_xag_90")
        ])
        .filter(
            (pl.col("minutes") > 450) &  # Pelo menos 5 jogos de 90 min
            (pl.col("xAG") > 0)  # Garantir que tem dados de xAG
        )
    )
    
    print(f"✅ {len(stats)} jogadores qualificados para análise")
    
except Exception as e:
    print(f"❌ Erro na agregação: {e}")
    exit(1)

# ============================================================================
# 4. GERAR TOP 100s
# ============================================================================

print("\n🏆 A gerar rankings TOP 100...")

# TOP 100 Subperformers (assists < xAG)
top100_subperformers = (
    stats
    .sort("assists_minus_xag")
    .head(100)
)

# TOP 100 Overperformers (assists > xAG)
top100_overperformers = (
    stats
    .sort("assists_minus_xag", descending=True)
    .head(100)
)

# TOP 100 por 90 minutos (mínimo 5 xAG)
top100_per90 = (
    stats
    .filter(pl.col("xAG") >= 5)
    .sort("assists_minus_xag_90", descending=True)
    .head(100)
)

print("✅ Rankings gerados com sucesso")

# ============================================================================
# 5. EXPORTAR PARA CSV E EXCEL
# ============================================================================

print("\n💾 A exportar dados...")

# Converter para pandas para exportar
top100_sub_pd = top100_subperformers.to_pandas()
top100_over_pd = top100_overperformers.to_pandas()
top100_p90_pd = top100_per90.to_pandas()

# Arredondar valores numéricos
for df_temp in [top100_sub_pd, top100_over_pd, top100_p90_pd]:
    for col in ['assists', 'xAG', 'assists_minus_xag', 'assists_minus_xag_90']:
        if col in df_temp.columns:
            df_temp[col] = df_temp[col].round(2)

# CSV
top100_sub_pd.to_csv(OUTPUT_DIR / "top100_subperformers.csv", index=False)
top100_over_pd.to_csv(OUTPUT_DIR / "top100_overperformers.csv", index=False)
top100_p90_pd.to_csv(OUTPUT_DIR / "top100_per90.csv", index=False)

# Excel (com múltiplas sheets)
with pd.ExcelWriter(OUTPUT_DIR / "top100_assists_analysis.xlsx", engine='openpyxl') as writer:
    top100_sub_pd.to_excel(writer, sheet_name='Subperformers', index=False)
    top100_over_pd.to_excel(writer, sheet_name='Overperformers', index=False)
    top100_p90_pd.to_excel(writer, sheet_name='Per 90 Minutes', index=False)

print("✅ CSV e Excel exportados")

# ============================================================================
# 6. GERAR GRÁFICOS
# ============================================================================

print("\n📈 A gerar gráficos...")

# Configuração global
plt.style.use('default')
fig_size = (12, 8)

# ---- GRÁFICO 1: Scatter xAG vs Assists ----
fig, ax = plt.subplots(figsize=fig_size)

stats_pd = stats.to_pandas()

ax.scatter(stats_pd['xAG'], stats_pd['assists'], alpha=0.5, s=30, c='steelblue')

# Linha de referência (assists = xAG)
max_val = max(stats_pd['xAG'].max(), stats_pd['assists'].max())
ax.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='Assists = xAG', alpha=0.7)

ax.set_xlabel('Expected Assisted Goals (xAG)', fontsize=12, fontweight='bold')
ax.set_ylabel('Assists', fontsize=12, fontweight='bold')
ax.set_title('Assists vs Expected Assists (xAG)\nBig 5 Leagues 2017-2025', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "scatter_xag_vs_assists.png", dpi=300, bbox_inches='tight')
plt.close()

# ---- GRÁFICO 2: Bar Chart Top 50 Overperformers ----
fig, ax = plt.subplots(figsize=(14, 10))

top20_over = top100_overperformers.head(20).to_pandas()
players = top20_over['player'].values
values = top20_over['assists_minus_xag'].values

colors = ['green' if v > 0 else 'red' for v in values]

y_pos = range(len(players))
ax.barh(y_pos, values, color=colors, alpha=0.7)

ax.set_yticks(y_pos)
ax.set_yticklabels(players, fontsize=9)
ax.invert_yaxis()
ax.set_xlabel('Assists - xAG', fontsize=12, fontweight='bold')
ax.set_title('TOP 20 Overperformers: Assists acima do Esperado\nBig 5 Leagues 2017-2025', 
             fontsize=14, fontweight='bold', pad=20)
ax.axvline(x=0, color='black', linewidth=0.8)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "bar_top20_overperformers.png", dpi=300, bbox_inches='tight')
plt.close()

# ---- GRÁFICO 3: Bar Chart Top 50 Subperformers ----
fig, ax = plt.subplots(figsize=(14, 10))

top20_sub = top100_subperformers.head(20).to_pandas()
players_sub = top20_sub['player'].values
values_sub = top20_sub['assists_minus_xag'].values

colors_sub = ['red' if v < 0 else 'green' for v in values_sub]

y_pos_sub = range(len(players_sub))
ax.barh(y_pos_sub, values_sub, color=colors_sub, alpha=0.7)

ax.set_yticks(y_pos_sub)
ax.set_yticklabels(players_sub, fontsize=9)
ax.invert_yaxis()
ax.set_xlabel('Assists - xAG', fontsize=12, fontweight='bold')
ax.set_title('TOP 20 Subperformers: Assists abaixo do Esperado\nBig 5 Leagues 2017-2025', 
             fontsize=14, fontweight='bold', pad=20)
ax.axvline(x=0, color='black', linewidth=0.8)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "bar_top20_subperformers.png", dpi=300, bbox_inches='tight')
plt.close()

print("✅ Gráficos exportados (PNG)")

# ============================================================================
# 7. MOSTRAR PREVIEW DOS RESULTADOS
# ============================================================================

print("\n" + "=" * 60)
print("📊 RESUMO DOS RESULTADOS")
print("=" * 60)

print("\n🔻 TOP 5 SUBPERFORMERS (Assists abaixo do esperado):")
print(top100_subperformers.select([
    'player', 'team', 'league', 'matches', 'assists', 'xAG', 'assists_minus_xag'
]).head(5))

print("\n🔺 TOP 5 OVERPERFORMERS (Assists acima do esperado):")
print(top100_overperformers.select([
    'player', 'team', 'league', 'matches', 'assists', 'xAG', 'assists_minus_xag'
]).head(5))

print("\n⚡ TOP 5 PER 90 MINUTES (mínimo 5 xAG):")
print(top100_per90.select([
    'player', 'team', 'league', 'matches', 'assists', 'xAG', 'assists_minus_xag_90'
]).head(5))

print("\n" + "=" * 60)
print("✅ ANÁLISE COMPLETA!")
print("=" * 60)
print(f"\n📁 Ficheiros gerados em: {OUTPUT_DIR.absolute()}")
print("   • top100_subperformers.csv")
print("   • top100_overperformers.csv")
print("   • top100_per90.csv")
print("   • top100_assists_analysis.xlsx")
print("   • scatter_xag_vs_assists.png")
print("   • bar_top20_overperformers.png")
print("   • bar_top20_subperformers.png")
print("\n🚀 Para dashboard interativo, execute: streamlit run streamlit_app.py")
print("=" * 60)
