# Trabalho Prático 6: Filtro Espacial da Média (Suavização Passa-Baixa)

Este trabalho implementa o **Filtro Espacial da Média** (*Spatial Mean / Box Filter*) no domínio espacial, utilizando **convolução 2D vetorizada via fatiamento (slicing)** e **tratamento de bordas por espelhamento simétrico** (*symmetric padding*).

---

## 🎯 Objetivos

- Implementar o filtro passa-baixa da média linear com máscara quadrada $N \times N$, onde $N = 2a + 1$ é um inteiro ímpar positivo.
- Otimizar a convolução espacial através de fatiamento (*slicing*) de matrizes NumPy, eliminando laços aninhados sobre as coordenadas espaciais $(x, y)$.
- Tratar as fronteiras da imagem com **espelhamento simétrico** (`np.pad(mode='symmetric')`), eliminando artefatos de moldura escura típicos do preenchimento com zeros (*zero-padding*).
- Avaliar comparativamente o efeito de suavização e perda de detalhes finos sob diferentes ordens de máscaras: $3 \times 3$, $7 \times 7$, $15 \times 15$ e $35 \times 35$.

---

## 📐 Fundamentação Teórica

### 1. Filtro da Média e Coeficiente Uniforme
A resposta de um filtro de média linear centrada em $(x, y)$ sobre uma vizinhança $N \times N$ com $a = (N - 1) / 2$ é dada por:

$$g(x, y) = \frac{1}{N^2} \sum_{s=-a}^{a} \sum_{t=-a}^{a} f(x + s, y + t)$$

Todos os coeficientes da máscara são homogêneos e somam 1: $w = \frac{1}{N^2}$.

### 2. Tratamento de Bordas: Espelhamento Simétrico (*Symmetric Padding*)
Ao convoluir uma máscara de dimensão $N$ sobre uma imagem de tamanho $H \times W$, os pixels na borda precisam de pixels além das dimensões originais. O preenchimento simétrico reflete os pixels das bordas:

$$\text{Tamanho com padding: } (H + 2a) \times (W + 2a)$$

Isso evita a queda artificial de luminosidade nas bordas gerada por zeros.

### 3. Convolução Vetorizada via Fatiamento (*Slicing*)
Em vez de dois laços lentos em Python percorrendo todos os pixels $(y, x)$, o algoritmo itera apenas sobre as dimensões do núcleo ($N \times N$ iterações), acumulando fatias contínuas completas da imagem acolchoada:

$$\text{slice}(i, j) = \text{padded}[i : i + H, \; j : j + W]$$
$$\text{output} = \sum_{i=0}^{N-1} \sum_{j=0}^{N-1} \left( \text{slice}(i, j) \cdot \frac{1}{N^2} \right)$$

---

## 📁 Estrutura de Arquivos

| Arquivo | Descrição |
|---|---|
| `filtro_media.py` | Implementação vetorizada do filtro da média e rotina de testes |
| `cobaia.jpg` | Imagem cobaia original utilizada nos experimentos |
| `01_imagem_original.jpg` | Imagem de entrada registrada |
| `02_filtro_media_3x3.jpg` | Resultado com máscara $3 \times 3$ (suavização sutil de ruído) |
| `03_filtro_media_7x7.jpg` | Resultado com máscara $7 \times 7$ (desfoque moderado) |
| `04_filtro_media_15x15.jpg` | Resultado com máscara $15 \times 15$ (desfoque intenso) |
| `05_filtro_media_35x35.jpg` | Resultado com máscara $35 \times 35$ (desfoque severo, preservando apenas grandes manchas) |
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
python filtro_media.py
```

*(Opcional) Passar uma imagem personalizada via linha de comando:*
```bash
python filtro_media.py caminho/para/outra_imagem.jpg
```
