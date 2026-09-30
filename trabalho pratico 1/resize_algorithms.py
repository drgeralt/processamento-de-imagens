import cv2
import numpy as np
import time
import os
import glob

def resize_nearest_neighbor(image, new_width, new_height):
    height, width = image.shape[:2]
    if len(image.shape) == 2:
        resized = np.zeros((new_height, new_width), dtype=image.dtype)
    else:
        channels = image.shape[2]
        resized = np.zeros((new_height, new_width, channels), dtype=image.dtype)
        
    scale_x = width / new_width
    scale_y = height / new_height
    
    for y_dst in range(new_height):
        for x_dst in range(new_width):
            x_src = x_dst * scale_x
            y_src = y_dst * scale_y
            
            x_nearest = int(round(x_src))
            y_nearest = int(round(y_src))
            
            # Limite de borda (replicação)
            x_nearest = min(x_nearest, width - 1)
            y_nearest = min(y_nearest, height - 1)
            
            resized[y_dst, x_dst] = image[y_nearest, x_nearest]
                
    return resized

def resize_bilinear(image, new_width, new_height):
    height, width = image.shape[:2]
    if len(image.shape) == 2:
        resized = np.zeros((new_height, new_width), dtype=np.float32)
    else:
        channels = image.shape[2]
        resized = np.zeros((new_height, new_width, channels), dtype=np.float32)
        
    scale_x = width / new_width
    scale_y = height / new_height
    
    for y_dst in range(new_height):
        for x_dst in range(new_width):
            x_src = x_dst * scale_x
            y_src = y_dst * scale_y
            
            x1 = int(np.floor(x_src))
            y1 = int(np.floor(y_src))
            
            # Limite de borda
            x2 = min(x1 + 1, width - 1)
            y2 = min(y1 + 1, height - 1)
            
            dx = x_src - x1
            dy = y_src - y1
            
            # Convertendo os pixels para float para evitar problemas de overflow no numpy
            p11 = image[y1, x1].astype(np.float32)
            p21 = image[y1, x2].astype(np.float32)
            p12 = image[y2, x1].astype(np.float32)
            p22 = image[y2, x2].astype(np.float32)
            
            val = p11 * (1 - dx) * (1 - dy) + \
                  p21 * dx * (1 - dy) + \
                  p12 * (1 - dx) * dy + \
                  p22 * dx * dy
                  
            resized[y_dst, x_dst] = val
                
    return np.clip(np.round(resized), 0, 255).astype(image.dtype)

def calculate_mse(imageA, imageB):
    # MSE entre as duas matrizes de imagem (verificar erro de conversao)
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1] * (imageA.shape[2] if len(imageA.shape) > 2 else 1))
    return err

if __name__ == '__main__':
    # Puxa qualquer imagem do diretório atual para teste (jpeg, png, jpg)
    images = glob.glob("*.jpeg") + glob.glob("*.png") + glob.glob("*.jpg")
    if not images:
        print("Nenhuma imagem encontrada para teste.")
        exit(1)
        
    img_path = images[0]
    print(f"Usando a imagem: {img_path}")
    image = cv2.imread(img_path)
    
    if image is None:
        print("Erro ao ler a imagem com OpenCV.")
        exit(1)
        
    # Tamanho original reduzido com cv2 para diminuir o tempo de benchmark, caso a imagem seja muito grande
    height, width = image.shape[:2]
    #if height > 500 or width > 500:
    #    print("Imagem muito grande, reduzindo um pouco previamente pra o benchmark não demorar horas...")
    #    image = cv2.resize(image, (300, int(300 * height / width)))
    #    height, width = image.shape[:2]
        
    new_width = int(width * 2)
    new_height = int(height * 2)
    
    print(f"Tamanho base: {width}x{height}")
    print(f"Novo tamanho (redimensionado): {new_width}x{new_height}\n")
    
    print("--- Vizinho Mais Próximo ---")
    start = time.time()
    img_nn_custom = resize_nearest_neighbor(image, new_width, new_height)
    end = time.time()
    time_nn_custom = end - start
    print(f"Implementação Própria : {time_nn_custom:.4f} segundos")
    
    start = time.time()
    img_nn_cv2 = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
    end = time.time()
    time_nn_cv2 = end - start
    print(f"OpenCV                : {time_nn_cv2:.4f} segundos")
    
    mse_nn = calculate_mse(img_nn_custom, img_nn_cv2)
    print(f"MSE Vizinho Mais Próximo: {mse_nn:.6f}\n")
    
    print("--- Interpolação Bilinear ---")
    start = time.time()
    img_bl_custom = resize_bilinear(image, new_width, new_height)
    end = time.time()
    time_bl_custom = end - start
    print(f"Implementação Própria : {time_bl_custom:.4f} segundos")
    
    start = time.time()
    img_bl_cv2 = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    end = time.time()
    time_bl_cv2 = end - start
    print(f"OpenCV                : {time_bl_cv2:.4f} segundos")
    
    mse_bl = calculate_mse(img_bl_custom, img_bl_cv2)
    print(f"MSE Bilinear: {mse_bl:.6f}\n")

    cv2.imwrite("Imagem_base.jpg", image)
    cv2.imwrite("resultado_nearest_neighbor_custom.jpg", img_nn_custom)
    cv2.imwrite("resultado_bilinear_custom.jpg", img_bl_custom)
    cv2.imwrite("resultado_nearest_neighbor_opencv.jpg", img_nn_cv2)
    cv2.imwrite("resultado_bilinear_opencv.jpg", img_bl_cv2)
    print("Imagens redimensionadas (nossas e do OpenCV) salvas no diretório atual.")
