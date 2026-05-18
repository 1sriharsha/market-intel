"""
Smoke test all configured feeds before deployment.
Run: python scripts/validate_sources.py
Prints PASS/FAIL per feed and exits non-zero if any required feeds fail.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import structlog

log = structlog.get_logger()


async def validate():
    from ingestion.rss_fetcher import fetch_feed, FeedFetchError, FeedParseError
    from config.sources import ALL_RSS_FEEDS, TIER1_FEEDS

    results: list[dict] = []
    required_feed_ids = {f.id for f in TIER1_FEEDS}

    import asyncio
    semaphore = asyncio.Semaphore(5)

    async def check_one(feed):
        async with semaphore:
            try:
                articles = await fetch_feed(feed)
                status = "PASS" if articles else "WARN_EMPTY"
                count = len(articles)
            except (FeedFetchError, FeedParseError) as e:
                status = "FAIL"
                count = 0
                return {"id": feed.id, "name": feed.name, "tier": feed.tier,
                        "status": status, "count": count, "error": str(e)}
            except Exception as e:
                status = "FAIL"
                count = 0
                return {"id": feed.id, "name": feed.name, "tier": feed.tier,
                        "status": status, "count": count, "error": str(e)}
            return {"id": feed.id, "name": feed.name, "tier": feed.tier,
                    "status": status, "count": count, "error": None}

    checks = await asyncio.gather(*[check_one(f) for f in ALL_RSS_FEEDS])
    results = list(checks)

    # Print results
    print("\n=== FEED VALIDATION RESULTS ===\n")
    required_failures = 0
    for r in sorted(results, key=lambda x: x["tier"]):
        icon = "✓" if r["status"] == "PASS" else ("⚠" if "WARN" in r["status"] else "✗")
        print(f"  {icon} [{r['tier']}] {r['name'][:50]:<50} {r['status']:10} ({r['count']} articles)")
        if r["error"]:
            print(f"       Error: {r['error'][:100]}")
        if r["status"] == "FAIL" and r["id"] in required_feed_ids:
            required_failures += 1

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    print(f"\n  Total: {total}  Passed: {passed}  Failed: {failed}")

    if required_failures > 0:
        print(f"\n  ⚠️  {required_failures} REQUIRED (Tier 1) feed(s) failed. Fix before deployment.\n")
        sys.exit(1)
    else:
        print("\n  All required feeds operational.\n")


if __name__ == "__main__":
    asyncio.run(validate())
