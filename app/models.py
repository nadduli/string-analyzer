from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class StringProperties(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Dict[str, int]

class StringAnalysisCreate(BaseModel):
    value: str = Field(..., description="String to analyze")

class StringAnalysisResponse(BaseModel):
    id: str
    value: str
    properties: StringProperties
    created_at: str

class StringListResponse(BaseModel):
    data: List[StringAnalysisResponse]
    count: int
    filters_applied: Optional[Dict[str, Any]] = None

class NaturalLanguageResponse(BaseModel):
    data: List[StringAnalysisResponse]
    count: int
    interpreted_query: Dict[str, Any]

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None