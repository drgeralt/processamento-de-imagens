# Trabalho Prático 5: Alargamento de Contraste e Equalização de Histograma

Este trabalho implementa técnicas de manipulação e redistribuição de histogramas no domínio espacial: **Alargamento de Contraste** (*Contrast Stretching*) e **Equalização Global de Histograma** (*Histogram Equalization*), com suporte tanto para imagens monocromáticas (tons de cinza) quanto policromáticas (coloridas no espaço BGR e HSV).

---

## 🎯 Objetivos

- Implementar o **Alargamento de Contraste Linear** para expandir a faixa dinâmica de intensidades para cobrir todo o intervalo $[0, 255]$.
- Implementar a **Equalização Global de Histograma** através do cálculo da probabilidade acumulada (CDF) e mapeamento via *Look-Up Table* (LUT) totalmente vetorizada com NumPy.
- Preservar a **fidelidade cromática** em imagens coloridas aplicando a equalização no canal $V$ (Value/Brilho) do espaço de cor **HSV**, comparando com a equalização independente nos canais $B, G, R$.

---

## 📐 Fundamentação Teórica

### 1. Alargamento de Contraste (*Contrast Stretching*)
Mapeia linearmente o menor nível de intensidade existente $c = \min(F)$ e o maior nível $d = \max(F)$ para o intervalo total $[0, 255]$:

$$G(x, y) = (F(x, y) - c) \cdot \frac{255.0}{d - c}$$

Inclui proteção defensiva para o caso de imagens constantes ($c = d$), evitando divisão por zero.

### 2. Equalização Global de Histograma via CDF e LUT
A equalização busca uniformizar a função densidade de probabilidade dos níveis de cinza:

1. **Histograma e Probabilidade ($p_r$):**
   $$p_r(r_k) = \frac{n_k}{M \cdot N}, \quad k \in [0, 255]$$

2. **Função de Distribuição Acumulada (CDF):**
   $$s_k = T(r_k) = (L - 1) \sum_{j=0}^{k} p_r(r_j) = 255 \cdot \mathrm{CDF}(r_k)$$

3. **Look-Up Table (LUT) Vetorizada:**
   A tabela de correspondência `LUT = np.round(255 * cdf).astype(np.uint8)` é aplicada diretamente à matriz da imagem via indexação avançada NumPy (`LUT[image]`), atingindo complexidade de mapeamento $O(1)$ por pixel.

### 3. Preservação de Cores via HSV
A equalização direta dos canais $B, G, R$ altera a relação proporcional entre as componentes, induzindo distorções severas de matiz e saturação. Para solucionar isso:
- Converte-se a imagem para o espaço **HSV** (*Hue, Saturation, Value*).
- Equaliza-se exclusivamente o canal $V$ (luminância).
- Converte-se de volta para BGR, mantendo cores naturais e vibrantes.

---

## 📁 Estrutura de Arquivos

| Arquivo | Descrição |
|---|---|
| `histogramas.py` | Implementação do alargamento, equalização (escala de cinza, HSV e BGR) |
| `Tip901-Before-1-scaled.jpg` | Imagem cobaia de entrada com baixo contraste dinâmico |
| `01_original.jpg` | Cópia de referência da imagem original |
| `01_original_cinza.jpg` | Versão convertida em escala de cinza |
| `02_alargamento_contraste.jpg` | Imagem após alargamento de contraste |
| `03_equalizacao_histograma.jpg` | Imagem equalizada com preservação cromática (via canal V no HSV) |
| `03_equalizacao_histograma_bgr.jpg` | Imagem equalizada com canais independentes BGR (para comparação de artefatos) |
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
python histogramas.py
```
