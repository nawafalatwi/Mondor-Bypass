from tqdm import tqdm
from os import path, listdir
import numpy as np
from ... import utils

def read_all_images() -> tuple[list[bytes], list[str]]:
    generator_path = path.realpath(path.join(__file__, path.pardir, "generator"))
    image_folder = path.realpath(path.join(generator_path, "tmp"))
    x, y = [], []
    print("Importing all images")
    for image_path in tqdm(listdir(image_folder)):
        with open(path.join(image_folder, image_path), "rb") as file:
            for cx, cy in utils.split_image(file.read(), image_path[:6]):
                x.append(np.expand_dims(cx, 0)), y.append(cy)
    return x, y
