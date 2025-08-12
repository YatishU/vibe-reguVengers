import asyncio
import json
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import openai
from datetime import datetime

from .rag_service import RAGService
from ..models import (
    CSRDGap, TaxonomyAlignment, ClimateRiskMetric, 
    BankCode, DocumentType, AnalysisType, Severity
)
from ..utils.config import settings

class EnhancedESGAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Initialize RAG service
        self.rag_service = RAGService()
        
        # Initialize analysis prompts with RAG integration
        self.csrd_prompt = self._create_enhanced_csrd_prompt()
        self.taxonomy_prompt = self._create_enhanced_taxonomy_prompt()
        self.climate_prompt = self._create_enhanced_climate_prompt()
        self.drift_prompt = self._create_enhanced_drift_prompt()

    def _create_enhanced_csrd_prompt(self) -> str:
        return """
        You are an ESG compliance expert analyzing CSRD Double Materiality Assessment Reports for Dutch banks.
        
        Use the following latest ESG knowledge and regulations to provide accurate analysis:
        
        RELEVANT KNOWLEDGE BASE:
        {rag_context}
        
        Analyze the following document content for {bank} bank and identify:
        1. Gaps in impact and financial materiality disclosures
        2. Compliance with EBA guidelines and Article 19a of CSRD directive
        3. Regulatory risks and improvement recommendations
        4. Latest regulatory requirements and best practices
        
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
                    "recommendation": "Specific improvement recommendation",
                    "regulatory_source": "Source regulation or guideline"
                }}
            ],
            "environmental_score": 0.85,
            "social_score": 0.78,
            "governance_score": 0.92,
            "overall_score": 0.85,
            "compliance_level": "High/Medium/Low",
            "latest_regulatory_updates": [
                {{
                    "update": "Description of latest requirement",
                    "impact": "High/Medium/Low",
                    "deadline": "Implementation deadline"
                }}
            ],
            "knowledge_sources_used": ["List of sources from knowledge base"]
        }}
        """

    def _create_enhanced_taxonomy_prompt(self) -> str:
        return """
        You are an EU Taxonomy expert analyzing alignment with technical screening criteria.
        
        Use the following latest ESG knowledge and regulations to provide accurate analysis:
        
        RELEVANT KNOWLEDGE BASE:
        {rag_context}
        
        Analyze the following document for {bank} bank and assess:
        1. EU Taxonomy alignment by sector
        2. Eligible green investments
        3. Non-compliant activities
        4. Recommendations for SFDR and green bond issuance
        5. Latest taxonomy criteria and updates
        
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
                    "recommendations": ["Increase renewable energy portfolio", "Phase out coal financing"],
                    "regulatory_basis": "EU Taxonomy Regulation Article X"
                }}
            ],
            "environmental_score": 0.82,
            "social_score": 0.75,
            "governance_score": 0.88,
            "overall_score": 0.82,
            "taxonomy_compliance": "High/Medium/Low",
            "latest_criteria_updates": [
                {{
                    "sector": "Affected sector",
                    "change": "Description of change",
                    "effective_date": "When change takes effect"
                }}
            ],
            "knowledge_sources_used": ["List of sources from knowledge base"]
        }}
        """

    def _create_enhanced_climate_prompt(self) -> str:
        return """
        You are a climate risk expert analyzing Climate Risk Stress Test Reports using TCFD principles.
        
        Use the following latest ESG knowledge and regulations to provide accurate analysis:
        
        RELEVANT KNOWLEDGE BASE:
        {rag_context}
        
        Analyze the following document for {bank} bank and evaluate:
        1. Climate stress test methodology
        2. Missing scenario analysis, transition risk metrics, and physical risk disclosures
        3. Recommendations for regulatory and investor transparency
        4. Latest climate risk requirements and best practices
        
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
                    "trend": "Decreasing",
                    "regulatory_requirement": "TCFD recommendation"
                }}
            ],
            "environmental_score": 0.79,
            "social_score": 0.81,
            "governance_score": 0.85,
            "overall_score": 0.82,
            "climate_risk_maturity": "Advanced/Intermediate/Basic",
            "latest_requirements": [
                {{
                    "requirement": "New climate risk disclosure requirement",
                    "deadline": "Implementation deadline",
                    "impact": "High/Medium/Low"
                }}
            ],
            "knowledge_sources_used": ["List of sources from knowledge base"]
        }}
        """

    def _create_enhanced_drift_prompt(self) -> str:
        return """
        You are an ESG drift detection expert comparing current disclosures with previous year's reports.
        
        Use the following latest ESG knowledge and regulations to provide accurate analysis:
        
        RELEVANT KNOWLEDGE BASE:
        {rag_context}
        
        Analyze the following document for {bank} bank and identify:
        1. Regression in sustainability KPIs
        2. Changes in taxonomy alignment
        3. Climate risk exposure changes
        4. Corrective actions needed
        5. Latest ESG trends and benchmarks
        
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
                    "significance": "Significant",
                    "benchmark": "Industry average or regulatory requirement"
                }}
            ],
            "environmental_score": 0.80,
            "social_score": 0.83,
            "governance_score": 0.87,
            "overall_score": 0.83,
            "drift_severity": "High/Medium/Low",
            "trend_analysis": [
                {{
                    "trend": "ESG trend description",
                    "industry_comparison": "How bank compares to industry",
                    "regulatory_implications": "Impact on compliance"
                }}
            ],
            "knowledge_sources_used": ["List of sources from knowledge base"]
        }}
        """

    async def analyze_document_with_rag(
        self, 
        content: str, 
        bank: str, 
        document_type: str, 
        year: int
    ) -> Dict[str, Any]:
        """Analyze ESG document using RAG for enhanced accuracy and latest information"""
        
        try:
            # Retrieve relevant context from knowledge base
            rag_context = await self._get_relevant_context(content, document_type, bank)
            
            # Select appropriate prompt based on document type
            if document_type == "CSRD":
                prompt = self.csrd_prompt
            elif document_type == "EU_Taxonomy":
                prompt = self.taxonomy_prompt
            elif document_type == "Climate_Risk":
                prompt = self.climate_prompt
            else:
                prompt = self.drift_prompt

            # Format prompt with content and RAG context
            formatted_prompt = prompt.format(
                content=content[:8000],  # Limit content length
                bank=bank,
                rag_context=self._format_rag_context(rag_context)
            )

            # Get AI analysis with RAG-enhanced context
            messages = [
                SystemMessage(content="You are an expert ESG analyst with access to the latest regulations and best practices. Use the provided knowledge base context to ensure your analysis is current and accurate. Provide detailed analysis in the specified JSON format."),
                HumanMessage(content=formatted_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            analysis_text = response.content
            
            # Parse JSON response
            try:
                analysis = json.loads(analysis_text)
            except json.JSONDecodeError:
                # Fallback analysis if JSON parsing fails
                analysis = await self._create_enhanced_fallback_analysis(bank, document_type, rag_context)
            
            # Add metadata and RAG information
            analysis.update({
                "bank": bank,
                "document_type": document_type,
                "year": year,
                "analysis_timestamp": datetime.now().isoformat(),
                "rag_enhanced": True,
                "context_sources": [ctx["metadata"].get("source", "Unknown") for ctx in rag_context],
                "context_relevance_scores": [ctx["relevance_score"] for ctx in rag_context]
            })
            
            return analysis
            
        except Exception as e:
            print(f"Error in enhanced ESG analysis: {str(e)}")
            return await self._create_enhanced_fallback_analysis(bank, document_type, [])

    async def _get_relevant_context(
        self, 
        content: str, 
        document_type: str, 
        bank: str
    ) -> List[Dict[str, Any]]:
        """Get relevant context from RAG knowledge base"""
        try:
            # Create search query based on content and document type
            search_query = f"{document_type} compliance analysis for {bank} bank"
            
            # Add key terms from content
            key_terms = self._extract_key_terms(content)
            if key_terms:
                search_query += f" {', '.join(key_terms)}"
            
            # Retrieve relevant context
            context = await self.rag_service.retrieve_relevant_context(
                query=search_query,
                document_type=document_type,
                bank=bank,
                top_k=5
            )
            
            return context
            
        except Exception as e:
            print(f"Error retrieving RAG context: {str(e)}")
            return []

    def _extract_key_terms(self, content: str) -> List[str]:
        """Extract key terms from content for better RAG retrieval"""
        try:
            # Simple keyword extraction (could be enhanced with NLP)
            key_terms = []
            
            # ESG-related keywords
            esg_keywords = [
                "sustainability", "environmental", "social", "governance", "climate",
                "carbon", "emissions", "risk", "compliance", "regulation",
                "taxonomy", "csrd", "sfdr", "tcfd", "materiality", "disclosure"
            ]
            
            content_lower = content.lower()
            for keyword in esg_keywords:
                if keyword in content_lower:
                    key_terms.append(keyword)
            
            return key_terms[:10]  # Limit to top 10 terms
            
        except Exception:
            return []

    def _format_rag_context(self, context: List[Dict[str, Any]]) -> str:
        """Format RAG context for prompt inclusion"""
        try:
            if not context:
                return "No relevant context available from knowledge base."
            
            formatted_context = "Latest ESG Knowledge and Regulations:\n\n"
            
            for i, ctx in enumerate(context, 1):
                source = ctx["metadata"].get("source", "Unknown")
                category = ctx["metadata"].get("category", "General")
                relevance = ctx["relevance_score"]
                
                formatted_context += f"{i}. Source: {source} ({category}) - Relevance: {relevance:.2f}\n"
                formatted_context += f"   Content: {ctx['content'][:500]}...\n\n"
            
            return formatted_context
            
        except Exception as e:
            print(f"Error formatting RAG context: {str(e)}")
            return "Error retrieving context from knowledge base."

    async def _create_enhanced_fallback_analysis(
        self, 
        bank: str, 
        document_type: str, 
        rag_context: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create enhanced fallback analysis when AI analysis fails"""
        fallback = {
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
            "rag_enhanced": True,
            "error": "Analysis failed, using fallback values",
            "context_sources": [ctx["metadata"].get("source", "Unknown") for ctx in rag_context] if rag_context else []
        }
        
        # Add document-type specific fields
        if document_type == "CSRD":
            fallback["compliance_level"] = "Medium"
            fallback["latest_regulatory_updates"] = []
        elif document_type == "EU_Taxonomy":
            fallback["taxonomy_compliance"] = "Medium"
            fallback["latest_criteria_updates"] = []
        elif document_type == "Climate_Risk":
            fallback["climate_risk_maturity"] = "Intermediate"
            fallback["latest_requirements"] = []
        else:
            fallback["drift_severity"] = "Medium"
            fallback["trend_analysis"] = []
        
        return fallback

    async def get_latest_regulatory_insights(self, bank: str, document_type: str) -> Dict[str, Any]:
        """Get latest regulatory insights for specific bank and document type"""
        try:
            # Get latest regulations from RAG service
            latest_regulations = await self.rag_service.get_latest_regulations()
            
            # Search for bank-specific insights
            bank_insights = await self.rag_service.search_esg_knowledge(
                query=f"{bank} bank {document_type} compliance",
                filters={"region": "Netherlands", "category": document_type}
            )
            
            return {
                "latest_regulations": latest_regulations,
                "bank_specific_insights": bank_insights,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting regulatory insights: {str(e)}")
            return {}

    async def compare_with_industry_benchmarks(
        self, 
        analysis: Dict[str, Any], 
        bank: str
    ) -> Dict[str, Any]:
        """Compare analysis results with industry benchmarks"""
        try:
            # Get industry benchmarks from knowledge base
            benchmarks = await self.rag_service.search_esg_knowledge(
                query="industry benchmarks ESG scores Dutch banks",
                filters={"category": "Benchmarks", "region": "Netherlands"}
            )
            
            # Calculate comparison metrics
            overall_score = analysis.get("overall_score", 0.75)
            
            # Mock industry average (in real implementation, this would come from actual data)
            industry_average = 0.78
            
            comparison = {
                "bank_score": overall_score,
                "industry_average": industry_average,
                "percentile": "75th" if overall_score > industry_average else "25th",
                "performance": "Above Average" if overall_score > industry_average else "Below Average",
                "benchmark_sources": [b["source"] for b in benchmarks],
                "recommendations": self._generate_benchmark_recommendations(overall_score, industry_average)
            }
            
            return comparison
            
        except Exception as e:
            print(f"Error comparing with benchmarks: {str(e)}")
            return {}

    def _generate_benchmark_recommendations(self, bank_score: float, industry_average: float) -> List[str]:
        """Generate recommendations based on benchmark comparison"""
        recommendations = []
        
        if bank_score < industry_average:
            recommendations.extend([
                "Focus on improving ESG disclosure quality",
                "Enhance stakeholder engagement practices",
                "Strengthen sustainability governance framework",
                "Invest in ESG data collection and reporting systems"
            ])
        else:
            recommendations.extend([
                "Maintain current ESG performance levels",
                "Share best practices with industry peers",
                "Continue innovation in sustainability initiatives",
                "Prepare for upcoming regulatory changes"
            ])
        
        return recommendations

    async def generate_enhanced_recommendations(
        self, 
        analysis: Dict[str, Any], 
        bank: str
    ) -> List[Dict[str, Any]]:
        """Generate enhanced recommendations using RAG knowledge"""
        try:
            recommendations = []
            
            # Get relevant knowledge for recommendations
            knowledge_context = await self.rag_service.search_esg_knowledge(
                query=f"{bank} ESG improvement recommendations",
                filters={"category": "Best_Practices"}
            )
            
            # Environmental recommendations
            env_score = analysis.get("environmental_score", 0.75)
            if env_score < 0.8:
                recommendations.append({
                    "category": "Environmental",
                    "priority": "High" if env_score < 0.7 else "Medium",
                    "recommendation": "Enhance environmental risk management and disclosure",
                    "regulatory_basis": "CSRD Article 19a",
                    "implementation_timeline": "6-12 months",
                    "knowledge_source": "EU Regulations"
                })
            
            # Social recommendations
            soc_score = analysis.get("social_score", 0.75)
            if soc_score < 0.8:
                recommendations.append({
                    "category": "Social",
                    "priority": "High" if soc_score < 0.7 else "Medium",
                    "recommendation": "Improve social impact measurement and reporting",
                    "regulatory_basis": "SFDR Requirements",
                    "implementation_timeline": "3-6 months",
                    "knowledge_source": "SFDR Guidelines"
                })
            
            # Governance recommendations
            gov_score = analysis.get("governance_score", 0.75)
            if gov_score < 0.8:
                recommendations.append({
                    "category": "Governance",
                    "priority": "High" if gov_score < 0.7 else "Medium",
                    "recommendation": "Strengthen governance frameworks and oversight",
                    "regulatory_basis": "Corporate Governance Code",
                    "implementation_timeline": "6-12 months",
                    "knowledge_source": "DNB Guidelines"
                })
            
            # Add knowledge-based recommendations
            for ctx in knowledge_context[:3]:  # Top 3 relevant pieces
                recommendations.append({
                    "category": "Best Practice",
                    "priority": "Medium",
                    "recommendation": f"Implement {ctx['metadata'].get('category', 'industry')} best practices",
                    "regulatory_basis": ctx['metadata'].get('source', 'Industry Standard'),
                    "implementation_timeline": "3-9 months",
                    "knowledge_source": ctx['metadata'].get('source', 'Knowledge Base')
                })
            
            return recommendations[:8]  # Limit to top 8 recommendations
            
        except Exception as e:
            print(f"Error generating enhanced recommendations: {str(e)}")
            return []

    async def get_knowledge_base_statistics(self) -> Dict[str, Any]:
        """Get statistics about the RAG knowledge base"""
        return await self.rag_service.get_knowledge_statistics() 