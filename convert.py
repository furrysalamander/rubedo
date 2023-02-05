from glob import glob
import os
from pathlib import Path
for file_name in glob("sample_data/*"):
    os.system(f"ffmpeg -i {file_name} gif/{Path(file_name).stem}.gif")