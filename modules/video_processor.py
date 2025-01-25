import torch
from moviepy import VideoFileClip, TextClip, CompositeVideoClip  # Robust Video Matting

class VideoProcessor:
    def __init__(self, model_path, device="cuda"):
        self.device = device if torch.cuda.is_available() else "cpu"
        ##self.model = rvm_model(model_path, device=self.device)

    def process_frame(self, frame):
        from PIL import Image
        from torchvision.transforms import functional as F

        image = Image.fromarray(frame)
        mask, _ = self.model(image)
        return F.to_pil_image(mask)

    def process_video(self, input_video, output_video):
        clip = VideoFileClip(input_video)
        processed_clip = clip.fl_image(self.process_frame)
        processed_clip.write_videofile(output_video, codec="libx264")
        return output_video
