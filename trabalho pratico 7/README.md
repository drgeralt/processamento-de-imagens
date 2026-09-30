# Trabalho Prático 7: Filtros Espaciais de Aguçamento (Laplaciano e Sobel)

Este trabalho explora filtros espaciais passa-alta baseados em **derivadas digitais de 1ª ordem (Gradiente de Sobel)** e **derivadas de 2ª ordem (Operador Laplaciano)** para detecção de bordas e realce (*sharpening*) de imagens.

---

## 🎯 Objetivos

- Implementar convolução espacial 2D vetorizada com tratamento de bordas por espelhamento simétrico.
- Aplicar o **Operador Laplaciano** nas quatro variações clássicas de máscaras $3 \times 3$ (com 4 e 8 vizinhos, e centros positivos/negativos).
- Implementar a recuperação do fundo para aguçamento da imagem: $g(x, y) = f(x, y) + c \cdot [\nabla^2 f(x, y)]$.
- Aplicar o **Gradiente de Sobel** utilizando as matrizes ortogonais $h_1$ (vertical) e $h_2$ (horizontal), calculando a magnitude vetorial euclidiana exata $M(x, y) = \sqrt{g_x^2 + g_y^2}$.
- Realizar reescalonamento numérico Min-Max para visualização coerente de bordas e mapas de derivadas.

---

## 📐 Fundamentação Teórica

### 1. Filtro Laplaciano (Derivada de 2ª Ordem)
O Laplaciano é um operador derivativo isotrópico (invariante à rotação):

$$\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}$$

As quatro máscaras implementadas:
- **Máscara A (4 vizinhos, centro -4, $c = -1$):**
  $$\begin{bmatrix} 0 & 1 & 0 \\ 1 & -4 & 1 \\ 0 & 1 & 0 \end{bmatrix}$$
- **Máscara B (8 vizinhos, centro -8, $c = -1$):**
  $$\begin{bmatrix} 1 & 1 & 1 \\ 1 & -8 & 1 \\ 1 & 1 & 1 \end{bmatrix}$$
- **Máscara C (4 vizinhos, centro 4, $c = +1$):**
  $$\begin{bmatrix} 0 & -1 & 0 \\ -1 & 4 & -1 \\ 0 & -1 & 0 \end{bmatrix}$$
- **Máscara D (8 vizinhos, centro 8, $c = +1$):**
  $$\begin{bmatrix} -1 & -1 & -1 \\ -1 & 8 & -1 \\ -1 & -1 & -1 \end{bmatrix}$$

A imagem realçada combina o sinal original com as bordas acentuadas:

$$g(x, y) = f(x, y) + c \cdot \nabla^2 f(x, y)$$

### 2. Gradiente de Sobel (Derivada de 1ª Ordem)
O operador de Sobel utiliza dois núcleos $3 \times 3$ com ponderação suavizada no pixel central:

$$h_1 = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix} \quad (\text{Variações em } Y), \qquad h_2 = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix} \quad (\text{Variações em } X)$$

A magnitude gradiente euclidiana é calculada por:

$$M(x, y) = \sqrt{g_x^2(x, y) + g_y^2(x, y)}$$

### 3. Reescalonamento Numérico (Min-Max Scaling)
Como os operadores derivativos geram valores negativos e amplitudes fora do intervalo $[0, 255]$, os mapas isolados são reescalonados para visualização:

$$I_{out} = 255.0 \cdot \frac{I_{in} - \min(I_{in})}{\max(I_{in}) - \min(I_{in})}$$

---

## 📁 Estrutura de Arquivos

| Arquivo | Descrição |
|---|---|
| `filtros_agucamento.py` | Implementação completa dos filtros Laplaciano, Sobel e Min-Max scaling |
| `cobaia.jpg` | Imagem de teste utilizada para os filtros |
| `01_imagem_original.jpg` | Imagem de entrada registrada |
| `02_laplaciano_isolado_mascara_a.jpg` | Laplaciano isolado (máscara A, 4-vizinhos, centro -4) |
| `03_laplaciano_realcado_mascara_a.jpg` | Imagem realçada com máscara A |
| `04_laplaciano_isolado_mascara_b.jpg` | Laplaciano isolado (máscara B, 8-vizinhos, centro -8) |
| `05_laplaciano_realcado_mascara_b.jpg` | Imagem realçada com máscara B (maior riqueza diagonal) |
| `06_laplaciano_isolado_mascara_c.jpg` | Laplaciano isolado (máscara C, centro 4) |
| `07_laplaciano_realcado_mascara_c.jpg` | Imagem realçada com máscara C |
| `08_laplaciano_isolado_mascara_d.jpg` | Laplaciano isolado (máscara D, centro 8) |
| `09_laplaciano_realcado_mascara_d.jpg` | Imagem realçada com máscara D |
| `10_sobel_magnitude.jpg` | Magnitude Euclidiana do gradiente de Sobel |
| `11_sobel_realcado.jpg` | Imagem aguçada com a magnitude de Sobel ($f + M$) |
| `12_sobel_gx_horizontal.jpg` | Gradiente horizontal $G_x$ reescalonado |
| `13_sobel_gy_vertical.jpg` | Gradiente vertical $G_y$ reescalonado |
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
python filtros_agucamento.py
```

*(Opcional) Passar uma imagem personalizada via linha de comando:*
```bash
python filtros_agucamento.py caminho/para/outra_imagem.jpg
```
