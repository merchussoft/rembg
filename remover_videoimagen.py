import os
import cv2
from PIL import Image
from rembg import remove
import streamlit as st
from datetime import datetime
from moviepy.editor import VideoFileClip

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg', 'mp4'}

# Carpetas de salida
IMAGE_OUTPUT_FOLDER = "output_rembg_image"
VIDEO_OUTPUT_FOLDER = "output_rembg_video"

BG_COLOR = (0, 255, 0, 255)  # Color de fondo verde para los videos
output_fps = 30  # FPS de salida para los videos


def save_uploaded_file(uploaded_file, folder):
    """Guarda el archivo subido en una carpeta organizada por fecha"""
    today = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    proceded_folder = os.path.join(folder, today)
    os.makedirs(proceded_folder, exist_ok=True)

    original_filename = uploaded_file.name
    file_path = os.path.join(proceded_folder, original_filename)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path, proceded_folder


def process_image(input_img_file):
    """Procesa imágenes eliminando el fondo con rembg"""
    input_img_path, output_folder = save_uploaded_file(input_img_file, IMAGE_OUTPUT_FOLDER)
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
            st.image(output_img_path, caption="Imagen sin fondo")
            with open(output_img_path, "rb") as imge_file:
                st.download_button(
                    label="Descargar imagen sin fondo",
                    data=imge_file,
                    file_name=os.path.basename(output_img_path),
                    mime="image/png"
                )

        st.success("Imagen procesada correctamente")

    except Exception as e:
        st.error(f"Error al procesar la imagen: {e}")


def remove_background_from_video(video_path, output_folder):
    """Procesa videos eliminando el fondo con rembg"""
    try:
        # Cargar el video
        video_input = VideoFileClip(video_path)
        output_video_path = os.path.join(output_folder, os.path.splitext(os.path.basename(video_path))[0] + "_rmbg.mp4")

        def remove_background(frame):
            """Aplica rembg a cada frame del video"""
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_no_bg = remove(frame_rgb, bgcolor=BG_COLOR)
            return cv2.cvtColor(frame_no_bg, cv2.COLOR_RGB2BGR)

        # Aplicar la función de eliminación de fondo
        video_no_bg = video_input.fl_image(remove_background)

        # Guardar el video procesado
        video_no_bg.write_videofile(output_video_path, fps=output_fps)

        return output_video_path

    except Exception as e:
        st.error(f"Error al procesar el video: {e}")
        return None


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
    st.title("Removedor de Fondo (Imágenes y Videos)")
    uploaded_file = st.file_uploader("Seleccione una imagen o video", type=ALLOWED_EXTENSIONS)

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()

        if file_extension in {"png", "jpg", "jpeg", "svg"}:
            process_image(uploaded_file)
        elif file_extension == "mp4":
            process_video(uploaded_file)
        else:
            st.error("Formato de archivo no soportado.")


if __name__ == '__main__':
    main()
