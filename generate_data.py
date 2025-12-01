"""
Script para gerar dados pré-carregados do FBref
Execute localmente: python generate_data.py
"""

import soccerdata as sd
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

print("🔄 Carregando dados do FBref...")

LEAGUES = [
    'ENG-Premier League',
    'ESP-La Liga',
    'FRA-Ligue 1',
    'GER-Bundesliga',
    'ITA-Serie A'
]
SEASONS = ['1718', '1819', '1920', '2021', '2122', '2223', '2324', '2425']

try:
    fbref = sd.FBref(leagues=LEAGUES, seasons=SEASONS, no_cache=False)
    player_season_stats = fbref.read_player_season_stats(stat_type="standard")
    
    print(f"✅ Dados carregados: {len(player_season_stats)} registros")
    
    # Processar colunas
    all_columns = player_season_stats.columns.tolist()
    column_mapping = {}
    
    for idx, col in enumerate(all_columns):
        col_str = str(col).lower()
        
        if 'pos' in col_str and 'position' not in column_mapping:
            column_mapping['position'] = idx
        elif ('mp' == col_str or 'matches' in col_str) and 'matches' not in column_mapping:
            column_mapping['matches'] = idx
        elif 'min' in col_str and 'minutes' not in column_mapping and 'per' not in col_str:
            column_mapping['minutes'] = idx
        elif (col_str == 'ast' or 'assist' in col_str) and 'assists' not in column_mapping and 'xag' not in col_str:
            column_mapping['assists'] = idx
        elif 'xag' in col_str and 'xAG' not in column_mapping:
            column_mapping['xAG'] = idx
    
    if len(column_mapping) < 5:
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
    
    # Resetar index
    df = df.reset_index()
    
    # Agregar dados
    stats = df.groupby(['league', 'team', 'player']).agg({
        'matches': 'sum',
        'assists': 'sum',
        'xAG': 'sum',
        'minutes': 'sum',
        'position': 'first'
    }).reset_index()
    
    # Calcular métricas
    stats['assists_minus_xag'] = stats['assists'] - stats['xAG']
    stats['assists_minus_xag_90'] = (stats['assists'] - stats['xAG']) / stats['minutes'] * 90
    
    # Filtrar
    stats = stats[
        (stats['minutes'] > 450) &
        (stats['xAG'] > 0)
    ]
    
    # Salvar CSV
    output_file = 'fbref_data.csv'
    stats.to_csv(output_file, index=False)
    
    print(f"✅ Dados salvos em: {output_file}")
    print(f"📊 Total jogadores processados: {len(stats)}")
    print(f"📁 Tamanho do arquivo: {len(stats.to_csv(index=False)) / 1024:.2f} KB")
    
except Exception as e:
    print(f"❌ Erro: {e}")
