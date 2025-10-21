# app/routes/strings.py
from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional, List

from app.storage import storage
from app.utils.analyzer import StringAnalyzer
from app.utils.natural_language import NaturalLanguageParser
from app.models import (
    StringAnalysisCreate, 
    StringAnalysisResponse,
    StringListResponse,
    NaturalLanguageResponse,
    ErrorResponse
)

router = APIRouter(prefix="/strings", tags=["strings"])

@router.post(
    "/",
    response_model=StringAnalysisResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse},
        422: {"model": ErrorResponse}
    }
)
async def create_string(string_data: StringAnalysisCreate):
    """
    Analyze a new string and store its properties
    """
    if storage.string_exists(string_data.value):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="String already exists in the system"
        )
    
    properties = StringAnalyzer.analyze_string(string_data.value)
    
    analysis_data = {
        "value": string_data.value,
        "properties": properties
    }
    
    stored_data = storage.add_string(analysis_data)
    
    return StringAnalysisResponse(**stored_data)

@router.get(
    "/{string_value}",
    response_model=StringAnalysisResponse,
    responses={404: {"model": ErrorResponse}}
)
async def get_string(string_value: str):
    """
    Get analysis for a specific string
    """
    analysis = storage.get_string_by_value(string_value)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system"
        )
    
    return StringAnalysisResponse(**analysis)

@router.get("/", response_model=StringListResponse)
async def get_all_strings(
    is_palindrome: Optional[bool] = Query(None, description="Filter by palindrome status"),
    min_length: Optional[int] = Query(None, ge=0, description="Minimum string length"),
    max_length: Optional[int] = Query(None, ge=0, description="Maximum string length"),
    word_count: Optional[int] = Query(None, ge=0, description="Exact word count"),
    contains_character: Optional[str] = Query(None, min_length=1, max_length=1, description="Single character to search for")
):
    """
    Get all strings with optional filtering
    """
    all_strings = storage.get_all_strings()
    filtered_strings = []
    
    for string_data in all_strings:
        properties = string_data["properties"]
        
        if is_palindrome is not None and properties["is_palindrome"] != is_palindrome:
            continue
            
        if min_length is not None and properties["length"] < min_length:
            continue
            
        if max_length is not None and properties["length"] > max_length:
            continue
            
        if word_count is not None and properties["word_count"] != word_count:
            continue
            
        if contains_character is not None:
            char = contains_character.lower()
            if char not in properties["character_frequency_map"]:
                continue
        
        filtered_strings.append(string_data)
    
    filters_applied = {}
    if is_palindrome is not None:
        filters_applied["is_palindrome"] = is_palindrome
    if min_length is not None:
        filters_applied["min_length"] = min_length
    if max_length is not None:
        filters_applied["max_length"] = max_length
    if word_count is not None:
        filters_applied["word_count"] = word_count
    if contains_character is not None:
        filters_applied["contains_character"] = contains_character
    
    return StringListResponse(
        data=[StringAnalysisResponse(**s) for s in filtered_strings],
        count=len(filtered_strings),
        filters_applied=filters_applied if filters_applied else None
    )

@router.get(
    "/filter-by-natural-language",
    response_model=NaturalLanguageResponse,
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse}
    }
)
async def filter_by_natural_language(
    query: str = Query(..., description="Natural language query")
):
    """
    Filter strings using natural language queries
    """
    try:
        parsed_filters = NaturalLanguageParser.parse_query(query)
        validated_filters = NaturalLanguageParser.validate_filters(parsed_filters)
        
        is_palindrome = validated_filters.get('is_palindrome')
        min_length = validated_filters.get('min_length')
        max_length = validated_filters.get('max_length')
        word_count = validated_filters.get('word_count')
        contains_character = validated_filters.get('contains_character')
        
        all_strings = storage.get_all_strings()
        filtered_strings = []
        
        for string_data in all_strings:
            properties = string_data["properties"]
            
            if is_palindrome is not None and properties["is_palindrome"] != is_palindrome:
                continue
                
            if min_length is not None and properties["length"] < min_length:
                continue
                
            if max_length is not None and properties["length"] > max_length:
                continue
                
            if word_count is not None and properties["word_count"] != word_count:
                continue
                
            if contains_character is not None:
                char = contains_character.lower()
                if char not in properties["character_frequency_map"]:
                    continue
            
            filtered_strings.append(string_data)
        
        return NaturalLanguageResponse(
            data=[StringAnalysisResponse(**s) for s in filtered_strings],
            count=len(filtered_strings),
            interpreted_query={
                "original": query,
                "parsed_filters": validated_filters
            }
        )
        
    except ValueError as e:
        if "Conflicting filters" in str(e):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse natural language query"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse natural language query"
        )

@router.delete(
    "/{string_value}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}}
)
async def delete_string(string_value: str):
    """
    Delete a string analysis
    """
    success = storage.delete_string(string_value)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system"
        )
    
    return None