from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class BankCode(str, Enum):
    IG = "IG"  # ING Group
    RB = "RB"  # Rabobank
    AB = "AB"  # ABN AMRO

class DocumentType(str, Enum):
    CSRD_DOUBLE_MATERIALITY = "csrd_double_materiality"
    EU_TAXONOMY_ALIGNMENT = "eu_taxonomy_alignment"
    CLIMATE_RISK_STRESS_TEST = "climate_risk_stress_test"

class ESGDimension(str, Enum):
    ENVIRONMENTAL = "environmental"
    SOCIAL = "social"
    GOVERNANCE = "governance"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"
    NOT_ASSESSED = "not_assessed"

class BankData(BaseModel):
    code: BankCode
    name: str
    full_name: str
    country: str
    sector: str
    esg_score: float = Field(ge=0, le=100)
    last_updated: datetime

class ESGReport(BaseModel):
    bank_code: BankCode
    document_type: DocumentType
    report_date: datetime
    content: str
    file_path: Optional[str] = None

class CSRDAnalysis(BaseModel):
    impact_materiality_score: float = Field(ge=0, le=100)
    financial_materiality_score: float = Field(ge=0, le=100)
    gaps_identified: List[str]
    regulatory_risks: List[str]
    recommendations: List[str]
    compliance_status: ComplianceStatus
    eba_guidelines_alignment: float = Field(ge=0, le=100)

class TaxonomyValidation(BaseModel):
    alignment_score: float = Field(ge=0, le=100)
    eligible_green_investments: float = Field(ge=0, le=100)
    non_compliant_sectors: List[str]
    technical_screening_compliance: Dict[str, bool]
    sfdr_improvements: List[str]
    green_bond_opportunities: List[str]

class ClimateRiskEvaluation(BaseModel):
    tcfd_compliance_score: float = Field(ge=0, le=100)
    scenario_analysis_coverage: Dict[str, bool]
    transition_risk_metrics: Dict[str, float]
    physical_risk_disclosures: Dict[str, bool]
    missing_components: List[str]
    enhancement_recommendations: List[str]

class ESGDriftDetection(BaseModel):
    kpi_regression: Dict[str, float]
    taxonomy_alignment_change: float
    climate_risk_exposure_change: float
    drift_indicators: List[str]
    corrective_actions: List[str]
    trend_direction: str

class ESGScoring(BaseModel):
    overall_score: float = Field(ge=0, le=100)
    environmental_score: float = Field(ge=0, le=100)
    social_score: float = Field(ge=0, le=100)
    governance_score: float = Field(ge=0, le=100)
    eu_regulation_alignment: float = Field(ge=0, le=100)
    sdg_alignment: Dict[str, float]
    weighted_breakdown: Dict[str, float]

class ImpactAnalysis(BaseModel):
    sector_risk_exposure: Dict[str, RiskLevel]
    regulatory_compliance_status: ComplianceStatus
    taxonomy_investment_alignment: float = Field(ge=0, le=100)
    climate_vulnerability_index: float = Field(ge=0, le=100)
    stakeholder_trust_indicators: Dict[str, float]
    strategic_gaps: List[str]
    opportunities: List[str]

class Vision2030Alignment(BaseModel):
    sdg_mapping: Dict[str, float]
    climate_neutrality_gaps: List[str]
    biodiversity_gaps: List[str]
    social_equity_gaps: List[str]
    strategic_initiatives: List[str]
    green_deal_readiness: float = Field(ge=0, le=100)
    net_zero_transition_score: float = Field(ge=0, le=100)

class AnalysisResult(BaseModel):
    bank_code: BankCode
    analysis_date: datetime
    csrd_analysis: CSRDAnalysis
    taxonomy_validation: TaxonomyValidation
    climate_risk: ClimateRiskEvaluation
    esg_drift: ESGDriftDetection
    esg_scoring: ESGScoring
    impact_analysis: ImpactAnalysis
    vision_2030: Vision2030Alignment

class TestCase(BaseModel):
    id: str
    title: str
    description: str
    priority: str
    tags: List[str]
    bank_code: BankCode
    document_type: DocumentType
    azure_test_plan_id: str
    feature_module: str
    gherkin_scenario: str
    acceptance_criteria: List[str]

class DashboardData(BaseModel):
    esg_scores: Dict[str, float]
    compliance_heatmap: Dict[str, Dict[str, str]]
    drift_trends: Dict[str, List[float]]
    taxonomy_alignment: Dict[str, float]
    climate_risk_exposure: Dict[str, float]
    risk_distribution: Dict[str, Dict[str, int]]
    sdg_progress: Dict[str, Dict[str, float]] 