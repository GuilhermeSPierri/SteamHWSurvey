import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('database.csv')
lang_data = df[df.iloc[:, 1] == 'Language'].iloc[:, [0, 2, 4]]
lang_data.columns = ['Date', 'Language', 'Percentage']
lang_data['Date'] = pd.to_datetime(lang_data['Date'])

lang_data['Percentage'] = lang_data['Percentage'] * 100

latest_lang = lang_data[lang_data['Date'] == '2025-04-01']
latest_lang = latest_lang[~latest_lang['Language'].str.contains('Unspecified|Other')]

# Selecionar top 10
top_langs = latest_lang.nlargest(10, 'Percentage')

# Paleta de cores atualizada
colors = {
    'English': '#1f77b4',        # Azul
    'Simplified Chinese': '#d62728', # Vermelho
    'Russian': '#2ca02c',        # Verde
    'Portuguese-Brazil': '#ff7f0e', # Laranja
    'German': '#9467bd',         # Roxo
    'French': '#8c564b',         # Marrom
    'Spanish - Spain': '#e377c2', # Rosa
    'Japanese': '#7f7f7f',       # Cinza
    'Korean': '#bcbd22',         # Verde-oliva
    'Polish': '#17becf'          # Ciano
}

# Criar figura
fig, ax = plt.subplots(figsize=(14, 10))

# Gráfico de pizza com valores CORRETOS
wedges, texts = plt.pie(
    top_langs['Percentage'],
    colors=[colors.get(lang, '#dddddd') for lang in top_langs['Language']],
    startangle=140,
    wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
    pctdistance=0.8
)

# Adicionar valores EXATOS
for i, wedge in enumerate(wedges):
    angle = (wedge.theta2 - wedge.theta1)/2. + wedge.theta1
    x = 0.8 * wedge.r * np.cos(np.deg2rad(angle))
    y = 0.8 * wedge.r * np.sin(np.deg2rad(angle))
    ax.text(x, y, f'{top_langs.iloc[i]["Percentage"]:.2f}%',
            ha='center', va='center',
            fontsize=10,
            fontweight='bold',
            color='white')

# Legenda com valores verificados
legend_labels = [f"{lang}: {pct:.2f}%" for lang, pct in zip(top_langs['Language'], top_langs['Percentage'])]
plt.legend(wedges, legend_labels,
           title="Top 10 Idiomas\n(Valores Reais)",
           loc="center left",
           bbox_to_anchor=(1, 0.5),
           fontsize=10)

# Título
plt.title('\n\nDistribuição Real de Idiomas na Steam\nAbril 2025 (Valores Oficiais)',
          fontsize=16, pad=20, fontweight='bold')

# Verificação no console

plt.tight_layout()
plt.show()