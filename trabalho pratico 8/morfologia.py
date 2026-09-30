import numpy as np
import cv2
import os
import sys
import glob
import time

def create_structuring_element(shape="rect", ksize=3):
    """
    Cria um elemento estruturante dinâmico (matriz binária 0 e 1) de dimensão ímpar.

    Parâmetros:
    -----------
    shape : str
        Formato do elemento:
        - 'rect': Quadrado preenchido de 1s (padrão).
        - 'cross': Cruz centrada de 1s.
        - 'ellipse': Disco/elipse de 1s.
    ksize : int
        Tamanho ímpar da matriz (ex: 3, 5, 7).

    Retorna:
    --------
    np.ndarray
        Matriz binária 2D uint8 contendo apenas valores 0 e 1.
    """
    if not isinstance(ksize, int) or ksize < 1 or ksize % 2 == 0:
        raise ValueError(f"ksize deve ser um inteiro ímpar positivo. Recebido: {ksize}")

    if shape == "rect":
        return np.ones((ksize, ksize), dtype=np.uint8)
    elif shape == "cross":
        B = np.zeros((ksize, ksize), dtype=np.uint8)
        center = ksize // 2
        B[center, :] = 1
        B[:, center] = 1
        return B
    elif shape == "ellipse":
        center = (ksize - 1) / 2.0
        y, x = np.ogrid[:ksize, :ksize]
        dist = ((x - center) ** 2 + (y - center) ** 2)
        radius_sq = (center) ** 2
        return (dist <= radius_sq).astype(np.uint8)
    else:
        raise ValueError(f"Formato desconhecido: '{shape}'. Opções: 'rect', 'cross', 'ellipse'.")

def _validate_structuring_element(B):
    """Valida se o elemento estruturante é uma matriz binária 2D de dimensão ímpar."""
    if B is None:
        return create_structuring_element(shape="rect", ksize=3)
    if not isinstance(B, np.ndarray) or len(B.shape) != 2:
        raise ValueError("O elemento estruturante B deve ser um numpy.ndarray bidimensional.")
    kh, kw = B.shape
    if kh % 2 == 0 or kw % 2 == 0:
        raise ValueError(f"As dimensões do elemento estruturante devem ser ímpares. Recebido: {kh}x{kw}")
    return (B != 0).astype(np.uint8)

def dilate(image, B=None):
    """
    Dilatação Morfológica Vetorizada via Slicing e Stacking (Projeção Temporal com np.max).
    
    Suporta imagens binárias ({0, 1} ou {0, 255}) e imagens em níveis de cinza [0, 255].
    Utiliza padding com 0 para evitar distorções nas bordas.
    """
    B = _validate_structuring_element(B)
    kh, kw = B.shape
    pad_h = (kh - 1) // 2
    pad_w = (kw - 1) // 2
    H, W = image.shape[:2]

    # 1. Padding com 0 (expansão da imagem)
    if len(image.shape) == 2:
        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    else:
        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w), (0, 0)), mode='constant', constant_values=0)

    # 2. Recorte de fatias contínuas onde o elemento estruturante B possui valor 1
    slices = []
    for i in range(kh):
        for j in range(kw):
            if B[i, j] == 1:
                slices.append(padded[i:i + H, j:j + W])

    # 3. Empilhamento em cubo multidimensional e projeção temporal (np.max)
    stack = np.stack(slices, axis=-1)
    return np.max(stack, axis=-1)

def erode(image, B=None, is_binary=False):
    """
    Erosão Morfológica Vetorizada via Slicing e Stacking (Projeção Temporal com np.min).
    
    Suporta imagens binárias e em níveis de cinza.
    Utiliza padding com 1 (se binária {0, 1}) ou 255 (se em cinza / {0, 255}),
    evitando o escurecimento artificial das bordas.
    """
    B = _validate_structuring_element(B)
    kh, kw = B.shape
    pad_h = (kh - 1) // 2
    pad_w = (kw - 1) // 2
    H, W = image.shape[:2]

    # Valor neutro do padding para a erosão:
    # 1 para binário {0, 1}; 255 para tons de cinza ou binário escalado em {0, 255}
    if is_binary and image.max() <= 1:
        pad_val = 1
    else:
        pad_val = 255

    # 1. Padding com valor máximo neutro (1 ou 255)
    if len(image.shape) == 2:
        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=pad_val)
    else:
        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w), (0, 0)), mode='constant', constant_values=pad_val)

    # 2. Recorte de fatias onde B == 1
    slices = []
    for i in range(kh):
        for j in range(kw):
            if B[i, j] == 1:
                slices.append(padded[i:i + H, j:j + W])

    # 3. Empilhamento e projeção temporal (np.min)
    stack = np.stack(slices, axis=-1)
    return np.min(stack, axis=-1)

def morphological_gradient(image, B=None):
    """
    Gradiente Morfológico em Tons de Cinzento: g = (f ⊕ b) - (f ⊖ b)
    
    Calcula a diferença aritmética entre a imagem dilatada e a imagem erodida,
    enfatizando as transições de intensidade (bordas) de forma isotrópica.
    """
    B = _validate_structuring_element(B)
    dilated = dilate(image, B)
    eroded = erode(image, B, is_binary=False)
    
    # Diferença com casting defensivo para evitar underflow em uint8
    gradient = np.clip(dilated.astype(np.int32) - eroded.astype(np.int32), 0, 255).astype(np.uint8)
    return gradient, dilated, eroded


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Localizar imagem cobaia
    img_path = None
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        img_path = sys.argv[1]
    else:
        candidates = [
            os.path.join(script_dir, "cobaia.jpg"),
            os.path.join(script_dir, "..", "trabalho pratico 7", "cobaia.jpg"),
            os.path.join(script_dir, "..", "trabalho pratico 6", "cobaia.jpg"),
            os.path.join(script_dir, "..", "trabalho pratico 5", "02_alargamento_contraste.jpg")
        ] + glob.glob(os.path.join(script_dir, "*.jpg")) + glob.glob(os.path.join(script_dir, "*.png"))

        for cand in candidates:
            base = os.path.basename(cand)
            if not base.startswith("0") and os.path.exists(cand):
                img_path = os.path.abspath(cand)
                break

    if img_path is None or not os.path.exists(img_path):
        print("Erro: Nenhuma imagem cobaia encontrada para o Trabalho Prático 8.")
        exit(1)

    print(f"-> Carregando imagem cobaia: {img_path}")
    image = cv2.imread(img_path)

    if image is None:
        print("Erro ao carregar a imagem com OpenCV.")
        exit(1)

    print(f"   Dimensões originais: {image.shape[1]}x{image.shape[0]} ({image.shape[2]} canais)")

    # 1. Salvar imagem original
    file_orig = os.path.join(script_dir, "01_imagem_original.jpg")
    cv2.imwrite(file_orig, image)
    print(f"   Salvo: {file_orig}")

    # 2. Converter para Tons de Cinza para processamento morfológico
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    file_gray = os.path.join(script_dir, "02_imagem_cinza.jpg")
    cv2.imwrite(file_gray, gray_image)
    print(f"   Salvo: {file_gray}")

    # =========================================================================
    # PARTE 1: MORFOLOGIA EM IMAGENS BINÁRIAS (OPÇÃO 1)
    # =========================================================================
    print("\n" + "=" * 68)
    print("  PARTE 1: MORFOLOGIA EM IMAGENS BINÁRIAS (OPÇÃO 1)")
    print("=" * 68)

    # Binarização com Otsu para obter representação binária automática {0, 255}
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    file_bin = os.path.join(script_dir, "03_imagem_binaria.png")
    cv2.imwrite(file_bin, binary_image)
    print(f"-> Imagem binarizada (Otsu) salva: {file_bin}")

    # Elementos Estruturantes para teste binário
    B_rect3 = create_structuring_element("rect", 3)
    B_cross3 = create_structuring_element("cross", 3)

    # 1.1 Dilatação e Erosão Binária com Elemento Quadrado 3x3
    print("\n-> Aplicando Dilatação Binária (Quadrado 3x3)...")
    t0 = time.perf_counter()
    bin_dilated_rect = dilate(binary_image, B_rect3)
    dt = time.perf_counter() - t0
    file_bin_dil_rect = os.path.join(script_dir, "04_dilatacao_binaria_rect3x3.png")
    cv2.imwrite(file_bin_dil_rect, bin_dilated_rect)
    print(f"   Salvo: {file_bin_dil_rect} (Tempo: {dt:.4f}s)")

    print("-> Aplicando Erosão Binária (Quadrado 3x3)...")
    t0 = time.perf_counter()
    bin_eroded_rect = erode(binary_image, B_rect3, is_binary=True)
    dt = time.perf_counter() - t0
    file_bin_ero_rect = os.path.join(script_dir, "05_erosao_binaria_rect3x3.png")
    cv2.imwrite(file_bin_ero_rect, bin_eroded_rect)
    print(f"   Salvo: {file_bin_ero_rect} (Tempo: {dt:.4f}s)")

    # 1.2 Dilatação e Erosão Binária com Elemento em Cruz 3x3
    print("-> Aplicando Dilatação Binária (Cruz 3x3)...")
    bin_dilated_cross = dilate(binary_image, B_cross3)
    file_bin_dil_cross = os.path.join(script_dir, "06_dilatacao_binaria_cruz3x3.png")
    cv2.imwrite(file_bin_dil_cross, bin_dilated_cross)
    print(f"   Salvo: {file_bin_dil_cross}")

    print("-> Aplicando Erosão Binária (Cruz 3x3)...")
    bin_eroded_cross = erode(binary_image, B_cross3, is_binary=True)
    file_bin_ero_cross = os.path.join(script_dir, "07_erosao_binaria_cruz3x3.png")
    cv2.imwrite(file_bin_ero_cross, bin_eroded_cross)
    print(f"   Salvo: {file_bin_ero_cross}")

    # =========================================================================
    # PARTE 2: GRADIENTE MORFOLÓGICO EM TONS DE CINZENTO (OPÇÃO 7)
    # =========================================================================
    print("\n" + "=" * 68)
    print("  PARTE 2: GRADIENTE MORFOLÓGICO EM TONS DE CINZENTO (OPÇÃO 7)")
    print("=" * 68)

    # 2.1 Dilatação, Erosão e Gradiente com Elemento Quadrado 3x3
    print("\n-> Aplicando Gradiente Morfológico g = (f ⊕ b) - (f ⊖ b) com Máscara 3x3...")
    t0 = time.perf_counter()
    grad_3x3, gray_dil_3x3, gray_ero_3x3 = morphological_gradient(gray_image, B_rect3)
    dt = time.perf_counter() - t0

    file_gray_dil = os.path.join(script_dir, "08_dilatacao_cinza_3x3.jpg")
    cv2.imwrite(file_gray_dil, gray_dil_3x3)
    print(f"   [Dilatação f ⊕ b] Salvo: {file_gray_dil}")

    file_gray_ero = os.path.join(script_dir, "09_erosao_cinza_3x3.jpg")
    cv2.imwrite(file_gray_ero, gray_ero_3x3)
    print(f"   [Erosão f ⊖ b] Salvo: {file_gray_ero}")

    file_grad_3x3 = os.path.join(script_dir, "10_gradiente_morfologico_3x3.jpg")
    cv2.imwrite(file_grad_3x3, grad_3x3)
    print(f"   [Gradiente Morfológico 3x3] Salvo: {file_grad_3x3} (Tempo: {dt:.4f}s)")

    # 2.2 Gradiente Morfológico com Elemento Quadrado 5x5 (Bordas mais espessas)
    B_rect5 = create_structuring_element("rect", 5)
    print("\n-> Aplicando Gradiente Morfológico com Máscara 5x5...")
    t0 = time.perf_counter()
    grad_5x5, _, _ = morphological_gradient(gray_image, B_rect5)
    dt = time.perf_counter() - t0

    file_grad_5x5 = os.path.join(script_dir, "11_gradiente_morfologico_5x5.jpg")
    cv2.imwrite(file_grad_5x5, grad_5x5)
    print(f"   [Gradiente Morfológico 5x5] Salvo: {file_grad_5x5} (Tempo: {dt:.4f}s)")

    print("\n" + "=" * 68)
    print("[SUCESSO] Tarefas do Trabalho Prático 8 concluídas com êxito!")
    print("=" * 68)
