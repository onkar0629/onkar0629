"""Analytics SVG generation entry point for future expansion."""

from __future__ import annotations

from generator.streak_generator import StreakMetrics
from generator.svg_renderer import SvgRenderer


class AnalyticsGenerator:
    """Generate analytics assets using the shared renderer."""

    def __init__(self, renderer: SvgRenderer) -> None:
        self.renderer = renderer

    def render(self, metrics: StreakMetrics) -> str:
        """Render the current analytics card."""

        return self.renderer.render_analytics_placeholder(metrics)
