from utils import *
from preprocess import *
from postprocess import *
from PIL import Image, ImageDraw, ImageFont
from configs import *

def prediction(session, image, cfg):
    image, ratio, (padd_left, padd_top) = resize_and_pad(image, new_shape=cfg.image_size)
    img_norm = normalization_input(image)
    pred = infer(session, img_norm)
    pred = postprocess(pred, cfg.conf_thres, cfg.iou_thres)[0]
    paddings = np.array([padd_left, padd_top, padd_left, padd_top])
    pred[:,:4] = (pred[:,:4] - paddings) / ratio
    return pred


def visualize(image, pred):
    img_ = image.copy()
    drawer = ImageDraw.Draw(img_)

    # Create a dictionary to store the count of each object
    object_counts = {}
    for p in pred:
        x1, y1, x2, y2, _, id = p
        id = int(id)

        # Increment the count of the object
        if id not in object_counts:
            object_counts[id] = 0
        object_counts[id] += 1

        # Draw the rectangle and label the object
        drawer.rectangle((x1, y1, x2, y2), outline=IDX2COLORs[id], width=3)
        drawer.text((x2 + 5, y1), IDX2TAGs[id], fill=IDX2COLORs[id], font=ImageFont.truetype("arial.ttf", 16))

    # Add a legend to the image
    drawer.text((0, 0), "", fill="#FFFFFF", font=ImageFont.truetype("arial.ttf", 16))
    for id, count in object_counts.items():
        drawer.text((0, 20 + 20 * id), f"{IDX2TAGs[id]}: {count}", fill=IDX2COLORs[id], font=ImageFont.truetype("arial.ttf", 16))

    return img_