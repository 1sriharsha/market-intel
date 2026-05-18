"""Enumerations used across models and business logic."""
import enum


class SourceTier(int, enum.Enum):
    TIER1 = 1
    TIER2A = 2
    TIER2B = 2   # same numeric weight as 2A for storage; distinguished in scoring logic
    TIER2C = 3
    TIER3 = 3
    TIER4 = 4


class FeedType(str, enum.Enum):
    RSS = "rss"
    API = "api"
    OFFICIAL = "official"
    SCRAPE = "scrape"


class SignificanceLevel(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class VolatilityRegime(str, enum.Enum):
    COMPRESSED = "compressed"   # VIX < 15
    NORMAL = "normal"           # VIX 15–25
    ELEVATED = "elevated"       # VIX 25–35
    PANIC = "panic"             # VIX > 35


class LiquidityRegime(str, enum.Enum):
    LOOSE = "loose"
    NORMAL = "normal"
    TIGHTENING = "tightening"
    STRESSED = "stressed"


class MacroRegime(str, enum.Enum):
    EXPANSION = "expansion"
    STAGFLATION = "stagflation"
    RECESSION_RISK = "recession_risk"
    DISINFLATION = "disinflation"


class SentimentRegime(str, enum.Enum):
    EUPHORIC = "euphoric"
    OPTIMISTIC = "optimistic"
    NEUTRAL = "neutral"
    PESSIMISTIC = "pessimistic"
    FEARFUL = "fearful"


class TriggerType(str, enum.Enum):
    SCHEDULED_CYCLE = "scheduled_cycle"
    EVENT_TRIGGERED = "event_triggered"
    MANUAL = "manual"


class ReactionLabel(str, enum.Enum):
    LARGE = "large"         # |abnormal_return| > 5%
    MODERATE = "moderate"   # |abnormal_return| 2–5%
    SMALL = "small"         # |abnormal_return| 0.5–2%
    NONE = "none"           # |abnormal_return| < 0.5%
    INVERSE = "inverse"     # opposite direction to narrative


class AttributionMethod(str, enum.Enum):
    EXPLICIT_MENTION = "explicit_mention"
    ENTITY_EXTRACT = "entity_extract"
    SOURCE_TAG = "source_tag"


class EventCategory(str, enum.Enum):
    MONETARY_POLICY = "monetary_policy"
    EARNINGS = "earnings"
    GEOPOLITICAL = "geopolitical"
    REGULATORY = "regulatory"
    MACRO = "macro"
    CORPORATE_ACTION = "corporate_action"
    NATURAL_DISASTER = "natural_disaster"
    OTHER = "other"
