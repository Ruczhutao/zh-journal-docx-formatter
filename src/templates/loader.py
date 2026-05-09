"""
Template loader with fuzzy matching support.
"""

import os
import glob
from typing import Optional, Dict, List
import yaml

from .schema import Template


class TemplateLoader:
    """Load and manage formatting templates."""
    
    def __init__(self, templates_dir: Optional[str] = None):
        if templates_dir is None:
            # Default to project root templates directory
            self.templates_dir = os.path.join(
                os.path.dirname(__file__), "..", "..", "templates"
            )
        else:
            self.templates_dir = templates_dir
        
        self.presets_dir = os.path.join(self.templates_dir, "presets")
        self.journals_dir = os.path.join(self.templates_dir, "journals")
        self.custom_dir = os.path.join(self.templates_dir, "custom")
        
        # Ensure directories exist
        for d in [self.presets_dir, self.journals_dir, self.custom_dir]:
            os.makedirs(d, exist_ok=True)
    
    def list_presets(self) -> List[Dict[str, str]]:
        """List all available preset templates."""
        return self._list_templates_in_dir(self.presets_dir)
    
    def list_journals(self) -> List[Dict[str, str]]:
        """List all available journal templates."""
        return self._list_templates_in_dir(self.journals_dir)
    
    def list_custom(self) -> List[Dict[str, str]]:
        """List all custom templates."""
        return self._list_templates_in_dir(self.custom_dir)
    
    def _list_templates_in_dir(self, directory: str) -> List[Dict[str, str]]:
        """List templates in a directory."""
        templates = []
        for filepath in glob.glob(os.path.join(directory, "*.yaml")):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                meta = data.get("meta", {})
                templates.append({
                    "name": meta.get("name", os.path.basename(filepath)),
                    "description": meta.get("description", ""),
                    "filename": os.path.basename(filepath),
                    "path": filepath,
                    "source": meta.get("source", "unknown")
                })
            except Exception:
                continue
        return templates
    
    def load(self, name: str) -> Optional[Dict]:
        """Load template by name with fuzzy matching."""
        # 1. Exact match in presets
        filepath = os.path.join(self.presets_dir, f"{name}.yaml")
        if os.path.exists(filepath):
            return self._load_yaml(filepath)
        
        # 2. Exact match in journals
        filepath = os.path.join(self.journals_dir, f"{name}.yaml")
        if os.path.exists(filepath):
            return self._load_yaml(filepath)
        
        # 3. Exact match in custom
        filepath = os.path.join(self.custom_dir, f"{name}.yaml")
        if os.path.exists(filepath):
            return self._load_yaml(filepath)
        
        # 4. Fuzzy match
        candidates = []
        candidates.extend(self.list_presets())
        candidates.extend(self.list_journals())
        candidates.extend(self.list_custom())
        
        # Try matching by name
        for candidate in candidates:
            if name.lower() in candidate["name"].lower() or \
               candidate["name"].lower() in name.lower():
                return self._load_yaml(candidate["path"])
        
        # Try matching by filename without extension
        for candidate in candidates:
            filename_no_ext = os.path.splitext(candidate["filename"])[0]
            if name.lower() == filename_no_ext.lower():
                return self._load_yaml(candidate["path"])
        
        return None
    
    def _load_yaml(self, filepath: str) -> Dict:
        """Load YAML file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get_all_templates(self) -> List[Dict[str, str]]:
        """Get all available templates."""
        all_templates = []
        all_templates.extend(self.list_presets())
        all_templates.extend(self.list_journals())
        all_templates.extend(self.list_custom())
        return all_templates
    
    def print_available(self):
        """Print all available templates."""
        presets = self.list_presets()
        journals = self.list_journals()
        custom = self.list_custom()
        
        print("=== 可用模板 ===\n")
        
        if presets:
            print("【预设模板】")
            for t in presets:
                print(f"  • {t['name']}")
                if t['description']:
                    print(f"    {t['description']}")
            print()
        
        if journals:
            print("【期刊模板】")
            for t in journals:
                print(f"  • {t['name']}")
                if t['description']:
                    print(f"    {t['description']}")
            print()
        
        if custom:
            print("【自定义模板】")
            for t in custom:
                print(f"  • {t['name']}")
            print()


if __name__ == "__main__":
    loader = TemplateLoader()
    loader.print_available()
