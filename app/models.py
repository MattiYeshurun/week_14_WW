from pydantic import BaseModel


class Weapons(BaseModel):
    id: int
    weapon_id: int
    weapon_name: str
    weapon_type: str
    range_km: int
    weight_kg: float
    manufacturer: str
    origin_country: str
    storage_location: str
    year_estimated: int
    risk_level: str



