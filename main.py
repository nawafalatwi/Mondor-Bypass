import sys
import time
match sys.argv[1]:
    case "train":
        from src.build.model import train
        train.train()

    case "export":
        from src.build.model import export
        export.run_export()

    case "torch_infer":
        from src.deploy.model.infer_torch import inference
        from src.deploy.interact import inter
        inter.start(inference)

    case "onnx_infer":
        from src.deploy.model.infer_onnx import inference
        from src.deploy.interact import inter
        inter.start(inference)

    case "plot":
        from src.plot import plot
        plot.start()

    case _:
        print("Wrong argument")
