# app/routers/facility_router.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db import get_db
from schemas.facility import (
    FacilityCreate,
    FacilityCreateResponse,
    FacilityDetailResponse,
    FacilityListResponse,
)
from services.facility_service import facility_service

router = APIRouter(prefix="/api/facilities", tags=["facilities"])


@router.post("", response_model=FacilityCreateResponse)
async def create_facility(
    req: FacilityCreate,
    db: AsyncSession = Depends(get_db),
):
    return await facility_service.create(db, req)


@router.get("/{facility_id}", response_model=FacilityDetailResponse)
async def read_facility(
    facility_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await facility_service.detail(db, facility_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=FacilityListResponse)
async def list_facilities(
    db: AsyncSession = Depends(get_db),
):
    return await facility_service.list(db)