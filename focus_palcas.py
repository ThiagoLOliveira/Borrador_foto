import os
import cv2
import easyocr

def blur_license_plates(input_folder, output_folder):
    # Cria o leitor OCR
    reader = easyocr.Reader(['en'])
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            
            results = reader.readtext(image, detail=1)
            
            for (bbox, text, prob) in results:
                # Pega as coordenadas da caixa delimitadora
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
            print(f"Processada: {filename}")
    
    print("Processamento concluído!")

input_folder = "C:\\Users\\conta\\Downloads\\plcas"
output_folder = "C:\\Users\\conta\\Downloads"

blur_license_plates(input_folder, output_folder)
