ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg', 'mp4'}

OUTPUT_FOLDER_IMAGE = "output_rembg_image"
OUTPUT_FOLDER_VIDEO = "output_rembg_video"

def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS