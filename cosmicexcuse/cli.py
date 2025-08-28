"""
Command-line interface for CosmicExcuse.
"""

import argparse
import json
import sys
from typing import Optional

from cosmicexcuse import CosmicExcuse, __version__
from cosmicexcuse.exceptions import CosmicExcuseError


def print_banner():
    """Print a fancy banner."""
    banner = """
    ╔═══════════════════════════════════════╗
    ║      🚀 COSMIC EXCUSE GENERATOR 🚀    ║
    ║    When code fails, excuses prevail!  ║
    ╚═══════════════════════════════════════╝
    """
    print(banner)


def main(argv: Optional[list] = None):
    """
    Main CLI entry point.

    Args:
        argv: Command line arguments (for testing)
    """
    parser = argparse.ArgumentParser(
        description=(
            "Generate quantum-grade excuses for your code failures"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cosmicexcuse                           # Generate a random excuse
  cosmicexcuse -e "Segmentation fault"   # Generate excuse for specific error
  cosmicexcuse --haiku                   # Generate haiku excuse
  cosmicexcuse -l bn -c 3                # Generate 3 Bengali excuses
  cosmicexcuse --category quantum        # Generate quantum-specific excuse
        """,
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"CosmicExcuse {__version__}"
    )

    parser.add_argument(
        "-e",
        "--error",
        type=str,
        default="",
        help="Error message to generate excuse for",
    )

    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="en",
        choices=["en", "bn"],
        help="Language for excuses (en=English, bn=Bengali)",
    )

    parser.add_argument(
        "-c", "--count",
        type=int,
        default=1,
        help="Number of excuses to generate"
    )

    parser.add_argument(
        "--category",
        type=str,
        choices=["quantum", "cosmic", "ai", "technical", "blame"],
        help="Specific category of excuses",
    )

    parser.add_argument(
        "--haiku",
        action="store_true",
        help="Generate excuse in haiku format"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )

    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Skip the banner display"
    )

    parser.add_argument(
        "--show-score",
        action="store_true",
        help="Show quality score for excuses"
    )

    parser.add_argument(
        "--min-score",
        type=int,
        default=0,
        help="Minimum quality score (regenerate until met)",
    )

    args = parser.parse_args(argv)

    # Print banner unless disabled
    if not args.no_banner and not args.json:
        print_banner()

    try:
        # Initialize generator
        generator = CosmicExcuse(language=args.language)

        # Generate haiku if requested
        if args.haiku:
            haiku = generator.generate_haiku(args.error)
            if args.json:
                print(json.dumps(
                    {"haiku": haiku, "language": args.language}
                ))
            else:
                print("\n🎋 Haiku Excuse:\n")
                print(haiku)
                print()
            return 0

        # Generate regular excuses
        excuses = []

        for i in range(args.count):
            # Generate excuse with minimum score if specified
            attempts = 0
            max_attempts = 50

            while attempts < max_attempts:
                excuse = generator.generate(
                    error_message=args.error,
                    category=args.category
                )

                if excuse.quality_score >= args.min_score:
                    excuses.append(excuse)
                    break

                attempts += 1

            if attempts >= max_attempts:
                excuses.append(excuse)  # Use last one even if below score

        # Output results
        if args.json:
            output = []
            for excuse in excuses:
                output.append(
                    {
                        "text": excuse.text,
                        "recommendation": excuse.recommendation,
                        "severity": excuse.severity,
                        "category": excuse.category,
                        "quality_score": excuse.quality_score,
                        "language": excuse.language,
                    }
                )
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            for i, excuse in enumerate(excuses, 1):
                if args.count > 1:
                    print(f"\n{'=' * 50}")
                    print(f"Excuse #{i}")
                    print("=" * 50)

                print(f"\n💫 Excuse: {excuse.text}")
                print(f"\n💡 Recommendation: {excuse.recommendation}")

                if args.show_score:
                    print(f"\n📊 Quality Score: {excuse.quality_score}/100")
                    print(f"⚠️  Severity: {excuse.severity}")
                    print(f"📁 Category: {excuse.category}")

                if i < len(excuses):
                    print()

        return 0

    except CosmicExcuseError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())