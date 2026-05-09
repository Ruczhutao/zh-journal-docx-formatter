"""
Template validation utilities.
"""

from typing import Dict, List, Optional


class ValidationError(Exception):
    """Template validation error."""
    pass


class TemplateValidator:
    """Validate template configuration."""
    
    REQUIRED_SECTIONS = ["meta", "page", "heading_styles", "body_style", "citation", "reference_list"]
    
    VALID_CITATION_STYLES = ["numbered", "circled", "author_year"]
    VALID_CITATION_POSITIONS = ["in-text", "footnote", "endnote"]
    VALID_NUMBERING_TYPES = ["chinese", "chinese_paren", "arabic", "arabic_paren", "none"]
    VALID_ALIGNS = ["left", "center", "right", "justify"]
    
    def validate(self, config: Dict) -> List[str]:
        """Validate template configuration. Returns list of errors."""
        errors = []
        
        # Check required sections
        for section in self.REQUIRED_SECTIONS:
            if section not in config:
                errors.append(f"缺少必需部分: {section}")
        
        if errors:
            return errors
        
        # Validate meta
        errors.extend(self._validate_meta(config.get("meta", {})))
        
        # Validate page
        errors.extend(self._validate_page(config.get("page", {})))
        
        # Validate heading styles
        errors.extend(self._validate_headings(config.get("heading_styles", {})))
        
        # Validate body style
        errors.extend(self._validate_body(config.get("body_style", {})))
        
        # Validate citation
        errors.extend(self._validate_citation(config.get("citation", {})))
        
        # Validate reference list
        errors.extend(self._validate_reference_list(config.get("reference_list", {})))
        
        return errors
    
    def _validate_meta(self, meta: Dict) -> List[str]:
        errors = []
        if "name" not in meta:
            errors.append("meta.name 是必需的")
        return errors
    
    def _validate_page(self, page: Dict) -> List[str]:
        errors = []
        # Page config is mostly optional with defaults
        return errors
    
    def _validate_headings(self, headings: Dict) -> List[str]:
        errors = []
        for level, style in headings.items():
            if "font" not in style:
                errors.append(f"heading_styles.{level} 缺少 font 定义")
            else:
                font = style["font"]
                if "font_family" not in font:
                    errors.append(f"heading_styles.{level}.font.font_family 是必需的")
                if "font_size" not in font:
                    errors.append(f"heading_styles.{level}.font.font_size 是必需的")
            
            numbering = style.get("numbering", "")
            if numbering and numbering not in self.VALID_NUMBERING_TYPES:
                errors.append(f"heading_styles.{level}.numbering '{numbering}' 无效，应为: {', '.join(self.VALID_NUMBERING_TYPES)}")
            
            align = style.get("align", "")
            if align and align not in self.VALID_ALIGNS:
                errors.append(f"heading_styles.{level}.align '{align}' 无效")
        
        return errors
    
    def _validate_body(self, body: Dict) -> List[str]:
        errors = []
        if "font" not in body:
            errors.append("body_style 缺少 font 定义")
        else:
            font = body["font"]
            if "font_family" not in font:
                errors.append("body_style.font.font_family 是必需的")
            if "font_size" not in font:
                errors.append("body_style.font.font_size 是必需的")
        
        return errors
    
    def _validate_citation(self, citation: Dict) -> List[str]:
        errors = []
        
        style = citation.get("style", "")
        if style not in self.VALID_CITATION_STYLES:
            errors.append(f"citation.style '{style}' 无效，应为: {', '.join(self.VALID_CITATION_STYLES)}")
        
        position = citation.get("position", "")
        if position not in self.VALID_CITATION_POSITIONS:
            errors.append(f"citation.position '{position}' 无效，应为: {', '.join(self.VALID_CITATION_POSITIONS)}")
        
        return errors
    
    def _validate_reference_list(self, ref_list: Dict) -> List[str]:
        errors = []
        sort_by = ref_list.get("sort_by", "")
        if sort_by and sort_by not in ["appearance", "author"]:
            errors.append("reference_list.sort_by 应为 'appearance' 或 'author'")
        
        return errors
    
    def is_valid(self, config: Dict) -> bool:
        """Check if config is valid."""
        return len(self.validate(config)) == 0


def validate_template(config: Dict) -> List[str]:
    """Convenience function to validate template."""
    validator = TemplateValidator()
    return validator.validate(config)
