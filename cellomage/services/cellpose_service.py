import cv2
import numpy as np
from skimage.measure import regionprops
from cellpose import models

model = models.CellposeModel(
    pretrained_model="models/my_cells_v2",
    gpu=False
)

def analyze_image(image_path, mode="dots"):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    masks, _, _ = model.eval(gray, diameter=30)

    cell_count = int(masks.max())
    confluency = round((np.sum(masks > 0) / masks.size) * 100, 2)

    output = img.copy()

    if mode == "dots":
        for prop in regionprops(masks):
            y, x = map(int, prop.centroid)
            cv2.circle(output, (x, y), 4, (0, 255, 0), -1)

    elif mode == "mask":
        color_mask = np.zeros_like(img)
        for i in range(1, masks.max() + 1):
            color_mask[masks == i] = np.random.randint(0, 255, 3)
        output = cv2.addWeighted(img, 0.6, color_mask, 0.4, 0)

    return output, cell_count, confluency
