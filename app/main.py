from fastapi import FastAPI, Request, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from pathlib import Path
from typing import List, Optional
import json
import asyncio

from .database import get_db, init_db
from .models import User, ESGDocument, Bank, ESGAnalysis
from .services.esg_analyzer import ESGAnalyzer
from .services.document_parser import DocumentParser
from .services.auth_service import AuthService
from .services.dashboard_service import DashboardService
from .utils.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="ESG Copilot - Dutch Banks Compliance Analysis",
    description="AI-powered ESG compliance analysis for Dutch banks (IG, RB, AB)",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize services
auth_service = AuthService()
esg_analyzer = ESGAnalyzer()
document_parser = DocumentParser()
dashboard_service = DashboardService()

@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup"""
    await init_db()
    print("🚀 ESG Copilot started successfully!")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with ESG dashboard"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db=Depends(get_db)):
    """Main ESG dashboard"""
    banks = ["IG", "RB", "AB"]
    dashboard_data = await dashboard_service.get_dashboard_data(db, banks)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "dashboard_data": dashboard_data
    })

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    """Document upload page"""
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    bank: str = Form(...),
    document_type: str = Form(...),
    year: int = Form(...),
    db=Depends(get_db)
):
    """Upload and analyze ESG document"""
    try:
        # Validate file
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Parse document
        content = await document_parser.parse_pdf(file.file)
        
        # Analyze ESG content
        analysis = await esg_analyzer.analyze_document(
            content=content,
            bank=bank,
            document_type=document_type,
            year=year
        )
        
        # Save to database
        document = ESGDocument(
            filename=file.filename,
            bank=bank,
            document_type=document_type,
            year=year,
            content=content,
            analysis=analysis
        )
        db.add(document)
        db.commit()
        
        return {"success": True, "analysis_id": document.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/banks/{bank}/analysis")
async def get_bank_analysis(bank: str, db=Depends(get_db)):
    """Get ESG analysis for specific bank"""
    analyses = db.query(ESGAnalysis).filter(ESGAnalysis.bank == bank).all()
    return {"bank": bank, "analyses": analyses}

@app.get("/api/dashboard/summary")
async def get_dashboard_summary(db=Depends(get_db)):
    """Get dashboard summary data"""
    return await dashboard_service.get_summary_data(db)

@app.get("/api/esg-scores")
async def get_esg_scores(db=Depends(get_db)):
    """Get ESG scores for all banks"""
    return await dashboard_service.get_esg_scores(db)

@app.get("/api/taxonomy-alignment")
async def get_taxonomy_alignment(db=Depends(get_db)):
    """Get EU Taxonomy alignment data"""
    return await dashboard_service.get_taxonomy_alignment(db)

@app.get("/api/climate-risk")
async def get_climate_risk_data(db=Depends(get_db)):
    """Get climate risk analysis data"""
    return await dashboard_service.get_climate_risk_data(db)

@app.get("/api/drift-analysis")
async def get_drift_analysis(db=Depends(get_db)):
    """Get ESG drift analysis"""
    return await dashboard_service.get_drift_analysis(db)

@app.get("/reports/{bank}")
async def generate_bank_report(bank: str, db=Depends(get_db)):
    """Generate comprehensive ESG report for a bank"""
    report = await dashboard_service.generate_bank_report(db, bank)
    return report

@app.get("/api/test-cases")
async def get_bdd_test_cases():
    """Get BDD test cases for Azure Test Plan"""
    return await dashboard_service.generate_bdd_test_cases()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ESG Copilot"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info"
    ) 