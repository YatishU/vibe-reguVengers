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
from datetime import datetime

from .database import get_db, init_db, ESGDocument, ESGAnalysis
from .services.esg_analyzer import ESGAnalyzer
from .services.enhanced_esg_analyzer import EnhancedESGAnalyzer
from .services.rag_service import RAGService
from .services.knowledge_manager import KnowledgeManager
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
enhanced_esg_analyzer = EnhancedESGAnalyzer()
rag_service = RAGService()
knowledge_manager = KnowledgeManager()
document_parser = DocumentParser()
dashboard_service = DashboardService()

@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup"""
    await init_db()
    
    # Initialize RAG knowledge base
    try:
        await rag_service.initialize_knowledge_base()
        await knowledge_manager.initialize()
        print("✅ RAG knowledge base initialized")
    except Exception as e:
        print(f"⚠️ RAG initialization warning: {str(e)}")
    
    print("🚀 ESG Copilot with RAG started successfully!")

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

@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    """Reports page"""
    return templates.TemplateResponse("reports.html", {"request": request})

@app.get("/rag-dashboard", response_class=HTMLResponse)
async def rag_dashboard(request: Request):
    """RAG dashboard page"""
    return templates.TemplateResponse("rag_dashboard.html", {"request": request})

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    bank: str = Form(...),
    document_type: str = Form(...),
    year: int = Form(...),
    use_rag: bool = Form(True),
    db=Depends(get_db)
):
    """Upload and analyze ESG document with optional RAG enhancement"""
    try:
        # Validate file
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Parse document
        content = await document_parser.parse_pdf(file.file)
        
        # Analyze ESG content with RAG enhancement if requested
        if use_rag:
            analysis = await enhanced_esg_analyzer.analyze_document_with_rag(
                content=content,
                bank=bank,
                document_type=document_type,
                year=year
            )
        else:
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
            analysis=analysis,
            file_size=len(content),
            status="analyzed"
        )
        db.add(document)
        db.commit()
        
        return {"success": True, "analysis_id": document.id, "rag_enhanced": use_rag}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/banks/{bank}/analysis")
async def get_bank_analysis(bank: str, db=Depends(get_db)):
    """Get ESG analysis for specific bank"""
    try:
        analyses = db.query(ESGAnalysis).filter(ESGAnalysis.bank == bank).all()
        return {"bank": bank, "analyses": [{"id": a.id, "document_type": a.document_type, "year": a.year, "esg_score": a.esg_score, "created_at": a.created_at.isoformat() if a.created_at else None} for a in analyses]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving bank analysis: {str(e)}")

@app.get("/api/bank/{bank}")
async def get_bank_data(bank: str, db=Depends(get_db)):
    """Get bank data and reports - this fixes the /api/bank/{bank} endpoint the user mentioned"""
    try:
        # Get bank documents
        documents = db.query(ESGDocument).filter(ESGDocument.bank == bank).all()
        
        # Get bank analyses
        analyses = db.query(ESGAnalysis).filter(ESGAnalysis.bank == bank).all()
        
        # Aggregate data
        bank_data = {
            "bank": bank,
            "bank_name": {"IG": "ING Group", "RB": "Rabobank", "AB": "ABN AMRO"}.get(bank, bank),
            "total_documents": len(documents),
            "total_analyses": len(analyses),
            "documents": [
                {
                    "id": doc.id,
                    "filename": doc.filename,
                    "document_type": doc.document_type,
                    "year": doc.year,
                    "status": doc.status,
                    "created_at": doc.created_at.isoformat() if doc.created_at else None
                } for doc in documents
            ],
            "analyses": [
                {
                    "id": a.id,
                    "document_type": a.document_type,
                    "year": a.year,
                    "esg_score": a.esg_score,
                    "environmental_score": getattr(a, 'environmental_score', 0.0),
                    "social_score": getattr(a, 'social_score', 0.0),
                    "governance_score": getattr(a, 'governance_score', 0.0),
                    "compliance_rate": getattr(a, 'compliance_rate', 0.0),
                    "created_at": a.created_at.isoformat() if a.created_at else None
                } for a in analyses
            ]
        }
        
        return bank_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving bank data: {str(e)}")

@app.get("/api/reports")
async def get_reports(db=Depends(get_db)):
    """Get all reports"""
    try:
        # Get all documents with analysis
        documents = db.query(ESGDocument).all()
        
        reports = []
        for doc in documents:
            # Try to get corresponding analysis
            analysis = db.query(ESGAnalysis).filter(
                ESGAnalysis.bank == doc.bank,
                ESGAnalysis.document_type == doc.document_type,
                ESGAnalysis.year == doc.year
            ).first()
            
            report = {
                "id": doc.id,
                "bank": doc.bank,
                "document_type": doc.document_type,
                "year": doc.year,
                "status": doc.status,
                "esg_score": analysis.esg_score if analysis else 0.0,
                "compliance_rate": getattr(analysis, 'compliance_rate', 0.0) if analysis else 0.0,
                "environmental_score": getattr(analysis, 'environmental_score', 0.0) if analysis else 0.0,
                "social_score": getattr(analysis, 'social_score', 0.0) if analysis else 0.0,
                "governance_score": getattr(analysis, 'governance_score', 0.0) if analysis else 0.0,
                "created_at": doc.created_at.isoformat() if doc.created_at else None,
                "analysis_summary": getattr(analysis, 'summary', '') if analysis else '',
                "recommendations": getattr(analysis, 'recommendations', []) if analysis else []
            }
            reports.append(report)
        
        return reports
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving reports: {str(e)}")

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
async def generate_bank_report(bank: str, request: Request, db=Depends(get_db)):
    """Generate comprehensive ESG report for a bank - returns HTML template instead of JSON"""
    try:
        report = await dashboard_service.generate_bank_report(db, bank)
        return templates.TemplateResponse("reports.html", {
            "request": request,
            "bank": bank,
            "report": report
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating bank report: {str(e)}")

@app.get("/api/reports/{report_id}/download")
async def download_report(report_id: int, db=Depends(get_db)):
    """Download a specific report as PDF"""
    try:
        document = db.query(ESGDocument).filter(ESGDocument.id == report_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # For now, return the document content as text
        # In a real implementation, you would generate a PDF here
        from fastapi.responses import Response
        return Response(
            content=f"ESG Report for {document.bank} - {document.document_type} {document.year}\n\n{document.content[:1000]}...",
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={document.bank}_{document.document_type}_{document.year}_Report.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading report: {str(e)}")

@app.post("/api/reports/generate")
async def generate_new_report(
    request_data: dict,
    db=Depends(get_db)
):
    """Generate a new ESG report"""
    try:
        bank = request_data.get("bank")
        document_type = request_data.get("document_type", "CSRD")
        year = request_data.get("year", datetime.now().year)
        
        if not bank:
            raise HTTPException(status_code=400, detail="Bank parameter is required")
        
        # Create a new analysis entry
        analysis = ESGAnalysis(
            bank=bank,
            document_type=document_type,
            year=year,
            esg_score=0.75 + (hash(f"{bank}{document_type}{year}") % 100) / 400,  # Mock score
            status="In Progress"
        )
        db.add(analysis)
        db.commit()
        
        return {"success": True, "message": "Report generation started", "analysis_id": analysis.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.get("/api/test-cases")
async def get_bdd_test_cases():
    """Get BDD test cases for Azure Test Plan"""
    return await dashboard_service.generate_bdd_test_cases()

# RAG-specific endpoints
@app.get("/api/rag/knowledge-base/stats")
async def get_knowledge_base_stats():
    """Get RAG knowledge base statistics"""
    return await rag_service.get_knowledge_statistics()

@app.get("/api/rag/search")
async def search_esg_knowledge(
    query: str,
    category: str = None,
    source: str = None
):
    """Search ESG knowledge base"""
    filters = {}
    if category:
        filters["category"] = category
    if source:
        filters["source"] = source
    
    results = await rag_service.search_esg_knowledge(query, filters)
    return {"query": query, "results": results, "total": len(results)}

@app.get("/api/rag/latest-regulations")
async def get_latest_regulations():
    """Get latest ESG regulations and updates"""
    return await rag_service.get_latest_regulations()

@app.post("/api/rag/analyze-with-context")
async def analyze_with_rag_context(
    content: str,
    bank: str,
    document_type: str,
    year: int = 2024
):
    """Analyze content with RAG context"""
    analysis = await enhanced_esg_analyzer.analyze_document_with_rag(
        content=content,
        bank=bank,
        document_type=document_type,
        year=year
    )
    return analysis

@app.get("/api/rag/regulatory-insights/{bank}/{document_type}")
async def get_regulatory_insights(bank: str, document_type: str):
    """Get latest regulatory insights for specific bank and document type"""
    return await enhanced_esg_analyzer.get_latest_regulatory_insights(bank, document_type)

@app.post("/api/rag/compare-benchmarks")
async def compare_with_benchmarks(analysis: dict, bank: str):
    """Compare analysis results with industry benchmarks"""
    return await enhanced_esg_analyzer.compare_with_industry_benchmarks(analysis, bank)

@app.post("/api/rag/enhanced-recommendations")
async def get_enhanced_recommendations(analysis: dict, bank: str):
    """Get enhanced recommendations using RAG knowledge"""
    return await enhanced_esg_analyzer.generate_enhanced_recommendations(analysis, bank)

# Knowledge Management endpoints
@app.get("/api/knowledge/status")
async def get_knowledge_status():
    """Get knowledge base update status"""
    return await knowledge_manager.get_update_status()

@app.post("/api/knowledge/force-update")
async def force_knowledge_update():
    """Force immediate knowledge base update"""
    await knowledge_manager.force_update()
    return {"message": "Knowledge base update initiated"}

@app.get("/api/knowledge/summary")
async def get_knowledge_summary():
    """Get knowledge base summary"""
    return await knowledge_manager.get_knowledge_summary()

@app.post("/api/knowledge/add-custom")
async def add_custom_knowledge(
    content: str,
    title: str,
    source: str,
    category: str,
    priority: str = "Medium"
):
    """Add custom knowledge to the knowledge base"""
    await knowledge_manager.add_custom_knowledge(content, title, source, category, priority)
    return {"message": "Custom knowledge added successfully"}

@app.get("/api/knowledge/search-by-date")
async def search_knowledge_by_date(
    start_date: str,
    end_date: str
):
    """Search knowledge base by date range"""
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    return await knowledge_manager.search_knowledge_by_date_range(start, end)

@app.get("/api/knowledge/export")
async def export_knowledge_base(format: str = "json"):
    """Export knowledge base"""
    return await knowledge_manager.export_knowledge_base(format)

@app.post("/api/knowledge/cleanup")
async def cleanup_knowledge_base(days_old: int = 365):
    """Clean up old knowledge base entries"""
    await knowledge_manager.cleanup_old_knowledge(days_old)
    return {"message": f"Cleaned up knowledge base entries older than {days_old} days"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ESG Copilot with RAG"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info"
    ) 