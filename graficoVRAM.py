import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick

# Carregar e preparar os dados
df = pd.read_csv('database.csv')
vram_data = df[df.iloc[:, 1] == 'VRAM'].iloc[:, [0, 2, 4]]
vram_data.columns = ['Date', 'VRAM', 'Percentage']
vram_data['Date'] = pd.to_datetime(vram_data['Date'])

# Converter para porcentagem real e filtrar abril/2025
vram_data['Percentage'] = vram_data['Percentage'] * 100
latest_vram = vram_data[vram_data['Date'] == '2025-04-01']
latest_vram = latest_vram[~latest_vram['VRAM'].str.contains('Other|Unspecified', case=False)]

# Ordenar por capacidade de VRAM
vram_order = ['512 MB', '1 GB', '2 GB', '3 GB', '4 GB', '6 GB', '8 GB', '10 GB', '11 GB', '12 GB', '16 GB', '24 GB']
latest_vram['VRAM'] = pd.Categorical(latest_vram['VRAM'], categories=vram_order, ordered=True)
latest_vram = latest_vram.sort_values('VRAM')

# Filtrar apenas entradas relevantes (>= 0.5%)
latest_vram = latest_vram[latest_vram['Percentage'] >= 0.5]

# Configuração do gráfico
plt.figure(figsize=(14, 8))
bar_colors = plt.cm.viridis_r(np.linspace(0.2, 0.8, len(latest_vram)))

# Gráfico de barras
bars = plt.bar(latest_vram['VRAM'], latest_vram['Percentage'], 
               color=bar_colors, edgecolor='black', width=0.7)

# Adicionar valores exatos
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}%',
             ha='center', va='bottom',
             fontsize=10,
             fontweight='bold')

# Personalização
plt.title('Distribuição de VRAM entre Usuários da Steam\nAbril 2025 (Valores Oficiais)', 
          fontsize=16, pad=20)
plt.xlabel('Capacidade de VRAM', fontsize=12)
plt.ylabel('Percentual de Usuários', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Linha de referência
plt.axhline(y=5, color='red', linestyle=':', linewidth=1, alpha=0.5)

# Verificação
print("\nDADOS REAIS UTILIZADOS:")
print(latest_vram[['VRAM', 'Percentage']].sort_values('VRAM'))

plt.tight_layout()
plt.show()