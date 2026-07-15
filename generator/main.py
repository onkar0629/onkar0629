"""Command-line entry point for the GitHub profile engine."""

from __future__ import annotations

import logging
from pathlib import Path

from generator.analytics_generator import AnalyticsGenerator
from generator.config import load_settings
from generator.github_client import GitHubClient
from generator.streak_generator import StreakGenerator
from generator.svg_renderer import SvgRenderer


LOGGER = logging.getLogger(__name__)


def write_svg(path: Path, content: str) -> None:
    """Write SVG content atomically enough for GitHub Actions runs."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    LOGGER.info("Wrote %s", path)


def main() -> None:
    """Generate all profile SVG assets."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    settings = load_settings()
    client = GitHubClient(settings.token, settings.graphql_url)
    renderer = SvgRenderer(settings.theme)
    streak_generator = StreakGenerator(client, settings.username)
    metrics = streak_generator.generate()

    write_svg(settings.assets_dir / "streak.svg", renderer.render_streak(metrics))
    write_svg(
        settings.assets_dir / "analytics.svg",
        AnalyticsGenerator(renderer).render(metrics),
    )
    write_svg(settings.assets_dir / "divider.svg", renderer.render_divider())
    write_svg(settings.assets_dir / "footer.svg", renderer.render_footer())


if __name__ == "__main__":
    main()
