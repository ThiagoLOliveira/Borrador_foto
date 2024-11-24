import os
import cv2
import easyocr
from cvzone.FaceDetectionModule import FaceDetector
import tkinter as tk
from tkinter import filedialog, messagebox

# Função para desfocar placas de carro
def blur_license_plates(input_folder):
    output_folder = os.path.join(input_folder, "fotos_borradas")
    reader = easyocr.Reader(['en'])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            results = reader.readtext(image, detail=1)
            
            for (bbox, text, prob) in results:
                (top_left, top_right, bottom_right, bottom_left) = bbox
                x_min = int(min(top_left[0], bottom_left[0]))
                y_min = int(min(top_left[1], top_right[1]))
                x_max = int(max(bottom_right[0], top_right[0]))
                y_max = int(max(bottom_right[1], bottom_left[1]))
                
                plate_region = image[y_min:y_max, x_min:x_max]
                blurred_plate = cv2.GaussianBlur(plate_region, (51, 51), 30)
                image[y_min:y_max, x_min:x_max] = blurred_plate
            
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, image)
    messagebox.showinfo("Sucesso", "Processamento de placas concluído!")

# Função para desfocar rostos
def blur_faces(input_folder):
    output_folder = os.path.join(input_folder, "fotos_borradas")
    detector = FaceDetector(minDetectionCon=0.5)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            image, bboxes = detector.findFaces(image, draw=False)
            
            if bboxes:
                for bbox in bboxes:
                    x, y, w, h = bbox['bbox']
                    face_region = image[y:y+h, x:x+w]
                    blurred_face = cv2.blur(face_region, (50, 50))
                    image[y:y+h, x:x+w] = blurred_face
            
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, image)
    messagebox.showinfo("Sucesso", "Processamento de rostos concluído!")

# Função para escolher pasta
def select_folder(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, tk.END)
        entry.insert(0, folder)

# Função principal
def process_images():
    input_folder = input_folder_entry.get()
    if not input_folder:
        messagebox.showwarning("Erro", "Por favor, selecione uma pasta de entrada.")
        return
    
    if processing_var.get() == "placas":
        blur_license_plates(input_folder)
    elif processing_var.get() == "rostos":
        blur_faces(input_folder)
    else:
        messagebox.showwarning("Erro", "Por favor, selecione um tipo de processamento.")

# Configuração da GUI
app = tk.Tk()
app.title("Desfoque de Imagens")
app.geometry("500x250")

# Entrada para a pasta de entrada
tk.Label(app, text="Pasta de entrada:").pack(pady=5)
input_folder_entry = tk.Entry(app, width=50)
input_folder_entry.pack(pady=5)
tk.Button(app, text="Selecionar", command=lambda: select_folder(input_folder_entry)).pack(pady=5)

# Opções de processamento
processing_var = tk.StringVar(value="placas")
tk.Label(app, text="Tipo de processamento:").pack(pady=5)
tk.Radiobutton(app, text="Desfocar placas", variable=processing_var, value="placas").pack()
tk.Radiobutton(app, text="Desfocar rostos", variable=processing_var, value="rostos").pack()

# Botão de iniciar
tk.Button(app, text="Iniciar", command=process_images).pack(pady=20)

app.mainloop()
