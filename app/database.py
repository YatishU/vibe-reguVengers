from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os
from datetime import datetime
from typing import Generator
import asyncio

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://esg_user:esg_password@localhost/esg_copilot")

# Create engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")

# Database models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="analyst")
    created_at = Column(DateTime, default=datetime.utcnow)

class Bank(Base):
    __tablename__ = "banks"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)  # IG, RB, AB
    name = Column(String)
    country = Column(String, default="Netherlands")
    sector = Column(String, default="Banking")
    created_at = Column(DateTime, default=datetime.utcnow)

class ESGDocument(Base):
    __tablename__ = "esg_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    bank = Column(String, index=True)
    document_type = Column(String)  # CSRD, EU_Taxonomy, Climate_Risk
    year = Column(Integer)
    content = Column(Text)
    analysis = Column(JSON)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    file_size = Column(Integer)
    status = Column(String, default="processed")

class ESGAnalysis(Base):
    __tablename__ = "esg_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    bank = Column(String, index=True)
    document_id = Column(Integer, ForeignKey("esg_documents.id"))
    analysis_type = Column(String)  # CSRD, EU_Taxonomy, Climate_Risk, Drift
    year = Column(Integer)
    
    # ESG Scores
    environmental_score = Column(Float)
    social_score = Column(Float)
    governance_score = Column(Float)
    overall_score = Column(Float)
    
    # Detailed analysis
    csrd_gaps = Column(JSON)
    taxonomy_alignment = Column(JSON)
    climate_risk_metrics = Column(JSON)
    drift_indicators = Column(JSON)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ESGMetrics(Base):
    __tablename__ = "esg_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    bank = Column(String, index=True)
    metric_name = Column(String)
    metric_value = Column(Float)
    metric_unit = Column(String)
    year = Column(Integer)
    category = Column(String)  # Environmental, Social, Governance
    created_at = Column(DateTime, default=datetime.utcnow)

class ComplianceGaps(Base):
    __tablename__ = "compliance_gaps"
    
    id = Column(Integer, primary_key=True, index=True)
    bank = Column(String, index=True)
    regulation = Column(String)  # CSRD, EU_Taxonomy, SFDR
    gap_type = Column(String)  # Missing, Incomplete, Non-compliant
    description = Column(Text)
    severity = Column(String)  # Low, Medium, High, Critical
    recommendation = Column(Text)
    year = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow) 