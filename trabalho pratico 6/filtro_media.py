import numpy as np
import cv2
import time
import os
import sys
import glob

def apply_mean_filter(image, N):
    """
    Filtro Espacial da Média (Passa-Baixa) com Convolução Vetorizada (Slicing)
    e Tratamento de Bordas por Espelhamento (Symmetric Padding).

    Parâmetros:
    -----------
    image : np.ndarray
        Matriz da imagem de entrada (escala de cinza 2D ou colorida 3D/BGR).
    N : int
        Dimensão ímpar da máscara quadrada N x N (N = 2a + 1).

    Retorna:
    --------
    np.ndarray
        Imagem filtrada suavizada com tipo uint8 no intervalo [0, 255].
    """
    # 1. Definição Dinâmica da Máscara e Validação
    if not isinstance(N, int) or N < 1 or N % 2 == 0:
        raise ValueError(f"Dimensão da máscara N deve ser um número inteiro ímpar positivo (N = 2a + 1). Recebido: {N}")

    # Margem de segurança: a = (N - 1) / 2
    a = (N - 1) // 2
    height, width = image.shape[:2]

    # Coeficiente uniforme: 1 / N^2
    weight = np.float32(1.0 / (N * N))

    # 2. Tratamento de Bordas: Espelhamento (Symmetric Padding)
    # Evita artefacto de moldura escura gerado por zero-padding
    if len(image.shape) == 2:
        # Imagem monocromática (tons de cinza)
        padded_image = np.pad(image, pad_width=a, mode='symmetric')
    else:
        # Imagem colorida multicanal (não expandir a dimensão de canais)
        padded_image = np.pad(image, pad_width=((a, a), (a, a), (0, 0)), mode='symmetric')

    # 3. Convolução Espacial Vetorizada (Slicing)
    # Inicializar matriz acumuladora com zeros em ponto flutuante
    output = np.zeros(image.shape, dtype=np.float32)

    # Itera apenas sobre a dimensão da máscara (N x N), acumulando fatias inteiras
    for i in range(N):
        for j in range(N):
            # Recorta fatia contínua correspondente ao tamanho exato da imagem original
            slice_window = padded_image[i:i + height, j:j + width]
            # Multiplica pelo coeficiente 1 / N^2 e acumula
            output += slice_window * weight

    # Arredondar e limitar ao intervalo válido [0, 255] em uint8
    return np.clip(np.round(output), 0, 255).astype(np.uint8)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Localizar imagem de entrada (argumento de linha de comando ou imagem na pasta)
    img_path = None
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        img_path = sys.argv[1]
    else:
        # Priorizar resultado de alargamento de contraste do trabalho pratico 5
        tp5_contrast = os.path.join(script_dir, "..", "trabalho pratico 5", "02_alargamento_contraste.jpg")
        candidates = [
            os.path.join(script_dir, "cobaia.jpg"),
            tp5_contrast,
            os.path.join(script_dir, "imagem_teste.jpg")
        ] + glob.glob(os.path.join(script_dir, "*.jpg")) + glob.glob(os.path.join(script_dir, "*.png"))

        for cand in candidates:
            # Nao selecionar imagens de saida previamente geradas do TP6
            base = os.path.basename(cand)
            if not base.startswith("0") and os.path.exists(cand):
                img_path = os.path.abspath(cand)
                break

    if img_path is None or not os.path.exists(img_path):
        print("Erro: Nenhuma imagem cobaia encontrada na pasta trabalho pratico 6.")
        exit(1)

    print(f"-> Carregando imagem cobaia: {img_path}")
    image = cv2.imread(img_path)

    if image is None:
        print("Erro: Falha ao carregar a imagem com OpenCV.")
        exit(1)

    is_color = len(image.shape) == 3
    tipo_str = f"Colorida ({image.shape[2]} canais)" if is_color else "Escala de Cinza (1 canal)"
    print(f"   Dimensões: {image.shape[1]}x{image.shape[0]} | Tipo: {tipo_str}")

    # Salvar a imagem original como 01_imagem_original.jpg
    orig_output = os.path.join(script_dir, "01_imagem_original.jpg")
    cv2.imwrite(orig_output, image)
    print(f"   Salvo: {orig_output}")

    # Testes com diferentes dimensões de máscara N x N (conforme especificação da documentação)
    test_masks = [3, 7, 15, 35]

    print("\n" + "=" * 65)
    print("  APLICAÇÃO DO FILTRO ESPACIAL DA MÉDIA VETORIZADO (SLICING)")
    print("=" * 65)

    for idx, N in enumerate(test_masks, start=2):
        print(f"\n-> Processando Máscara N = {N}x{N} (a = {(N-1)//2}, coeficiente = 1/{N*N})...")
        
        start_time = time.perf_counter()
        filtered = apply_mean_filter(image, N)
        elapsed_time = time.perf_counter() - start_time

        output_filename = f"0{idx}_filtro_media_{N}x{N}.jpg"
        output_filepath = os.path.join(script_dir, output_filename)
        cv2.imwrite(output_filepath, filtered)

        print(f"   Tempo de Execução: {elapsed_time:.4f}s")
        print(f"   Salvo: {output_filepath}")

    print("\n" + "=" * 65)
    print("[SUCESSO] Tarefas do Trabalho Prático 6 concluídas com êxito!")
    print("=" * 65)
