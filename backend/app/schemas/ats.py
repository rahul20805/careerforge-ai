from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class ATSFactorScore(BaseModel):
    name: str
    score: float  # 0 to 100
    weight: float
    status: str  # EXCELLENT, GOOD, MODERATE, NEEDS_IMPROVEMENT, CRITICAL
    findings: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)


class ATSScoreResponse(BaseModel):
    overall_score: float  # 0 to 100
    maximum_truthful_score: float  # The highest score achievable without fabricating missing skills
    verdict: str  # Highly Compatible, Moderately Compatible, Needs Alignment
    is_truthful: bool = True
    
    factors: Dict[str, ATSFactorScore]
    # keyword_match, skill_match, experience_match, education_match, semantic_match, formatting, completeness, truthfulness
    
    found_keywords: List[str] = Field(default_factory=list)
    missing_required_keywords: List[str] = Field(default_factory=list)
    missing_preferred_keywords: List[str] = Field(default_factory=list)
    unsupported_claims_detected: List[str] = Field(default_factory=list)
    
    formatting_issues: List[str] = Field(default_factory=list)
    detailed_explanation: str


class ATSComparisonResponse(BaseModel):
    before_score: float
    after_score: float
    improvement_delta: float
    added_truthful_keywords: List[str]
    reordered_sections: List[str]
    realigned_bullet_points: List[str]
    rejected_fabrications: List[str]
    explanation: str
