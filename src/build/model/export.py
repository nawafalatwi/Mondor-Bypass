import onnx, torch
import numpy as np
import onnxruntime
from . import models

model_input = torch.randn(size=(1, 1, 32, 16), requires_grad=True, dtype=torch.float)

def to_numpy(tensor: torch.Tensor) -> np.ndarray:
    if tensor.requires_grad:
        return tensor.detach().cpu().numpy()
    else:
        return tensor.cpu().numpy()

def export_model() -> torch.Tensor:
    model = models.BasicCNN()
    assert torch.cuda.is_available()

    model.load_state_dict(torch.load("blob/CNN.pt"))
    model = model.to(models.device)

    torch_input = model_input.to(models.device)
    torch_output = model(torch_input)

    print("Exporting")
    torch.onnx.export(
        model=model,
        args=torch_input,
        f="blob/CNN.onnx",
        export_params=True,
        opset_version=10,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'},
                    'output':{0: 'batch_size'}}
    )
    return to_numpy(torch_output)

def check_model():
    print("Performing checks")

    onnx_model = onnx.load("blob/CNN.onnx")
    onnx.checker.check_model(onnx_model)

    ort_session = onnxruntime.InferenceSession("blob/CNN.onnx")
    ort_input = {ort_session.get_inputs()[0].name: to_numpy(model_input)}
    ort_output = ort_session.run(None, ort_input)

    return ort_output

def run_export():
    torch_output = export_model()
    ort_output = check_model()
    np.testing.assert_allclose(torch_output, ort_output[0], rtol=1e-3, atol=1e-5)

    print("Export completed, satisfying checks")
