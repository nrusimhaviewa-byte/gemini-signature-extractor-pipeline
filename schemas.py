from typing import List, Optional
from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    ymin: int = Field(description="Top coordinate in normalized scale (0 to 1000)")
    xmin: int = Field(description="Left coordinate in normalized scale (0 to 1000)")
    ymax: int = Field(description="Bottom coordinate in normalized scale (0 to 1000)")
    xmax: int = Field(description="Right coordinate in normalized scale (0 to 1000)")

class Stage1SignatureAnalysis(BaseModel):
    signature_present: bool = Field(description="True if a signature, initials, or stamp is detected")
    classification: str = Field(description="Classification: 'wet_signature', 'pasted_image', 'signature_does_not_exist', or 'uncertain'")
    confidence: float = Field(description="Detection confidence between 0.0 and 1.0 (or 0-100)")
    signatory_name: Optional[str] = Field(None, description="Extracted name of signatory if visible")
    signatory_role: Optional[str] = Field(None, description="Title/role of signatory if visible")
    date_signed: Optional[str] = Field(None, description="Date accompanying signature if visible")
    bounding_box: BoundingBox = Field(description="Bounding box in [ymin, xmin, ymax, xmax] 0-1000 scale")
    explanation: str = Field(description="Detailed explanation of the visual detection reasoning")
    visual_evidence: List[str] = Field(default_factory=list, description="Bullet points of visual indicators observed")
    limitations: List[str] = Field(default_factory=list, description="Image quality, blur, resolution, or scanning limitations")

class Stage2DatasetComparison(BaseModel):
    dataset_signature_name: str = Field(description="Filename of the reference signature image from dataset")
    match_result: str = Field(description="Must be one of: 'PERFECT MATCH', 'PARTIAL MATCH', 'NO MATCH', or 'UNCERTAIN'")
    confidence: int = Field(description="Confidence score integer from 1 to 100")
    explanation: str = Field(description="Detailed comparative analysis of initial strokes, loops, terminal strokes, and trajectory")
    visual_evidence: List[str] = Field(default_factory=list, description="Visual characteristics agreeing or differing")
    limitations: List[str] = Field(default_factory=list, description="Factors limiting comparison accuracy (scale, resolution, noise)")
