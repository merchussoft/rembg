from PIL import Image
import os
from rembg import remove
import streamlit as st
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg'}
output_folder = "output_rembg"


##valida la extencion del archivo
def allowedFile(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def saveUploadedFile(uploaded_file):
    today = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
    
    proceded_folder = os.path.join(output_folder, today)
    os.makedirs(proceded_folder, exist_ok=True)

    originals_folder = os.path.join(proceded_folder, "originals")
    os.makedirs(originals_folder, exist_ok=True)


    original_filename = uploaded_file.name

    original_file_path = os.path.join(originals_folder, original_filename)
    with open(original_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return original_file_path

def runBackgroundRemover(input_img_file):
    input_img_path = saveUploadedFile(input_img_file)
    output_img_path = input_img_path.replace('.', '_rmbg.').replace('jpg', 'png').replace('jpeg', 'png')

    try:
        image = Image.open(input_img_path)
        output = remove(image)
        output.save(output_img_path, 'PNG')
        col1, col2 = st.columns(2)
        with col1:
            st.header("Original")
            st.image(input_img_path, caption="Imagen original")
            with open(input_img_path, "rb") as imge_file:
                st.download_button(
                    label="Descargar imagen original", 
                    data=imge_file, 
                    file_name=os.path.basename(input_img_path),
                    mime="image/jpeg"
                )
        with col2:
            st.header("Procesada")
            st.image(output_img_path, caption="Imagen procesada")
            with open(output_img_path, "rb") as imge_file:
                st.download_button(
                    label="Descargar imagen procesada", 
                    data=imge_file, 
                    file_name=os.path.basename(output_img_path),
                    mime="image/png"
                )
        st.success("Imagen procesada correctamente")
    except Exception as e:
        st.error(f"Error al procesar la imagen: {e}")

def main():
    st.title("Removedor de fondos")
    uploaded_file = st.file_uploader("Seleccione una imagen", type=ALLOWED_EXTENSIONS)
    if uploaded_file is not None:
        runBackgroundRemover(uploaded_file)


if __name__ == '__main__':
    main()