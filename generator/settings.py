"""配置管理 — 用户级持久化设置（generator.json）"""

import json
import os
from pathlib import Path
from typing import Optional


# 配置文件名
SETTINGS_FILENAME = "generator.json"


class GeneratorSettings:
    """生成器持久化设置管理

    配置查找顺序：
    1. 当前工作目录下的 generator.json
    2. 项目根目录下的 generator.json（包含 generator/ 目录的父目录）
    3. 用户主目录下的 .generator.json
    """

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path.cwd()
        self._data: dict = {}
        self._load()

    @staticmethod
    def discover(base_dir: Optional[Path] = None) -> Path:
        """自动发现配置文件路径"""
        search_dirs = []

        if base_dir:
            search_dirs.append(base_dir)

        cwd = Path.cwd()
        search_dirs.append(cwd)

        # 向上查找项目根
        for parent in cwd.parents:
            if (parent / "generator").is_dir() or (parent / ".git").is_dir():
                search_dirs.append(parent)
                break

        # 用户主目录
        search_dirs.append(Path.home())

        for d in search_dirs:
            config_path = d / SETTINGS_FILENAME
            if config_path.exists():
                return config_path

            # 也检查隐藏文件
            hidden_path = d / f".{SETTINGS_FILENAME}"
            if hidden_path.exists():
                return hidden_path

        return search_dirs[0] / SETTINGS_FILENAME

    def _load(self):
        """加载配置文件"""
        self.config_path = self.discover(self.base_dir)
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._data = {}
        else:
            self._data = {}

    def save(self):
        """保存配置到文件"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def get(self, key: str, default=None):
        """获取配置项"""
        return self._data.get(key, default)

    def set(self, key: str, value):
        """设置配置项"""
        self._data[key] = value

    @property
    def default_generator_type(self) -> str:
        return str(self.get("default_generator_type", "rule"))

    @property
    def default_output_format(self) -> str:
        return str(self.get("default_output_format", "md"))

    @property
    def docs_base_dir(self) -> Optional[str]:
        return self.get("docs_base_dir")

    @property
    def template_dir(self) -> Optional[str]:
        return self.get("template_dir")

    @property
    def domain_yaml_path(self) -> Optional[str]:
        return self.get("domain_yaml_path")

    @property
    def verbose(self) -> bool:
        return bool(self.get("verbose", True))

    def to_dict(self) -> dict:
        """导出全部配置"""
        return dict(self._data)
