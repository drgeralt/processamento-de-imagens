# Trabalho Prático 2: Rotulagem de Componentes Conexas (Connected-Component Labeling)

Este trabalho implementa o algoritmo clássico de **Rotulagem de Componentes Conexas (Two-Pass)** utilizando **8-conectividade** e a estrutura de dados **Union-Find** (Disjoint-Set) com compressão de caminho (*path compression*) para resolução de equivalências entre regiões.

---

## 🎯 Objetivos

- Gerar sinteticamente imagens de teste contendo múltiplas formas geométricas aleatórias (círculos, retângulos, elipses e linhas).
- Implementar **binarização defensiva** baseada em limiar fixo ($T = 127$).
- Implementar o algoritmo **Two-Pass com 8-conectividade** para identificar e individualizar objetos conectados na imagem.
- Desenvolver a estrutura **Union-Find** para gerenciamento ótimo de equivalências entre rótulos adjacentes.
- Colorir artificialmente cada componente conectada para validação e visualização qualitativa.

---

## 📐 Fundamentação Teórica

### 1. Binarização Defensiva
A matriz de entrada $f(x, y)$ é convertida para uma matriz binária $f'(x, y) \in \{0, 1\}$:

$$f'(x, y) = \begin{cases} 1, & \text{se } f(x, y) \ge 127 \\ 0, & \text{se } f(x, y) < 127 \end{cases}$$

### 2. Algoritmo Two-Pass com 8-Conectividade
Para cada pixel de primeiro plano $p = 1$, são inspecionados os vizinhos previamente visitados no padrão de varredura (cima para baixo, esquerda para direita):
- Noroeste ($NW$): $(y-1, x-1)$
- Norte ($N$): $(y-1, x)$
- Nordeste ($NE$): $(y-1, x+1)$
- Oeste ($W$): $(y, x-1)$

Casos de atribuição:
1. **Sem vizinhos rotulados:** atribui novo rótulo sequencial único e registra no Union-Find.
2. **Um único rótulo vizinho (ou múltiplos idênticos):** propaga esse rótulo para o pixel atual.
3. **Múltiplos rótulos distintos (Colisão de Equivalência):** atribui o menor rótulo aos pixels e registra uma união (`union`) entre os rótulos no Union-Find.

### 3. Segunda Varredura
Após finalizar a primeira passada, os rótulos de equivalência são achatados via `find(label)`. A segunda varredura substitui todos os rótulos provisórios por sua raiz canônica definitiva.

---

## 📁 Estrutura de Arquivos

| Arquivo | Descrição |
|---|---|
| `connected_components.py` | Implementação completa do algoritmo Two-Pass, Union-Find e pipeline |
| `01_imagem_original.png` | Imagem sintética original com formas geométricas em níveis de intensidade |
| `02_imagem_binarizada.png` | Imagem binarizada (apenas 0 e 255 para visualização) |
| `03_componentes_coloridas.png` | Mapa de componentes com cores RGB aleatórias para cada objeto distinto |
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
python connected_components.py
```
