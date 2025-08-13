from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class BankCode(str, Enum):
    IG = "IG"
    RB = "RB"
    AB = "AB"

class DocumentType(str, Enum):
    CSRD = "CSRD"
    EU_TAXONOMY = "EU_Taxonomy"
    CLIMATE_RISK = "Climate_Risk"

class AnalysisType(str, Enum):
    CSRD = "CSRD"
    EU_TAXONOMY = "EU_Taxonomy"
    CLIMATE_RISK = "Climate_Risk"
    DRIFT = "Drift"

class Severity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

# Base models
class UserBase(BaseModel):
    username: str
    email: str
    role: str = "analyst"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class BankBase(BaseModel):
    code: BankCode
    name: str
    country: str = "Netherlands"
    sector: str = "Banking"

class Bank(BankBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ESGDocumentBase(BaseModel):
    filename: str
    bank: BankCode
    document_type: DocumentType
    year: int

class ESGDocumentCreate(ESGDocumentBase):
    content: str
    file_size: int

class ESGDocument(ESGDocumentBase):
    id: int
    content: str
    analysis: Optional[Dict[str, Any]]
    uploaded_at: datetime
    file_size: int
    status: str
    
    class Config:
        from_attributes = True

# Analysis models
class CSRDGap(BaseModel):
    article: str
    requirement: str
    status: str
    severity: Severity
    description: str
    recommendation: str

class TaxonomyAlignment(BaseModel):
    sector: str
    alignment_percentage: float
    eligible_activities: List[str]
    non_compliant_activities: List[str]
    recommendations: List[str]

class ClimateRiskMetric(BaseModel):
    metric_name: str
    value: float
    unit: str
    scenario: str
    risk_level: str
    trend: str

class DriftIndicator(BaseModel):
    kpi_name: str
    previous_value: float
    current_value: float
    change_percentage: float
    direction: str
    significance: str

class ESGAnalysisBase(BaseModel):
    bank: BankCode
    analysis_type: AnalysisType
    year: int
    environmental_score: float
    social_score: float
    governance_score: float
    overall_score: float

class ESGAnalysisCreate(ESGAnalysisBase):
    csrd_gaps: List[CSRDGap]
    taxonomy_alignment: List[TaxonomyAlignment]
    climate_risk_metrics: List[ClimateRiskMetric]
    drift_indicators: List[DriftIndicator]

class ESGAnalysis(ESGAnalysisBase):
    id: int
    document_id: int
    csrd_gaps: List[CSRDGap]
    taxonomy_alignment: List[TaxonomyAlignment]
    climate_risk_metrics: List[ClimateRiskMetric]
    drift_indicators: List[DriftIndicator]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Dashboard models
class DashboardSummary(BaseModel):
    total_banks: int
    total_documents: int
    total_analyses: int
    average_esg_score: float
    compliance_rate: float
    critical_gaps: int

class ESGScoreCard(BaseModel):
    bank: BankCode
    environmental_score: float
    social_score: float
    governance_score: float
    overall_score: float
    rank: int
    trend: str

class ComplianceGap(BaseModel):
    bank: BankCode
    regulation: str
    gap_type: str
    description: str
    severity: Severity
    recommendation: str
    year: int

class TaxonomyAlignmentSummary(BaseModel):
    bank: BankCode
    total_alignment: float
    eligible_investments: float
    non_compliant_investments: float
    sectors: List[str]

class ClimateRiskSummary(BaseModel):
    bank: BankCode
    physical_risk_score: float
    transition_risk_score: float
    overall_climate_risk: float
    risk_trend: str

class DriftAnalysis(BaseModel):
    bank: BankCode
    year: int
    kpi_changes: List[DriftIndicator]
    overall_drift_score: float
    risk_level: str

# API Response models
class DashboardData(BaseModel):
    summary: DashboardSummary
    esg_scores: List[ESGScoreCard]
    compliance_gaps: List[ComplianceGap]
    taxonomy_alignment: List[TaxonomyAlignmentSummary]
    climate_risk: List[ClimateRiskSummary]
    drift_analysis: List[DriftAnalysis]

class BankReport(BaseModel):
    bank: BankCode
    executive_summary: str
    esg_analysis: ESGAnalysis
    compliance_status: Dict[str, Any]
    recommendations: List[str]
    risk_assessment: Dict[str, Any]
    generated_at: datetime

class BDDTestCase(BaseModel):
    title: str
    description: str
    priority: str
    tags: List[str]
    feature_module: str
    steps: List[str]
    expected_result: str

class TestCaseResponse(BaseModel):
    test_cases: List[BDDTestCase]
    total_count: int
    generated_at: datetime 