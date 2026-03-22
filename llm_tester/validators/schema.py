"""
Schema 验证器
"""

from typing import Dict, Any, Optional
from ..providers.base import LLMResponse


class ValidationResult:
    """验证结果"""
    
    def __init__(self, is_valid: bool, errors: Optional[list] = None):
        self.is_valid = is_valid
        self.errors = errors or []
    
    def __bool__(self):
        return self.is_valid


class ResponseValidator:
    """
    响应验证器
    
    Usage:
        validator = ResponseValidator()
        result = validator.validate(response, schema={...})
    """
    
    def validate(
        self,
        response: LLMResponse,
        schema: Optional[Dict] = None
    ) -> ValidationResult:
        """
        验证响应
        
        Args:
            response: LLM 响应
            schema: JSON Schema（可选）
        
        Returns:
            ValidationResult: 验证结果
        """
        errors = []
        
        # 基础验证
        if response.error:
            errors.append(f"API Error: {response.error}")
        
        if not response.content:
            errors.append("Response content is empty")
        
        # Schema 验证（如果有）
        if schema and response.content:
            schema_errors = self._validate_schema(response.content, schema)
            errors.extend(schema_errors)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors
        )
    
    def _validate_schema(
        self,
        content: str,
        schema: Dict
    ) -> list:
        """
        简单的 Schema 验证
        
        TODO: 使用 jsonschema 库进行完整验证
        """
        errors = []
        
        # 基础类型检查
        if schema.get("type") == "string":
            if not isinstance(content, str):
                errors.append("Content should be string")
            
            min_length = schema.get("minLength")
            if min_length and len(content) < min_length:
                errors.append(f"Content too short (min: {min_length})")
        
        return errors
