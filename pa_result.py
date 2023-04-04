import numpy as np

class PaResult:
    def __init__(self, video_file: str, height_data: np.ndarray, score: float):
        self.video_file = video_file
        self.height_data = height_data
        self.score = score
