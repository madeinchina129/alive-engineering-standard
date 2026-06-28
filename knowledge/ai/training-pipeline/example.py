```python
# PyTorch Lightning 训练流水线
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping, LearningRateMonitor
from pytorch_lightning.loggers import WandbLogger

# 数据模块
class DataModule(pl.LightningDataModule):
    def __init__(self, data_path, batch_size=32):
        super().__init__()
        self.data_path = data_path
        self.batch_size = batch_size

    def prepare_data(self):
        # 数据质量检查
        dataset = load_dataset(self.data_path)
        check_data_quality(dataset)  # 缺失率、异常值

    def setup(self, stage=None):
        # 划分训练/验证/测试 (80/10/10)
        full_dataset = load_dataset(self.data_path)
        train_size = int(0.8 * len(full_dataset))
        val_size = int(0.1 * len(full_dataset))
        test_size = len(full_dataset) - train_size - val_size

        self.train, self.val, self.test = random_split(
            full_dataset, [train_size, val_size, test_size]
        )

    def train_dataloader(self):
        return DataLoader(self.train, batch_size=self.batch_size,
                          num_workers=8, shuffle=True, pin_memory=True)

# 模型模块
class TransformerModel(pl.LightningModule):
    def __init__(self, config):
        super().__init__()
        self.save_hyperparameters()
        self.model = build_transformer(config)
        self.learning_rate = config.learning_rate

    def training_step(self, batch, batch_idx):
        loss = self.model(batch)
        self.log('train_loss', loss, on_step=True, on_epoch=True)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=self.learning_rate)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=100
        )
        return [optimizer], [scheduler]

# 训练配置
config = {
    'batch_size': 128,
    'learning_rate': 1e-4,
    'max_epochs': 100,
    'precision': '16-mixed',  # 混合精度训练
    'accumulate_grad_batches': 4,  # 梯度累积
}

# 回调
callbacks = [
    ModelCheckpoint(monitor='val_loss', mode='min', save_top_k=3),
    EarlyStopping(monitor='val_loss', patience=10, mode='min'),
    LearningRateMonitor(logging_interval='step'),
]

# 启动训练
trainer = pl.Trainer(
    max_epochs=config['max_epochs'],
    precision=config['precision'],
    accumulate_grad_batches=config['accumulate_grad_batches'],
    callbacks=callbacks,
    logger=WandbLogger(project='transformer-training'),
    num_nodes=4,  # 多节点分布式训练
    devices=8,    # 每节点 8 GPU
    strategy='deepspeed_stage_2',  # DeepSpeed 优化
)

trainer.fit(DataModule(), TransformerModel(config))
```