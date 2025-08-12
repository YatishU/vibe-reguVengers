import os
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application settings
    app_name: str = "ESG Copilot"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://esg_user:esg_password@localhost/esg_copilot")
    
    # Security settings
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    openai_temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
    
    # Azure settings
    azure_tenant_id: Optional[str] = os.getenv("AZURE_TENANT_ID")
    azure_client_id: Optional[str] = os.getenv("AZURE_CLIENT_ID")
    azure_client_secret: Optional[str] = os.getenv("AZURE_CLIENT_SECRET")
    
    # Vector database settings
    pinecone_api_key: Optional[str] = os.getenv("PINECONE_API_KEY")
    pinecone_environment: Optional[str] = os.getenv("PINECONE_ENVIRONMENT")
    weaviate_url: Optional[str] = os.getenv("WEAVIATE_URL")
    
    # File upload settings
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "52428800"))  # 50MB
    upload_directory: str = os.getenv("UPLOAD_DIRECTORY", "uploads")
    allowed_file_types: list = ["application/pdf"]
    
    # Monitoring settings
    sentry_dsn: Optional[str] = os.getenv("SENTRY_DSN")
    prometheus_enabled: bool = os.getenv("PROMETHEUS_ENABLED", "True").lower() == "true"
    
    # ESG Analysis settings
    esg_analysis_batch_size: int = int(os.getenv("ESG_ANALYSIS_BATCH_SIZE", "10"))
    esg_score_weights: dict = {
        "environmental": 0.4,
        "social": 0.3,
        "governance": 0.3
    }
    
    # Banks configuration
    supported_banks: list = ["IG", "RB", "AB"]
    bank_names: dict = {
        "IG": "ING Group",
        "RB": "Rabobank",
        "AB": "ABN AMRO"
    }
    
    # Document types
    document_types: list = ["CSRD", "EU_Taxonomy", "Climate_Risk"]
    
    # Compliance frameworks
    compliance_frameworks: dict = {
        "CSRD": {
            "name": "Corporate Sustainability Reporting Directive",
            "version": "2024",
            "requirements": ["Double Materiality Assessment", "ESG Metrics", "Risk Disclosure"]
        },
        "EU_Taxonomy": {
            "name": "EU Taxonomy for Sustainable Activities",
            "version": "2024",
            "requirements": ["Technical Screening Criteria", "Alignment Assessment", "Green Investment Tracking"]
        },
        "Climate_Risk": {
            "name": "Climate Risk Stress Testing",
            "version": "2024",
            "requirements": ["TCFD Alignment", "Scenario Analysis", "Physical Risk Assessment"]
        }
    }
    
    # ESG Scoring thresholds
    esg_score_thresholds: dict = {
        "excellent": 0.85,
        "good": 0.75,
        "fair": 0.65,
        "poor": 0.55
    }
    
    # Risk levels
    risk_levels: dict = {
        "low": {"color": "#10B981", "score_range": (0.8, 1.0)},
        "medium": {"color": "#F59E0B", "score_range": (0.6, 0.8)},
        "high": {"color": "#EF4444", "score_range": (0.4, 0.6)},
        "critical": {"color": "#7F1D1D", "score_range": (0.0, 0.4)}
    }
    
    # Dashboard settings
    dashboard_refresh_interval: int = int(os.getenv("DASHBOARD_REFRESH_INTERVAL", "300"))  # 5 minutes
    chart_colors: list = [
        "#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6",
        "#06B6D4", "#84CC16", "#F97316", "#EC4899", "#6366F1"
    ]
    
    # API rate limiting
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # 1 hour
    
    # Logging settings
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Email settings (for notifications)
    smtp_host: Optional[str] = os.getenv("SMTP_HOST")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: Optional[str] = os.getenv("SMTP_USERNAME")
    smtp_password: Optional[str] = os.getenv("SMTP_PASSWORD")
    smtp_use_tls: bool = os.getenv("SMTP_USE_TLS", "True").lower() == "true"
    
    # Feature flags
    enable_ai_analysis: bool = os.getenv("ENABLE_AI_ANALYSIS", "True").lower() == "true"
    enable_real_time_updates: bool = os.getenv("ENABLE_REAL_TIME_UPDATES", "True").lower() == "true"
    enable_export_reports: bool = os.getenv("ENABLE_EXPORT_REPORTS", "True").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()

# Validate required settings
def validate_settings():
    """Validate required settings"""
    required_settings = [
        ("OPENAI_API_KEY", settings.openai_api_key),
        ("DATABASE_URL", settings.database_url),
        ("SECRET_KEY", settings.secret_key)
    ]
    
    missing_settings = []
    for name, value in required_settings:
        if not value:
            missing_settings.append(name)
    
    if missing_settings:
        print(f"Warning: Missing required environment variables: {', '.join(missing_settings)}")
        print("Some features may not work correctly without these settings.")

# Validate settings on import
validate_settings() 