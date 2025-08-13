import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from app.services.esg_analyzer import ESGAnalyzer
from app.models import BankCode, DocumentType

class TestESGAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return ESGAnalyzer()

    @pytest.fixture
    def sample_content(self):
        return """
        This is a sample ESG document content for testing purposes.
        It contains information about environmental, social, and governance practices.
        The document discusses carbon emissions, employee diversity, and board composition.
        """

    @pytest.mark.asyncio
    async def test_analyze_document_csrd(self, analyzer, sample_content):
        """Test CSRD document analysis"""
        with patch.object(analyzer.llm, 'agenerate') as mock_generate:
            mock_response = Mock()
            mock_response.generations = [[Mock(text='{"environmental_score": 0.85, "social_score": 0.78, "governance_score": 0.92, "overall_score": 0.85, "csrd_gaps": []}')]]
            mock_generate.return_value = mock_response

            result = await analyzer.analyze_document(
                content=sample_content,
                bank="IG",
                document_type="CSRD",
                year=2024
            )

            assert result["bank"] == "IG"
            assert result["document_type"] == "CSRD"
            assert result["year"] == 2024
            assert "environmental_score" in result
            assert "social_score" in result
            assert "governance_score" in result

    @pytest.mark.asyncio
    async def test_analyze_document_taxonomy(self, analyzer, sample_content):
        """Test EU Taxonomy document analysis"""
        with patch.object(analyzer.llm, 'agenerate') as mock_generate:
            mock_response = Mock()
            mock_response.generations = [[Mock(text='{"environmental_score": 0.82, "social_score": 0.75, "governance_score": 0.88, "overall_score": 0.82, "taxonomy_alignment": []}')]]
            mock_generate.return_value = mock_response

            result = await analyzer.analyze_document(
                content=sample_content,
                bank="RB",
                document_type="EU_Taxonomy",
                year=2024
            )

            assert result["bank"] == "RB"
            assert result["document_type"] == "EU_Taxonomy"
            assert result["year"] == 2024

    @pytest.mark.asyncio
    async def test_analyze_document_climate_risk(self, analyzer, sample_content):
        """Test Climate Risk document analysis"""
        with patch.object(analyzer.llm, 'agenerate') as mock_generate:
            mock_response = Mock()
            mock_response.generations = [[Mock(text='{"environmental_score": 0.79, "social_score": 0.81, "governance_score": 0.85, "overall_score": 0.82, "climate_risk_metrics": []}')]]
            mock_generate.return_value = mock_response

            result = await analyzer.analyze_document(
                content=sample_content,
                bank="AB",
                document_type="Climate_Risk",
                year=2024
            )

            assert result["bank"] == "AB"
            assert result["document_type"] == "Climate_Risk"
            assert result["year"] == 2024

    @pytest.mark.asyncio
    async def test_analyze_document_json_error(self, analyzer, sample_content):
        """Test handling of JSON parsing errors"""
        with patch.object(analyzer.llm, 'agenerate') as mock_generate:
            mock_response = Mock()
            mock_response.generations = [[Mock(text='invalid json')]]
            mock_generate.return_value = mock_response

            result = await analyzer.analyze_document(
                content=sample_content,
                bank="IG",
                document_type="CSRD",
                year=2024
            )

            assert result["bank"] == "IG"
            assert result["document_type"] == "CSRD"
            assert "error" in result

    @pytest.mark.asyncio
    async def test_analyze_document_exception(self, analyzer, sample_content):
        """Test handling of analysis exceptions"""
        with patch.object(analyzer.llm, 'agenerate', side_effect=Exception("API Error")):
            result = await analyzer.analyze_document(
                content=sample_content,
                bank="IG",
                document_type="CSRD",
                year=2024
            )

            assert result["bank"] == "IG"
            assert result["document_type"] == "CSRD"
            assert "error" in result

    @pytest.mark.asyncio
    async def test_calculate_esg_score(self, analyzer):
        """Test ESG score calculation"""
        analysis = {
            "environmental_score": 0.8,
            "social_score": 0.7,
            "governance_score": 0.9
        }

        score = await analyzer.calculate_esg_score(analysis)
        expected_score = 0.8 * 0.4 + 0.7 * 0.3 + 0.9 * 0.3
        assert abs(score - expected_score) < 0.01

    @pytest.mark.asyncio
    async def test_detect_compliance_gaps(self, analyzer):
        """Test compliance gap detection"""
        analysis = {
            "csrd_gaps": [
                {
                    "article": "Article 19a",
                    "requirement": "Materiality assessment",
                    "status": "Missing",
                    "severity": "High",
                    "description": "No materiality assessment found",
                    "recommendation": "Conduct comprehensive assessment"
                },
                {
                    "article": "Article 19a",
                    "requirement": "Risk disclosure",
                    "status": "Incomplete",
                    "severity": "Low",
                    "description": "Basic risk disclosure present",
                    "recommendation": "Enhance risk disclosure"
                }
            ]
        }

        gaps = await analyzer.detect_compliance_gaps(analysis)
        assert len(gaps) == 1  # Only high severity gaps
        assert gaps[0]["severity"] == "High"

    @pytest.mark.asyncio
    async def test_generate_recommendations(self, analyzer):
        """Test recommendation generation"""
        analysis = {
            "environmental_score": 0.75,
            "social_score": 0.65,
            "governance_score": 0.85,
            "taxonomy_alignment": [
                {
                    "sector": "Manufacturing",
                    "alignment_percentage": 0.6
                }
            ]
        }

        recommendations = await analyzer.generate_recommendations(analysis)
        assert len(recommendations) > 0
        assert any("environmental" in rec.lower() for rec in recommendations)
        assert any("social" in rec.lower() for rec in recommendations)

    def test_create_fallback_analysis(self, analyzer):
        """Test fallback analysis creation"""
        fallback = analyzer._create_fallback_analysis("IG", "CSRD")
        
        assert fallback["bank"] == "IG"
        assert fallback["document_type"] == "CSRD"
        assert fallback["environmental_score"] == 0.75
        assert fallback["social_score"] == 0.75
        assert fallback["governance_score"] == 0.75
        assert fallback["overall_score"] == 0.75

    def test_csrd_prompt_creation(self, analyzer):
        """Test CSRD prompt creation"""
        prompt = analyzer._create_csrd_prompt()
        assert "CSRD" in prompt
        assert "Article 19a" in prompt
        assert "materiality" in prompt.lower()

    def test_taxonomy_prompt_creation(self, analyzer):
        """Test EU Taxonomy prompt creation"""
        prompt = analyzer._create_taxonomy_prompt()
        assert "EU Taxonomy" in prompt
        assert "technical screening criteria" in prompt.lower()

    def test_climate_prompt_creation(self, analyzer):
        """Test Climate Risk prompt creation"""
        prompt = analyzer._create_climate_prompt()
        assert "TCFD" in prompt
        assert "climate stress test" in prompt.lower()

    def test_drift_prompt_creation(self, analyzer):
        """Test Drift Detection prompt creation"""
        prompt = analyzer._create_drift_prompt()
        assert "drift" in prompt.lower()
        assert "KPIs" in prompt

if __name__ == "__main__":
    pytest.main([__file__]) 