import os
import uuid

def save_image(file, folder):
    os.makedirs(folder, exist_ok=True)
    filename = f"{uuid.uuid4()}.jpg"
    path = os.path.join(folder, filename)
    file.save(path)
    return filename, path
