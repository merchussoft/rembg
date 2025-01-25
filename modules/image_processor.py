import os
from datetime import datetime   # datetime is a class in the datetime module
from rembg import remove

class BackgroundRemover:

    def __init__(self, output_folder_image):
        self.output_folder = output_folder_image


    def processImage(self, image_file):

        today = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        processed_folder = os.path.join(self.output_folder, today)
        os.makedirs(processed_folder, exist_ok=True)

        original_folder = os.path.join(processed_folder, 'originals')
        os.makedirs(original_folder, exist_ok=True)

        original_path = os.path.join(original_folder, image_file.filename)
        image_file.save(original_path)

        output_path = os.path.join(processed_folder, f"output_{image_file.filename.rsplit('.', 1)[0]}.png")
        self._remove_background(original_path, output_path)

        return output_path

    def _remove_background(self, input_path, output_path):
        with open(input_path, 'rb') as inp, open(output_path, 'wb') as outp:
            outp.write(remove(inp.read()))