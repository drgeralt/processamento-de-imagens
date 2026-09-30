# Processamento Digital de Imagens (PDI)

Repositório contendo implementações práticas, algoritmos fundamentais e relatórios técnicos desenvolvidos para a disciplina de **Processamento Digital de Imagens**.

Todos os algoritmos foram implementados em **Python**, priorizando a construção *from scratch* com operações matriciais vetorizadas em **NumPy**, tratamento defensivo de overflow/underflow, tratamento de bordas e validação visual e quantitativa com **OpenCV**.

---

## 📚 Trabalhos Práticos

A tabela abaixo resume os trabalhos práticos contidos neste repositório. Cada diretório contém seu próprio código-fonte, imagens cobaia de entrada, saídas visuais geradas e um `README.md` detalhado com a fundamentação matemática.

| Trabalho | Tópico Principal | Algoritmos & Técnicas Principais | Documentação |
|:---:|:---|:---|:---:|
| **TP 01** | Redimensionamento e Interpolação | Vizinho Mais Próximo (*Nearest-Neighbor*), Interpolação Bilinear, Avaliação por MSE e Benchmark contra OpenCV | [Ver Detalhes](trabalho%20pratico%201/README.md) |
| **TP 02** | Rotulagem de Componentes Conexas | Binarização defensiva, Algoritmo Two-Pass (8-conectividade), Union-Find com *Path Compression*, Colorização RGB | [Ver Detalhes](trabalho%20pratico%202/README.md) |
| **TP 03** | Operações Aritméticas e Geométricas | Adição com média aritmética ($g_s = \lfloor (g_1+g_2)/2 \rfloor$), Subtração por diferença absoluta ($d = \|f-g\|$), Rotação por Mapeamento Inverso e Interpolação | [Ver Detalhes](trabalho%20pratico%203/README.md) |
| **TP 04** | Transformações de Intensidade | Pipeline de normalização $[0, 1]$, Negativo ($s = 1 - r$), Transformação Logarítmica ($s = c \log(1+r)$), Correção Gama / Potência ($s = c \cdot r^\gamma$) | [Ver Detalhes](trabalho%20pratico%204/README.md) |
| **TP 05** | Histogramas e Contraste | Alargamento de Contraste (*Contrast Stretching*), Equalização Global via CDF e Look-Up Table (LUT) vetorizada, Preservação de cor no espaço HSV | [Ver Detalhes](trabalho%20pratico%205/README.md) |
| **TP 06** | Filtros Espaciais de Suavização | Filtro Espacial da Média linear ($N \times N$), Convolução 2D vetorizada por *slicing*, Espelhamento Simétrico de bordas (*Symmetric Padding*) | [Ver Detalhes](trabalho%20pratico%206/README.md) |
| **TP 07** | Filtros Espaciais de Aguçamento | Derivadas espaciais, Laplaciano ($2ª$ ordem) com 4 e 8 vizinhos e recuperação de fundo ($g = f + c \cdot \nabla^2 f$), Gradiente de Sobel ($1ª$ ordem) com magnitude euclidiana | [Ver Detalhes](trabalho%20pratico%207/README.md) |
| **TP 08** | Morfologia Matemática | Elementos estruturantes dinâmicos (quadrado, cruz, elipse), Dilatação e Erosão vetorizadas (`np.max` e `np.min`), Morfologia binária (Otsu) e Gradiente Morfológico em níveis de cinza | [Ver Detalhes](trabalho%20pratico%208/README.md) |

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** [Python 3.10+](https://www.python.org/)
- **Cálculo Numérico Matricial:** [NumPy](https://numpy.org/)
- **Processamento de Imagens e I/O:** [OpenCV (opencv-python)](https://opencv.org/)

---

## 🚀 Como Executar

### 1. Clonar o repositório
```bash
git clone git@github.com:drgeralt/processamento-de-imagens.git
cd "processamento de imagens"
```

### 2. Configurar o Ambiente Virtual
Recomenda-se criar um ambiente virtual isolado para executar os projetos:

```bash
python -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate   # No Windows
```

### 3. Instalar as Dependências
Você pode instalar as dependências de todo o projeto usando o arquivo de requisitos global:
```bash
pip install -r requirements.txt
```
*(Ou, se preferir, instalar as dependências no diretório de um trabalho específico através do `requirements.txt` da respectiva pasta).*

### 4. Executar um Trabalho Prático
Entre na pasta do trabalho desejado e execute o script correspondente:

```bash
# Exemplo 1: Executar o Trabalho 1
cd "trabalho pratico 1"
python resize_algorithms.py

# Exemplo 2: Executar o Trabalho 7 (Filtros de Aguçamento)
cd "../trabalho pratico 7"
python filtros_agucamento.py
```

---

## 📂 Estrutura do Repositório

```plaintext
processamento-de-imagens/
├── .gitignore
├── README.md
├── requirements.txt
├── trabalho pratico 1/
│   ├── README.md
│   ├── requirements.txt
│   ├── resize_algorithms.py
│   └── ... (imagens de teste e resultados)
├── trabalho pratico 2/
│   ├── README.md
│   ├── requirements.txt
│   ├── connected_components.py
│   └── ...
├── trabalho pratico 3/
│   ├── README.md
│   ├── requirements.txt
│   ├── operacoes.py
│   └── ...
├── trabalho pratico 4/
│   ├── README.md
│   ├── requirements.txt
│   ├── transformacoes.py
│   └── ...
├── trabalho pratico 5/
│   ├── README.md
│   ├── requirements.txt
│   ├── histogramas.py
│   └── ...
├── trabalho pratico 6/
│   ├── README.md
│   ├── requirements.txt
│   ├── filtro_media.py
│   └── ...
├── trabalho pratico 7/
│   ├── README.md
│   ├── requirements.txt
│   ├── filtros_agucamento.py
│   └── ...
└── trabalho pratico 8/
    ├── README.md
    ├── requirements.txt
    ├── morfologia.py
    └── ...
```

---

## 👤 Autor

Desenvolvido por **Rhyan** ([@drgeralt](https://github.com/drgeralt)).
