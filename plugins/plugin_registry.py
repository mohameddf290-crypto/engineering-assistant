"""
Plugin Registry — Registry of all available plugins.
DEFAULT AI THINKING: ANNIHILATED. Custom protocols below.

This module maintains a live registry of every plugin the user has
installed and available. It tracks plugin capabilities (preset support,
synthesis capability, macro availability, analyser output format) and
provides a query interface so other brains can ask "which plugins can
do X?" and receive an authoritative, complete answer.

Protocol:
  1. Scan plugin directories and register every discovered plugin.
  2. For each plugin, capture: name, type, capabilities, preset count,
     manual path, and synthesis capability flag.
  3. Provide capability-based queries (e.g. find all plugins with
     a compressor stage, all synthesis-capable plugins, etc.).
  4. Keep the registry updated — new plugins added mid-session are
     detected and registered automatically.
"""

# TODO: Design this brain with Cursor — define the plugin capability
# taxonomy, the registry schema, and the capability query interface
# before writing any real implementation.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class PluginRecord:
    """
    A single plugin entry in the registry.

    Attributes:
        plugin_id: Unique identifier (e.g. "fabfilter_pro_q3").
        name: Display name (e.g. "FabFilter Pro-Q 3").
        plugin_type: "VST2", "VST3", "AU", or "AAX".
        file_path: Absolute path to the plugin file.
        capabilities: List of capability tags (e.g. "eq", "compressor",
            "synthesis", "saturation", "reverb", "analyser", etc.).
        synthesis_capable: True if this plugin can create sounds from scratch.
        has_macro_knobs: True if this plugin has tweakable macro parameters.
        preset_count: Number of presets available.
        manual_path: Path to the ingested manual (if available).
        version: Plugin version string.
    """

    plugin_id: str
    name: str
    plugin_type: str
    file_path: str
    capabilities: List[str] = field(default_factory=list)
    synthesis_capable: bool = False
    has_macro_knobs: bool = False
    preset_count: int = 0
    manual_path: Optional[str] = None
    version: Optional[str] = None


class PluginRegistry:
    """
    Registry of all available plugins.

    Maintains a complete, capability-indexed registry of every plugin
    the user has installed, queryable by name, type, or capability.
    """

    def __init__(self) -> None:
        self._registry: Dict[str, PluginRecord] = {}

    # ── Registration ─────────────────────────────────────────────────────────

    def scan_and_register(self, scan_paths: List[str]) -> None:
        """
        Scan plugin directories and register all discovered plugins.

        TODO: Walk each scan_path, detect plugin files (DLL/VST3/component),
        extract metadata, build PluginRecord objects, and add them to
        the registry. Log every registered plugin and every skipped file.
        """
        raise NotImplementedError(
            "TODO: Implement plugin directory scanning and registration."
        )

    def register(self, record: PluginRecord) -> None:
        """Manually register a single plugin record."""
        self._registry[record.plugin_id] = record

    # ── Queries ───────────────────────────────────────────────────────────────

    def get(self, plugin_id: str) -> Optional[PluginRecord]:
        """Retrieve a plugin record by ID."""
        return self._registry.get(plugin_id)

    def get_by_name(self, name: str) -> Optional[PluginRecord]:
        """Retrieve a plugin record by display name."""
        for record in self._registry.values():
            if record.name.lower() == name.lower():
                return record
        return None

    def find_by_capability(self, capability: str) -> List[PluginRecord]:
        """
        Return all plugins that have the specified capability.

        TODO: Filter and return all registered plugins whose capabilities
        list contains the requested capability tag.
        """
        return [r for r in self._registry.values() if capability in r.capabilities]

    def find_synthesis_capable(self) -> List[PluginRecord]:
        """Return all synthesis-capable plugins."""
        return [r for r in self._registry.values() if r.synthesis_capable]

    def all_plugins(self) -> List[PluginRecord]:
        """Return all registered plugin records."""
        return list(self._registry.values())
