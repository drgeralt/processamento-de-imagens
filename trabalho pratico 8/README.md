# Trabalho Prático 8: Processamento Morfológico de Imagens

Este trabalho implementa as operações fundamentais da **Morfologia Matemática**: **Dilatação**, **Erosão** e **Gradiente Morfológico**, cobrindo o processamento tanto em imagens binárias quanto em imagens em níveis de cinza.

---

## 🎯 Objetivos

- Criar geradores dinâmicos de **elementos estruturantes** parametrizáveis (quadrado/retangular, cruz e elipse) de dimensões ímpares $N \times N$.
- Implementar **dilatação e erosão morfológica vetorizadas** utilizando fatiamento contínuo (*slicing*) e projeção temporal multidimensional via `np.max` e `np.min`.
- Aplicar morfologia binária (com binarização automática de Otsu) para avaliar os efeitos geométricos dos elementos estruturantes quadrado $3 \times 3$ e em cruz $3 \times 3$.
- Implementar e aplicar o **Gradiente Morfológico** em níveis de cinza ($g = (f \oplus b) - (f \ominus b)$) com elementos estruturantes $3 \times 3$ e $5 \times 5$, evidenciando contornos de forma isotrópica.

---

## 📐 Fundamentação Teórica

### 1. Elementos Estruturantes
Matrizes binárias centradas de dimensão ímpar $(2a+1) \times (2a+1)$ definindo a vizinhança de análise:
- **Retangular (`rect`):** matriz preenchida integralmente com 1s.
- **Cruz (`cross`):** 1s apenas na linha central e coluna central.
- **Elipse (`ellipse`):** disco discreto com raio $r = a$.

### 2. Dilatação Morfológica ($\oplus$)
- **Binária:** $A \oplus B = \{z \mid (\hat{B})_z \cap A \neq \emptyset\}$ (expande regiões claras).
- **Níveis de cinza:** $(f \oplus b)(x, y) = \max_{(s,t) \in B} \{ f(x - s, y - t) \}$.
- **Tratamento de borda:** padding constante com valor neutro $0$.

### 3. Erosão Morfológica ($\ominus$)
- **Binária:** $A \ominus B = \{z \mid (B)_z \subseteq A\}$ (reduz regiões claras e remove pequenos ruídos).
- **Níveis de cinza:** $(f \ominus b)(x, y) = \min_{(s,t) \in B} \{ f(x + s, y + t) \}$.
- **Tratamento de borda:** padding defensivo com valor neutro máximo ($1$ se binária ou $255$ em escala de cinza), prevenindo o escurecimento artificial das fronteiras da imagem.

### 4. Gradiente Morfológico
O gradiente morfológico calcula a diferença entre a dilatação e a erosão da imagem com o mesmo elemento estruturante:

$$g(x, y) = (f \oplus b)(x, y) - (f \ominus b)(x, y)$$

Destaca contornos e transições bruscas de intensidade sem a sensibilidade direcional de operadores gradientes baseados em derivadas lineares.

---

## 📁 Estrutura de Arquivos

| Arquivo | Descrição |
|---|---|
| `morfologia.py` | Implementação vetorizada de dilatação, erosão, gradiente morfológico e testes |
| `cobaia.jpg` | Imagem de teste original |
| `01_imagem_original.jpg` | Cópia registrada da imagem de entrada |
| `02_imagem_cinza.jpg` | Versão convertida em escala de cinza |
| `03_imagem_binaria.png` | Imagem binarizada pelo método de Otsu |
| `04_dilatacao_binaria_rect3x3.png` | Dilatação binária com elemento quadrado $3 \times 3$ |
| `05_erosao_binaria_rect3x3.png` | Erosão binária com elemento quadrado $3 \times 3$ |
| `06_dilatacao_binaria_cruz3x3.png` | Dilatação binária com elemento em cruz $3 \times 3$ |
| `07_erosao_binaria_cruz3x3.png` | Erosão binária com elemento em cruz $3 \times 3$ |
| `08_dilatacao_cinza_3x3.jpg` | Dilatação em tons de cinza com elemento $3 \times 3$ |
| `09_erosao_cinza_3x3.jpg` | Erosão em tons de cinza com elemento $3 \times 3$ |
| `10_gradiente_morfologico_3x3.jpg` | Gradiente morfológico $3 \times 3$ (bordas nítidas e finas) |
| `11_gradiente_morfologico_5x5.jpg` | Gradiente morfológico $5 \times 5$ (bordas mais espessas) |
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
python morfologia.py
```

*(Opcional) Passar uma imagem personalizada via linha de comando:*
```bash
python morfologia.py caminho/para/outra_imagem.jpg
```
