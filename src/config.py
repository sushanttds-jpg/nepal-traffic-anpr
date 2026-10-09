from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseModel):
    PROJECT_NAME: str = "Nepal Traffic ANPR & Violation System"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Paths
    MODEL_WEIGHTS_PATH: Path = BASE_DIR / "models" / "best_plate_yolo.pt"
    DATA_RAW_DIR: Path = BASE_DIR / "data" / "raw"
    DATA_PROCESSED_DIR: Path = BASE_DIR / "data" / "processed"
    DATA_SYNTHETIC_DIR: Path = BASE_DIR / "data" / "synthetic"
    
    # Inference Defaults
    CONFIDENCE_THRESHOLD: float = 0.50
    IOU_THRESHOLD: float = 0.45
    IMAGE_SIZE: int = 640

settings = Settings()
