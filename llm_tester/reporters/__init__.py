"""
报告生成模块
"""

from .text import TextReporter
from .json_reporter import JSONReporter

__all__ = ["TextReporter", "JSONReporter"]
