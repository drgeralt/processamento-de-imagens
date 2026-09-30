# Trabalho Prático 3: Operações Aritméticas e Transformações Geométricas em Imagens

Este trabalho aborda o processamento pixel a pixel através de **operações aritméticas matriciais** (adição e subtração) e **transformações geométricas espaciais** (rotação por mapeamento inverso com interpolação bilinear).

---

## 🎯 Objetivos

- Gerar sinteticamente imagens de teste padronizadas (gradientes, figuras geométricas e padrões de xadrez).
- Implementar a **adição de imagens** com média aritmética truncada para evitar overflow em inteiros de 8 bits.
- Implementar a **subtração de imagens** utilizando diferença absoluta para capturar variações entre cenas.
- Implementar **rotação geométrica** utilizando a estratégia de **Mapeamento Inverso** ($T^{-1}$) e **Interpolação Bilinear**, calculando dinamicamente a caixa delimitadora (*bounding box*) para que os cantos da imagem não sejam cortados.

---

## 📐 Fundamentação Teórica

### 1. Adição de Imagens (Média Aritmética)
Para combinar duas imagens $g_1$ e $g_2$ do mesmo tamanho sem estouro da escala dinâmica de 8 bits ($[0, 255]$):

$$g_s(x, y) = \mathrm{trunc}\left(\frac{g_1(x, y) + g_2(x, y)}{2}\right)$$

A soma intermediária é realizada em `int32` para prevenção de overflow antes da divisão e truncamento.

### 2. Subtração de Imagens (Diferença Absoluta)
Para identificar contrastes e mudanças estruturais entre duas imagens:

$$d(x, y) = |f(x, y) - g(x, y)|$$

Os valores negativos gerados pela subtração ponto a ponto são convertidos via magnitude absoluta ($|\cdot|$) antes da conversão para `uint8`.

### 3. Rotação com Mapeamento Inverso e Interpolação Bilinear
A rotação direta pode gerar "buracos" ou lacunas na imagem de destino. Para evitar isso, adota-se o **Mapeamento Inverso**, iterando sobre os pixels da nova imagem e consultando a imagem original via matriz de rotação inversa:

$$\begin{bmatrix} x_0 \\ y_0 \end{bmatrix} = \begin{bmatrix} \cos(\theta) & \sin(\theta) \\ -\sin(\theta) & \cos(\theta) \end{bmatrix} \begin{bmatrix} x_d - c_x^{out} \\ y_d - c_y^{out} \end{bmatrix} + \begin{bmatrix} c_x^{in} \\ c_y^{in} \end{bmatrix}$$

Onde:
- As dimensões da nova imagem são ajustadas projetando os 4 vértices originais através da matriz de rotação, garantindo que o enquadramento total seja mantido.
- A intensidade $I(x_0, y_0)$ é estimada via interpolação bilinear contínua.

---

## 📁 Estrutura de Arquivos

| Arquivo | Descrição |
|---|---|
| `operacoes.py` | Implementação das operações aritméticas e da rotação geométrica |
| `01_cobaia_A.png` | Imagem cobaia 1: gradiente horizontal com círculo branco central |
| `02_cobaia_B.png` | Imagem cobaia 2: tabuleiro de xadrez com quadrado preto |
| `03_adicao.png` | Resultado da adição com média aritmética |
| `04_subtracao.png` | Resultado da subtração com diferença absoluta |
| `05_rotacao.png` | Resultado da rotação com mapeamento inverso e interpolação |
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
python operacoes.py
```
