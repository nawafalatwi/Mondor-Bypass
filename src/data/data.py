import io
from os import path, listdir
from PIL import Image
import numpy as np

def encode_result(c: str):
    if str.isdigit(c):
        return ord(c) - ord('0')
    else:
        return ord(c) - ord('A') + 10
    
def decode_result(c: int):
    if c < 10:
        return c
    else:
        return chr(c - 10 + ord('A'))

def split_image(image_bytes: bytes, result: str) -> list[tuple[np.array, np.int8]]:
    characters = []
    image = Image.open(io.BytesIO(image_bytes))
    step = 17
    for idx, c in zip(range(0, 6), reversed(result)):
        single_char = image.crop((105 - idx * step - 16, 0, 105 - idx * step, 32)).convert('L')
        single_char = np.array(single_char)
        single_char = np.expand_dims(single_char, axis=0)
        characters.append((
            np.array(single_char),
            encode_result(c))
        )
    return characters

def read_all_images() -> tuple[list[bytes], list[str]]:
    generator_path = path.realpath(path.join(__file__, path.pardir, "generator"))
    image_folder = path.realpath(path.join(generator_path, "tmp"))
    x, y = [], []
    for image_path in listdir(image_folder):
        with open(path.join(image_folder, image_path), "rb") as file:
            for cx, cy in split_image(file.read(), image_path[:6]):
                x.append(np.expand_dims(cx, 0)), y.append(cy)
    return x, y
