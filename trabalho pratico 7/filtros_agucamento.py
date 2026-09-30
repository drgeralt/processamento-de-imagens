import numpy as np
import cv2
import os
import sys
import glob
import time

def convolve2d_vectorized(image, kernel):
    """
    Aplica convolução/correlação espacial 2D vetorizada via fatiamento (slicing)
    com tratamento de bordas por espelhamento simétrico (symmetric padding).

    Suporta imagens em escala de cinza (2D) e imagens coloridas (3D / BGR).
    """
    kh, kw = kernel.shape
    pad_h = (kh - 1) // 2
    pad_w = (kw - 1) // 2
    H, W = image.shape[:2]

    # Tratamento de bordas com espelhamento simétrico
    if len(image.shape) == 2:
        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='symmetric')
    else:
        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w), (0, 0)), mode='symmetric')

    img_float = padded.astype(np.float32)
    output = np.zeros(image.shape, dtype=np.float32)

    # Itera sobre os coeficientes da máscara aplicando fatiamento contínuo
    for i in range(kh):
        for j in range(kw):
            w = kernel[i, j]
            if w != 0.0:
                output += img_float[i:i + H, j:j + W] * w

    return output

def min_max_scale(image_float):
    """
    Reescalonamento Numérico (Min-Max Scaling) para a gama [0, 255].
    I_out = 255 * (I_in - min(I_in)) / (max(I_in) - min(I_in))
    
    Permite visualizar saídas brutas com valores negativos ou superiores a 255.
    """
    val_min = np.min(image_float)
    val_max = np.max(image_float)

    if val_max == val_min:
        return np.zeros_like(image_float, dtype=np.uint8)

    scaled = 255.0 * (image_float - val_min) / (val_max - val_min)
    return np.clip(np.round(scaled), 0, 255).astype(np.uint8)

def apply_laplacian(image, mask_type='b'):
    """
    Aplica o Filtro Laplaciano (Derivada de 2ª Ordem) e recupera o fundo
    para gerar a imagem aguçada (sharpened).

    Máscaras suportadas:
    - 'a': Centro -4, vizinhos ortogonais 1 (c = -1)
    - 'b': Centro -8, vizinhos ortogonais e diagonais 1 (c = -1)
    - 'c': Centro 4, vizinhos ortogonais -1 (c = 1)
    - 'd': Centro 8, vizinhos ortogonais e diagonais -1 (c = 1)

    Retorna:
    --------
    laplacian_raw : np.ndarray (float32)
        Laplaciano bruto (contém valores negativos e positivos).
    laplacian_scaled : np.ndarray (uint8)
        Laplaciano isolado reescalonado para [0, 255].
    sharpened : np.ndarray (uint8)
        Imagem aguçada final com recuperação de fundo g(x,y) = f(x,y) + c * Laplaciano.
    """
    masks = {
        'a': (
            np.array([
                [ 0,  1,  0],
                [ 1, -4,  1],
                [ 0,  1,  0]
            ], dtype=np.float32),
            -1.0
        ),
        'b': (
            np.array([
                [ 1,  1,  1],
                [ 1, -8,  1],
                [ 1,  1,  1]
            ], dtype=np.float32),
            -1.0
        ),
        'c': (
            np.array([
                [ 0, -1,  0],
                [-1,  4, -1],
                [ 0, -1,  0]
            ], dtype=np.float32),
            1.0
        ),
        'd': (
            np.array([
                [-1, -1, -1],
                [-1,  8, -1],
                [-1, -1, -1]
            ], dtype=np.float32),
            1.0
        )
    }

    if mask_type not in masks:
        raise ValueError(f"Máscara inválida '{mask_type}'. Opções: 'a', 'b', 'c', 'd'.")

    kernel, c = masks[mask_type]

    # 1. Laplaciano em ponto flutuante
    laplacian_raw = convolve2d_vectorized(image, kernel)

    # 2. Laplaciano isolado com Min-Max Scaling [0, 255]
    laplacian_scaled = min_max_scale(laplacian_raw)

    # 3. Recuperação do Fundo: g(x,y) = f(x,y) + c * [Laplaciano]
    img_float = image.astype(np.float32)
    g = img_float + c * laplacian_raw
    sharpened = np.clip(np.round(g), 0, 255).astype(np.uint8)

    return laplacian_raw, laplacian_scaled, sharpened

def apply_sobel(image):
    """
    Filtro Gradiente de Sobel (Derivada de 1ª Ordem).
    Utiliza as matrizes ortogonais h1 (variações verticais) e h2 (variações horizontais).
    Calcula a magnitude exata via Distância Euclidiana M(x,y) = sqrt(gx^2 + gy^2).

    Retorna:
    --------
    magnitude_scaled : np.ndarray (uint8)
        Magnitude do gradiente reescalonada via Min-Max para [0, 255].
    sharpened_sobel : np.ndarray (uint8)
        Imagem original realçada com a magnitude de Sobel: f(x,y) + M(x,y).
    gx_scaled : np.ndarray (uint8)
        Gradiente horizontal reescalonado.
    gy_scaled : np.ndarray (uint8)
        Gradiente vertical reescalonado.
    """
    # h1 para variações verticais (derivada em Y)
    h1 = np.array([
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ], dtype=np.float32)

    # h2 para variações horizontais (derivada em X)
    h2 = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float32)

    # Convoluções ortogonais
    gy = convolve2d_vectorized(image, h1)
    gx = convolve2d_vectorized(image, h2)

    # Magnitude Exata: Distância Euclidiana rigorosa via NumPy
    magnitude = np.sqrt(gx ** 2 + gy ** 2)

    # Reescalonamento Min-Max para visualização
    magnitude_scaled = min_max_scale(magnitude)
    gx_scaled = min_max_scale(gx)
    gy_scaled = min_max_scale(gy)

    # Aguçamento combinando a imagem original com as bordas do gradiente
    img_float = image.astype(np.float32)
    sharpened_sobel = np.clip(np.round(img_float + magnitude), 0, 255).astype(np.uint8)

    return magnitude_scaled, sharpened_sobel, gx_scaled, gy_scaled


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Localizar imagem cobaia
    img_path = None
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        img_path = sys.argv[1]
    else:
        candidates = [
            os.path.join(script_dir, "cobaia.jpg"),
            os.path.join(script_dir, "..", "trabalho pratico 6", "cobaia.jpg"),
            os.path.join(script_dir, "..", "trabalho pratico 5", "02_alargamento_contraste.jpg")
        ] + glob.glob(os.path.join(script_dir, "*.jpg")) + glob.glob(os.path.join(script_dir, "*.png"))

        for cand in candidates:
            base = os.path.basename(cand)
            if not base.startswith("0") and os.path.exists(cand):
                img_path = os.path.abspath(cand)
                break

    if img_path is None or not os.path.exists(img_path):
        print("Erro: Nenhuma imagem cobaia encontrada para o Trabalho Pratico 7.")
        exit(1)

    print(f"-> Carregando imagem cobaia: {img_path}")
    image = cv2.imread(img_path)

    if image is None:
        print("Erro ao carregar a imagem com OpenCV.")
        exit(1)

    is_color = len(image.shape) == 3
    print(f"   Dimensões: {image.shape[1]}x{image.shape[0]} | {'Colorida (3 canais)' if is_color else 'Escala de Cinza (1 canal)'}")

    # Salvar cópia da imagem original
    orig_output = os.path.join(script_dir, "01_imagem_original.jpg")
    cv2.imwrite(orig_output, image)
    print(f"   Salvo: {orig_output}")

    print("\n" + "=" * 68)
    print("  PARTE 1: FILTRO LAPLACIANO (DERIVADA DE 2ª ORDEM)")
    print("=" * 68)

    masks_info = [
        ('a', "Centro -4, Vizinhos Ortogonais 1 (c = -1)"),
        ('b', "Centro -8, Vizinhos Ortogonais e Diagonais 1 (c = -1)"),
        ('c', "Centro  4, Vizinhos Ortogonais -1 (c = 1)"),
        ('d', "Centro  8, Vizinhos Ortogonais e Diagonais -1 (c = 1)")
    ]

    out_counter = 2
    for mask_key, mask_desc in masks_info:
        print(f"\n-> Aplicando Máscara ({mask_key}): {mask_desc}...")
        t0 = time.perf_counter()
        raw_lap, lap_scaled, sharpened = apply_laplacian(image, mask_type=mask_key)
        dt = time.perf_counter() - t0

        file_lap = os.path.join(script_dir, f"0{out_counter}_laplaciano_isolado_mascara_{mask_key}.jpg")
        cv2.imwrite(file_lap, lap_scaled)
        print(f"   [Min-Max Scaled] Salvo: {file_lap}")
        out_counter += 1

        file_sharp = os.path.join(script_dir, f"{out_counter:02d}_laplaciano_realcado_mascara_{mask_key}.jpg")
        cv2.imwrite(file_sharp, sharpened)
        print(f"   [Realçado g=f+c*Lap] Salvo: {file_sharp} (Tempo: {dt:.4f}s)")
        out_counter += 1

    print("\n" + "=" * 68)
    print("  PARTE 2: GRADIENTE DE SOBEL (DERIVADA DE 1ª ORDEM)")
    print("=" * 68)

    print("\n-> Calculando Convoluções Ortogonais (h1 e h2) e Magnitude Euclidiana M(x,y)...")
    t0 = time.perf_counter()
    mag_scaled, sharp_sobel, gx_scaled, gy_scaled = apply_sobel(image)
    dt_sobel = time.perf_counter() - t0

    file_mag = os.path.join(script_dir, f"{out_counter:02d}_sobel_magnitude.jpg")
    cv2.imwrite(file_mag, mag_scaled)
    print(f"   [Magnitude Exata] Salvo: {file_mag}")
    out_counter += 1

    file_sharp_sobel = os.path.join(script_dir, f"{out_counter:02d}_sobel_realcado.jpg")
    cv2.imwrite(file_sharp_sobel, sharp_sobel)
    print(f"   [Aguçamento com Sobel] Salvo: {file_sharp_sobel}")
    out_counter += 1

    file_gx = os.path.join(script_dir, f"{out_counter:02d}_sobel_gx_horizontal.jpg")
    cv2.imwrite(file_gx, gx_scaled)
    print(f"   [Gradiente Horizontal] Salvo: {file_gx}")
    out_counter += 1

    file_gy = os.path.join(script_dir, f"{out_counter:02d}_sobel_gy_vertical.jpg")
    cv2.imwrite(file_gy, gy_scaled)
    print(f"   [Gradiente Vertical] Salvo: {file_gy} (Tempo total Sobel: {dt_sobel:.4f}s)")

    print("\n" + "=" * 68)
    print("[SUCESSO] Tarefas do Trabalho Prático 7 concluídas com êxito!")
    print("=" * 68)
