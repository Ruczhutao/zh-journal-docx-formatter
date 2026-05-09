"""
Interactive template configuration wizard.
"""

import os
from typing import Optional, Dict, Any
import yaml

from .schema import (
    Template, PageConfig, FontStyle, ParagraphStyle, HeadingStyle,
    CitationConfig, ReferenceListConfig, CitationPosition, CitationStyle,
    NumberingType, Align
)


class TemplateWizard:
    """Interactive wizard for creating custom templates."""
    
    def __init__(self):
        self.config = {}
    
    def run(self) -> Template:
        """Run the interactive configuration wizard."""
        print("=== 论文格式配置向导 ===\n")
        
        # 1. 选择基础模板
        base = self._select_base_template()
        
        # 2. 页面设置
        self._configure_page(base)
        
        # 3. 标题样式
        self._configure_headings(base)
        
        # 4. 正文样式
        self._configure_body(base)
        
        # 5. 引注设置
        self._configure_citation(base)
        
        # 6. 参考文献
        self._configure_reference_list(base)
        
        return self._build_template(base)
    
    def _select_base_template(self) -> Dict[str, Any]:
        """Select a base template to start from."""
        print("请选择基础模板（可在此基础上修改）：")
        print("1) GB/T 7714 文中注 - 标准学术格式")
        print("2) GB/T 7714 页下注 - 脚注形式")
        print("3) 圆圈上标文中注 - 部分社科期刊常用")
        print("4) 完全自定义 - 从零开始")
        
        choice = input("\n选择 [1-4]: ").strip()
        
        templates = {
            "1": "gb7714-in-text",
            "2": "gb7714-footnote", 
            "3": "circled-in-text",
            "4": None
        }
        
        template_name = templates.get(choice, "gb7714-in-text")
        
        if template_name:
            return self._load_template_file(template_name)
        else:
            return self._default_config()
    
    def _load_template_file(self, name: str) -> Dict[str, Any]:
        """Load a preset template from file."""
        path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "templates", "presets", f"{name}.yaml"
        )
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Create default empty config."""
        return {
            "meta": {"name": "自定义模板", "description": "", "source": "custom"},
            "page": {},
            "heading_styles": {},
            "body_style": {},
            "citation": {},
            "reference_list": {}
        }
    
    def _configure_page(self, base: Dict[str, Any]):
        """Configure page settings."""
        print("\n--- 页面设置 ---")
        page = base.get("page", {})
        
        if self._confirm("修改页边距？", False):
            page["top_margin"] = input(f"上边距 [{page.get('top_margin', '2.54cm')}]: ").strip() or page.get("top_margin", "2.54cm")
            page["bottom_margin"] = input(f"下边距 [{page.get('bottom_margin', '2.54cm')}]: ").strip() or page.get("bottom_margin", "2.54cm")
            page["left_margin"] = input(f"左边距 [{page.get('left_margin', '3.17cm')}]: ").strip() or page.get("left_margin", "3.17cm")
            page["right_margin"] = input(f"右边距 [{page.get('right_margin', '3.17cm')}]: ").strip() or page.get("right_margin", "3.17cm")
        
        base["page"] = page
    
    def _configure_headings(self, base: Dict[str, Any]):
        """Configure heading styles."""
        print("\n--- 标题样式 ---")
        headings = base.get("heading_styles", {})
        
        for level in [1, 2, 3]:
            h = headings.get(str(level), {})
            font = h.get("font", {})
            
            print(f"\n【{self._level_name(level)}】")
            
            if self._confirm(f"修改 {self._level_name(level)} 样式？", False):
                font["font_family"] = input(f"字体 [{font.get('font_family', '黑体')}]: ").strip() or font.get("font_family", "黑体")
                font["font_size"] = input(f"字号 [{font.get('font_size', '14pt')}]: ").strip() or font.get("font_size", "14pt")
                
                print("编号方式：1) 中文'一、' 2) 中文'（一）' 3) 数字'1.' 4) 不编号")
                num_choice = input(f"选择 [1-4]: ").strip()
                numbering_map = {"1": "chinese", "2": "chinese_paren", "3": "arabic", "4": "none"}
                font["numbering"] = numbering_map.get(num_choice, font.get("numbering", "chinese"))
                
                h["font"] = font
                headings[str(level)] = h
        
        base["heading_styles"] = headings
    
    def _configure_body(self, base: Dict[str, Any]):
        """Configure body text style."""
        print("\n--- 正文样式 ---")
        body = base.get("body_style", {})
        font = body.get("font", {})
        
        if self._confirm("修改正文样式？", False):
            font["font_family"] = input(f"字体 [{font.get('font_family', '宋体')}]: ").strip() or font.get("font_family", "宋体")
            font["font_size"] = input(f"字号 [{font.get('font_size', '12pt')}]: ").strip() or font.get("font_size", "12pt")
            
            lh = input(f"行距倍数 [{body.get('line_height', 1.25)}]: ").strip()
            body["line_height"] = float(lh) if lh else body.get("line_height", 1.25)
            
            indent = input(f"首行缩进 [{body.get('first_line_indent', '2em')}]: ").strip()
            body["first_line_indent"] = indent if indent else body.get("first_line_indent", "2em")
            
            body["font"] = font
        
        base["body_style"] = body
    
    def _configure_citation(self, base: Dict[str, Any]):
        """Configure citation style."""
        print("\n--- 引注设置 ---")
        citation = base.get("citation", {})
        
        print("引注位置：1) 文中上标 2) 页下注 3) 尾注")
        pos_choice = input("选择 [1-3]: ").strip()
        pos_map = {"1": "in-text", "2": "footnote", "3": "endnote"}
        citation["position"] = pos_map.get(pos_choice, citation.get("position", "in-text"))
        
        print("引注样式：1) 数字[1] 2) 圆圈① 3) 作者年份")
        style_choice = input("选择 [1-3]: ").strip()
        style_map = {"1": "numbered", "2": "circled", "3": "author_year"}
        citation["style"] = style_map.get(style_choice, citation.get("style", "numbered"))
        
        base["citation"] = citation
    
    def _configure_reference_list(self, base: Dict[str, Any]):
        """Configure reference list."""
        print("\n--- 参考文献列表 ---")
        ref = base.get("reference_list", {})
        
        if self._confirm("生成文末参考文献列表？", ref.get("enabled", True)):
            ref["enabled"] = True
            
            print("排序方式：1) 首次出现顺序 2) 作者字母顺序")
            sort_choice = input("选择 [1-2]: ").strip()
            ref["sort_by"] = "appearance" if sort_choice == "1" else "author"
        else:
            ref["enabled"] = False
        
        base["reference_list"] = ref
    
    def _confirm(self, prompt: str, default: bool) -> bool:
        """Ask yes/no question."""
        suffix = " [Y/n]: " if default else " [y/N]: "
        response = input(prompt + suffix).strip().lower()
        if not response:
            return default
        return response in ('y', 'yes', '是', '1')
    
    def _level_name(self, level: int) -> str:
        """Get Chinese name for heading level."""
        names = {1: "一级标题", 2: "二级标题", 3: "三级标题"}
        return names.get(level, f"{level}级标题")
    
    def _build_template(self, config: Dict[str, Any]) -> Template:
        """Build Template object from config dict."""
        # TODO: Convert dict to Template dataclass
        # For now, return as-is for YAML serialization
        return config
    
    def save(self, config: Dict[str, Any], filepath: str):
        """Save configuration to YAML file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, sort_keys=False)
        print(f"\n配置已保存至: {filepath}")


def interactive_config():
    """Entry point for interactive configuration."""
    wizard = TemplateWizard()
    config = wizard.run()
    
    name = input("\n保存模板名称（不含扩展名）: ").strip()
    if not name:
        name = "custom"
    
    filepath = os.path.join("templates", "custom", f"{name}.yaml")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    wizard.save(config, filepath)
    
    return filepath


if __name__ == "__main__":
    interactive_config()
