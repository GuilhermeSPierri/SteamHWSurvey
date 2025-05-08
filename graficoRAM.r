library(ggplot2)
library(dplyr)
library(stringr)

# Carregar e processar os dados
dados_ram <- read.csv("shs.csv") %>% 
  filter(category == "System RAM") %>% 
  mutate(
    # Extrair valor numérico e ordenar categorias
    RAM_numeric = case_when(
      name == "Less than 4 GB" ~ 2,
      name == "More than 64 GB" ~ 128,
      name == "Other" ~ 256,
      TRUE ~ as.numeric(str_extract(name, "\\d+"))
    ),
    Porcentagem = percentage * 100,
    # Manter label original
    RAM = factor(name) %>% reorder(RAM_numeric)
  )

# Criar gráfico de barras
ggplot(dados_ram, aes(x = RAM, y = Porcentagem)) +
  geom_col(fill = "#2c7fb8", width = 0.7) +
  geom_text(
    aes(label = sprintf("%.1f%%", Porcentagem)),
    vjust = -0.5, 
    color = "darkblue",
    size = 3.5
  ) +
  labs(
    title = "Distribuição de Memória RAM",
    x = "Quantidade de RAM",
    y = "Percentual (%)"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1, size = 10),
    plot.title = element_text(hjust = 0.5, size = 14),
    panel.grid.major.x = element_blank()
  ) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.1)))

# Salvar gráfico
ggsave("distribuicao_ram.png", width = 10, height = 6)