import io
import numpy as np
from PIL import Image

def encode_result(c: str) -> int:
    if str.isdigit(c):
        return ord(c) - ord('0')
    else:
        return ord(c) - ord('A') + 10
    
def decode_result(c: int) -> str:
    if c < 10:
        return str(c)
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
