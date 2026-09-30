# Trabalho Prático 4: Transformações de Intensidade e Normalização

Este trabalho implementa e analisa as transformações pontuais de intensidade no domínio espacial: **Transformação Negativa**, **Transformação Logarítmica** e **Transformação de Potência (Gama)**, aplicando um pipeline rigoroso de normalização numérica.

---

## 🎯 Objetivos

- Estabelecer um pipeline de pré-processamento com **normalização para $[0, 1]$** e pós-processamento com **desnormalização para $[0, 255]$** e *clipping* defensivo.
- Aplicar a **Transformação Negativa** para realçar detalhes em áreas escuras de exames médicos (ex.: Raio-X de tórax).
- Aplicar a **Transformação Logarítmica** para expandir a faixa de níveis escuros e comprimir níveis claros em imagens de alto contraste noturno.
- Aplicar a **Transformação de Potência (Gama / Power-Law)** comparando os efeitos de $\gamma < 1$ (clareamento de sombras) e $\gamma > 1$ (escurecimento de altas luzes).

---

## 📐 Fundamentação Teórica

### 1. Pipeline de Normalização e Desnormalização
Todas as transformações operam sobre matrizes normalizadas para evitar inconsistências com funções transcendentes ($\log$, potências):

- **Normalização:** $r = \frac{f(x, y)}{255.0} \in [0.0, 1.0]$ em ponto flutuante (`float32`).
- **Desnormalização:** $s_{uint8} = \mathrm{clip}\left(\mathrm{round}(s \cdot 255.0), 0, 255\right)$.

### 2. Transformação Negativa
Inverte a escala de brilho da imagem, equivalente a um filme fotográfico negativo:

$$s = 1.0 - r$$

Ideal para ressaltar estruturas densas e opacidades em imagens biomédicas.

### 3. Transformação Logarítmica
Comprime a faixa dinâmica de valores muito altos e expande tons escuros:

$$s = c \cdot \log(1.0 + r)$$

Onde a constante de escala $c$ é parametrizada para normalizar a saída máxima (ex.: $c = \frac{5.0}{\log(2.0)}$).

### 4. Transformação Gama / Lei de Potência (*Power-Law*)
Modela respostas não-lineares de dispositivos de captura e exibição (CRT, monitores modernos):

$$s = c \cdot r^\gamma$$

- **$\gamma < 1$ (ex: $\gamma = 0.4$):** Expande valores escuros, clareando detalhes em sombras sem saturar excessivamente os tons claros.
- **$\gamma > 1$ (ex: $\gamma = 2.5$):** Comprime valores escuros e escurece a imagem como um todo, aumentando o contraste em áreas superexpostas.

---

## 📁 Estrutura de Arquivos

| Arquivo | Descrição |
|---|---|
| `transformacoes.py` | Implementação do pipeline de normalização e das três transformações |
| `m2400651-pneumonia.jpg` | Imagem médica de entrada (Raio-X de tórax em escala de cinza) |
| `ricardo-wu-C_jHDwWSgu8-unsplash.jpg` | Imagem colorida de entrada (cenário urbano noturno com alto contraste) |
| `01_pneumonia_negativo.jpg` | Resultado do negativo aplicado ao Raio-X |
| `02_noite_logaritmica.jpg` | Resultado da transformação logarítmica na foto noturna |
| `03_noite_gama_0.4_clareada.jpg` | Resultado da transformação gama com $\gamma = 0.4$ (clareada) |
| `04_noite_gama_2.5_escurecida.jpg` | Resultado da transformação gama com $\gamma = 2.5$ (escurecida) |
| `requirements.txt` | Dependências necessárias para execução |

---

## 🚀 Como Executar

### 1. Criar e ativar o ambiente virtual (opcional)
```bash
python -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate   # No Windows
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Rodar o script
```bash
python transformacoes.py
```
