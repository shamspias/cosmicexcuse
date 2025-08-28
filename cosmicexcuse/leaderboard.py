"""
Excuse leaderboard module for tracking and ranking excuses.
"""

import json
import sqlite3
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class LeaderboardEntry:
    """Represents a leaderboard entry."""

    excuse_text: str
    quality_score: int
    severity: str
    category: str
    language: str
    timestamp: float
    upvotes: int = 0
    downvotes: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def net_votes(self) -> int:
        """Calculate net votes (upvotes - downvotes)."""
        return self.upvotes - self.downvotes

    @property
    def controversy_score(self) -> float:
        """Calculate controversy score (high when votes are split)."""
        total_votes = self.upvotes + self.downvotes
        if total_votes == 0:
            return 0.0

        # Higher score when votes are evenly split
        ratio = min(self.upvotes, self.downvotes) / max(self.upvotes, self.downvotes, 1)
        return ratio * total_votes

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class ExcuseLeaderboard:
    """
    Manages a leaderboard of excuses with various ranking methods.
    """

    def __init__(self, max_size: int = 100, storage_path: Optional[Path] = None):
        """
        Initialize leaderboard.

        Args:
            max_size: Maximum number of entries to keep
            storage_path: Optional path for persistent storage
        """
        self.max_size = max_size
        self.entries: List[LeaderboardEntry] = []
        self.storage_path = storage_path

        # Load existing data if storage path provided
        if self.storage_path:
            self.load()

    def add_excuse(
        self,
        excuse_text: str,
        quality_score: int,
        severity: str = "medium",
        category: str = "general",
        language: str = "en",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> LeaderboardEntry:
        """
        Add an excuse to the leaderboard.

        Args:
            excuse_text: The excuse text
            quality_score: Quality score (0-100)
            severity: Severity level
            category: Excuse category
            language: Language code
            metadata: Additional metadata

        Returns:
            The created LeaderboardEntry
        """
        entry = LeaderboardEntry(
            excuse_text=excuse_text,
            quality_score=quality_score,
            severity=severity,
            category=category,
            language=language,
            timestamp=time.time(),
            metadata=metadata or {},
        )

        self.entries.append(entry)

        # Maintain max size
        if len(self.entries) > self.max_size:
            # Remove lowest quality score
            self.entries.sort(key=lambda x: x.quality_score, reverse=True)
            self.entries = self.entries[: self.max_size]

        # Save if storage enabled
        if self.storage_path:
            self.save()

        return entry

    def add_from_excuse_object(self, excuse) -> LeaderboardEntry:
        """
        Add from an Excuse object.

        Args:
            excuse: Excuse object from generator

        Returns:
            Created LeaderboardEntry
        """
        return self.add_excuse(
            excuse_text=excuse.text,
            quality_score=excuse.quality_score,
            severity=excuse.severity,
            category=excuse.category,
            language=excuse.language,
            metadata=excuse.metadata,
        )

    def vote(self, excuse_text: str, upvote: bool = True):
        """
        Vote on an excuse.

        Args:
            excuse_text: The excuse text to vote on
            upvote: True for upvote, False for downvote
        """
        for entry in self.entries:
            if entry.excuse_text == excuse_text:
                if upvote:
                    entry.upvotes += 1
                else:
                    entry.downvotes += 1

                if self.storage_path:
                    self.save()
                break

    def get_top_by_quality(self, n: int = 10) -> List[LeaderboardEntry]:
        """
        Get top excuses by quality score.

        Args:
            n: Number of entries to return

        Returns:
            List of top entries
        """
        sorted_entries = sorted(
            self.entries, key=lambda x: x.quality_score, reverse=True
        )
        return sorted_entries[:n]

    def get_top_by_votes(self, n: int = 10) -> List[LeaderboardEntry]:
        """
        Get top excuses by net votes.

        Args:
            n: Number of entries to return

        Returns:
            List of top entries
        """
        sorted_entries = sorted(self.entries, key=lambda x: x.net_votes, reverse=True)
        return sorted_entries[:n]

    def get_most_controversial(self, n: int = 10) -> List[LeaderboardEntry]:
        """
        Get most controversial excuses.

        Args:
            n: Number of entries to return

        Returns:
            List of most controversial entries
        """
        sorted_entries = sorted(
            self.entries, key=lambda x: x.controversy_score, reverse=True
        )
        return sorted_entries[:n]

    def get_recent(self, n: int = 10) -> List[LeaderboardEntry]:
        """
        Get most recent excuses.

        Args:
            n: Number of entries to return

        Returns:
            List of recent entries
        """
        sorted_entries = sorted(self.entries, key=lambda x: x.timestamp, reverse=True)
        return sorted_entries[:n]

    def get_by_category(self, category: str, n: int = 10) -> List[LeaderboardEntry]:
        """
        Get top excuses in a specific category.

        Args:
            category: Category to filter by
            n: Number of entries to return

        Returns:
            List of entries in category
        """
        filtered = [e for e in self.entries if e.category == category]
        sorted_entries = sorted(filtered, key=lambda x: x.quality_score, reverse=True)
        return sorted_entries[:n]

    def get_by_severity(self, severity: str, n: int = 10) -> List[LeaderboardEntry]:
        """
        Get top excuses by severity.

        Args:
            severity: Severity level to filter by
            n: Number of entries to return

        Returns:
            List of entries with severity
        """
        filtered = [e for e in self.entries if e.severity == severity]
        sorted_entries = sorted(filtered, key=lambda x: x.quality_score, reverse=True)
        return sorted_entries[:n]

    def get_stats(self) -> Dict[str, Any]:
        """
        Get leaderboard statistics.

        Returns:
            Dictionary with statistics
        """
        if not self.entries:
            return {
                "total_excuses": 0,
                "average_quality": 0,
                "categories": {},
                "severities": {},
                "languages": {},
            }

        total = len(self.entries)
        avg_quality = sum(e.quality_score for e in self.entries) / total

        # Count by category
        categories = {}
        for entry in self.entries:
            categories[entry.category] = categories.get(entry.category, 0) + 1

        # Count by severity
        severities = {}
        for entry in self.entries:
            severities[entry.severity] = severities.get(entry.severity, 0) + 1

        # Count by language
        languages = {}
        for entry in self.entries:
            languages[entry.language] = languages.get(entry.language, 0) + 1

        # Find best and worst
        best = (
            max(self.entries, key=lambda x: x.quality_score) if self.entries else None
        )
        worst = (
            min(self.entries, key=lambda x: x.quality_score) if self.entries else None
        )

        return {
            "total_excuses": total,
            "average_quality": avg_quality,
            "categories": categories,
            "severities": severities,
            "languages": languages,
            "best_excuse": best.excuse_text if best else None,
            "best_score": best.quality_score if best else None,
            "worst_excuse": worst.excuse_text if worst else None,
            "worst_score": worst.quality_score if worst else None,
            "total_upvotes": sum(e.upvotes for e in self.entries),
            "total_downvotes": sum(e.downvotes for e in self.entries),
        }

    def clear(self):
        """Clear all entries."""
        self.entries.clear()
        if self.storage_path:
            self.save()

    def save(self):
        """Save leaderboard to storage."""
        if not self.storage_path:
            return

        data = {
            "entries": [entry.to_dict() for entry in self.entries],
            "max_size": self.max_size,
            "timestamp": time.time(),
        }

        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self):
        """Load leaderboard from storage."""
        if not self.storage_path or not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.entries = [
                LeaderboardEntry(**entry) for entry in data.get("entries", [])
            ]

            # Maintain max size
            if len(self.entries) > self.max_size:
                self.entries = self.entries[: self.max_size]

        except Exception:
            # If loading fails, start fresh
            self.entries = []

    def export(self, format: str = "json") -> str:
        """
        Export leaderboard in specified format.

        Args:
            format: Export format ('json', 'csv', 'markdown')

        Returns:
            Exported data as string
        """
        if format == "json":
            return json.dumps(
                [entry.to_dict() for entry in self.entries],
                indent=2,
                ensure_ascii=False,
            )

        elif format == "csv":
            import csv
            from io import StringIO

            output = StringIO()
            writer = csv.writer(output)

            # Header
            writer.writerow(
                [
                    "Excuse",
                    "Score",
                    "Severity",
                    "Category",
                    "Language",
                    "Upvotes",
                    "Downvotes",
                    "Timestamp",
                ]
            )

            # Data
            for entry in self.entries:
                writer.writerow(
                    [
                        entry.excuse_text,
                        entry.quality_score,
                        entry.severity,
                        entry.category,
                        entry.language,
                        entry.upvotes,
                        entry.downvotes,
                        entry.timestamp,
                    ]
                )

            return output.getvalue()

        elif format == "markdown":
            lines = ["# Excuse Leaderboard\n"]

            # Top by quality
            lines.append("## Top by Quality Score\n")
            for i, entry in enumerate(self.get_top_by_quality(5), 1):
                lines.append(
                    f"{i}. **Score {entry.quality_score}**: {entry.excuse_text}"
                )

            lines.append("\n## Top by Votes\n")
            for i, entry in enumerate(self.get_top_by_votes(5), 1):
                lines.append(f"{i}. **+{entry.net_votes}**: {entry.excuse_text}")

            # Stats
            stats = self.get_stats()
            lines.append("\n## Statistics\n")
            lines.append(f"- Total Excuses: {stats['total_excuses']}")
            lines.append(f"- Average Quality: {stats['average_quality']:.1f}")

            return "\n".join(lines)

        else:
            raise ValueError(f"Unsupported format: {format}")


class GlobalLeaderboard(ExcuseLeaderboard):
    """
    Global leaderboard with database backend for persistence.
    """

    def __init__(self, db_path: Path):
        """
        Initialize global leaderboard with database.

        Args:
            db_path: Path to SQLite database
        """
        super().__init__(max_size=1000)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        with self._get_db() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS excuses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    excuse_text TEXT UNIQUE NOT NULL,
                    quality_score INTEGER NOT NULL,
                    severity TEXT NOT NULL,
                    category TEXT NOT NULL,
                    language TEXT NOT NULL,
                    upvotes INTEGER DEFAULT 0,
                    downvotes INTEGER DEFAULT 0,
                    timestamp REAL NOT NULL,
                    metadata TEXT
                )
            """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_quality
                ON excuses(quality_score DESC)
            """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_votes
                ON excuses(upvotes DESC, downvotes ASC)
            """
            )

    @contextmanager
    def _get_db(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
