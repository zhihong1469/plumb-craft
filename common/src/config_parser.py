"""
配置解析模块

支持多种配置文件格式：JSON、YAML、INI
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    from configparser import ConfigParser
    INI_AVAILABLE = True
except ImportError:
    INI_AVAILABLE = False


@dataclass
class ConfigSource:
    """配置源信息"""
    source_type: str  # file, env, default
    path: Optional[str] = None
    priority: int = 0  # 优先级，数值越大优先级越高


class ConfigParser:
    """配置解析器"""

    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.sources: List[ConfigSource] = []

    def load_from_file(self, file_path: str, priority: int = 10) -> bool:
        """
        从文件加载配置

        Args:
            file_path: 配置文件路径
            priority: 优先级

        Returns:
            是否加载成功
        """
        path = Path(file_path)
        
        if not path.exists():
            return False

        ext = path.suffix.lower()

        try:
            if ext == ".json":
                self._load_json(path, priority)
            elif ext == ".yaml" or ext == ".yml":
                self._load_yaml(path, priority)
            elif ext == ".ini" or ext == ".cfg":
                self._load_ini(path, priority)
            else:
                # 尝试作为简单键值对文件加载
                self._load_kv(path, priority)
            
            return True
        except Exception:
            return False

    def _load_json(self, path: Path, priority: int):
        """加载 JSON 配置"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._merge_config(data, priority, str(path), "file")

    def _load_yaml(self, path: Path, priority: int):
        """加载 YAML 配置"""
        if not YAML_AVAILABLE:
            raise ImportError("yaml 模块未安装，请安装 PyYAML")
        
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        if data:
            self._merge_config(data, priority, str(path), "file")

    def _load_ini(self, path: Path, priority: int):
        """加载 INI 配置"""
        if not INI_AVAILABLE:
            raise ImportError("configparser 模块不可用")
        
        config = ConfigParser()
        config.read(path)
        
        data = {}
        for section in config.sections():
            data[section] = dict(config.items(section))
        
        self._merge_config(data, priority, str(path), "file")

    def _load_kv(self, path: Path, priority: int):
        """加载简单键值对配置"""
        data = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    data[key.strip()] = value.strip()
        
        self._merge_config(data, priority, str(path), "file")

    def load_from_env(self, prefix: str = "", priority: int = 20):
        """
        从环境变量加载配置

        Args:
            prefix: 环境变量前缀
            priority: 优先级
        """
        data = {}
        for key, value in os.environ.items():
            if prefix and not key.startswith(prefix):
                continue
            
            if prefix:
                config_key = key[len(prefix):].lower().replace("_", ".")
            else:
                config_key = key.lower().replace("_", ".")
            
            data[config_key] = value
        
        if data:
            self._merge_config(data, priority, "environment", "env")

    def load_from_dict(self, data: Dict[str, Any], priority: int = 30, source_name: str = "dict"):
        """
        从字典加载配置

        Args:
            data: 配置字典
            priority: 优先级
            source_name: 源名称
        """
        if data:
            self._merge_config(data, priority, source_name, "dict")

    def _merge_config(self, data: Dict[str, Any], priority: int, source: str, source_type: str):
        """合并配置"""
        # 记录源信息
        self.sources.append(ConfigSource(
            source_type=source_type,
            path=source,
            priority=priority
        ))

        # 合并配置（扁平化处理）
        flat_data = self._flatten_dict(data)
        for key, value in flat_data.items():
            # 检查是否已存在且优先级更高
            existing_info = self.config.get(key)
            if existing_info:
                if existing_info["priority"] >= priority:
                    continue
            
            self.config[key] = {
                "value": value,
                "priority": priority,
                "source": source
            }

    def _flatten_dict(self, data: Dict[str, Any], parent_key: str = "") -> Dict[str, Any]:
        """扁平化字典"""
        result = {}
        for key, value in data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            
            if isinstance(value, dict):
                result.update(self._flatten_dict(value, new_key))
            else:
                result[new_key] = value
        
        return result

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值
        """
        info = self.config.get(key)
        if info:
            return info["value"]
        return default

    def get_int(self, key: str, default: int = 0) -> int:
        """获取整数配置"""
        value = self.get(key, default)
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def get_float(self, key: str, default: float = 0.0) -> float:
        """获取浮点数配置"""
        value = self.get(key, default)
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """获取布尔配置"""
        value = self.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "yes", "1", "on")
        return bool(value)

    def get_list(self, key: str, default: List = None) -> List:
        """获取列表配置"""
        value = self.get(key, default or [])
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        if isinstance(value, list):
            return value
        return default or []

    def get_dict(self, key: str, default: Dict = None) -> Dict:
        """获取字典配置"""
        value = self.get(key, default or {})
        if isinstance(value, dict):
            return value
        return default or {}

    def has_key(self, key: str) -> bool:
        """检查配置键是否存在"""
        return key in self.config

    def set(self, key: str, value: Any, priority: int = 100, source: str = "manual"):
        """
        设置配置值

        Args:
            key: 配置键
            value: 配置值
            priority: 优先级
            source: 来源
        """
        self.config[key] = {
            "value": value,
            "priority": priority,
            "source": source
        }

    def to_dict(self) -> Dict[str, Any]:
        """转换为普通字典"""
        return {key: info["value"] for key, info in self.config.items()}

    def get_sources(self) -> List[ConfigSource]:
        """获取配置源列表"""
        return self.sources

    def clear(self):
        """清空配置"""
        self.config = {}
        self.sources = []


def load_config(config_files: Optional[List[str]] = None, env_prefix: str = "") -> ConfigParser:
    """
    加载配置（按优先级）

    优先级顺序（从低到高）：
    1. 默认配置（代码中定义）
    2. 全局配置文件
    3. 项目配置文件
    4. 环境变量
    5. 命令行参数

    Args:
        config_files: 配置文件路径列表
        env_prefix: 环境变量前缀

    Returns:
        配置解析器实例
    """
    parser = ConfigParser()

    # 加载配置文件
    if config_files:
        for i, config_file in enumerate(config_files):
            parser.load_from_file(config_file, priority=10 + i)

    # 加载环境变量
    parser.load_from_env(env_prefix, priority=20)

    return parser


def save_config(config: Dict[str, Any], file_path: str) -> bool:
    """
    保存配置到文件

    Args:
        config: 配置字典
        file_path: 文件路径

    Returns:
        是否保存成功
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    ext = path.suffix.lower()

    try:
        if ext == ".json":
            with open(path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        elif ext == ".yaml" or ext == ".yml":
            if not YAML_AVAILABLE:
                raise ImportError("yaml 模块未安装")
            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        elif ext == ".ini":
            if not INI_AVAILABLE:
                raise ImportError("configparser 不可用")
            config_parser = ConfigParser()
            for key, value in config.items():
                section, _, option = key.partition(".")
                if not section:
                    section = "DEFAULT"
                if section not in config_parser:
                    config_parser[section] = {}
                config_parser[section][option] = str(value)
            with open(path, "w", encoding="utf-8") as f:
                config_parser.write(f)
        else:
            # 保存为简单键值对格式
            with open(path, "w", encoding="utf-8") as f:
                for key, value in config.items():
                    f.write(f"{key}={value}\n")
        
        return True
    except Exception:
        return False