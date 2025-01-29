from PIL import Image
import os
from rembg import remove
import streamlit as st
from datetime import datetime
from moviepy.editor import VideoFileClip
import cv2

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg', 'mp4'}
output_folder = "output_rembg"

IMAGE_OUTPUT_FOLDER = "output_rembg_image"
VIDEO_OUTPUT_FOLDER = "output_rembg_video"
BG_COLOR=(0, 255,0, 255)
output_fps = 30  # FPS de salida para los videos



def save_uploaded_file(uploaded_file, folder):
    today = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    
    proceded_folder = os.path.join(folder, today)
    os.makedirs(proceded_folder, exist_ok=True)

    original_filename = uploaded_file.name
    original_file_path = os.path.join(proceded_folder, original_filename)

    with open(original_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return original_file_path, proceded_folder



## aplkicacion poara remover el fondo de un imagen 
def run_background_remover(input_img_file):
    """ procesa imagenes eliminado el fondo con rembg """
    input_img_path, output_folder = save_uploaded_file(input_img_file, IMAGE_OUTPUT_FOLDER)
    ##output_img_path = input_img_path.replace('.', '_rmbg.').replace('jpg', 'png').replace('jpeg', 'png')

    output_img_path = os.path.join(output_folder, os.path.splitext(input_img_file.name)[0] + "_rmbg.png")

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

## esta funcion me ayuda a remover los fondos de un video
def remove_background_from_video(video_path, output_folder): 
    """Procesa videos eliminando el fondo con rembg"""

    try:
        # Cargar el video
        video_input = VideoFileClip(video_path)
        output_video_path = os.path.join(output_folder, os.path.splitext(os.path.basename(video_path))[0] + "_rmbg.mp4")

        video_no_bg = video_input.fl_image(remove_background_video)
        video_no_bg.write_videofile(output_video_path, fps=output_fps)

        return output_video_path
    except Exception as e:
        st.error(f"Error al procesar el video: {e}")
        return None



def remove_background_video(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = remove(frame_rgb, bgcolor=BG_COLOR)
    
    return cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)


def process_video(input_video_file):
    """Guarda el video subido y procesa la eliminación de fondo"""
    input_video_path, output_folder = save_uploaded_file(input_video_file, VIDEO_OUTPUT_FOLDER)
    
    output_video_path = remove_background_from_video(input_video_path, output_folder)

    if output_video_path:
        st.video(output_video_path)
        with open(output_video_path, "rb") as video_file:
            st.download_button(
                label="Descargar video sin fondo",
                data=video_file,
                file_name=os.path.basename(output_video_path),
                mime="video/mp4"
            )
        st.success("Video procesado correctamente")



def main():
    st.title("Removedor de fondos (Imágenes y Videos)")
    uploaded_file = st.file_uploader("Seleccione una imagen o video", type=ALLOWED_EXTENSIONS)
    if uploaded_file is not None:

        file_extension = uploaded_file.name.split('.')[-1].lower()

        if file_extension in { "png", "jpg", "jpeg", "svg" }:
            run_background_remover(uploaded_file)
        elif file_extension in { "mp4"}:
            process_video(uploaded_file)
        else:
            st.error("Formato de archivo no soportado")


if __name__ == '__main__':
    main()