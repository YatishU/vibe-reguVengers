import asyncio
import json
from typing import List, Dict, Any, Optional
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import openai
from ..models import (
    ESGAnalysis, CSRDGap, TaxonomyAlignment, ClimateRiskMetric, 
    DriftIndicator, BankCode, DocumentType, AnalysisType, Severity
)
from ..utils.config import settings

class ESGAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Initialize analysis prompts
        self.csrd_prompt = self._create_csrd_prompt()
        self.taxonomy_prompt = self._create_taxonomy_prompt()
        self.climate_prompt = self._create_climate_prompt()
        self.drift_prompt = self._create_drift_prompt()

    def _create_csrd_prompt(self) -> str:
        return """
        You are an ESG compliance expert analyzing CSRD Double Materiality Assessment Reports for Dutch banks.
        
        Analyze the following document content for {bank} bank and identify:
        1. Gaps in impact and financial materiality disclosures
        2. Compliance with EBA guidelines and Article 19a of CSRD directive
        3. Regulatory risks and improvement recommendations
        
        Document Content:
        {content}
        
        Provide analysis in the following JSON format:
        {{
            "csrd_gaps": [
                {{
                    "article": "Article 19a",
                    "requirement": "Specific requirement",
                    "status": "Missing/Incomplete/Compliant",
                    "severity": "Low/Medium/High/Critical",
                    "description": "Detailed description of the gap",
                    "recommendation": "Specific improvement recommendation"
                }}
            ],
            "environmental_score": 0.85,
            "social_score": 0.78,
            "governance_score": 0.92,
            "overall_score": 0.85
        }}
        """

    def _create_taxonomy_prompt(self) -> str:
        return """
        You are an EU Taxonomy expert analyzing alignment with technical screening criteria.
        
        Analyze the following document for {bank} bank and assess:
        1. EU Taxonomy alignment by sector
        2. Eligible green investments
        3. Non-compliant activities
        4. Recommendations for SFDR and green bond issuance
        
        Document Content:
        {content}
        
        Provide analysis in the following JSON format:
        {{
            "taxonomy_alignment": [
                {{
                    "sector": "Manufacturing",
                    "alignment_percentage": 0.75,
                    "eligible_activities": ["Renewable energy", "Green buildings"],
                    "non_compliant_activities": ["Fossil fuel financing"],
                    "recommendations": ["Increase renewable energy portfolio", "Phase out coal financing"]
                }}
            ],
            "environmental_score": 0.82,
            "social_score": 0.75,
            "governance_score": 0.88,
            "overall_score": 0.82
        }}
        """

    def _create_climate_prompt(self) -> str:
        return """
        You are a climate risk expert analyzing Climate Risk Stress Test Reports using TCFD principles.
        
        Analyze the following document for {bank} bank and evaluate:
        1. Climate stress test methodology
        2. Missing scenario analysis, transition risk metrics, and physical risk disclosures
        3. Recommendations for regulatory and investor transparency
        
        Document Content:
        {content}
        
        Provide analysis in the following JSON format:
        {{
            "climate_risk_metrics": [
                {{
                    "metric_name": "Carbon footprint",
                    "value": 125.5,
                    "unit": "tCO2e",
                    "scenario": "2°C pathway",
                    "risk_level": "Medium",
                    "trend": "Decreasing"
                }}
            ],
            "environmental_score": 0.79,
            "social_score": 0.81,
            "governance_score": 0.85,
            "overall_score": 0.82
        }}
        """

    def _create_drift_prompt(self) -> str:
        return """
        You are an ESG drift detection expert comparing current disclosures with previous year's reports.
        
        Analyze the following document for {bank} bank and identify:
        1. Regression in sustainability KPIs
        2. Changes in taxonomy alignment
        3. Climate risk exposure changes
        4. Corrective actions needed
        
        Document Content:
        {content}
        
        Provide analysis in the following JSON format:
        {{
            "drift_indicators": [
                {{
                    "kpi_name": "ESG Score",
                    "previous_value": 0.85,
                    "current_value": 0.82,
                    "change_percentage": -3.5,
                    "direction": "Decreasing",
                    "significance": "Significant"
                }}
            ],
            "environmental_score": 0.80,
            "social_score": 0.83,
            "governance_score": 0.87,
            "overall_score": 0.83
        }}
        """

    async def analyze_document(
        self, 
        content: str, 
        bank: str, 
        document_type: str, 
        year: int
    ) -> Dict[str, Any]:
        """Analyze ESG document and return comprehensive analysis"""
        
        try:
            # Select appropriate prompt based on document type
            if document_type == "CSRD":
                prompt = self.csrd_prompt
            elif document_type == "EU_Taxonomy":
                prompt = self.taxonomy_prompt
            elif document_type == "Climate_Risk":
                prompt = self.climate_prompt
            else:
                prompt = self.drift_prompt

            # Format prompt with content
            formatted_prompt = prompt.format(
                content=content[:8000],  # Limit content length
                bank=bank
            )

            # Get AI analysis
            messages = [
                SystemMessage(content="You are an expert ESG analyst. Provide accurate, detailed analysis in the specified JSON format."),
                HumanMessage(content=formatted_prompt)
            ]
            
            response = await self.llm.agenerate([messages])
            analysis_text = response.generations[0][0].text
            
            # Parse JSON response
            try:
                analysis = json.loads(analysis_text)
            except json.JSONDecodeError:
                # Fallback analysis if JSON parsing fails
                analysis = self._create_fallback_analysis(bank, document_type)
            
            # Add metadata
            analysis.update({
                "bank": bank,
                "document_type": document_type,
                "year": year,
                "analysis_timestamp": asyncio.get_event_loop().time()
            })
            
            return analysis
            
        except Exception as e:
            print(f"Error in ESG analysis: {str(e)}")
            return self._create_fallback_analysis(bank, document_type)

    def _create_fallback_analysis(self, bank: str, document_type: str) -> Dict[str, Any]:
        """Create fallback analysis when AI analysis fails"""
        return {
            "bank": bank,
            "document_type": document_type,
            "environmental_score": 0.75,
            "social_score": 0.75,
            "governance_score": 0.75,
            "overall_score": 0.75,
            "csrd_gaps": [],
            "taxonomy_alignment": [],
            "climate_risk_metrics": [],
            "drift_indicators": [],
            "error": "Analysis failed, using fallback values"
        }

    async def calculate_esg_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate weighted ESG score"""
        env_score = analysis.get("environmental_score", 0.75)
        soc_score = analysis.get("social_score", 0.75)
        gov_score = analysis.get("governance_score", 0.75)
        
        # Weighted average (can be customized)
        weights = {"environmental": 0.4, "social": 0.3, "governance": 0.3}
        
        overall_score = (
            env_score * weights["environmental"] +
            soc_score * weights["social"] +
            gov_score * weights["governance"]
        )
        
        return round(overall_score, 2)

    async def detect_compliance_gaps(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect compliance gaps from analysis"""
        gaps = []
        
        # CSRD gaps
        csrd_gaps = analysis.get("csrd_gaps", [])
        for gap in csrd_gaps:
            if gap.get("severity") in ["High", "Critical"]:
                gaps.append({
                    "regulation": "CSRD",
                    "gap_type": gap.get("status", "Missing"),
                    "description": gap.get("description", ""),
                    "severity": gap.get("severity", "Medium"),
                    "recommendation": gap.get("recommendation", "")
                })
        
        return gaps

    async def generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate strategic recommendations based on analysis"""
        recommendations = []
        
        # Environmental recommendations
        env_score = analysis.get("environmental_score", 0.75)
        if env_score < 0.8:
            recommendations.append("Enhance environmental risk management and disclosure")
        
        # Social recommendations
        soc_score = analysis.get("social_score", 0.75)
        if soc_score < 0.8:
            recommendations.append("Improve social impact measurement and reporting")
        
        # Governance recommendations
        gov_score = analysis.get("governance_score", 0.75)
        if gov_score < 0.8:
            recommendations.append("Strengthen governance frameworks and oversight")
        
        # Taxonomy recommendations
        taxonomy_data = analysis.get("taxonomy_alignment", [])
        for sector in taxonomy_data:
            if sector.get("alignment_percentage", 0) < 0.7:
                recommendations.append(f"Increase EU Taxonomy alignment in {sector.get('sector', 'sector')}")
        
        return recommendations[:5]  # Limit to top 5 recommendations 