# 模型服务规范 — FAQ

## Q1: Triton vs TorchServe vs BentoML？
Triton Inference Server（推荐）：NVIDIA 出品、支持多框架、动态批处理、GPU 优化最好。TorchServe：PyTorch 原生、易于使用。BentoML：Python 原生、生态系统好、支持自定义框架。

## Q2: 模型推理优化方法？
① 模型量化（FP16/INT8）② 模型剪枝 ③ ONNX Runtime/TensorRT 加速 ④ KV Cache 优化（LLM）⑤ 请求批处理（增大吞吐）⑥ 推理结果缓存。通常组合使用可提升 2-5 倍性能。
