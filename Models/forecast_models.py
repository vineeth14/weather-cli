from pydantic import BaseModel
from typing import Optional, List


class GetForecastReq(BaseModel):
    latitude: float
    longitude: float


class GetForecastModel(BaseModel):
    latitude: float
    longitude: float
    daily: str
    forecast_days: Optional[int]
    temperature_unit: str


class GetForecastResp(BaseModel):
    latitude: float
    longitude: float
    temperature_2m_min: List[float]
    temperature_2m_max: List[float]
