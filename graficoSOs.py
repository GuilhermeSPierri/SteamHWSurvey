import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carregar e preparar os dados
df = pd.read_csv('database.csv')
os_data = df[df.iloc[:, 1] == 'OS Version'].iloc[:, [0, 2, 4]]
os_data.columns = ['Date', 'OS', 'Percentage']
os_data['Date'] = pd.to_datetime(os_data['Date'])

# Converter para porcentagem real (×100) e filtrar abril/2025
os_data['Percentage'] = os_data['Percentage'] * 100
latest_os = os_data[os_data['Date'] == '2025-04-01']
latest_os = latest_os[~latest_os['OS'].str.contains('Unspecified|Other', case=False)]

# Selecionar top 7 (para melhor visualização) e agrupar o restante como "Outros"
top_os = latest_os.nlargest(7, 'Percentage')
other_perc = latest_os['Percentage'].sum() - top_os['Percentage'].sum()
top_os = pd.concat([top_os, pd.DataFrame([{'OS': 'Outros', 'Percentage': other_perc}])])

# Paleta de cores para sistemas operacionais
colors = {
    'Windows 11 64 bit': '#0078d7',  # Azul Windows
    'Windows 10 64 bit': '#00a2ed',   # Azul mais claro
    'MacOS 15.4.0 64 bit': '#a2a2a2', # Cinza Apple
    'Ubuntu 24.04.2 LTS 64 bit': '#dd4814', # Laranja Ubuntu
    'Linux Mint 22.1 64 bit': '#87cf3e',   # Verde Mint
    'Arch Linux 64 bit': '#1793d1',      # Azul Arch
    'Windows 7 64 bit': '#f25022',       # Laranja Windows
    'Outros': '#cccccc'                  # Cinza para outros
}

# Criar figura
fig, ax = plt.subplots(figsize=(14, 10))

# Gráfico de pizza
wedges, texts = plt.pie(
    top_os['Percentage'],
    colors=[colors.get(os, '#dddddd') for os in top_os['OS']],
    startangle=140,
    wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
    pctdistance=0.8,
    textprops={'fontsize': 10}
)

# Adicionar valores exatos
for i, wedge in enumerate(wedges):
    angle = (wedge.theta2 - wedge.theta1)/2. + wedge.theta1
    x = 0.8 * wedge.r * np.cos(np.deg2rad(angle))
    y = 0.8 * wedge.r * np.sin(np.deg2rad(angle))
    value = top_os.iloc[i]['Percentage']
    if value > 3:  # Só mostra % em fatias grandes
        ax.text(x, y, f'{value:.2f}%', 
                ha='center', va='center',
                fontsize=10,
                fontweight='bold',
                color='white')

# Legenda detalhada
legend_labels = [f"{os.replace(' 64 bit','')}: {pct:.1f}%" 
                for os, pct in zip(top_os['OS'], top_os['Percentage'])]
plt.legend(wedges, legend_labels,
           title="Versões de SO (Valores Reais)",
           loc="center left",
           bbox_to_anchor=(1, 0.5),
           fontsize=10)

# Título
plt.title('\n\nDistribuição de Sistemas Operacionais na Steam\nAbril 2025 (Valores Oficiais)',
          fontsize=16, pad=20, fontweight='bold')

plt.tight_layout()
plt.show()