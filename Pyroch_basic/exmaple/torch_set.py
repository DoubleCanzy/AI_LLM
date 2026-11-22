import torch

print("PyTorch 版本:", torch.__version__)
print("CUDA 是否可用:", torch.cuda.is_available())
x=torch.rand(5, 3)
print("随机张量 x:")
print(x)