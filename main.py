from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json
import os
from pathlib import Path
from typing import List, Optional
import uuid
from datetime import datetime
import asyncio

from src.services.esg_analyzer import ESGAnalyzer
from src.services.document_parser import DocumentParser
from src.services.mock_llm import MockLLMService
from src.models.esg_models import BankData, ESGReport, AnalysisResult
from src.utils.dashboard_generator import DashboardGenerator
from src.utils.test_case_generator import TestCaseGenerator

app = FastAPI(
    title="ESG Copilot - Dutch Banks ESG Compliance Assistant",
    description="AI-powered ESG compliance, risk detection, and sustainability framework alignment for Dutch banks",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize services
esg_analyzer = ESGAnalyzer()
document_parser = DocumentParser()
mock_llm = MockLLMService()
dashboard_generator = DashboardGenerator()
test_generator = TestCaseGenerator()

# Sample bank data for demonstration
SAMPLE_BANKS = {
    "IG": {
        "name": "ING Group",
        "full_name": "ING Groep N.V.",
        "country": "Netherlands",
        "sector": "Banking",
        "esg_score": 78.5
    },
    "RB": {
        "name": "Rabobank",
        "full_name": "Coöperatieve Rabobank U.A.",
        "country": "Netherlands", 
        "sector": "Banking",
        "esg_score": 82.3
    },
    "AB": {
        "name": "ABN AMRO",
        "full_name": "ABN AMRO Bank N.V.",
        "country": "Netherlands",
        "sector": "Banking", 
        "esg_score": 75.8
    }
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main dashboard page"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "banks": SAMPLE_BANKS
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """ESG Dashboard with comprehensive analysis"""
    # Generate comprehensive ESG analysis
    analysis_results = {}
    
    for bank_code, bank_info in SAMPLE_BANKS.items():
        analysis_results[bank_code] = {
            "csrd_analysis": esg_analyzer.analyze_csrd_compliance(bank_code),
            "taxonomy_validation": esg_analyzer.validate_eu_taxonomy(bank_code),
            "climate_risk": esg_analyzer.evaluate_climate_risk(bank_code),
            "esg_drift": esg_analyzer.detect_esg_drift(bank_code),
            "esg_scoring": esg_analyzer.generate_esg_score(bank_code),
            "impact_analysis": esg_analyzer.generate_impact_analysis(bank_code),
            "vision_2030": esg_analyzer.assess_vision_2030_alignment(bank_code)
        }
    
    dashboard_data = dashboard_generator.generate_dashboard_data(analysis_results)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "banks": SAMPLE_BANKS,
        "analysis_results": analysis_results,
        "dashboard_data": dashboard_data
    })

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    """Document upload page"""
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    bank_code: str = Form(...),
    document_type: str = Form(...)
):
    """Handle document upload and analysis"""
    try:
        # Save uploaded file
        file_path = f"uploads/{bank_code}_{document_type}_{uuid.uuid4()}.pdf"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Parse document
        parsed_content = document_parser.parse_pdf(file_path)
        
        # Analyze with ESG analyzer
        analysis_result = esg_analyzer.analyze_document(
            bank_code, document_type, parsed_content
        )
        
        return JSONResponse({
            "success": True,
            "message": "Document analyzed successfully",
            "analysis": analysis_result
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error processing document: {str(e)}"
        }, status_code=500)

@app.get("/analysis/{bank_code}", response_class=HTMLResponse)
async def bank_analysis(request: Request, bank_code: str):
    """Detailed analysis page for a specific bank"""
    if bank_code not in SAMPLE_BANKS:
        return JSONResponse({"error": "Bank not found"}, status_code=404)
    
    analysis_result = {
        "csrd_analysis": esg_analyzer.analyze_csrd_compliance(bank_code),
        "taxonomy_validation": esg_analyzer.validate_eu_taxonomy(bank_code),
        "climate_risk": esg_analyzer.evaluate_climate_risk(bank_code),
        "esg_drift": esg_analyzer.detect_esg_drift(bank_code),
        "esg_scoring": esg_analyzer.generate_esg_score(bank_code),
        "impact_analysis": esg_analyzer.generate_impact_analysis(bank_code),
        "vision_2030": esg_analyzer.assess_vision_2030_alignment(bank_code)
    }
    
    return templates.TemplateResponse("bank_analysis.html", {
        "request": request,
        "bank": SAMPLE_BANKS[bank_code],
        "bank_code": bank_code,
        "analysis": analysis_result
    })

@app.get("/test-cases", response_class=HTMLResponse)
async def test_cases(request: Request):
    """BDD test cases page"""
    test_cases = test_generator.generate_all_test_cases(SAMPLE_BANKS)
    
    return templates.TemplateResponse("test_cases.html", {
        "request": request,
        "test_cases": test_cases,
        "banks": SAMPLE_BANKS
    })

@app.get("/api/esg-data/{bank_code}")
async def get_esg_data(bank_code: str):
    """API endpoint for ESG data"""
    if bank_code not in SAMPLE_BANKS:
        return JSONResponse({"error": "Bank not found"}, status_code=404)
    
    analysis_result = {
        "csrd_analysis": esg_analyzer.analyze_csrd_compliance(bank_code),
        "taxonomy_validation": esg_analyzer.validate_eu_taxonomy(bank_code),
        "climate_risk": esg_analyzer.evaluate_climate_risk(bank_code),
        "esg_drift": esg_analyzer.detect_esg_drift(bank_code),
        "esg_scoring": esg_analyzer.generate_esg_score(bank_code),
        "impact_analysis": esg_analyzer.generate_impact_analysis(bank_code),
        "vision_2030": esg_analyzer.assess_vision_2030_alignment(bank_code)
    }
    
    return JSONResponse(analysis_result)

@app.get("/api/dashboard-data")
async def get_dashboard_data():
    """API endpoint for dashboard data"""
    analysis_results = {}
    
    for bank_code in SAMPLE_BANKS.keys():
        analysis_results[bank_code] = {
            "csrd_analysis": esg_analyzer.analyze_csrd_compliance(bank_code),
            "taxonomy_validation": esg_analyzer.validate_eu_taxonomy(bank_code),
            "climate_risk": esg_analyzer.evaluate_climate_risk(bank_code),
            "esg_drift": esg_analyzer.detect_esg_drift(bank_code),
            "esg_scoring": esg_analyzer.generate_esg_score(bank_code),
            "impact_analysis": esg_analyzer.generate_impact_analysis(bank_code),
            "vision_2030": esg_analyzer.assess_vision_2030_alignment(bank_code)
        }
    
    dashboard_data = dashboard_generator.generate_dashboard_data(analysis_results)
    return JSONResponse(dashboard_data)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info"
    ) 