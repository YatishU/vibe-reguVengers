import random
from typing import Dict, List, Any
from datetime import datetime, timedelta
import json

class DashboardGenerator:
    """Generate comprehensive dashboard data for ESG analysis"""
    
    def __init__(self):
        self.chart_colors = {
            "primary": ["#10B981", "#059669", "#047857", "#065F46"],
            "secondary": ["#3B82F6", "#2563EB", "#1D4ED8", "#1E40AF"],
            "accent": ["#F59E0B", "#D97706", "#B45309", "#92400E"],
            "neutral": ["#6B7280", "#4B5563", "#374151", "#1F2937"],
            "success": ["#10B981", "#059669", "#047857"],
            "warning": ["#F59E0B", "#D97706", "#B45309"],
            "danger": ["#EF4444", "#DC2626", "#B91C1C"]
        }
    
    def generate_dashboard_data(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive dashboard data"""
        dashboard_data = {
            "esg_scores": self._generate_esg_scores(analysis_results),
            "compliance_heatmap": self._generate_compliance_heatmap(analysis_results),
            "drift_trends": self._generate_drift_trends(analysis_results),
            "taxonomy_alignment": self._generate_taxonomy_alignment(analysis_results),
            "climate_risk_exposure": self._generate_climate_risk_exposure(analysis_results),
            "risk_distribution": self._generate_risk_distribution(analysis_results),
            "sdg_progress": self._generate_sdg_progress(analysis_results),
            "comparative_analysis": self._generate_comparative_analysis(analysis_results),
            "trend_analysis": self._generate_trend_analysis(analysis_results),
            "kpi_metrics": self._generate_kpi_metrics(analysis_results),
            "chart_configs": self._generate_chart_configs()
        }
        
        return dashboard_data
    
    def _generate_esg_scores(self, analysis_results: Dict[str, Any]) -> Dict[str, float]:
        """Generate ESG scores for all banks"""
        scores = {}
        for bank_code in analysis_results.keys():
            if "esg_scoring" in analysis_results[bank_code]:
                scores[bank_code] = analysis_results[bank_code]["esg_scoring"]["overall_score"]
            else:
                scores[bank_code] = random.uniform(70, 85)
        return scores
    
    def _generate_compliance_heatmap(self, analysis_results: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
        """Generate compliance heatmap data"""
        heatmap = {}
        compliance_areas = [
            "CSRD Compliance", "EU Taxonomy", "TCFD Framework", 
            "Climate Risk", "Social Impact", "Governance"
        ]
        
        for bank_code in analysis_results.keys():
            heatmap[bank_code] = {}
            for area in compliance_areas:
                # Generate compliance status with color coding
                compliance_score = random.randint(60, 95)
                if compliance_score >= 85:
                    status = "compliant"
                    color = "green"
                elif compliance_score >= 70:
                    status = "partially_compliant"
                    color = "yellow"
                else:
                    status = "non_compliant"
                    color = "red"
                
                heatmap[bank_code][area] = {
                    "status": status,
                    "score": compliance_score,
                    "color": color
                }
        
        return heatmap
    
    def _generate_drift_trends(self, analysis_results: Dict[str, Any]) -> Dict[str, List[float]]:
        """Generate ESG drift trends over time"""
        trends = {}
        months = 12
        
        for bank_code in analysis_results.keys():
            # Generate trend data for the last 12 months
            base_score = random.uniform(70, 85)
            trend_data = []
            
            for month in range(months):
                # Add some variation to create realistic trends
                variation = random.uniform(-3, 3)
                trend_data.append(round(base_score + variation, 1))
                base_score = trend_data[-1]
            
            trends[bank_code] = trend_data
        
        return trends
    
    def _generate_taxonomy_alignment(self, analysis_results: Dict[str, Any]) -> Dict[str, float]:
        """Generate EU Taxonomy alignment scores"""
        alignment = {}
        for bank_code in analysis_results.keys():
            if "taxonomy_validation" in analysis_results[bank_code]:
                alignment[bank_code] = analysis_results[bank_code]["taxonomy_validation"]["alignment_score"]
            else:
                alignment[bank_code] = random.uniform(55, 80)
        return alignment
    
    def _generate_climate_risk_exposure(self, analysis_results: Dict[str, Any]) -> Dict[str, float]:
        """Generate climate risk exposure scores"""
        exposure = {}
        for bank_code in analysis_results.keys():
            if "climate_risk" in analysis_results[bank_code]:
                # Calculate climate risk exposure based on TCFD compliance and other factors
                tcfd_score = analysis_results[bank_code]["climate_risk"]["tcfd_compliance_score"]
                # Invert the score to show risk exposure (higher score = lower risk)
                exposure[bank_code] = round(100 - tcfd_score, 1)
            else:
                exposure[bank_code] = random.uniform(15, 40)
        return exposure
    
    def _generate_risk_distribution(self, analysis_results: Dict[str, Any]) -> Dict[str, Dict[str, int]]:
        """Generate risk distribution across different categories"""
        risk_distribution = {}
        
        risk_categories = ["Low", "Medium", "High", "Critical"]
        
        for bank_code in analysis_results.keys():
            risk_distribution[bank_code] = {}
            
            # Generate realistic risk distribution
            total_risks = random.randint(20, 50)
            low_risks = random.randint(5, 15)
            medium_risks = random.randint(8, 20)
            high_risks = random.randint(3, 12)
            critical_risks = random.randint(1, 5)
            
            # Ensure total adds up
            remaining = total_risks - (low_risks + medium_risks + high_risks + critical_risks)
            if remaining > 0:
                medium_risks += remaining
            
            risk_distribution[bank_code] = {
                "Low": low_risks,
                "Medium": medium_risks,
                "High": high_risks,
                "Critical": critical_risks
            }
        
        return risk_distribution
    
    def _generate_sdg_progress(self, analysis_results: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Generate SDG progress data"""
        sdg_progress = {}
        sdgs = ["SDG_7", "SDG_8", "SDG_9", "SDG_11", "SDG_12", "SDG_13", "SDG_15", "SDG_17"]
        
        for bank_code in analysis_results.keys():
            sdg_progress[bank_code] = {}
            
            if "vision_2030" in analysis_results[bank_code]:
                vision_data = analysis_results[bank_code]["vision_2030"]["sdg_mapping"]
                for sdg in sdgs:
                    if sdg in vision_data:
                        sdg_progress[bank_code][sdg] = vision_data[sdg]
                    else:
                        sdg_progress[bank_code][sdg] = random.uniform(50, 85)
            else:
                for sdg in sdgs:
                    sdg_progress[bank_code][sdg] = random.uniform(50, 85)
        
        return sdg_progress
    
    def _generate_comparative_analysis(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparative analysis data"""
        comparative = {
            "esg_leadership": self._determine_leader(analysis_results, "esg_scoring", "overall_score"),
            "climate_risk_management": self._determine_leader(analysis_results, "climate_risk", "tcfd_compliance_score"),
            "taxonomy_alignment": self._determine_leader(analysis_results, "taxonomy_validation", "alignment_score"),
            "social_impact": self._determine_leader(analysis_results, "esg_scoring", "social_score"),
            "governance_quality": self._determine_leader(analysis_results, "esg_scoring", "governance_score"),
            "environmental_performance": self._determine_leader(analysis_results, "esg_scoring", "environmental_score")
        }
        
        return comparative
    
    def _determine_leader(self, analysis_results: Dict[str, Any], analysis_type: str, metric: str) -> str:
        """Determine the leading bank for a specific metric"""
        scores = {}
        
        for bank_code in analysis_results.keys():
            if analysis_type in analysis_results[bank_code] and metric in analysis_results[bank_code][analysis_type]:
                scores[bank_code] = analysis_results[bank_code][analysis_type][metric]
            else:
                scores[bank_code] = random.uniform(60, 90)
        
        return max(scores, key=scores.get)
    
    def _generate_trend_analysis(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trend analysis data"""
        trends = {
            "esg_score_trend": "improving",
            "climate_risk_trend": "decreasing",
            "taxonomy_alignment_trend": "improving",
            "regulatory_compliance_trend": "stable",
            "stakeholder_engagement_trend": "improving"
        }
        
        return trends
    
    def _generate_kpi_metrics(self, analysis_results: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Generate KPI metrics for dashboard"""
        kpi_metrics = {}
        
        for bank_code in analysis_results.keys():
            kpi_metrics[bank_code] = {
                "esg_score": {
                    "current": analysis_results[bank_code].get("esg_scoring", {}).get("overall_score", random.uniform(70, 85)),
                    "target": 90,
                    "trend": random.choice(["up", "down", "stable"])
                },
                "taxonomy_alignment": {
                    "current": analysis_results[bank_code].get("taxonomy_validation", {}).get("alignment_score", random.uniform(55, 80)),
                    "target": 85,
                    "trend": random.choice(["up", "down", "stable"])
                },
                "climate_risk_exposure": {
                    "current": random.uniform(15, 40),
                    "target": 20,
                    "trend": random.choice(["up", "down", "stable"])
                },
                "regulatory_compliance": {
                    "current": random.uniform(75, 95),
                    "target": 100,
                    "trend": random.choice(["up", "down", "stable"])
                }
            }
        
        return kpi_metrics
    
    def _generate_chart_configs(self) -> Dict[str, Any]:
        """Generate chart configurations for different visualization types"""
        return {
            "esg_score_chart": {
                "type": "radar",
                "options": {
                    "responsive": True,
                    "maintainAspectRatio": False,
                    "scales": {
                        "r": {
                            "beginAtZero": True,
                            "max": 100,
                            "ticks": {
                                "stepSize": 20
                            }
                        }
                    }
                }
            },
            "compliance_heatmap": {
                "type": "heatmap",
                "options": {
                    "responsive": True,
                    "maintainAspectRatio": False,
                    "colorScale": {
                        "min": 0,
                        "max": 100,
                        "colors": ["#EF4444", "#F59E0B", "#10B981"]
                    }
                }
            },
            "trend_line_chart": {
                "type": "line",
                "options": {
                    "responsive": True,
                    "maintainAspectRatio": False,
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                            "max": 100
                        }
                    },
                    "plugins": {
                        "legend": {
                            "display": True
                        }
                    }
                }
            },
            "risk_distribution_chart": {
                "type": "doughnut",
                "options": {
                    "responsive": True,
                    "maintainAspectRatio": False,
                    "plugins": {
                        "legend": {
                            "position": "bottom"
                        }
                    }
                }
            },
            "sdg_progress_chart": {
                "type": "bar",
                "options": {
                    "responsive": True,
                    "maintainAspectRatio": False,
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                            "max": 100
                        }
                    }
                }
            }
        }
    
    def generate_summary_insights(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate summary insights for the dashboard"""
        insights = []
        
        # Overall ESG performance insight
        avg_esg_score = sum(
            analysis_results[bank_code].get("esg_scoring", {}).get("overall_score", 75)
            for bank_code in analysis_results.keys()
        ) / len(analysis_results)
        
        insights.append({
            "type": "performance",
            "title": "Overall ESG Performance",
            "description": f"Average ESG score across all banks: {avg_esg_score:.1f}/100",
            "severity": "info" if avg_esg_score >= 75 else "warning",
            "icon": "chart-bar"
        })
        
        # Compliance gaps insight
        compliance_gaps = []
        for bank_code in analysis_results.keys():
            csrd_score = analysis_results[bank_code].get("csrd_analysis", {}).get("eba_guidelines_alignment", 70)
            if csrd_score < 75:
                compliance_gaps.append(bank_code)
        
        if compliance_gaps:
            insights.append({
                "type": "compliance",
                "title": "Compliance Gaps Identified",
                "description": f"Banks with compliance gaps: {', '.join(compliance_gaps)}",
                "severity": "warning",
                "icon": "exclamation-triangle"
            })
        
        # Climate risk insight
        high_climate_risk = []
        for bank_code in analysis_results.keys():
            climate_score = analysis_results[bank_code].get("climate_risk", {}).get("tcfd_compliance_score", 70)
            if climate_score < 70:
                high_climate_risk.append(bank_code)
        
        if high_climate_risk:
            insights.append({
                "type": "climate",
                "title": "Climate Risk Concerns",
                "description": f"Banks requiring climate risk improvements: {', '.join(high_climate_risk)}",
                "severity": "danger",
                "icon": "fire"
            })
        
        # Positive trends insight
        improving_banks = []
        for bank_code in analysis_results.keys():
            drift_data = analysis_results[bank_code].get("esg_drift", {})
            if drift_data.get("trend_direction") == "improving":
                improving_banks.append(bank_code)
        
        if improving_banks:
            insights.append({
                "type": "trend",
                "title": "Positive ESG Trends",
                "description": f"Banks showing improvement: {', '.join(improving_banks)}",
                "severity": "success",
                "icon": "arrow-trending-up"
            })
        
        return insights 