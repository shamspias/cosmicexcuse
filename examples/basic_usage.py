"""
Basic usage examples for CosmicExcuse package.
"""

from cosmicexcuse import CosmicExcuse, generate
from cosmicexcuse.analyzer import SeverityAnalyzer
from cosmicexcuse.formatter import (
    MarkdownFormatter,
    TwitterFormatter,
)
from cosmicexcuse.leaderboard import ExcuseLeaderboard


def basic_generation():
    """Basic excuse generation examples."""
    print("=" * 60)
    print("BASIC EXCUSE GENERATION")
    print("=" * 60)

    # Create generator
    generator = CosmicExcuse()

    # Generate simple excuse
    excuse = generator.generate()
    print("\n📝 Random Excuse:")
    print(f"   {excuse.text}")
    print("   💡 Tip: {excuse.recommendation}")

    # Generate for specific error
    excuse = generator.generate("NullPointerException in UserService.java")
    print("\n🎯 Specific Error Excuse:")
    print(f"   {excuse.text}")
    print(f"   Severity: {excuse.severity}")
    print("   Score: {excuse.quality_score}/100")

    # Generate with category
    excuse = generator.generate(category="quantum")
    print("\n🔬 Quantum Category Excuse:")
    print(f"   {excuse.text}")


def one_liner_examples():
    """One-liner usage examples."""
    print("\n" + "=" * 60)
    print("ONE-LINER EXAMPLES")
    print("=" * 60)

    # Quick generation
    print(f"\n🚀 Quick excuse: {generate()}")

    # With error message
    print(f"\n💥 For error: {generate('Segmentation fault')}")


def batch_generation():
    """Batch generation examples."""
    print("\n" + "=" * 60)
    print("BATCH GENERATION")
    print("=" * 60)

    generator = CosmicExcuse()
    excuses = generator.generate_batch(3)

    print("\n📦 Generated 3 excuses:")
    for i, excuse in enumerate(excuses, 1):
        print(f"\n   {i}. {excuse.text}")
        print(f"      Category: {excuse.category}, Score: {excuse.quality_score}")


def haiku_mode():
    """Haiku generation examples."""
    print("\n" + "=" * 60)
    print("HAIKU MODE")
    print("=" * 60)

    generator = CosmicExcuse()
    haiku = generator.generate_haiku("Memory leak detected")

    print("\n🎋 Error Haiku:")
    print("   " + haiku.replace("\n", "\n   "))


def severity_analysis():
    """Severity analysis examples."""
    print("\n" + "=" * 60)
    print("SEVERITY ANALYSIS")
    print("=" * 60)

    analyzer = SeverityAnalyzer()
    generator = CosmicExcuse()

    errors = [
        "Warning: deprecated function used",
        "ERROR: Connection timeout",
        "FATAL: System crash! Database corrupted!!!",
    ]

    for error in errors:
        severity = analyzer.analyze(error)
        excuse = generator.generate(error)

        print(f"\n📊 Error: {error}")
        print(f"   Severity: {severity}")
        print(f"   Excuse: {excuse.text[:100]}...")


def formatting_examples():
    """Different formatting examples."""
    print("\n" + "=" * 60)
    print("FORMATTING OPTIONS")
    print("=" * 60)

    generator = CosmicExcuse()
    excuse = generator.generate("Database connection failed")

    # Markdown format
    md_formatter = MarkdownFormatter()
    md_output = md_formatter.format(
        {
            "text": excuse.text,
            "recommendation": excuse.recommendation,
            "severity": excuse.severity,
            "category": excuse.category,
            "quality_score": excuse.quality_score,
            "quantum_probability": excuse.quantum_probability,
            "metadata": excuse.metadata,
        }
    )

    print("\n📄 Markdown Format:")
    print(md_output[:300] + "...")

    # Twitter format
    twitter_formatter = TwitterFormatter()
    tweet = twitter_formatter.format({"text": excuse.text})

    print(f"\n🐦 Twitter Format ({len(tweet)} chars):")
    print(f"   {tweet}")


def leaderboard_examples():
    """Leaderboard usage examples."""
    print("\n" + "=" * 60)
    print("LEADERBOARD SYSTEM")
    print("=" * 60)

    generator = CosmicExcuse()
    leaderboard = ExcuseLeaderboard()

    # Generate and add excuses
    print("\n🏆 Generating excuses for leaderboard...")
    for i in range(10):
        excuse = generator.generate(f"Error {i}")
        leaderboard.add_from_excuse_object(excuse)

    # Get top excuses
    top_excuses = leaderboard.get_top_by_quality(3)

    print("\n📊 Top 3 Excuses by Quality:")
    for i, entry in enumerate(top_excuses, 1):
        print(f"\n   {i}. Score {entry.quality_score}: {entry.excuse_text[:80]}...")

    # Get statistics
    stats = leaderboard.get_stats()
    print("\n📈 Statistics:")
    print(f"   Total excuses: {stats['total_excuses']}")
    print(f"   Average quality: {stats['average_quality']:.1f}")
    print(f"   Categories: {stats['categories']}")


def history_tracking():
    """History tracking examples."""
    print("\n" + "=" * 60)
    print("HISTORY TRACKING")
    print("=" * 60)

    generator = CosmicExcuse()

    # Generate some excuses
    print("\n📚 Generating excuses with history...")
    for i in range(5):
        generator.generate(f"Historical error {i}")

    # Get best excuse
    best = generator.get_best_excuse()
    if best:
        print(f"\n🥇 Best excuse (score {best.quality_score}):")
        print(f"   {best.text}")

    # Export history
    print(f"\n📤 Exported {len(generator.history)} excuses to JSON")

    # Clear history
    generator.clear_history()
    print("🗑️  History cleared")


def multi_language():
    """Multi-language examples."""
    print("\n" + "=" * 60)
    print("MULTI-LANGUAGE SUPPORT")
    print("=" * 60)

    # English
    en_gen = CosmicExcuse(language="en")
    en_excuse = en_gen.generate("Database error")
    print(f"\n🇬🇧 English: {en_excuse.text}")

    # Bengali (if available)
    try:
        bn_gen = CosmicExcuse(language="bn")
        bn_excuse = bn_gen.generate("ডাটাবেস ত্রুটি")
        print(f"\n🇧🇩 Bengali: {bn_excuse.text}")
    except Exception as e:
        print(f"\n🇧🇩 Bengali: Data not available ({e})")


def error_handler_integration():
    """Example of integrating with error handling."""
    print("\n" + "=" * 60)
    print("ERROR HANDLER INTEGRATION")
    print("=" * 60)

    generator = CosmicExcuse()

    def risky_operation():
        """Simulate a risky operation."""
        raise ValueError("Division by coffee not allowed!")

    def handle_with_excuse(func):
        """Decorator to handle errors with excuses."""

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                excuse = generator.generate(str(e))
                print(f"\n⚠️  Error occurred: {e}")
                print(f"🎭 Official explanation: {excuse.text}")
                print(f"💡 Suggested fix: {excuse.recommendation}")
                return None

        return wrapper

    @handle_with_excuse
    def safe_operation():
        return risky_operation()

    # This will trigger the error handler
    safe_operation()


def main():
    """Run all examples."""
    print("\n" + "🚀" * 30)
    print(" COSMICEXCUSE EXAMPLES SHOWCASE")
    print("🚀" * 30)

    examples = [
        ("Basic Generation", basic_generation),
        ("One-Liners", one_liner_examples),
        ("Batch Generation", batch_generation),
        ("Haiku Mode", haiku_mode),
        ("Severity Analysis", severity_analysis),
        ("Formatting Options", formatting_examples),
        ("Leaderboard System", leaderboard_examples),
        ("History Tracking", history_tracking),
        ("Multi-Language", multi_language),
        ("Error Handler", error_handler_integration),
    ]

    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n❌ Example '{name}' failed: {e}")

    print("\n" + "=" * 60)
    print("✅ EXAMPLES COMPLETE!")
    print("=" * 60)
    print("\nRemember: It's not a bug, it's a quantum feature! 🐛✨")


if __name__ == "__main__":
    main()
