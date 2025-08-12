# 🌍 ESG Copilot with RAG - Dutch Banks Compliance Analysis

**AI-powered ESG compliance analysis for Dutch banks (IG, RB, AB) with Retrieval-Augmented Generation (RAG)**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Overview

ESG Copilot with RAG is a comprehensive AI-powered application designed to automate ESG compliance analysis for Dutch banks. The system uses **Retrieval-Augmented Generation (RAG)** to provide the most accurate and up-to-date analysis by combining:

- **Real-time Knowledge Base**: Continuously updated ESG regulations, guidelines, and best practices
- **Vector Search**: Semantic search across extensive ESG knowledge base
- **Enhanced AI Analysis**: Context-aware analysis using latest regulatory information
- **Automatic Updates**: Background updates from regulatory sources, news, and research

The system analyzes ESG-related documents including CSRD reports, EU Taxonomy alignments, and Climate Risk assessments to provide actionable insights and ensure regulatory compliance with the latest requirements.

### 🎯 Key Features

- **🧠 RAG-Enhanced Analysis**: Retrieval-Augmented Generation for accurate, up-to-date analysis
- **📊 AI-Powered Document Analysis**: Advanced NLP analysis of ESG documents using GPT-4
- **🏦 Multi-Bank Support**: Analysis for ING Group (IG), Rabobank (RB), and ABN AMRO (AB)
- **📈 Real-time Dashboard**: Beautiful visualizations with Chart.js and Tailwind CSS
- **🔍 Compliance Gap Detection**: Automated identification of regulatory gaps
- **📋 BDD Test Generation**: Azure Test Plan compatible test case generation
- **🔄 ESG Drift Detection**: Track changes in sustainability performance over time
- **📱 Responsive Design**: Modern, accessible UI that works on all devices
- **🔄 Auto-Updating Knowledge Base**: Continuous updates from regulatory sources
- **🔍 Semantic Search**: Advanced vector search across ESG knowledge base
- **📊 Industry Benchmarks**: Compare with industry standards and best practices

## 🏗️ Architecture

### Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | FastAPI + Jinja2 Templates + Tailwind CSS |
| **Backend** | Python (FastAPI), LangChain |
| **AI** | Azure OpenAI / HuggingFace Transformers |
| **Parsing** | PyMuPDF, PDF.js |
| **Storage** | PostgreSQL + ChromaDB Vector Store |
| **Security** | OAuth2, JWT, Azure AD |
| **Deployment** | Azure App Services / Docker |
| **Monitoring** | Sentry, Prometheus, Grafana |

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI Services   │
│   (Tailwind)    │◄──►│   (FastAPI)     │◄──►│   (OpenAI)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Templates     │    │   PostgreSQL    │    │   RAG Services  │
│   (Jinja2)      │    │   Database      │    │   (ChromaDB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   RAG Dashboard │    │   Knowledge     │    │   Auto-Updates  │
│   (Enhanced UI) │    │   Manager       │    │   (Background)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- OpenAI API key
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/esg-copilot.git
   cd esg-copilot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   # Create PostgreSQL database
   createdb esg_copilot
   
   # Run database migrations
   python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"
   ```

6. **Start the application**
   ```bash
   python -m app.main
   ```

7. **Access the application**
   - Open your browser and navigate to `http://localhost:3000`
   - The dashboard will be available at the root URL

## 📋 Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# Required
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=postgresql://user:password@localhost/esg_copilot
SECRET_KEY=your-secret-key

# Optional
DEBUG=False
AZURE_TENANT_ID=your-azure-tenant-id
PINECONE_API_KEY=your-pinecone-key
SENTRY_DSN=your-sentry-dsn
```

### Database Setup

The application uses PostgreSQL with the following tables:
- `users` - User management
- `banks` - Bank information
- `esg_documents` - Uploaded documents
- `esg_analyses` - Analysis results
- `esg_metrics` - ESG performance metrics
- `compliance_gaps` - Identified compliance gaps

## 🎯 Usage

### 1. RAG Dashboard

The RAG dashboard provides:
- **Knowledge Base Statistics**: Overview of ESG knowledge base content
- **Real-time Search**: Semantic search across ESG regulations and best practices
- **RAG Analysis Demo**: Interactive demo of enhanced analysis capabilities
- **Knowledge Management**: Tools for managing and updating the knowledge base
- **Auto-update Status**: Monitor background knowledge base updates

### 2. Dashboard Overview

The main dashboard provides:
- **ESG Performance Rankings**: Compare banks across environmental, social, and governance dimensions
- **Compliance Gap Analysis**: Identify regulatory compliance issues
- **Taxonomy Alignment**: Track EU Taxonomy compliance
- **Climate Risk Assessment**: Monitor climate-related risks
- **Drift Analysis**: Track changes over time

### 3. Document Upload

1. Navigate to the Upload page
2. Select the target bank (IG, RB, AB)
3. Choose document type (CSRD, EU Taxonomy, Climate Risk)
4. Upload PDF document (max 50MB)
5. Choose analysis type:
   - **Standard Analysis**: Traditional AI analysis
   - **RAG-Enhanced Analysis**: Enhanced with latest regulatory knowledge (recommended)
6. Submit for AI analysis

### 4. Analysis Results

The RAG-enhanced AI analysis provides:
- **CSRD Compliance**: Gap analysis against latest Article 19a requirements
- **EU Taxonomy Alignment**: Sector-specific alignment percentages with current criteria
- **Climate Risk Metrics**: TCFD-aligned risk assessments with latest guidelines
- **ESG Scoring**: Weighted environmental, social, and governance scores
- **Enhanced Recommendations**: Actionable suggestions based on latest best practices
- **Regulatory Context**: References to specific regulations and guidelines used
- **Industry Benchmarks**: Comparison with industry standards
- **Knowledge Sources**: Transparency about information sources used

### 5. Report Generation

Generate comprehensive reports including:
- Executive summaries
- Detailed compliance analysis with regulatory context
- Risk assessments using latest guidelines
- Strategic recommendations based on best practices
- Industry benchmark comparisons
- BDD test cases for Azure Test Plan

## 🔧 Development

### Project Structure

```
esg-copilot/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database models and connection
│   ├── models.py            # Pydantic models
│   ├── services/
│   │   ├── esg_analyzer.py  # AI analysis service
│   │   ├── document_parser.py # PDF parsing
│   │   ├── auth_service.py  # Authentication
│   │   └── dashboard_service.py # Dashboard data
│   ├── templates/           # Jinja2 templates
│   ├── static/              # Static files
│   └── utils/
│       └── config.py        # Configuration management
├── requirements.txt
├── env.example
└── README.md
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-bdd

# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

### Code Quality

```bash
# Install development dependencies
pip install black flake8 mypy

# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## 🚀 Deployment

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t esg-copilot .
   ```

2. **Run the container**
   ```bash
   docker run -p 3000:3000 --env-file .env esg-copilot
   ```

### Azure App Service

1. **Deploy to Azure**
   ```bash
   az webapp up --name esg-copilot --resource-group your-rg --runtime "PYTHON:3.9"
   ```

2. **Configure environment variables**
   ```bash
   az webapp config appsettings set --name esg-copilot --resource-group your-rg --settings @env.json
   ```

## 📊 API Documentation

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard |
| `/dashboard` | GET | ESG dashboard with charts |
| `/upload` | GET | Document upload page |
| `/upload-document` | POST | Upload and analyze document |
| `/api/esg-scores` | GET | Get ESG scores for all banks |
| `/api/taxonomy-alignment` | GET | Get EU Taxonomy alignment data |
| `/api/climate-risk` | GET | Get climate risk analysis |
| `/api/drift-analysis` | GET | Get ESG drift analysis |
| `/reports/{bank}` | GET | Generate bank-specific report |
| `/api/test-cases` | GET | Generate BDD test cases |
| `/rag-dashboard` | GET | RAG dashboard interface |
| `/api/rag/knowledge-base/stats` | GET | Get knowledge base statistics |
| `/api/rag/search` | GET | Search ESG knowledge base |
| `/api/rag/latest-regulations` | GET | Get latest regulatory updates |
| `/api/rag/analyze-with-context` | POST | Perform RAG-enhanced analysis |
| `/api/rag/regulatory-insights/{bank}/{doc_type}` | GET | Get regulatory insights |
| `/api/knowledge/status` | GET | Get knowledge base update status |
| `/api/knowledge/force-update` | POST | Force knowledge base update |

### Example API Usage

```python
import requests

# Get ESG scores
response = requests.get('http://localhost:3000/api/esg-scores')
esg_scores = response.json()

# Upload document with RAG enhancement
files = {'file': open('document.pdf', 'rb')}
data = {
    'bank': 'IG',
    'document_type': 'CSRD',
    'year': 2024,
    'use_rag': True  # Enable RAG enhancement
}
response = requests.post('http://localhost:3000/upload-document', files=files, data=data)

# Search ESG knowledge base
response = requests.get('http://localhost:3000/api/rag/search', params={
    'query': 'CSRD compliance requirements',
    'category': 'CSRD'
})
search_results = response.json()

# Get latest regulatory insights
response = requests.get('http://localhost:3000/api/rag/regulatory-insights/IG/CSRD')
insights = response.json()

# Perform RAG-enhanced analysis
response = requests.post('http://localhost:3000/api/rag/analyze-with-context', json={
    'content': 'Sample ESG document content...',
    'bank': 'IG',
    'document_type': 'CSRD',
    'year': 2024
})
analysis = response.json()
```

## 🧠 RAG Benefits

### Enhanced Accuracy
- **Up-to-date Analysis**: Always uses the latest regulatory requirements and guidelines
- **Context-Aware**: Provides analysis based on relevant regulatory context
- **Source Transparency**: Shows which regulations and guidelines were used
- **Industry Alignment**: Compares with current industry best practices

### Real-time Knowledge
- **Automatic Updates**: Background updates from regulatory sources
- **Latest Regulations**: CSRD, EU Taxonomy, SFDR, and TCFD updates
- **News Integration**: Latest ESG news and insights
- **Research Integration**: Best practices from UN PRI, SASB, and other organizations

### Improved Compliance
- **Regulatory Tracking**: Monitors changes in ESG regulations
- **Gap Identification**: Identifies compliance gaps against current requirements
- **Recommendation Quality**: Provides actionable recommendations based on latest standards
- **Risk Assessment**: Enhanced risk assessment using current guidelines

## 🔒 Security

- **Authentication**: JWT-based authentication with OAuth2
- **Authorization**: Role-based access control (admin, analyst, viewer)
- **Data Protection**: Encrypted storage and secure file handling
- **API Security**: Rate limiting and input validation
- **Compliance**: GDPR and financial data protection standards

## 📈 Monitoring

- **Application Monitoring**: Sentry for error tracking
- **Performance Monitoring**: Prometheus metrics
- **Health Checks**: Built-in health check endpoints
- **Logging**: Structured logging with configurable levels

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation for new features
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT-4 API
- **FastAPI** team for the excellent web framework
- **Tailwind CSS** for the beautiful UI components
- **Chart.js** for the interactive visualizations

## 📞 Support

For support and questions:
- 📧 Email: support@esgcopilot.com
- 💬 Discord: [ESG Copilot Community](https://discord.gg/esgcopilot)
- 📖 Documentation: [docs.esgcopilot.com](https://docs.esgcopilot.com)

---

**Made with ❤️ for sustainable banking compliance** 