import numpy as np
import cv2
import math

def normalize(image):
    """
    Pré-processamento: Converta a matriz da imagem de entrada para o tipo de ponto
    flutuante e divida todos os píxeis por 255.0. Mapeando para [0, 1].
    """
    return image.astype(np.float32) / 255.0

def denormalize(image_norm):
    """
    Pós-processamento: Multiplique a matriz resultante por 255.0 e converta
    o tipo de dado de volta para inteiro de 8 bits sem sinal (uint8).
    """
    # clippando pra respeitar entre 0 e 255, caso algum valor tenha extrapolado
    image_scaled = np.clip(image_norm * 255.0, 0, 255)
    return image_scaled.astype(np.uint8)

def transform_negative(image):
    """
    Transformação Negativa
    Fórmula normalizada: s = 1 - r
    """
    r = normalize(image)
    s = 1.0 - r
    return denormalize(s)

def transform_logarithmic(image, c=1.0):
    """
    Transformação Logarítmica
    Fórmula: s = c * log(1 + r)
    """
    r = normalize(image)
    s = c * np.log(1.0 + r)
    return denormalize(s)

def transform_gamma(image, gamma, c=1.0):
    """
    Transformação de Potência (Gama / Power-Law)
    Fórmula: s = c * (r ** gamma)
    """
    r = normalize(image)
    s = c * (r ** gamma)
    return denormalize(s)

if __name__ == '__main__':
    print("-> Carregando imagens de teste...")
    img_pneumonia = cv2.imread("m2400651-pneumonia.jpg", cv2.IMREAD_GRAYSCALE)
    # 3 canais pra aceitar cores
    img_noite = cv2.imread("ricardo-wu-C_jHDwWSgu8-unsplash.jpg", cv2.IMREAD_COLOR)
    
    if img_pneumonia is None or img_noite is None:
        print("Erro: Nao foi possivel ler as imagens originais na pasta.")
        exit(1)
        
    print("-> Aplicando Transformacao Negativa no raio x...")
    neg_pneumonia = transform_negative(img_pneumonia)
    cv2.imwrite("01_pneumonia_negativo.jpg", neg_pneumonia)
    print("   Salvo: 01_pneumonia_negativo.jpg")
    
    print("-> Aplicando Transformacao Logaritmica na foto da cidade...")
    c_log = 5.0 / np.log(2.0)
    log_noite = transform_logarithmic(img_noite, c=c_log)
    cv2.imwrite("02_noite_logaritmica.jpg", log_noite)
    print("   Salvo: 02_noite_logaritmica.jpg")
    
    print("-> Aplicando Transformacao de Gama na foto da cidade...")
    # Clarear imagem escura usando gama < 1
    gamma_clara = transform_gamma(img_noite, gamma=0.4, c=1.0)
    # Escurecer usando gama > 1
    gamma_escura = transform_gamma(img_noite, gamma=2.5, c=1.0) 
    
    cv2.imwrite("03_noite_gama_0.4_clareada.jpg", gamma_clara)
    print("   Salvo: 03_noite_gama_0.4_clareada.jpg")
    cv2.imwrite("04_noite_gama_2.5_escurecida.jpg", gamma_escura)
    print("   Salvo: 04_noite_gama_2.5_escurecida.jpg")
    
    print("\n[SUCESSO] Todo o pipeline de normalizacao e transformacao operou perfeitamente!")
