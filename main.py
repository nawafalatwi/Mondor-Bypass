import sys

match sys.argv[1]:
    case "train":
        from src.build.model import train
        train.train()

    case "export":
        from src.build.model import export
        export.run_export()

    case "torch_infer":
        from src.deploy.model.infer_torch import inference
        from src.deploy.interact import main
        main.start(inference)

    case "onnx_infer":
        from src.deploy.model.infer_onnx import inference
        from src.deploy.interact import main
        main.start(inference)
