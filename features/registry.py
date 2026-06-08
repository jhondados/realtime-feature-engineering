"""Feature registry and serving client."""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from datetime import datetime
import redis, json

@dataclass
class FeatureDefinition:
    name: str
    entity: str  # e.g. "user_id", "product_id"
    dtype: str   # "float", "int", "string"
    description: str
    owner_team: str
    computation: str  # Python expression or SQL
    ttl_seconds: int = 3600
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

class FeatureRegistry:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self._local_registry: Dict[str, FeatureDefinition] = {}

    def register(self, feature: FeatureDefinition):
        self._local_registry[feature.name] = feature
        self.redis.hset("feature_registry", feature.name, json.dumps({
            "entity": feature.entity, "dtype": feature.dtype,
            "description": feature.description, "owner_team": feature.owner_team,
            "tags": feature.tags, "ttl_seconds": feature.ttl_seconds}))

    def get_feature(self, feature_name: str, entity_id: str) -> Optional[float]:
        key = f"feat:{feature_name}:{entity_id}"
        val = self.redis.get(key)
        return float(val) if val else None

    def batch_get(self, feature_names: List[str], entity_id: str) -> Dict[str, Optional[float]]:
        pipe = self.redis.pipeline()
        for name in feature_names: pipe.get(f"feat:{name}:{entity_id}")
        values = pipe.execute()
        return {name: float(v) if v else None for name, v in zip(feature_names, values)}

    def set_feature(self, feature_name: str, entity_id: str, value: float, ttl: int = 3600):
        key = f"feat:{feature_name}:{entity_id}"
        self.redis.set(key, str(value), ex=ttl)

    def search_features(self, query: str) -> List[str]:
        all_features = self.redis.hkeys("feature_registry")
        return [f.decode() for f in all_features if query.lower() in f.decode().lower()]
