"""
FastAPI Backend for Nepal Traffic ANPR and E-Challan Violation System.
"""

from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from pydantic import BaseModel, Field

from src.config import settings
from src.rules.nepali_plates import parse_nepali_plate

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Automatic Nepali License Plate Recognition & Traffic Violation Ticketing API"
)

# --- Mock Department of Transport Management (DoTM) Database ---
MOCK_DOTM_DATABASE = {
    "बा २ ख १२३४": {
        "owner_name": "Ram Bahadur Shrestha",
        "vehicle_type": "Public Minibus",
        "engine_no": "ENG98124912",
        "chassis_no": "CHS8127391823",
        "tax_paid_until": "2081-04-32",
        "registered_office": "Ekantakuna, Lalitpur",
        "phone_number": "+9779841000001"
    },
    "बागमती ०१-०२५ च ५६७८": {
        "owner_name": "Sita Kumari Sharma",
        "vehicle_type": "Private Car (Hyundai Creta)",
        "engine_no": "ENG11223344",
        "chassis_no": "CHS9988776655",
        "tax_paid_until": "2081-12-30",
        "registered_office": "Sano Bharyang, Kathmandu",
        "phone_number": "+9779841000002"
    },
    "BAGMATI 01-028 CA 1234": {
        "owner_name": "Bikash Thapa",
        "vehicle_type": "Motorcycle (Pulsar 220)",
        "engine_no": "ENG55667788",
        "chassis_no": "CHS4433221100",
        "tax_paid_until": "2082-03-31",
        "registered_office": "Gurjudhara, Kathmandu",
        "phone_number": "+9779841000003"
    }
}

# --- Pydantic Schemas ---
class PlateAnalysisResponse(BaseModel):
    raw_ocr_text: str
    confidence: float
    parsed_metadata: dict
    dotm_record: Optional[dict] = None

class ViolationCreateRequest(BaseModel):
    plate_number: str
    violation_type: str = Field(..., example="Red Light Jump / लेन अनुशासन उल्लङ्घन")
    fine_amount_npr: int = Field(default=1500, example=1500)
    location: str = Field(..., example="Maitighar Mandala, Kathmandu")
    latitude: Optional[float] = 27.6945
    longitude: Optional[float] = 85.3206
    officer_badge_id: str = Field(..., example="TP-KTM-4091")

class ViolationTicketResponse(BaseModel):
    ticket_id: str
    issued_at: datetime
    plate_number: str
    owner_name: str
    owner_phone: str
    violation_type: str
    fine_amount_npr: int
    status: str
    payment_link: str


# --- Endpoints ---
@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post(f"{settings.API_V1_STR}/analyze-plate", response_model=PlateAnalysisResponse, tags=["ANPR Engine"])
async def analyze_plate(file: UploadFile = File(...)):
    """
    Accepts vehicle image, detects plate via YOLO, performs OCR, and parses Nepali syntax.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File provided is not an image."
        )
    
    # Placeholder for model inference pipeline
    # In full implementation: YOLO -> Crop -> OCR -> Regex
    mock_detected_plate = "बा २ ख १२३४"
    parsed_info = parse_nepali_plate(mock_detected_plate)
    dotm_info = MOCK_DOTM_DATABASE.get(mock_detected_plate)
    
    return PlateAnalysisResponse(
        raw_ocr_text=mock_detected_plate,
        confidence=0.94,
        parsed_metadata=parsed_info,
        dotm_record=dotm_info
    )


@app.get(f"{settings.API_V1_STR}/vehicles/{{plate_number}}", tags=["DoTM Registry"])
def get_vehicle_details(plate_number: str):
    """Query vehicle ownership record from Mock DoTM database."""
    record = MOCK_DOTM_DATABASE.get(plate_number)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No vehicle registered with plate number '{plate_number}' in DoTM database."
        )
    return {"plate_number": plate_number, "details": record}


@app.post(f"{settings.API_V1_STR}/violations/issue", response_model=ViolationTicketResponse, tags=["Traffic Violations"])
def issue_violation_ticket(req: ViolationCreateRequest):
    """
    Generates a formal digital E-Challan ticket for a traffic violation.
    """
    dotm_record = MOCK_DOTM_DATABASE.get(req.plate_number)
    owner_name = dotm_record["owner_name"] if dotm_record else "Unregistered / Unknown"
    owner_phone = dotm_record["phone_number"] if dotm_record else "N/A"
    
    ticket_id = f"CHALLAN-NP-{int(datetime.utcnow().timestamp())}"
    
    return ViolationTicketResponse(
        ticket_id=ticket_id,
        issued_at=datetime.utcnow(),
        plate_number=req.plate_number,
        owner_name=owner_name,
        owner_phone=owner_phone,
        violation_type=req.violation_type,
        fine_amount_npr=req.fine_amount_npr,
        status="PENDING_PAYMENT",
        payment_link=f"https://traffic.nepalpolice.gov.np/pay/{ticket_id}"
    )
