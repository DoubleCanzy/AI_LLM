import torch
import torch.nn as nn
import torch.optim as optim

class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(10, 5)  # 输入层到隐藏层
        self.fc2 = nn.Linear(5, 1)   # 隐藏层到输出层

    def forward(self, x):
        x = torch.relu(self.fc1(x))  # 使用 ReLU 激活函数
        x = self.fc2(x)
        return x

model = SimpleNN()

criterion = nn.MSELoss()  # 均方误差损失函数
optimizer = optim.Adam(model.parameters(), lr=0.01)  # Adam 优化器

X = torch.randn(100, 10)  # 100 个样本，每个样本有 10 个特征
y = torch.randn(100, 1)   # 100 个样本的目标

for epoch in range(100):  # 训练 100 个 epoch
    optimizer.zero_grad()  # 清空梯度
    outputs = model(X)      # 前向传播
    loss = criterion(outputs, y)  # 计算损失
    loss.backward()        # 反向传播
    optimizer.step()       # 更新参数

    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/100], Loss: {loss.item():.4f}')

