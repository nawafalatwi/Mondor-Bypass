import onnxruntime
import numpy as np
from ... import utils

onnx_session = onnxruntime.InferenceSession("blob/CNN.onnx")

def inference(image: bytes) -> str:
    result = []
    for img, _ in utils.split_image(image, "AAAAAA"):
        img = np.expand_dims(img, 0)
        img = img.astype(dtype=np.float32)
        input = {onnx_session.get_inputs()[0].name: img}
        output = onnx_session.run(None, input)
        idx = int(output[0][0].argmax())
        result.append(utils.decode_result(idx))
    return "".join(reversed(result))
