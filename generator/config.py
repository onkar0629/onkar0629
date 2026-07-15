"""Runtime configuration for the GitHub profile engine."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - only used before dependencies install.
    def load_dotenv() -> bool:
        """No-op fallback for environments before requirements are installed."""

        return False


load_dotenv()


@dataclass(frozen=True)
class Theme:
    """Shared visual design tokens for all generated SVG assets."""

    background: str = "#0D1117"
    primary: str = "#00D4FF"
    secondary: str = "#58A6FF"
    accent: str = "#7C3AED"
    text: str = "#F8FAFC"
    muted: str = "#8B949E"


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    username: str
    token: str
    graphql_url: str
    repository_root: Path
    assets_dir: Path
    theme: Theme


def _github_username() -> str:
    explicit_username = os.getenv("GITHUB_USERNAME")
    if explicit_username:
        return explicit_username

    repository = os.getenv("GITHUB_REPOSITORY", "")
    owner = repository.split("/", maxsplit=1)[0].strip()
    if owner:
        return owner

    return "onkar0629"


def load_settings() -> Settings:
    """Load validated settings for local runs and GitHub Actions."""

    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        raise RuntimeError(
            "GITHUB_TOKEN is required. In GitHub Actions, pass "
            "secrets.GITHUB_TOKEN to the generator step."
        )

    repository_root = Path(__file__).resolve().parent.parent
    assets_dir = repository_root / "assets"

    return Settings(
        username=_github_username(),
        token=token,
        graphql_url=os.getenv("GITHUB_GRAPHQL_URL", "https://api.github.com/graphql"),
        repository_root=repository_root,
        assets_dir=assets_dir,
        theme=Theme(),
    )
