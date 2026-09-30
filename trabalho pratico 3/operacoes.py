import numpy as np
import cv2
import math
import time

def generate_test_images(width=300, height=300):
    """Gera imagens de mesmo tamanho para servir de cobaia"""
    # Imagem 1: Gradiente horizontal com um círculo branco no centro
    img1 = np.zeros((height, width), dtype=np.uint8)
    for i in range(width):
        img1[:, i] = int((i / width) * 255)
    cv2.circle(img1, (width//2, height//2), min(width, height)//3, 255, -1)
    
    # Imagem 2: Tabuleiro de xadrez com um quadrado preto no centro
    img2 = np.zeros((height, width), dtype=np.uint8)
    square_size = max(width//10, 10)
    for y in range(height):
        for x in range(width):
            if (x // square_size) % 2 == (y // square_size) % 2:
                img2[y, x] = 127
            else:
                img2[y, x] = 200
    cv2.rectangle(img2, (width//4, height//4), (width*3//4, height*3//4), 0, -1)
    
    return img1, img2

def add_images(img1, img2):
    """
    Soma as duas imagens.
    A equação a aplicar matricialmente é gs = fix((g1 + g2) / 2).
    """
    if img1.shape != img2.shape:
        raise ValueError("Imagens precisam ter o mesmo tamanho")
        
    # Converter para int32
    soma = img1.astype(np.int32) + img2.astype(np.int32)
    # Aplicar gs = trunc((g1 + g2) / 2)
    gs = np.trunc(soma / 2.0)
    return gs.astype(np.uint8)

def subtract_images(img1, img2):
    """
    Subtrai as duas imagens usando diferença absoluta.
    d(x,y) = |f(x,y) - g(x,y)|
    """
    if img1.shape != img2.shape:
        raise ValueError("Imagens precisam ter o mesmo tamanho")
        
    # Converter para float ou int32
    diff = img1.astype(np.float32) - img2.astype(np.float32)
    # Pega o valor absoluto
    abs_diff = np.abs(diff)
    return abs_diff.astype(np.uint8)

def get_pixel_bilinear(image, x_f, y_f):
    """
    Determina a intensidade usando Interpolação Bilinear (trabalho prático 1)
    """
    height, width = image.shape
    
    x1 = int(np.floor(x_f))
    y1 = int(np.floor(y_f))
    
    x2 = min(x1 + 1, width - 1)
    y2 = min(y1 + 1, height - 1)
    
    x1 = max(0, x1)
    y1 = max(0, y1)
    
    dx = x_f - x1
    dy = y_f - y1
    
    p11 = float(image[y1, x1])
    p21 = float(image[y1, x2])
    p12 = float(image[y2, x1])
    p22 = float(image[y2, x2])
    
    val = (p11 * (1 - dx) * (1 - dy) +
           p21 * dx * (1 - dy) +
           p12 * (1 - dx) * dy +
           p22 * dx * dy)
           
    return np.clip(np.round(val), 0, 255)

def rotate_image(image, angle_degrees):
    """
    Rotaciona a imagem através da estratégia de Mapeamento Inverso,
    usando a inversão matricial rigorosa e interpolação.
    """
    height, width = image.shape
    
    theta = math.radians(angle_degrees)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    
    # 1. Encontrar o tamanho da nova imagem para não cortar as quinas
    cx_in = width / 2.0
    cy_in = height / 2.0
    
    # resolver pontas
    # [ nx ] = [ cos  -sin ] [ x ]
    # [ ny ]   [ sin   cos ] [ y ]
    corners = [
        (-cx_in, -cy_in),
        (cx_in, -cy_in),
        (-cx_in, cy_in),
        (cx_in, cy_in)
    ]
    
    new_corners = []
    for cx, cy in corners:
        nx = cx * cos_t - cy * sin_t
        ny = cx * sin_t + cy * cos_t
        new_corners.append((nx, ny))
        
    min_x = min([p[0] for p in new_corners])
    max_x = max([p[0] for p in new_corners])
    min_y = min([p[1] for p in new_corners])
    max_y = max([p[1] for p in new_corners])
    
    new_width = int(math.ceil(max_x - min_x))
    new_height = int(math.ceil(max_y - min_y))
    
    cx_out = new_width / 2.0
    cy_out = new_height / 2.0
    
    rotated = np.zeros((new_height, new_width), dtype=np.uint8)
    
    # formula da Rotação Inversa (T^-1):
    # [ x_0 ] = [ cos   sin ] [ x_d ]
    # [ y_0 ]   [-sin   cos ] [ y_d ]
    
    for y_d in range(new_height):
        for x_d in range(new_width):
            # rotacionar ao redor do centro
            nx = x_d - cx_out
            ny = y_d - cy_out
            
            # encontrando valor novo com a formula da Rotação Inversa
            x_0 = nx * cos_t + ny * sin_t
            y_0 = -nx * sin_t + ny * cos_t
            
            # convertendo pra matriz original (com centro no meio da imagem)
            x_0 += cx_in
            y_0 += cy_in
            
            # se a posicao nova equivale a uma antiga posicao da imagem original, pega o valor do pixel
            if 0 <= x_0 <= width - 1 and 0 <= y_0 <= height - 1:
                # Usa Interpolação para chutar o valor
                pixel_val = get_pixel_bilinear(image, x_0, y_0)
                rotated[y_d, x_d] = int(pixel_val)
                
    return rotated

if __name__ == '__main__':
    print("-> Gerando cobaias (400x400)...")
    img1, img2 = generate_test_images(400, 400)
    cv2.imwrite("01_cobaia_A.png", img1)
    cv2.imwrite("02_cobaia_B.png", img2)
    print("Salvo: 01_cobaia_A.png")
    print("Salvo: 02_cobaia_B.png")
    
    print("\n-> Aplicando: Adicao (Media Aritmetica)...")
    t0 = time.time()
    img_add = add_images(img1, img2)
    print(f"Feito em {time.time()-t0:.4f}s")
    cv2.imwrite("03_adicao.png", img_add)
    print("Salvo: 03_adicao.png")
    
    print("\n-> Aplicando: Subtracao (Diferenca Absoluta)...")
    t0 = time.time()
    img_sub = subtract_images(img1, img2)
    print(f"Feito em {time.time()-t0:.4f}s")
    cv2.imwrite("04_subtracao.png", img_sub)
    print("Salvo: 04_subtracao.png")
    
    print("\n-> Aplicando: Rotacao Geometrica (45 graus com Inversao Matricial e Bilinear)...")
    print("Processando Mapeamento Inverso, isso deve demorar alguns segundos por ser python nativo sem Cython/Vetorizacao...")
    t0 = time.time()
    img_rot = rotate_image(img1, 90) # Vamos rotacionar a primeira cobaia
    print(f"Feito em {time.time()-t0:.4f}s")
    cv2.imwrite("05_rotacao.png", img_rot)
    print("Salvo: 05_rotacao.png")
    
    print("\n[SUCESSO] Operacoes concluidas com maestria!")
