import numpy as np
import cv2
import os

def convert_to_grayscale(image):
    """
    Converte a imagem para tons de cinza se for colorida (3 canais).
    Mantida como funcao utilitaria.
    """
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def stretch_contrast(image):
    """
    Alargamento de Contraste (Contrast Stretching).
    Expande a faixa dinamica da imagem para usar todo o espectro [0, 255].
    Suporta imagens em escala de cinza (1 canal / 2D) e coloridas (3 canais / BGR).
    G(F(i,j)) = (F(i,j) - c) * (255 / (d - c))
    """
    if len(image.shape) == 2:
        c = np.min(image)
        d = np.max(image)
        
        # Validacao de seguranca para divisoes por zero em imagens de 1 tom so
        if c == d:
            return image.copy()
            
        img_float = image.astype(np.float32)
        stretched = (img_float - c) * (255.0 / (d - c))
        return np.clip(np.round(stretched), 0, 255).astype(np.uint8)
    
    # Processamento para imagem colorida multicanal (BGR)
    stretched = np.zeros_like(image)
    for ch in range(image.shape[2]):
        channel = image[:, :, ch]
        c = np.min(channel)
        d = np.max(channel)
        
        if c == d:
            stretched[:, :, ch] = channel
        else:
            ch_float = channel.astype(np.float32)
            stretched_ch = (ch_float - c) * (255.0 / (d - c))
            stretched[:, :, ch] = np.clip(np.round(stretched_ch), 0, 255).astype(np.uint8)
            
    return stretched

def _equalize_channel(channel):
    """
    Equaliza um canal individual (2D) utilizando Funcao de Distribuicao
    Acumulada (CDF) e Look-up Table (LUT) vetorizada via Advanced Indexing.
    """
    total_pixels = channel.size
    
    # 1. Montagem do Histograma e Probabilidade Normalizada (p_r)
    frequencies = np.bincount(channel.ravel(), minlength=256)
    p_r = frequencies / total_pixels
    
    # 2. Calculo da Distribuicao Acumulada (CDF)
    cdf = np.cumsum(p_r)
    
    # 3. Criacao da Look-up Table (LUT)
    LUT = np.round(255.0 * cdf).astype(np.uint8)
    
    # 4. Transformacao Vetorizada da Imagem via NumPy
    return LUT[channel]

def equalize_histogram(image, method="hsv"):
    """
    Equaliza o histograma utilizando Funcao de Distribuicao Acumulada (CDF)
    e uma Look-up Table rigorosamente vetorizada (Advanced Indexing).
    
    Suporta:
    - Imagens em tons de cinza (2D).
    - Imagens coloridas (3D / BGR):
        - method='hsv': Converte para HSV e equaliza o canal V (brilho/intensidade),
          preservando matiz (H) e saturacao (S) para evitar distorcoes de cor (recomendado).
        - method='bgr' ou 'channels': Equaliza cada canal B, G, R independentemente.
        - method='ycrcb': Converte para YCrCb e equaliza o canal Y (luminancia).
    """
    if len(image.shape) == 2:
        return _equalize_channel(image)
        
    if method == "hsv":
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = _equalize_channel(hsv[:, :, 2])
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    elif method in ("bgr", "rgb", "channels"):
        equalized = np.zeros_like(image)
        for ch in range(image.shape[2]):
            equalized[:, :, ch] = _equalize_channel(image[:, :, ch])
        return equalized
    elif method == "ycrcb":
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        ycrcb[:, :, 0] = _equalize_channel(ycrcb[:, :, 0])
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    else:
        raise ValueError(f"Metodo desconhecido: '{method}'. Use 'hsv', 'bgr' ou 'ycrcb'.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_filename = "Tip901-Before-1-scaled.jpg"
    img_path = os.path.join(script_dir, img_filename)
    if not os.path.exists(img_path):
        img_path = img_filename
        
    print(f"-> Carregando imagem cobaia fornecida: {img_path}")
    image = cv2.imread(img_path)
    
    if image is None:
        print("Erro: Falha ao carregar a imagem na pasta.")
        exit(1)
        
    is_color = len(image.shape) == 3
    print(f"   Dimensoes da imagem: {image.shape} ({'Colorida (3 canais)' if is_color else 'Escala de Cinza (1 canal)'})")
    
    # 1. Salvar imagem original de referencia
    orig_path = os.path.join(script_dir, "01_original.jpg")
    cv2.imwrite(orig_path, image)
    print(f"\n-> Salvando copia da imagem original...")
    print(f"   Salvo: {orig_path}")
    
    if is_color:
        gray_path = os.path.join(script_dir, "01_original_cinza.jpg")
        cv2.imwrite(gray_path, convert_to_grayscale(image))
        print(f"   Salvo (copia em escala de cinza): {gray_path}")
        
    # 2. Alargamento de Contraste (Contrast Stretching)
    print("\n-> Aplicando Alargamento de Contraste (Contrast Stretching)...")
    img_stretched = stretch_contrast(image)
    stretched_path = os.path.join(script_dir, "02_alargamento_contraste.jpg")
    cv2.imwrite(stretched_path, img_stretched)
    print(f"   Salvo: {stretched_path}")
    
    # 3. Equalizacao Global de Histograma
    print("\n-> Aplicando Equalizacao Global de Histograma (preservando fidelidade cromatica via HSV)...")
    img_equalized = equalize_histogram(image, method="hsv")
    equalized_path = os.path.join(script_dir, "03_equalizacao_histograma.jpg")
    cv2.imwrite(equalized_path, img_equalized)
    print(f"   Salvo: {equalized_path}")
    
    if is_color:
        print("\n-> Aplicando tambem Equalizacao por Canais Independentes (BGR)...")
        img_equalized_bgr = equalize_histogram(image, method="bgr")
        equalized_bgr_path = os.path.join(script_dir, "03_equalizacao_histograma_bgr.jpg")
        cv2.imwrite(equalized_bgr_path, img_equalized_bgr)
        print(f"   Salvo: {equalized_bgr_path}")
        
    print("\n[SUCESSO] Tarefas do Trabalho Pratico 5 concluidas com suporte a cores e escala de cinza!")
