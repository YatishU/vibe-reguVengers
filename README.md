# ESG Copilot - Dutch Banks ESG Compliance Assistant

🚀 **AI-powered ESG compliance, risk detection, and sustainability framework alignment for Dutch banks**

## 🌟 Features

### 📊 Comprehensive ESG Analysis
- **CSRD Compliance Analysis**: Double materiality assessment, stakeholder engagement, value chain analysis
- **EU Taxonomy Validation**: Technical screening criteria, sustainable activities classification
- **Climate Risk Assessment**: TCFD framework compliance, scenario analysis, stress testing
- **ESG Drift Detection**: Performance monitoring, trend analysis, corrective actions
- **Impact Analysis**: Risk exposure, stakeholder trust, strategic opportunities
- **Vision 2030 Alignment**: UN SDG mapping, climate neutrality, biodiversity assessment

### 🎯 Supported Banks
- **ING Group (IG)**: Retail banking, corporate banking, investment banking
- **Rabobank (RB)**: Agriculture, food processing, rural development
- **ABN AMRO (AB)**: Retail banking, private banking, commercial banking

### 📈 Advanced Analytics
- Real-time ESG scoring and benchmarking
- Interactive dashboards with Chart.js visualizations
- Compliance heatmaps and risk distribution analysis
- Trend analysis and drift detection
- Comparative analysis across banks

### 🧪 BDD Test Cases
- Comprehensive test coverage for all ESG analysis features
- Azure Test Plan integration with unique test IDs
- Gherkin scenarios for behavior-driven development
- Automated test execution ready
- Export capabilities for Azure DevOps

## 🛠️ Tech Stack

### Frontend
- **FastAPI** with Jinja2 templates
- **Tailwind CSS** for modern, responsive design
- **Chart.js** for interactive data visualizations
- **Heroicons** for beautiful UI icons

### Backend
- **Python FastAPI** for high-performance API
- **LangChain** for AI-powered document analysis
- **Mock LLM Service** for demonstration (no API keys required)
- **PyMuPDF** for PDF document parsing

### Testing
- **BDD/Cucumber** test cases
- **Azure Test Plan** integration
- **Comprehensive test coverage**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ESG-Sustainable-App
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python main.py
```

4. **Access the application**
Open your browser and navigate to: `http://localhost:3000`

## 📱 Application Structure

### Main Pages
- **Dashboard** (`/`): Overview with bank cards and quick stats
- **Comprehensive Dashboard** (`/dashboard`): Detailed ESG analysis with charts
- **Document Upload** (`/upload`): Upload ESG reports for analysis
- **Test Cases** (`/test-cases`): BDD test cases with Azure integration

### API Endpoints
- `GET /`: Main dashboard
- `GET /dashboard`: Comprehensive ESG dashboard
- `GET /upload`: Document upload page
- `POST /upload-document`: Handle document upload and analysis
- `GET /analysis/{bank_code}`: Detailed bank analysis
- `GET /test-cases`: BDD test cases page
- `GET /api/esg-data/{bank_code}`: ESG data API
- `GET /api/dashboard-data`: Dashboard data API

## 📊 ESG Analysis Features

### CSRD Compliance
- Double materiality assessment scoring
- Stakeholder engagement analysis
- Value chain impact assessment
- Forward-looking information disclosure
- EBA guidelines alignment

### EU Taxonomy Validation
- Technical screening criteria compliance
- Sustainable activities classification
- Climate change mitigation assessment
- Climate change adaptation evaluation
- Green investment opportunities

### Climate Risk Assessment
- TCFD framework compliance scoring
- Scenario analysis coverage
- Transition risk metrics
- Physical risk disclosures
- Climate stress testing methodology

### ESG Scoring
- Overall ESG score (0-100)
- Environmental, Social, Governance breakdown
- EU regulation alignment
- UN SDG mapping
- Weighted performance analysis

## 🧪 Testing Framework

### BDD Test Cases
- **21 comprehensive test cases** across all banks
- **Azure Test Plan integration** with unique IDs
- **Gherkin scenarios** for behavior-driven development
- **Acceptance criteria** for each test case
- **Automation-ready** test execution

### Test Categories
- CSRD Compliance Analysis
- EU Taxonomy Validation
- Climate Risk Assessment
- ESG Scoring System
- Drift Detection
- Impact Analysis
- Vision 2030 Alignment

### Azure Integration
- Test cases mapped to Azure Test Plan components
- Unique test IDs for traceability
- Export capabilities for Azure DevOps
- Comprehensive test execution reporting

## 🎨 UI/UX Features

### Modern Design
- **Responsive design** for all devices
- **Beautiful gradients** and color schemes
- **Interactive charts** and visualizations
- **Smooth animations** and transitions
- **Accessibility compliant** interface

### User Experience
- **Intuitive navigation** with clear sections
- **Real-time data updates** and live indicators
- **Comprehensive tooltips** and help text
- **Export capabilities** for reports and data
- **Mobile-friendly** responsive design

### Data Visualization
- **ESG score comparison charts**
- **Compliance heatmaps**
- **Risk distribution analysis**
- **Trend analysis graphs**
- **SDG progress tracking**

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set for production deployment
PORT=3000
HOST=0.0.0.0
DEBUG=False
```

### Customization
- Modify bank data in `main.py` (SAMPLE_BANKS)
- Adjust ESG analysis parameters in `src/services/esg_analyzer.py`
- Customize test cases in `src/utils/test_case_generator.py`
- Update UI colors in `templates/base.html`

## 📈 Performance

### Optimizations
- **FastAPI** for high-performance API responses
- **Efficient PDF parsing** with PyMuPDF
- **Optimized database queries** (when implemented)
- **Caching strategies** for repeated analysis
- **Async processing** for document uploads

### Scalability
- **Modular architecture** for easy scaling
- **Microservices ready** design
- **Container deployment** support
- **Load balancing** capabilities
- **Database optimization** ready

## 🔒 Security

### Features
- **Input validation** for all user inputs
- **File upload security** with type checking
- **XSS protection** with template escaping
- **CSRF protection** for forms
- **Secure headers** implementation

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
```bash
# Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 3000 --workers 4

# Using Docker (if Dockerfile is added)
docker build -t esg-copilot .
docker run -p 3000:3000 esg-copilot
```

## 📝 API Documentation

### ESG Data Endpoint
```http
GET /api/esg-data/{bank_code}
```

**Response:**
```json
{
  "csrd_analysis": {
    "impact_materiality_score": 78.5,
    "financial_materiality_score": 82.3,
    "compliance_status": "partially_compliant"
  },
  "taxonomy_validation": {
    "alignment_score": 75.8,
    "eligible_green_investments": 35.2
  },
  "climate_risk": {
    "tcfd_compliance_score": 81.5,
    "scenario_analysis_coverage": {...}
  }
}
```

### Dashboard Data Endpoint
```http
GET /api/dashboard-data
```

**Response:**
```json
{
  "esg_scores": {
    "IG": 78.5,
    "RB": 82.3,
    "AB": 75.8
  },
  "compliance_heatmap": {...},
  "drift_trends": {...}
}
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

### Code Standards
- Follow PEP 8 Python style guide
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation for changes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Dutch Banking Sector** for ESG compliance requirements
- **EU Regulatory Framework** for sustainability standards
- **UN Sustainable Development Goals** for global impact
- **TCFD Framework** for climate risk assessment
- **Azure DevOps** for test management integration

## 📞 Support

For questions, issues, or contributions:
- Create an issue in the repository
- Contact the development team
- Check the documentation for common solutions

---

**ESG Copilot** - Empowering Dutch banks with AI-driven ESG compliance and sustainability insights! 🌱📊 