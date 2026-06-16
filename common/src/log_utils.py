"""
日志工具模块

提供统一的日志记录功能
"""

import logging
import os
from pathlib import Path
from typing import Optional
from datetime import datetime


class Logger:
    """统一日志记录器"""

    def __init__(
        self,
        name: str = "plumb-link",
        level: str = "INFO",
        log_file: Optional[str] = None,
        console_output: bool = True
    ):
        """
        初始化日志记录器

        Args:
            name: 日志记录器名称
            level: 日志级别
            log_file: 日志文件路径
            console_output: 是否输出到控制台
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        self.logger.propagate = False

        # 清除已有处理器
        self.logger.handlers.clear()

        # 格式化器
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 控制台输出
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # 文件输出
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str):
        """调试级别日志"""
        self.logger.debug(message)

    def info(self, message: str):
        """信息级别日志"""
        self.logger.info(message)

    def warning(self, message: str):
        """警告级别日志"""
        self.logger.warning(message)

    def error(self, message: str):
        """错误级别日志"""
        self.logger.error(message)

    def critical(self, message: str):
        """严重错误级别日志"""
        self.logger.critical(message)

    def exception(self, message: str):
        """异常级别日志（包含堆栈信息）"""
        self.logger.exception(message)


def get_logger(name: str = "plumb-link") -> Logger:
    """获取日志记录器"""
    return Logger(name)


def log_function_call(func):
    """函数调用日志装饰器"""
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.debug(f"调用函数: {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"函数 {func.__name__} 执行成功")
            return result
        except Exception as e:
            logger.error(f"函数 {func.__name__} 执行失败: {str(e)}")
            raise
    
    return wrapper


def log_execution_time(func):
    """函数执行时间日志装饰器"""
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = datetime.now()
        
        try:
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"函数 {func.__name__} 执行耗时: {duration:.2f} 秒")
            return result
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.error(f"函数 {func.__name__} 执行失败，耗时: {duration:.2f} 秒: {str(e)}")
            raise
    
    return wrapper


def setup_global_logging(
    level: str = "INFO",
    log_dir: str = "logs",
    console_output: bool = True
):
    """
    设置全局日志配置

    Args:
        level: 日志级别
        log_dir: 日志目录
        console_output: 是否输出到控制台
    """
    # 创建日志目录
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # 设置日志文件名（包含日期）
    log_file_name = f"plumb-link_{datetime.now().strftime('%Y%m%d')}.log"
    log_file_path = log_path / log_file_name

    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    root_logger.propagate = False

    # 清除已有处理器
    root_logger.handlers.clear()

    # 格式化器
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 控制台输出
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # 文件输出
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


# 默认日志记录器
default_logger = get_logger()