"""SVG rendering utilities for the GitHub profile engine."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timezone
from html import escape

from generator.config import Theme
from generator.streak_generator import StreakMetrics


@dataclass(frozen=True)
class MetricBox:
    """A single dashboard metric displayed in an SVG card."""

    label: str
    value: str
    x: int
    y: int
    width: int
    accent: str


class SvgRenderer:
    """Render profile SVG assets using a shared visual system."""

    def __init__(self, theme: Theme) -> None:
        self.theme = theme

    def render_streak(self, metrics: StreakMetrics) -> str:
        """Render the custom GitHub streak dashboard card."""

        updated = self._updated(metrics)
        boxes = [
            MetricBox("Current Streak", f"{metrics.current_streak} days", 64, 148, 206, self.theme.primary),
            MetricBox("Longest Streak", f"{metrics.longest_streak} days", 292, 148, 206, self.theme.secondary),
            MetricBox("Today's Contributions", f"{metrics.contributions_today:,}", 520, 148, 228, self.theme.accent),
            MetricBox("Total Contributions", f"{metrics.total_contributions:,}", 770, 148, 206, self.theme.primary),
            MetricBox("Updated", updated, 998, 148, 138, self.theme.secondary),
        ]

        return self._document(
            width=1200,
            height=300,
            body=f"""
  <defs>{self._shared_defs()}{self._glow_def()}</defs>
  <rect width="1200" height="300" rx="28" fill="{self.theme.background}"/>
  <rect x="1.5" y="1.5" width="1197" height="297" rx="26.5" fill="none" stroke="url(#borderGradient)" stroke-width="3" opacity="0.86" filter="url(#glow)"/>
  {self._grid(1200, 300, step=100)}
  {self._pipeline(64, 108, 422, 78, 860, 108, 1136)}
  <text x="64" y="62" font-family="Segoe UI, Arial, sans-serif" font-size="30" font-weight="700" fill="{self.theme.text}">GITHUB STREAK</text>
  <text x="66" y="92" font-family="Segoe UI, Arial, sans-serif" font-size="16" fill="{self.theme.muted}">Consistency Builds Excellence</text>
  {''.join(self._metric_box(box) for box in boxes)}
  <path d="M64 260H1136" stroke="url(#borderGradient)" stroke-width="2" stroke-linecap="round" opacity="0.62"/>
  <text x="64" y="280" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="{self.theme.muted}">Generated daily with GitHub Actions and GitHub GraphQL API</text>
""",
        )

    def render_analytics(self, metrics: StreakMetrics) -> str:
        """Render the custom GitHub analytics dashboard card."""

        updated = self._updated(metrics)
        boxes = [
            MetricBox("Repositories", f"{metrics.repositories:,}", 64, 148, 148, self.theme.primary),
            MetricBox("Followers", f"{metrics.followers:,}", 228, 148, 148, self.theme.secondary),
            MetricBox("Following", f"{metrics.following:,}", 392, 148, 148, self.theme.accent),
            MetricBox("Stars", f"{metrics.stars:,}", 556, 148, 148, self.theme.primary),
            MetricBox("Commits", f"{metrics.commits:,}", 720, 148, 148, self.theme.secondary),
            MetricBox("Contributions", f"{metrics.total_contributions:,}", 884, 148, 252, self.theme.accent),
        ]

        return self._document(
            width=1200,
            height=360,
            body=f"""
  <defs>{self._shared_defs()}{self._glow_def()}</defs>
  <rect width="1200" height="360" rx="28" fill="{self.theme.background}"/>
  <rect x="1.5" y="1.5" width="1197" height="357" rx="26.5" fill="none" stroke="url(#borderGradient)" stroke-width="3" opacity="0.86" filter="url(#glow)"/>
  {self._grid(1200, 360, step=96)}
  {self._pipeline(64, 112, 404, 82, 860, 112, 1136)}
  <text x="64" y="64" font-family="Segoe UI, Arial, sans-serif" font-size="30" font-weight="700" fill="{self.theme.text}">GITHUB ANALYTICS</text>
  <text x="66" y="94" font-family="Segoe UI, Arial, sans-serif" font-size="16" fill="{self.theme.muted}">Repository signal and contribution overview</text>
  {''.join(self._metric_box(box) for box in boxes)}
  <g>
    <rect x="64" y="248" width="1072" height="58" rx="16" fill="{self.theme.background}" stroke="{self.theme.secondary}" stroke-width="1.2" opacity="0.96"/>
    <rect x="64" y="248" width="1072" height="58" rx="16" fill="{self.theme.secondary}" opacity="0.05"/>
    <text x="88" y="283" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="{self.theme.muted}">Last Updated</text>
    <text x="240" y="284" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="700" fill="{self.theme.text}">{escape(updated)}</text>
    <text x="934" y="284" text-anchor="end" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="{self.theme.muted}">GitHub GraphQL API only</text>
  </g>
  <path d="M64 328H1136" stroke="url(#borderGradient)" stroke-width="2" stroke-linecap="round" opacity="0.62"/>
""",
        )

    def render_divider(self) -> str:
        """Render a compact animated divider."""

        return self._document(
            width=1200,
            height=80,
            body=f"""
  <defs>{self._shared_defs()}</defs>
  <rect width="1200" height="80" fill="{self.theme.background}"/>
  <path d="M60 40 H1140" stroke="url(#borderGradient)" stroke-width="3"
        stroke-linecap="round"/>
  <circle cx="600" cy="40" r="8" fill="{self.theme.primary}">
    <animate attributeName="r" values="8;13;8" dur="3s" repeatCount="indefinite"/>
  </circle>
""",
        )

    def render_footer(self) -> str:
        """Render the local footer SVG displayed by README."""

        return self._document(
            width=1200,
            height=140,
            body=f"""
  <defs>{self._shared_defs()}</defs>
  <rect width="1200" height="140" fill="{self.theme.background}"/>
  <path d="M0 96 C220 42 360 142 560 86 S900 42 1200 92 V140 H0 Z"
        fill="{self.theme.accent}" opacity="0.24"/>
  <path d="M0 104 C240 50 410 132 610 78 S940 58 1200 102"
        fill="none" stroke="{self.theme.primary}" stroke-width="3" opacity="0.82"/>
  <text x="600" y="54" text-anchor="middle"
        font-family="Segoe UI, Arial, sans-serif" font-size="22"
        font-weight="700" fill="{self.theme.text}">Made with GitHub Actions by Onkar Jadhav</text>
  <text x="600" y="82" text-anchor="middle"
        font-family="Segoe UI, Arial, sans-serif" font-size="14"
        fill="{self.theme.muted}">Learning today. Building tomorrow.</text>
""",
        )

    def _metric_box(self, box: MetricBox) -> str:
        value_size = 19 if len(box.value) > 14 else 30
        return f"""
  <g>
    <rect x="{box.x}" y="{box.y}" width="{box.width}" height="82" rx="16"
          fill="{self.theme.background}" stroke="{box.accent}" stroke-width="1.5"
          opacity="0.96"/>
    <rect x="{box.x}" y="{box.y}" width="{box.width}" height="82" rx="16"
          fill="{box.accent}" opacity="0.06"/>
    <text x="{box.x + 20}" y="{box.y + 30}" font-family="Segoe UI, Arial, sans-serif"
          font-size="13" fill="{self.theme.muted}">{escape(box.label)}</text>
    <text x="{box.x + 20}" y="{box.y + 62}" font-family="Segoe UI, Arial, sans-serif"
          font-size="{value_size}" font-weight="700" fill="{self.theme.text}">{escape(box.value)}</text>
  </g>
"""

    def _shared_defs(self) -> str:
        return f"""
    <linearGradient id="borderGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{self.theme.primary}"/>
      <stop offset="52%" stop-color="{self.theme.secondary}"/>
      <stop offset="100%" stop-color="{self.theme.accent}"/>
</linearGradient>
"""

    @staticmethod
    def _glow_def() -> str:
        return """
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
"""

    def _grid(self, width: int, height: int, step: int = 80) -> str:
        vertical = "\n".join(
            f'    <path d="M{x} 0 V{height}"/>' for x in range(step, width, step)
        )
        horizontal = "\n".join(
            f'    <path d="M0 {y} H{width}"/>' for y in range(step // 2, height, step // 2)
        )
        return f"""
  <g opacity="0.07" stroke="{self.theme.muted}" stroke-width="1">
{horizontal}
{vertical}
  </g>
"""

    def _pipeline(
        self,
        start_x: int,
        start_y: int,
        bend_x: int,
        bend_y: int,
        final_x: int,
        final_y: int,
        end_x: int,
    ) -> str:
        path = (
            f"M{start_x} {start_y}H{bend_x - 80}"
            f"C{bend_x - 40} {start_y} {bend_x - 40} {bend_y} {bend_x} {bend_y}"
            f"H{final_x - 80}"
            f"C{final_x - 40} {bend_y} {final_x - 40} {final_y} {final_x} {final_y}"
            f"H{end_x}"
        )
        return f"""
  <path d="{path}" fill="none" stroke="url(#borderGradient)" stroke-width="3" stroke-linecap="round" opacity="0.72"
        stroke-dasharray="18 14">
    <animate attributeName="stroke-dashoffset" values="0;-64" dur="5s" repeatCount="indefinite"/>
  </path>
  <circle r="5" fill="{self.theme.primary}" filter="url(#glow)">
    <animateMotion dur="7s" repeatCount="indefinite" path="{path}"/>
    <animate attributeName="opacity" values="0.35;1;0.35" dur="7s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{start_x}" cy="{start_y}" r="6" fill="{self.theme.primary}"/>
  <circle cx="{bend_x}" cy="{bend_y}" r="6" fill="{self.theme.secondary}"/>
  <circle cx="{final_x}" cy="{final_y}" r="6" fill="{self.theme.accent}"/>
"""

    @staticmethod
    def _updated(metrics: StreakMetrics) -> str:
        return metrics.last_updated.astimezone(timezone.utc).strftime("%b %d %H:%M UTC")

    @staticmethod
    def _document(width: int, height: int, body: str) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}" '
            'role="img" aria-labelledby="title desc">\n'
            "  <title id=\"title\">Onkar Jadhav GitHub Profile Asset</title>\n"
            "  <desc id=\"desc\">Generated SVG asset for the onkar0629 GitHub profile.</desc>\n"
            f"{body}\n"
            "</svg>\n"
        )
