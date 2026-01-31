from pydantic import BaseModel
import requests


class GetTemperatureModel(BaseModel):
    latitude: float
    longitude: float
    hourly: str
    current: str
    forecast_days: int
    temperature_unit: str


class GetLatitudeLongitudeReq(BaseModel):
    location: str


class GetLatitudeLongitudeResp(BaseModel):
    latitude: float
    longitude: float


class GetAPIReq(BaseModel):
    params: dict
    api_url: str


class GetTemperatureReq(BaseModel):
    latitude: float
    longitude: float


class GetTemperatureResp(BaseModel):
    temperature: float
