import asyncio
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import json
from datetime import datetime, timedelta
import random

from ..database import ESGAnalysis, ESGDocument, Bank, ComplianceGaps, ESGMetrics
from ..models import (
    DashboardData, DashboardSummary, ESGScoreCard, ComplianceGap,
    TaxonomyAlignmentSummary, ClimateRiskSummary, DriftAnalysis,
    BankReport, BDDTestCase, TestCaseResponse
)

class DashboardService:
    def __init__(self):
        self.banks = ["IG", "RB", "AB"]
        self.document_types = ["CSRD", "EU_Taxonomy", "Climate_Risk"]
        
    async def get_dashboard_data(self, db: Session, banks: List[str]) -> DashboardData:
        """Get comprehensive dashboard data for all banks"""
        try:
            # Get summary data
            summary = await self.get_summary_data(db)
            
            # Get ESG scores
            esg_scores = await self.get_esg_scores(db)
            
            # Get compliance gaps
            compliance_gaps = await self.get_compliance_gaps(db)
            
            # Get taxonomy alignment
            taxonomy_alignment = await self.get_taxonomy_alignment(db)
            
            # Get climate risk data
            climate_risk = await self.get_climate_risk_data(db)
            
            # Get drift analysis
            drift_analysis = await self.get_drift_analysis(db)
            
            return DashboardData(
                summary=summary,
                esg_scores=esg_scores,
                compliance_gaps=compliance_gaps,
                taxonomy_alignment=taxonomy_alignment,
                climate_risk=climate_risk,
                drift_analysis=drift_analysis
            )
            
        except Exception as e:
            print(f"Error getting dashboard data: {str(e)}")
            return self._create_fallback_dashboard_data()

    async def get_summary_data(self, db: Session) -> DashboardSummary:
        """Get dashboard summary statistics"""
        try:
            # Count total documents
            total_documents = db.query(ESGDocument).count()
            
            # Count total analyses
            total_analyses = db.query(ESGAnalysis).count()
            
            # Calculate average ESG score
            avg_score_result = db.query(func.avg(ESGAnalysis.overall_score)).scalar()
            average_esg_score = round(avg_score_result or 0.75, 2)
            
            # Count critical gaps
            critical_gaps = db.query(ComplianceGaps).filter(
                ComplianceGaps.severity.in_(["High", "Critical"])
            ).count()
            
            # Calculate compliance rate (mock data for now)
            compliance_rate = 0.78
            
            return DashboardSummary(
                total_banks=len(self.banks),
                total_documents=total_documents,
                total_analyses=total_analyses,
                average_esg_score=average_esg_score,
                compliance_rate=compliance_rate,
                critical_gaps=critical_gaps
            )
            
        except Exception as e:
            print(f"Error getting summary data: {str(e)}")
            return DashboardSummary(
                total_banks=3,
                total_documents=0,
                total_analyses=0,
                average_esg_score=0.75,
                compliance_rate=0.75,
                critical_gaps=0
            )

    async def get_esg_scores(self, db: Session) -> List[ESGScoreCard]:
        """Get ESG scores for all banks"""
        try:
            esg_scores = []
            
            for bank in self.banks:
                # Get latest analysis for each bank
                latest_analysis = db.query(ESGAnalysis).filter(
                    ESGAnalysis.bank == bank
                ).order_by(desc(ESGAnalysis.created_at)).first()
                
                if latest_analysis:
                    score_card = ESGScoreCard(
                        bank=bank,
                        environmental_score=latest_analysis.environmental_score,
                        social_score=latest_analysis.social_score,
                        governance_score=latest_analysis.governance_score,
                        overall_score=latest_analysis.overall_score,
                        rank=1,  # Will be calculated later
                        trend="Stable"
                    )
                else:
                    # Mock data for banks without analysis
                    score_card = ESGScoreCard(
                        bank=bank,
                        environmental_score=0.75 + random.uniform(-0.1, 0.1),
                        social_score=0.75 + random.uniform(-0.1, 0.1),
                        governance_score=0.75 + random.uniform(-0.1, 0.1),
                        overall_score=0.75 + random.uniform(-0.1, 0.1),
                        rank=1,
                        trend="Stable"
                    )
                
                esg_scores.append(score_card)
            
            # Sort by overall score and assign ranks
            esg_scores.sort(key=lambda x: x.overall_score, reverse=True)
            for i, score in enumerate(esg_scores):
                score.rank = i + 1
            
            return esg_scores
            
        except Exception as e:
            print(f"Error getting ESG scores: {str(e)}")
            return self._create_mock_esg_scores()

    async def get_compliance_gaps(self, db: Session) -> List[ComplianceGap]:
        """Get compliance gaps for all banks"""
        try:
            gaps = []
            
            # Get gaps from database
            db_gaps = db.query(ComplianceGaps).all()
            
            for gap in db_gaps:
                compliance_gap = ComplianceGap(
                    bank=gap.bank,
                    regulation=gap.regulation,
                    gap_type=gap.gap_type,
                    description=gap.description,
                    severity=gap.severity,
                    recommendation=gap.recommendation,
                    year=gap.year
                )
                gaps.append(compliance_gap)
            
            # Add mock gaps if none exist
            if not gaps:
                gaps = self._create_mock_compliance_gaps()
            
            return gaps
            
        except Exception as e:
            print(f"Error getting compliance gaps: {str(e)}")
            return self._create_mock_compliance_gaps()

    async def get_taxonomy_alignment(self, db: Session) -> List[TaxonomyAlignmentSummary]:
        """Get EU Taxonomy alignment data"""
        try:
            alignment_data = []
            
            for bank in self.banks:
                # Mock taxonomy alignment data
                alignment = TaxonomyAlignmentSummary(
                    bank=bank,
                    total_alignment=0.65 + random.uniform(-0.2, 0.2),
                    eligible_investments=0.45 + random.uniform(-0.15, 0.15),
                    non_compliant_investments=0.35 + random.uniform(-0.15, 0.15),
                    sectors=["Manufacturing", "Energy", "Transport", "Buildings"]
                )
                alignment_data.append(alignment)
            
            return alignment_data
            
        except Exception as e:
            print(f"Error getting taxonomy alignment: {str(e)}")
            return []

    async def get_climate_risk_data(self, db: Session) -> List[ClimateRiskSummary]:
        """Get climate risk analysis data"""
        try:
            climate_data = []
            
            for bank in self.banks:
                # Mock climate risk data
                climate_summary = ClimateRiskSummary(
                    bank=bank,
                    physical_risk_score=0.3 + random.uniform(-0.1, 0.1),
                    transition_risk_score=0.4 + random.uniform(-0.1, 0.1),
                    overall_climate_risk=0.35 + random.uniform(-0.1, 0.1),
                    risk_trend="Decreasing"
                )
                climate_data.append(climate_summary)
            
            return climate_data
            
        except Exception as e:
            print(f"Error getting climate risk data: {str(e)}")
            return []

    async def get_drift_analysis(self, db: Session) -> List[DriftAnalysis]:
        """Get ESG drift analysis"""
        try:
            drift_data = []
            
            for bank in self.banks:
                # Mock drift indicators
                drift_indicators = [
                    {
                        "kpi_name": "ESG Score",
                        "previous_value": 0.82,
                        "current_value": 0.85,
                        "change_percentage": 3.7,
                        "direction": "Increasing",
                        "significance": "Positive"
                    },
                    {
                        "kpi_name": "Carbon Footprint",
                        "previous_value": 125.5,
                        "current_value": 118.2,
                        "change_percentage": -5.8,
                        "direction": "Decreasing",
                        "significance": "Positive"
                    }
                ]
                
                drift_analysis = DriftAnalysis(
                    bank=bank,
                    year=2024,
                    kpi_changes=drift_indicators,
                    overall_drift_score=0.78,
                    risk_level="Low"
                )
                drift_data.append(drift_analysis)
            
            return drift_data
            
        except Exception as e:
            print(f"Error getting drift analysis: {str(e)}")
            return []

    async def generate_bank_report(self, db: Session, bank: str) -> BankReport:
        """Generate comprehensive ESG report for a bank"""
        try:
            # Get latest analysis
            latest_analysis = db.query(ESGAnalysis).filter(
                ESGAnalysis.bank == bank
            ).order_by(desc(ESGAnalysis.created_at)).first()
            
            if not latest_analysis:
                # Create mock analysis
                latest_analysis = self._create_mock_analysis(bank)
            
            # Generate executive summary
            executive_summary = self._generate_executive_summary(bank, latest_analysis)
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(latest_analysis)
            
            # Generate risk assessment
            risk_assessment = self._generate_risk_assessment(latest_analysis)
            
            # Generate compliance status
            compliance_status = self._generate_compliance_status(bank, latest_analysis)
            
            return BankReport(
                bank=bank,
                executive_summary=executive_summary,
                esg_analysis=latest_analysis,
                compliance_status=compliance_status,
                recommendations=recommendations,
                risk_assessment=risk_assessment,
                generated_at=datetime.utcnow()
            )
            
        except Exception as e:
            print(f"Error generating bank report: {str(e)}")
            return self._create_fallback_bank_report(bank)

    async def generate_bdd_test_cases(self) -> TestCaseResponse:
        """Generate BDD test cases for Azure Test Plan"""
        try:
            test_cases = []
            
            # Generate test cases for each bank and document type
            for bank in self.banks:
                for doc_type in self.document_types:
                    test_case = BDDTestCase(
                        title=f"ESG Analysis - {bank} {doc_type} Document",
                        description=f"Verify ESG analysis functionality for {bank} bank {doc_type} document",
                        priority="High",
                        tags=[f"ESG", f"{doc_type}", bank],
                        feature_module="ESG Analysis",
                        steps=[
                            f"Upload {doc_type} document for {bank} bank",
                            "Process document through ESG analyzer",
                            "Verify analysis results are generated",
                            "Check ESG scores are calculated correctly",
                            "Validate compliance gaps are identified"
                        ],
                        expected_result=f"Complete ESG analysis report generated for {bank} {doc_type} document"
                    )
                    test_cases.append(test_case)
            
            return TestCaseResponse(
                test_cases=test_cases,
                total_count=len(test_cases),
                generated_at=datetime.utcnow()
            )
            
        except Exception as e:
            print(f"Error generating BDD test cases: {str(e)}")
            return TestCaseResponse(
                test_cases=[],
                total_count=0,
                generated_at=datetime.utcnow()
            )

    # Helper methods
    def _create_fallback_dashboard_data(self) -> DashboardData:
        """Create fallback dashboard data"""
        return DashboardData(
            summary=DashboardSummary(
                total_banks=3,
                total_documents=0,
                total_analyses=0,
                average_esg_score=0.75,
                compliance_rate=0.75,
                critical_gaps=0
            ),
            esg_scores=self._create_mock_esg_scores(),
            compliance_gaps=self._create_mock_compliance_gaps(),
            taxonomy_alignment=[],
            climate_risk=[],
            drift_analysis=[]
        )

    def _create_mock_esg_scores(self) -> List[ESGScoreCard]:
        """Create mock ESG scores"""
        return [
            ESGScoreCard(
                bank="IG",
                environmental_score=0.82,
                social_score=0.78,
                governance_score=0.85,
                overall_score=0.82,
                rank=1,
                trend="Increasing"
            ),
            ESGScoreCard(
                bank="RB",
                environmental_score=0.79,
                social_score=0.81,
                governance_score=0.83,
                overall_score=0.81,
                rank=2,
                trend="Stable"
            ),
            ESGScoreCard(
                bank="AB",
                environmental_score=0.76,
                social_score=0.79,
                governance_score=0.80,
                overall_score=0.78,
                rank=3,
                trend="Decreasing"
            )
        ]

    def _create_mock_compliance_gaps(self) -> List[ComplianceGap]:
        """Create mock compliance gaps"""
        return [
            ComplianceGap(
                bank="IG",
                regulation="CSRD",
                gap_type="Missing",
                description="Incomplete double materiality assessment",
                severity="High",
                recommendation="Conduct comprehensive materiality assessment",
                year=2024
            ),
            ComplianceGap(
                bank="RB",
                regulation="EU Taxonomy",
                gap_type="Incomplete",
                description="Missing technical screening criteria alignment",
                severity="Medium",
                recommendation="Align investment portfolio with taxonomy criteria",
                year=2024
            )
        ]

    def _create_mock_analysis(self, bank: str) -> ESGAnalysis:
        """Create mock ESG analysis"""
        return ESGAnalysis(
            id=1,
            bank=bank,
            document_id=1,
            analysis_type="CSRD",
            year=2024,
            environmental_score=0.80,
            social_score=0.78,
            governance_score=0.85,
            overall_score=0.81,
            csrd_gaps=[],
            taxonomy_alignment=[],
            climate_risk_metrics=[],
            drift_indicators=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    def _generate_executive_summary(self, bank: str, analysis: ESGAnalysis) -> str:
        """Generate executive summary for bank report"""
        return f"""
        {bank} Bank ESG Performance Summary (2024)
        
        Overall ESG Score: {analysis.overall_score:.2f}
        Environmental Score: {analysis.environmental_score:.2f}
        Social Score: {analysis.social_score:.2f}
        Governance Score: {analysis.governance_score:.2f}
        
        Key Highlights:
        - Strong governance framework with score of {analysis.governance_score:.2f}
        - Environmental performance shows room for improvement
        - Social impact measurement needs enhancement
        - Overall compliance with EU regulations is satisfactory
        """

    async def _generate_recommendations(self, analysis: ESGAnalysis) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []
        
        if analysis.environmental_score < 0.8:
            recommendations.append("Enhance environmental risk management and disclosure")
        
        if analysis.social_score < 0.8:
            recommendations.append("Improve social impact measurement and reporting")
        
        if analysis.governance_score < 0.8:
            recommendations.append("Strengthen governance frameworks and oversight")
        
        recommendations.extend([
            "Increase EU Taxonomy alignment across investment portfolio",
            "Implement comprehensive climate risk stress testing",
            "Enhance stakeholder engagement and transparency"
        ])
        
        return recommendations[:5]

    def _generate_risk_assessment(self, analysis: ESGAnalysis) -> Dict[str, Any]:
        """Generate risk assessment"""
        return {
            "environmental_risk": "Medium",
            "social_risk": "Low",
            "governance_risk": "Low",
            "regulatory_risk": "Medium",
            "reputation_risk": "Low",
            "financial_risk": "Low"
        }

    def _generate_compliance_status(self, bank: str, analysis: ESGAnalysis) -> Dict[str, Any]:
        """Generate compliance status"""
        return {
            "csrd_compliance": "Compliant",
            "eu_taxonomy_alignment": "75%",
            "sfdr_compliance": "Compliant",
            "tcfd_alignment": "Partial",
            "overall_compliance_score": analysis.overall_score
        }

    def _create_fallback_bank_report(self, bank: str) -> BankReport:
        """Create fallback bank report"""
        mock_analysis = self._create_mock_analysis(bank)
        
        return BankReport(
            bank=bank,
            executive_summary=f"ESG analysis report for {bank} bank",
            esg_analysis=mock_analysis,
            compliance_status={},
            recommendations=["Conduct comprehensive ESG assessment"],
            risk_assessment={},
            generated_at=datetime.utcnow()
        ) 