library(dplyr)
library(stringr)

# Ler o arquivo CSV
data <- read.csv("shs.csv")

# Função para calcular a mediana ponderada
WeightedMedian <- function(x, w) {
  ord <- order(x)
  x_sorted <- x[ord]
  w_sorted <- w[ord]
  cum_w <- cumsum(w_sorted)
  median_idx <- which(cum_w >= 0.5)[1]
  x_sorted[median_idx]
}

# Função para calcular a moda (valor com maior peso)
Mode <- function(x, w) {
  x[which.max(w)]
}

# Processar CPUs Físicas
cpus <- data %>%
  filter(category == "Physical CPUs") %>%
  mutate(
    cpus = as.numeric(str_extract(name, "^\\d+"))
  ) %>%
  filter(!is.na(cpus)) %>%
  select(cpus, percentage) %>%
  mutate(adjusted_percent = percentage / sum(percentage))

mean_cpus <- sum(cpus$cpus * cpus$adjusted_percent)
median_cpus <- WeightedMedian(cpus$cpus, cpus$adjusted_percent)
mode_cpus <- Mode(cpus$cpus, cpus$adjusted_percent)

# Processar Memória RAM
ram <- data %>%
  filter(category == "System RAM") %>%
  mutate(
    ram_gb = as.numeric(str_extract(name, "^\\d+"))
  ) %>%
  filter(!is.na(ram_gb)) %>%
  select(ram_gb, percentage) %>%
  mutate(adjusted_percent = percentage / sum(percentage))

mean_ram <- sum(ram$ram_gb * ram$adjusted_percent)
median_ram <- WeightedMedian(ram$ram_gb, ram$adjusted_percent)
mode_ram <- Mode(ram$ram_gb, ram$adjusted_percent)

# Processar VRAM
vram <- data %>%
  filter(category == "VRAM") %>%
  mutate(
    value = as.numeric(str_extract(name, "^\\d+")),
    unit = str_extract(name, "GB|MB")
  ) %>%
  filter(!is.na(value), !is.na(unit), name != "Other") %>%
  mutate(
    vram_gb = ifelse(unit == "MB", value / 1024, value)
  ) %>%
  select(vram_gb, percentage) %>%
  mutate(adjusted_percent = percentage / sum(percentage))

mean_vram <- sum(vram$vram_gb * vram$adjusted_percent)
median_vram <- WeightedMedian(vram$vram_gb, vram$adjusted_percent)
mode_vram <- Mode(vram$vram_gb, vram$adjusted_percent)

# Criar tabela de resultados
results <- data.frame(
  Variável = c("CPUs Físicas", "RAM (GB)", "VRAM (GB)"),
  Média = c(mean_cpus, mean_ram, mean_vram),
  Mediana = c(median_cpus, median_ram, median_vram),
  Moda = c(mode_cpus, mode_ram, mode_vram)
)

# Exibir resultados
print(results)