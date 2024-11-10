import cv2
from cvzone.FaceDetectionModule import FaceDetector
import os

def borrar(caminho):
    # Verifica se o caminho é válido
    if not caminho:
        print("Caminho inválido.")
        return

    # Defina o caminho da pasta com as imagens
    input_folder = caminho
    output_folder = os.path.join(input_folder, "blurred_faces")
    os.makedirs(output_folder, exist_ok=True)

    # Configuração do detector de rostos
    detector = FaceDetector(minDetectionCon=0.5)

    # Itera sobre cada imagem na pasta de entrada
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)

            # Detecção de rosto e aplicação do desfoque
            img, bboxes = detector.findFaces(img, draw=False)
            if bboxes:
                for bbox in bboxes:
                    x, y, w, h = bbox['bbox']
                    rec = img[y:y+h, x:x+w]
                    recBlur = cv2.blur(rec, (50, 50))
                    img[y:y+h, x:x+w] = recBlur

            # Salva a imagem com o rosto desfocado na pasta de saída
            output_path = os.path.join(output_folder, f"blurred_{filename}")
            cv2.imwrite(output_path, img)
            print(f"Processada e salva: {output_path}")
        else:
            print(f"Arquivo desconhecido: {filename}")

    print("Processamento concluído.")