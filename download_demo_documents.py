#!/usr/bin/env python3
"""
ESG Demo Documents Downloader
Downloads publicly available ESG documents and structures them for demo use
"""

import os
import requests
import urllib.parse
from pathlib import Path
import time
import json
from typing import Dict, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ESGDocumentDownloader:
    def __init__(self):
        self.demo_dir = Path("demo_documents")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Create directory structure
        self.create_directory_structure()
        
    def create_directory_structure(self):
        """Create the directory structure for demo documents"""
        directories = [
            self.demo_dir / "bank_reports",
            self.demo_dir / "regulatory",
            self.demo_dir / "best_practices",
            self.demo_dir / "metadata"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")

    def download_file(self, url: str, filename: str, category: str) -> bool:
        """Download a file from URL and save it to the appropriate directory"""
        try:
            logger.info(f"Downloading {filename} from {url}")
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Determine file extension
            content_type = response.headers.get('content-type', '')
            if 'pdf' in content_type.lower():
                ext = '.pdf'
            elif 'html' in content_type.lower():
                ext = '.html'
            else:
                ext = '.txt'
            
            # Save file
            file_path = self.demo_dir / category / f"{filename}{ext}"
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Successfully downloaded: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to download {filename}: {str(e)}")
            return False

    def create_sample_esg_content(self):
        """Create sample ESG content for demo purposes"""
        sample_documents = {
            "ING_ESG_Sample_2023": {
                "content": """
                ING Group ESG Report 2023 - Sample Content
                
                SUSTAINABILITY STRATEGY
                ING's sustainability strategy focuses on three key areas:
                1. Climate Action: Supporting the transition to a low-carbon economy
                2. Financial Health: Promoting financial inclusion and well-being
                3. Responsible Business: Operating with integrity and transparency
                
                CLIMATE RISK MANAGEMENT
                We have implemented comprehensive climate risk management frameworks:
                - Climate stress testing aligned with TCFD recommendations
                - Portfolio carbon footprint measurement and reduction targets
                - Green financing portfolio of €67 billion (2023)
                - Coal phase-out commitment by 2025
                
                CSRD COMPLIANCE
                Our reporting aligns with CSRD requirements:
                - Double materiality assessment completed
                - Principal adverse impacts identified and disclosed
                - Sustainability targets and progress tracking
                - Due diligence processes for ESG risks
                
                EU TAXONOMY ALIGNMENT
                Green asset ratio: 15.2% (2023)
                Eligible activities include:
                - Renewable energy financing
                - Green building projects
                - Sustainable transport
                - Circular economy initiatives
                
                ESG PERFORMANCE METRICS
                Environmental Score: 0.82
                Social Score: 0.78
                Governance Score: 0.91
                Overall ESG Score: 0.84
                
                CLIMATE TARGETS
                - Net-zero financed emissions by 2050
                - 50% reduction in financed emissions by 2030
                - 100% renewable energy for operations by 2025
                """,
                "metadata": {
                    "bank": "IG",
                    "document_type": "CSRD",
                    "year": 2023,
                    "source": "ING Group",
                    "category": "bank_reports"
                }
            },
            
            "Rabobank_Sustainability_Sample_2023": {
                "content": """
                Rabobank Sustainability Report 2023 - Sample Content
                
                SUSTAINABILITY APPROACH
                Rabobank's mission is "Growing a better world together" through:
                - Sustainable food and agriculture financing
                - Climate-positive banking
                - Social impact initiatives
                - Circular economy support
                
                CLIMATE RISK ASSESSMENT
                TCFD-aligned climate risk management:
                - Physical risk assessment for agricultural portfolios
                - Transition risk analysis for energy-intensive sectors
                - Scenario analysis using 2°C and 4°C pathways
                - Climate stress testing results disclosed
                
                AGRICULTURAL SUSTAINABILITY
                Key initiatives include:
                - €25 billion in sustainable food and agriculture financing
                - Support for regenerative agriculture practices
                - Biodiversity protection in farming operations
                - Food waste reduction programs
                
                EU TAXONOMY COMPLIANCE
                Green asset ratio: 18.7% (2023)
                Focus areas:
                - Sustainable agriculture and forestry
                - Renewable energy projects
                - Green building certification
                - Clean transportation
                
                SOCIAL IMPACT
                Financial inclusion programs:
                - €2.1 billion in microfinance
                - Support for 2.3 million smallholder farmers
                - Financial literacy programs reaching 500,000 people
                - Community development initiatives
                
                ESG PERFORMANCE
                Environmental Score: 0.85
                Social Score: 0.83
                Governance Score: 0.88
                Overall ESG Score: 0.85
                """,
                "metadata": {
                    "bank": "RB",
                    "document_type": "Climate_Risk",
                    "year": 2023,
                    "source": "Rabobank",
                    "category": "bank_reports"
                }
            },
            
            "ABN_AMRO_ESG_Sample_2023": {
                "content": """
                ABN AMRO ESG Report 2023 - Sample Content
                
                SUSTAINABILITY STRATEGY
                ABN AMRO's sustainability focus areas:
                1. Climate Action: Supporting the energy transition
                2. Circular Economy: Promoting resource efficiency
                3. Social Impact: Enhancing financial well-being
                4. Responsible Banking: Maintaining high governance standards
                
                CLIMATE TRANSITION SUPPORT
                Energy transition financing:
                - €15 billion in renewable energy projects
                - Support for hydrogen and battery storage
                - Green building financing programs
                - Electric vehicle infrastructure investment
                
                CIRCULAR ECONOMY INITIATIVES
                Circular economy financing:
                - €3.2 billion in circular economy projects
                - Support for waste-to-resource technologies
                - Product-as-a-service business models
                - Sustainable packaging solutions
                
                EU TAXONOMY ALIGNMENT
                Green asset ratio: 12.8% (2023)
                Eligible activities:
                - Renewable energy generation
                - Energy efficiency improvements
                - Sustainable transport infrastructure
                - Circular economy projects
                
                RISK MANAGEMENT
                ESG risk integration:
                - ESG risk assessment in credit processes
                - Climate risk stress testing
                - Biodiversity risk evaluation
                - Social risk monitoring
                
                ESG PERFORMANCE METRICS
                Environmental Score: 0.79
                Social Score: 0.81
                Governance Score: 0.89
                Overall ESG Score: 0.83
                
                SUSTAINABILITY TARGETS
                - Net-zero operations by 2030
                - 50% reduction in financed emissions by 2030
                - 100% sustainable electricity by 2025
                - Zero waste to landfill by 2025
                """,
                "metadata": {
                    "bank": "AB",
                    "document_type": "EU_Taxonomy",
                    "year": 2023,
                    "source": "ABN AMRO",
                    "category": "bank_reports"
                }
            }
        }
        
        # Save sample documents
        for doc_name, doc_data in sample_documents.items():
            # Save content as text file
            content_path = self.demo_dir / "bank_reports" / f"{doc_name}.txt"
            with open(content_path, 'w', encoding='utf-8') as f:
                f.write(doc_data["content"])
            
            # Save metadata
            metadata_path = self.demo_dir / "metadata" / f"{doc_name}_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(doc_data["metadata"], f, indent=2)
            
            logger.info(f"Created sample document: {doc_name}")

    def create_regulatory_documents(self):
        """Create sample regulatory documents"""
        regulatory_docs = {
            "DNB_Climate_Risk_Guidelines": {
                "content": """
                DNB Climate Risk Guidelines for Financial Institutions
                
                SUPERVISORY EXPECTATIONS
                The Dutch National Bank (DNB) expects financial institutions to:
                1. Integrate climate risks into risk management frameworks
                2. Conduct climate stress testing
                3. Disclose climate-related financial risks
                4. Develop climate transition plans
                
                CLIMATE RISK CATEGORIES
                Physical Risks:
                - Acute: Extreme weather events, natural disasters
                - Chronic: Gradual climate changes, temperature increases
                
                Transition Risks:
                - Policy: Regulatory changes, carbon pricing
                - Legal: Climate litigation, liability claims
                - Technology: Clean technology adoption
                - Market: Changing consumer preferences
                - Reputation: Stakeholder expectations
                
                RISK MANAGEMENT REQUIREMENTS
                1. Climate Risk Identification
                   - Portfolio carbon footprint assessment
                   - Sector-specific climate risk analysis
                   - Geographic exposure mapping
                
                2. Climate Risk Assessment
                   - Scenario analysis using multiple pathways
                   - Impact assessment on business models
                   - Financial impact quantification
                
                3. Integration into Risk Framework
                   - Credit risk: Climate factors in lending decisions
                   - Market risk: Climate-related market changes
                   - Operational risk: Climate impact on operations
                   - Strategic risk: Business model adaptation
                
                4. Monitoring and Reporting
                   - Regular climate risk reporting
                   - Progress tracking on climate targets
                   - Stakeholder communication
                
                SUPERVISORY REVIEW
                DNB will review:
                - Climate risk governance and oversight
                - Risk identification and assessment processes
                - Integration into risk management
                - Climate stress testing capabilities
                - Disclosure quality and transparency
                """,
                "metadata": {
                    "source": "DNB",
                    "category": "Climate_Risk",
                    "region": "Netherlands",
                    "type": "guideline"
                }
            },
            
            "EBA_ESG_Guidelines": {
                "content": """
                EBA Guidelines on ESG Risk Management
                
                REGULATORY FRAMEWORK
                The European Banking Authority (EBA) provides guidelines for:
                - ESG risk management and supervision
                - Climate risk stress testing
                - ESG disclosure requirements
                - Sustainable finance integration
                
                ESG RISK MANAGEMENT PRINCIPLES
                1. Governance and Strategy
                   - Board oversight of ESG risks
                   - ESG risk appetite definition
                   - Integration into business strategy
                   - Stakeholder engagement
                
                2. Risk Identification and Assessment
                   - ESG risk taxonomy development
                   - Materiality assessment
                   - Risk measurement methodologies
                   - Data quality and availability
                
                3. Risk Management and Controls
                   - ESG risk limits and thresholds
                   - Risk mitigation strategies
                   - Monitoring and reporting frameworks
                   - Internal control systems
                
                4. Disclosure and Transparency
                   - ESG risk disclosure requirements
                   - Reporting standards alignment
                   - Stakeholder communication
                   - Regulatory reporting
                
                CLIMATE RISK STRESS TESTING
                Requirements for climate stress testing:
                - Multiple scenario analysis (2°C, 4°C, disorderly transition)
                - Time horizons: short-term (1-3 years), medium-term (3-10 years)
                - Risk transmission channels analysis
                - Impact assessment on capital adequacy
                
                SUSTAINABLE FINANCE INTEGRATION
                Guidelines for sustainable finance:
                - Green asset ratio calculation
                - EU Taxonomy alignment assessment
                - Sustainable finance product development
                - ESG investment strategy implementation
                """,
                "metadata": {
                    "source": "EBA",
                    "category": "Sustainable_Finance",
                    "region": "EU",
                    "type": "guideline"
                }
            }
        }
        
        # Save regulatory documents
        for doc_name, doc_data in regulatory_docs.items():
            content_path = self.demo_dir / "regulatory" / f"{doc_name}.txt"
            with open(content_path, 'w', encoding='utf-8') as f:
                f.write(doc_data["content"])
            
            metadata_path = self.demo_dir / "metadata" / f"{doc_name}_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(doc_data["metadata"], f, indent=2)
            
            logger.info(f"Created regulatory document: {doc_name}")

    def create_best_practice_documents(self):
        """Create sample best practice documents"""
        best_practices = {
            "TCFD_Recommendations": {
                "content": """
                TCFD Recommendations for Climate-Related Financial Disclosures
                
                GOVERNANCE
                Disclose the organization's governance around climate-related risks and opportunities:
                1. Board oversight of climate-related risks and opportunities
                2. Management's role in assessing and managing climate-related risks and opportunities
                
                STRATEGY
                Disclose the actual and potential impacts of climate-related risks and opportunities on the organization's businesses, strategy, and financial planning:
                1. Climate-related risks and opportunities identified over short, medium, and long term
                2. Impact of climate-related risks and opportunities on businesses, strategy, and financial planning
                3. Resilience of organization's strategy to climate-related risks and opportunities
                
                RISK MANAGEMENT
                Disclose how the organization identifies, assesses, and manages climate-related risks:
                1. Processes for identifying and assessing climate-related risks
                2. Processes for managing climate-related risks
                3. Integration of climate-related risks into overall risk management
                
                METRICS AND TARGETS
                Disclose the metrics and targets used to assess and manage climate-related risks and opportunities:
                1. Metrics used to assess climate-related risks and opportunities
                2. Scope 1, Scope 2, and Scope 3 greenhouse gas emissions
                3. Targets used to manage climate-related risks and opportunities
                
                SCENARIO ANALYSIS
                Organizations should use scenario analysis to assess the resilience of their strategy:
                - 2°C scenario (orderly transition)
                - 4°C scenario (business as usual)
                - Disorderly transition scenarios
                - Physical risk scenarios
                
                DISCLOSURE PRINCIPLES
                1. Represent relevant information fairly, accurately, and completely
                2. Provide clear, balanced, and understandable information
                3. Present information in a consistent manner over time
                4. Disclose information on a timely basis
                5. Present information in a way that enables stakeholders to understand the impact
                """,
                "metadata": {
                    "source": "TCFD",
                    "category": "Climate_Risk",
                    "type": "best_practice"
                }
            },
            
            "GRI_Standards_Overview": {
                "content": """
                GRI Sustainability Reporting Standards Overview
                
                UNIVERSAL STANDARDS
                GRI 1: Foundation
                - Reporting principles and requirements
                - Stakeholder inclusiveness
                - Sustainability context
                - Materiality
                - Completeness
                
                GRI 2: General Disclosures
                - Organizational profile
                - Strategy, ethics, and integrity
                - Stakeholder engagement
                - Reporting practice
                - Governance
                
                GRI 3: Material Topics
                - Process for determining material topics
                - List of material topics
                - Management approach for material topics
                
                TOPIC STANDARDS
                Economic Topics:
                - Economic performance
                - Market presence
                - Indirect economic impacts
                - Procurement practices
                - Anti-corruption
                - Anti-competitive behavior
                
                Environmental Topics:
                - Materials
                - Energy
                - Water and effluents
                - Biodiversity
                - Emissions
                - Effluents and waste
                - Environmental compliance
                - Supplier environmental assessment
                
                Social Topics:
                - Employment
                - Labor/management relations
                - Occupational health and safety
                - Training and education
                - Diversity and equal opportunity
                - Non-discrimination
                - Freedom of association and collective bargaining
                - Child labor
                - Forced or compulsory labor
                - Human rights assessment
                - Local communities
                - Supplier social assessment
                - Public policy
                - Customer health and safety
                - Marketing and labeling
                - Customer privacy
                - Socioeconomic compliance
                
                REPORTING PRINCIPLES
                1. Accuracy: Information should be accurate and detailed
                2. Balance: Information should be unbiased and fairly represent positive and negative impacts
                3. Clarity: Information should be understandable and accessible
                4. Comparability: Information should be presented in a consistent manner
                5. Completeness: Information should cover all material topics
                6. Reliability: Information should be gathered, recorded, compiled, analyzed, and disclosed in a way that can be subject to examination
                7. Timeliness: Information should be available in time for stakeholders to make decisions
                8. Verifiability: Information should be presented in a way that enables internal and external parties to check it
                """,
                "metadata": {
                    "source": "GRI",
                    "category": "Reporting",
                    "type": "best_practice"
                }
            }
        }
        
        # Save best practice documents
        for doc_name, doc_data in best_practices.items():
            content_path = self.demo_dir / "best_practices" / f"{doc_name}.txt"
            with open(content_path, 'w', encoding='utf-8') as f:
                f.write(doc_data["content"])
            
            metadata_path = self.demo_dir / "metadata" / f"{doc_name}_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(doc_data["metadata"], f, indent=2)
            
            logger.info(f"Created best practice document: {doc_name}")

    def create_demo_index(self):
        """Create an index file for the demo documents"""
        index = {
            "demo_documents": {
                "description": "ESG Demo Documents for RAG-Enhanced Analysis",
                "created_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_documents": 7,
                "categories": {
                    "bank_reports": {
                        "description": "Sample ESG reports from Dutch banks",
                        "documents": [
                            {
                                "name": "ING_ESG_Sample_2023.txt",
                                "bank": "IG",
                                "document_type": "CSRD",
                                "year": 2023,
                                "description": "ING Group ESG report with climate risk and CSRD compliance"
                            },
                            {
                                "name": "Rabobank_Sustainability_Sample_2023.txt",
                                "bank": "RB",
                                "document_type": "Climate_Risk",
                                "year": 2023,
                                "description": "Rabobank sustainability report with agricultural focus"
                            },
                            {
                                "name": "ABN_AMRO_ESG_Sample_2023.txt",
                                "bank": "AB",
                                "document_type": "EU_Taxonomy",
                                "year": 2023,
                                "description": "ABN AMRO ESG report with circular economy focus"
                            }
                        ]
                    },
                    "regulatory": {
                        "description": "Regulatory guidelines and requirements",
                        "documents": [
                            {
                                "name": "DNB_Climate_Risk_Guidelines.txt",
                                "source": "DNB",
                                "category": "Climate_Risk",
                                "description": "Dutch National Bank climate risk guidelines"
                            },
                            {
                                "name": "EBA_ESG_Guidelines.txt",
                                "source": "EBA",
                                "category": "Sustainable_Finance",
                                "description": "EBA guidelines on ESG risk management"
                            }
                        ]
                    },
                    "best_practices": {
                        "description": "Industry best practices and frameworks",
                        "documents": [
                            {
                                "name": "TCFD_Recommendations.txt",
                                "source": "TCFD",
                                "category": "Climate_Risk",
                                "description": "TCFD recommendations for climate disclosures"
                            },
                            {
                                "name": "GRI_Standards_Overview.txt",
                                "source": "GRI",
                                "category": "Reporting",
                                "description": "GRI sustainability reporting standards"
                            }
                        ]
                    }
                }
            },
            "usage_instructions": {
                "upload_sequence": [
                    "1. Start with ING_ESG_Sample_2023.txt (CSRD document type)",
                    "2. Add Rabobank_Sustainability_Sample_2023.txt (Climate Risk document type)",
                    "3. Include ABN_AMRO_ESG_Sample_2023.txt (EU Taxonomy document type)",
                    "4. Use RAG-enhanced analysis for best results"
                ],
                "demo_scenarios": [
                    "Compare standard vs RAG-enhanced analysis",
                    "Search knowledge base for regulatory requirements",
                    "Generate enhanced recommendations",
                    "View industry benchmark comparisons"
                ]
            }
        }
        
        # Save index
        index_path = self.demo_dir / "demo_index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
        
        logger.info(f"Created demo index: {index_path}")

    def run(self):
        """Run the complete document download and creation process"""
        logger.info("Starting ESG demo document creation...")
        
        # Create sample documents
        self.create_sample_esg_content()
        self.create_regulatory_documents()
        self.create_best_practice_documents()
        
        # Create demo index
        self.create_demo_index()
        
        logger.info("Demo document creation completed!")
        logger.info(f"Documents created in: {self.demo_dir.absolute()}")
        
        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print a summary of created documents"""
        print("\n" + "="*60)
        print("ESG DEMO DOCUMENTS CREATED SUCCESSFULLY")
        print("="*60)
        
        print("\n📁 Directory Structure:")
        print(f"   {self.demo_dir}/")
        print("   ├── bank_reports/     (3 sample bank ESG reports)")
        print("   ├── regulatory/       (2 regulatory guidelines)")
        print("   ├── best_practices/   (2 best practice frameworks)")
        print("   └── metadata/         (document metadata)")
        
        print("\n🏦 Bank Reports (Ready for Upload):")
        print("   1. ING_ESG_Sample_2023.txt - CSRD compliance focus")
        print("   2. Rabobank_Sustainability_Sample_2023.txt - Climate risk focus")
        print("   3. ABN_AMRO_ESG_Sample_2023.txt - EU Taxonomy focus")
        
        print("\n📋 Regulatory Documents:")
        print("   1. DNB_Climate_Risk_Guidelines.txt - Dutch regulatory requirements")
        print("   2. EBA_ESG_Guidelines.txt - EU banking authority guidelines")
        
        print("\n📚 Best Practice Frameworks:")
        print("   1. TCFD_Recommendations.txt - Climate disclosure framework")
        print("   2. GRI_Standards_Overview.txt - Sustainability reporting standards")
        
        print("\n🎯 Demo Instructions:")
        print("   1. Upload bank reports using the web interface")
        print("   2. Choose 'RAG-Enhanced Analysis' for best results")
        print("   3. Compare standard vs enhanced analysis")
        print("   4. Explore the RAG dashboard for additional features")
        
        print("\n✅ All documents are ready for demo use!")
        print("="*60)

if __name__ == "__main__":
    downloader = ESGDocumentDownloader()
    downloader.run() 