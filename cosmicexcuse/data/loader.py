"""
Data loader module for loading JSON excuse data.
"""

import json
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional

from cosmicexcuse.exceptions import DataLoadError, LanguageNotSupportedError


class DataLoader:
    """
    Loads excuse data from JSON files.
    """

    def __init__(self, language: str = "en", data_path: Optional[Path] = None):
        """
        Initialize data loader.

        Args:
            language: Language code ('en' or 'bn')
            data_path: Optional custom data path
        """
        self.language = language

        if data_path:
            self.data_path = Path(data_path)
        else:
            # Get the default data path relative to this file
            self.data_path = Path(__file__).parent / language

        if not self.data_path.exists():
            raise LanguageNotSupportedError(
                f"Data directory for language '{language}' not found at {self.data_path}"
            )

    def load_file(self, filename: str) -> Dict[str, Any]:
        """
        Load a single JSON file.

        Args:
            filename: Name of the JSON file (without extension)

        Returns:
            Dictionary containing the loaded data

        Raises:
            DataLoadError: If file cannot be loaded
        """
        file_path = self.data_path / f"{filename}.json"

        if not file_path.exists():
            warnings.warn(f"Data file {file_path} not found, using empty data")
            return {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Extract the excuses list if it exists
            if "excuses" in data:
                return data["excuses"]
            return data

        except json.JSONDecodeError as e:
            raise DataLoadError(f"Failed to parse JSON from {file_path}: {e}")
        except Exception as e:
            raise DataLoadError(f"Failed to load {file_path}: {e}")

    def load_all(self) -> Dict[str, List[str]]:
        """
        Load all excuse data files for the language.

        Returns:
            Dictionary mapping category names to lists of excuses
        """
        categories = [
            "quantum",
            "cosmic",
            "ai",
            "technical",
            "blame",
            "recommendations",
            "connectors",
            "intensifiers",
        ]

        data = {}

        for category in categories:
            try:
                loaded_data = self.load_file(category)
                if loaded_data:
                    data[category] = loaded_data
            except DataLoadError as e:
                warnings.warn(f"Failed to load {category}: {e}")
                # Provide fallback data
                data[category] = self._get_fallback_data(category)

        return data

    def _get_fallback_data(self, category: str) -> List[str]:
        """
        Provide fallback data if a category fails to load.

        Args:
            category: Category name

        Returns:
            List of fallback excuses
        """
        fallbacks = {
            "quantum": ["quantum interference"],
            "cosmic": ["cosmic ray interference"],
            "ai": ["AI malfunction"],
            "technical": ["technical difficulties"],
            "blame": ["unexpected behavior"],
            "recommendations": ["Try again later"],
            "connectors": ["which caused", "resulting in"],
            "intensifiers": {
                "mild": ["slightly"],
                "medium": ["definitely"],
                "severe": ["catastrophically"],
            },
        }

        return fallbacks.get(category, ["unknown error"])

    def get_available_languages(self) -> List[str]:
        """
        Get list of available languages.

        Returns:
            List of language codes
        """
        data_root = self.data_path.parent
        languages = []

        for path in data_root.iterdir():
            if path.is_dir() and not path.name.startswith("_"):
                languages.append(path.name)

        return languages

    def validate_data(self) -> Dict[str, bool]:
        """
        Validate that all expected data files exist and are valid.

        Returns:
            Dictionary mapping category names to validation status
        """
        categories = [
            "quantum",
            "cosmic",
            "ai",
            "technical",
            "blame",
            "recommendations",
            "connectors",
            "intensifiers",
        ]

        validation = {}

        for category in categories:
            file_path = self.data_path / f"{category}.json"

            if not file_path.exists():
                validation[category] = False
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Check if data has expected structure
                if "excuses" in data and isinstance(data["excuses"], list):
                    validation[category] = len(data["excuses"]) > 0
                elif isinstance(data, list):
                    validation[category] = len(data) > 0
                elif isinstance(data, dict):
                    validation[category] = True
                else:
                    validation[category] = False

            except Exception as e:
                print(str(e))
                validation[category] = False

        return validation
