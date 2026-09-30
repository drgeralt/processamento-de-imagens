import numpy as np
import cv2
import random

def generate_random_image(width=600, height=400):
    """
    Gera uma imagem aleatória com fundo preto e formas claras (intensidade >= 127).
    Cada vez que for rodado, as formas e posições serão diferentes.
    """
    # Fundo escuro (0)
    image = np.zeros((height, width), dtype=np.uint8)
    
    # Criar um número aleatório de formas
    num_shapes = random.randint(15, 35)
    
    for _ in range(num_shapes):
        shape_type = random.choice(['circle', 'rect', 'line', 'ellipse'])
        x = random.randint(0, width)
        y = random.randint(0, height)
        # Cor clara, acima do threshold de 127 (para virar 1 na binarização)
        color = random.randint(130, 255)
        thickness = -1 if shape_type != 'line' else random.randint(3, 10)
        
        if shape_type == 'circle':
            r = random.randint(10, 50)
            cv2.circle(image, (x, y), r, color, thickness)
        elif shape_type == 'rect':
            w = random.randint(20, 80)
            h = random.randint(20, 80)
            cv2.rectangle(image, (x, y), (x+w, y+h), color, thickness)
        elif shape_type == 'ellipse':
            axes = (random.randint(10, 50), random.randint(10, 50))
            angle = random.randint(0, 180)
            cv2.ellipse(image, (x, y), axes, angle, 0, 360, color, thickness)
        elif shape_type == 'line':
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            cv2.line(image, (x, y), (x2, y2), color, thickness)
            
    return image

def binarize_image(image):
    """
    Binarização Defensiva conforme documentação:
    Se f(x,y) < 127 -> f'(x,y) = 0
    Senão -> f'(x,y) = 1
    """
    binary = np.zeros_like(image, dtype=np.uint8)
    # Apenas onde a intensidade é maior ou igual a 127 se torna 1
    binary[image >= 127] = 1
    return binary

class UnionFind:
    """
    Estrutura de dados para gerenciar as equivalências entre rótulos.
    """
    def __init__(self):
        self.parent = {}
        
    def add(self, label):
        if label not in self.parent:
            self.parent[label] = label
            
    def find(self, label):
        # Encontra a raiz e faz path compression para otimização
        if self.parent[label] == label:
            return label
        self.parent[label] = self.find(self.parent[label])
        return self.parent[label]
        
    def union(self, label1, label2):
        root1 = self.find(label1)
        root2 = self.find(label2)
        
        if root1 != root2:
            # Une apontando sempre para a menor raiz
            if root1 < root2:
                self.parent[root2] = root1
            else:
                self.parent[root1] = root2

def two_pass_labeling(binary_matrix):
    """
    Implementação do Algoritmo Two-Pass com 8-conectividade.
    """
    height, width = binary_matrix.shape
    # Matriz de Rótulos inicializada com zeros, tipo int32 para evitar overflow
    labels = np.zeros((height, width), dtype=np.int32)
    uf = UnionFind()
    current_label = 1
    
    # Primeira Varredura
    for y in range(height):
        for x in range(width):
            p = binary_matrix[y, x]
            if p == 0:
                continue
                
            # Verifica vizinhos processados (8-conectividade)
            neighbors = []
            if y > 0 and x > 0 and labels[y-1, x-1] > 0: # NW
                neighbors.append(labels[y-1, x-1])
            if y > 0 and labels[y-1, x] > 0: # N
                neighbors.append(labels[y-1, x])
            if y > 0 and x < width - 1 and labels[y-1, x+1] > 0: # NE
                neighbors.append(labels[y-1, x+1])
            if x > 0 and labels[y, x-1] > 0: # W
                neighbors.append(labels[y, x-1])
                
            if not neighbors:
                # Caso A: Novo rótulo
                labels[y, x] = current_label
                uf.add(current_label)
                current_label += 1
            else:
                unique_neighbors = list(set(neighbors))
                if len(unique_neighbors) == 1:
                    # Caso B e C: Propagação Simples ou Colisão Idêntica
                    labels[y, x] = unique_neighbors[0]
                else:
                    # Caso D: Colisão de Equivalência
                    min_label = min(unique_neighbors)
                    labels[y, x] = min_label
                    # Registra a equivalência unindo todos os vizinhos
                    for n in unique_neighbors:
                        uf.union(min_label, n)
                        
    # Resolução de Equivalências
    flattened_map = {}
    for lbl in uf.parent.keys():
        flattened_map[lbl] = uf.find(lbl)
        
# Segunda Varredura
    for y in range(height):
        for x in range(width):
            if labels[y, x] > 0:
                # Substitui pelo rótulo definitivo
                labels[y, x] = flattened_map[labels[y, x]]
                
    return labels

def colorize_labels(labels):
    """
    Pinta cada componente conectada com uma cor única e aleatória
    para que possamos verificar visualmente o resultado.
    """
    height, width = labels.shape
    colored = np.zeros((height, width, 3), dtype=np.uint8)
    
    unique_labels = np.unique(labels)
    # Dicionário de cores, onde a chave 0 (fundo) é preto.
    color_map = {0: (0, 0, 0)} 
    
    for lbl in unique_labels:
        if lbl != 0:
            # Cor aleatória
            color_map[lbl] = (random.randint(50, 255), 
                              random.randint(50, 255), 
                              random.randint(50, 255))
                              
    for y in range(height):
        for x in range(width):
            colored[y, x] = color_map[labels[y, x]]
            
    return colored

if __name__ == '__main__':
    print("-> Gerando imagem aleatoria de teste...")
    image = generate_random_image(600, 400)
    cv2.imwrite("01_imagem_original.png", image)
    print("Salvo: 01_imagem_original.png")
    
    print("-> Aplicando binarizacao defensiva...")
    binary = binarize_image(image)
    binary_vis = (binary * 255).astype(np.uint8) # Multiplicar por 255 pra podermos enxergar a imagem salva
    cv2.imwrite("02_imagem_binarizada.png", binary_vis)
    print("Salvo: 02_imagem_binarizada.png")
    
    print("-> Iniciando rotulacao Two-Pass (isso pode demorar uns segundinhos)...")
    labels = two_pass_labeling(binary)
    num_components = len(np.unique(labels)) - 1 # descontando o background (0)
    print(f"-> SUCESSO! Componentes conectadas independentes encontradas: {num_components}")
    
    print("-> Colorizando resultados...")
    colored = colorize_labels(labels)
    cv2.imwrite("03_componentes_coloridas.png", colored)
    print("Salvo: 03_componentes_coloridas.png")
    
    print("\nProcesso finalizado. Voce pode checar as tres imagens geradas na pasta!")
