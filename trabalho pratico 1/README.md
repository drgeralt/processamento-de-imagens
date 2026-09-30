# Trabalho Prático 1: Algoritmos de Redimensionamento e Interpolação Espacial

Este trabalho aborda os conceitos fundamentais de amostragem, interpolação espacial e redimensionamento de imagens digitais, comparando implementações manuais (from scratch) com as funções otimizadas do OpenCV.

---

## 🎯 Objetivos

- Implementar manualmente o algoritmo de **Interpolação por Vizinho Mais Próximo** (*Nearest-Neighbor Interpolation*).
- Implementar manualmente o algoritmo de **Interpolação Bilinear** (*Bilinear Interpolation*).
- Avaliar a fidelidade das implementações através do cálculo do **Erro Quadrático Médio (MSE)** em relação às funções nativas do OpenCV (`cv2.INTER_NEAREST` e `cv2.INTER_LINEAR`).
- Medir e comparar o tempo de execução (benchmark) entre as versões manuais e as otimizadas.

---

## 📐 Fundamentação Teórica

### 1. Vizinho Mais Próximo (*Nearest Neighbor*)
O método mapeia as coordenadas do espaço de destino $(x_{dst}, y_{dst})$ de volta para o espaço original da imagem através das escalas $s_x = W / W_{new}$ e $s_y = H / H_{new}$:

$$x_{src} = x_{dst} \cdot s_x, \quad y_{src} = y_{dst} \cdot s_y$$

O valor de intensidade atribuído é o do pixel mais próximo por arredondamento:

$$I_{dst}(x_{dst}, y_{dst}) = I_{src}(\mathrm{round}(x_{src}), \mathrm{round}(y_{src}))$$

Tratamento de bordas é aplicado por replicação: $\min(\mathrm{round}(x_{src}), W - 1)$.

### 2. Interpolação Bilinear (*Bilinear Interpolation*)
A interpolação bilinear utiliza uma média ponderada dos 4 pixels vizinhos mais próximos $(x_1, y_1), (x_2, y_1), (x_1, y_2), (x_2, y_2)$:

Seja $x_1 = \lfloor x_{src} \rfloor$, $y_1 = \lfloor y_{src} \rfloor$, $x_2 = \min(x_1 + 1, W - 1)$, $y_2 = \min(y_1 + 1, H - 1)$, e as frações de deslocamento $dx = x_{src} - x_1$ e $dy = y_{src} - y_1$:

$$I(x, y) = (1 - dx)(1 - dy) I(x_1, y_1) + dx(1 - dy) I(x_2, y_1) + (1 - dx)dy I(x_1, y_2) + dx \cdot dy I(x_2, y_2)$$

Os cálculos são realizados em ponto flutuante (`float32`) para evitar overflow aritmético e posteriormente convertidos de volta para `uint8` no intervalo $[0, 255]$.

### 3. Erro Quadrático Médio (*MSE - Mean Squared Error*)

$$\mathrm{MSE} = \frac{1}{M \cdot N \cdot C} \sum_{c=1}^{C} \sum_{y=1}^{M} \sum_{x=1}^{N} (I_1(x, y, c) - I_2(x, y, c))^2$$

---

## 📁 Estrutura de Arquivos

| Arquivo | Descrição |
|---|---|
| `resize_algorithms.py` | Script principal contendo as funções de interpolação e benchmark |
| `cobaia.jpg` | Imagem cobaia utilizada para teste |
| `Imagem_base.jpg` | Imagem base lida |
| `resultado_nearest_neighbor_custom.jpg` | Saída gerada pela implementação manual do Vizinho Mais Próximo |
| `resultado_nearest_neighbor_opencv.jpg` | Saída de referência gerada pelo OpenCV (`INTER_NEAREST`) |
| `resultado_bilinear_custom.jpg` | Saída gerada pela implementação manual da Interpolação Bilinear |
| `resultado_bilinear_opencv.jpg` | Saída de referência gerada pelo OpenCV (`INTER_LINEAR`) |
| `requirements.txt` | Dependências necessárias para execução |

---

## 🚀 Como Executar

### 1. Criar e ativar o ambiente virtual (opcional, mas recomendado)
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
python resize_algorithms.py
```
