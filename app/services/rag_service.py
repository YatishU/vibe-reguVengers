import asyncio
import json
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import aiohttp
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, WebBaseLoader
from langchain.schema import Document
import chromadb
from chromadb.config import Settings
import os
from pathlib import Path

from ..utils.config import settings

class RAGService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            model="text-embedding-ada-002"
        )
        
        # Initialize vector store
        self.persist_directory = "app/data/vectorstore"
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="esg_knowledge_base"
        )
        
        # Text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # ESG knowledge sources
        self.knowledge_sources = {
            "regulations": [
                "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2464",  # CSRD
                "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32020L0852",  # EU Taxonomy
                "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019R2088",  # SFDR
            ],
            "guidelines": [
                "https://www.eba.europa.eu/regulation-and-policy/sustainable-finance",
                "https://www.tcfdhub.org/",
                "https://www.globalreporting.org/standards/",
            ],
            "best_practices": [
                "https://www.unpri.org/",
                "https://www.sasb.org/",
                "https://www.cdp.net/",
            ]
        }
        
        # Initialize knowledge base (will be done asynchronously when needed)
        pass

    async def initialize_knowledge_base(self):
        """Async initialization of knowledge base"""
        await asyncio.to_thread(self._initialize_knowledge_base)

    def _initialize_knowledge_base(self):
        """Initialize the ESG knowledge base with regulations and best practices"""
        try:
            # Check if knowledge base already exists
            try:
                if self.vectorstore._collection.count() > 0:
                    print("✅ ESG Knowledge base already initialized")
                    return
            except Exception:
                pass
            
            print("🔄 Initializing ESG Knowledge Base...")
            
            # Load ESG regulations and guidelines
            self._load_esg_regulations()
            self._load_esg_best_practices()
            self._load_dutch_banking_guidelines()
            
            print("✅ ESG Knowledge Base initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing knowledge base: {str(e)}")

    def _load_esg_regulations(self):
        """Load ESG regulations into vector store"""
        regulations = [
            {
                "title": "CSRD (Corporate Sustainability Reporting Directive)",
                "content": """
                The CSRD requires companies to report on sustainability matters including:
                - Environmental protection
                - Social responsibility and treatment of employees
                - Respect for human rights
                - Anti-corruption and anti-bribery matters
                
                Key requirements:
                - Double materiality assessment
                - Forward-looking information
                - Sustainability targets and progress
                - Due diligence processes
                - Principal adverse impacts
                """,
                "metadata": {"type": "regulation", "source": "EU", "category": "CSRD"}
            },
            {
                "title": "EU Taxonomy Regulation",
                "content": """
                The EU Taxonomy establishes a classification system for sustainable economic activities:
                
                Environmental objectives:
                - Climate change mitigation
                - Climate change adaptation
                - Sustainable use and protection of water and marine resources
                - Transition to a circular economy
                - Pollution prevention and control
                - Protection and restoration of biodiversity and ecosystems
                
                Technical screening criteria must be met for activities to be considered sustainable.
                """,
                "metadata": {"type": "regulation", "source": "EU", "category": "Taxonomy"}
            },
            {
                "title": "SFDR (Sustainable Finance Disclosure Regulation)",
                "content": """
                SFDR requires financial market participants to disclose:
                - Sustainability risks in investment decisions
                - Principal adverse impacts on sustainability factors
                - Remuneration policies linked to sustainability
                
                Disclosure requirements:
                - Pre-contractual disclosures
                - Periodic reports
                - Website disclosures
                - Product-level disclosures
                """,
                "metadata": {"type": "regulation", "source": "EU", "category": "SFDR"}
            }
        ]
        
        for reg in regulations:
            self._add_document(reg["content"], reg["metadata"])

    def _load_esg_best_practices(self):
        """Load ESG best practices into vector store"""
        best_practices = [
            {
                "title": "TCFD Climate Risk Framework",
                "content": """
                TCFD framework for climate-related financial disclosures:
                
                Governance:
                - Board oversight of climate risks
                - Management role in climate risk assessment
                
                Strategy:
                - Climate risks and opportunities
                - Impact on business strategy and financial planning
                - Scenario analysis
                
                Risk Management:
                - Integration into risk management processes
                - Climate risk identification and assessment
                
                Metrics and Targets:
                - Climate-related metrics
                - GHG emissions and targets
                - Climate-related targets
                """,
                "metadata": {"type": "best_practice", "source": "TCFD", "category": "Climate_Risk"}
            },
            {
                "title": "GRI Standards",
                "content": """
                Global Reporting Initiative standards for sustainability reporting:
                
                Universal Standards:
                - GRI 1: Foundation
                - GRI 2: General Disclosures
                - GRI 3: Material Topics
                
                Topic Standards:
                - Economic topics
                - Environmental topics
                - Social topics
                
                Key principles:
                - Stakeholder inclusiveness
                - Sustainability context
                - Materiality
                - Completeness
                """,
                "metadata": {"type": "best_practice", "source": "GRI", "category": "Reporting"}
            }
        ]
        
        for practice in best_practices:
            self._add_document(practice["content"], practice["metadata"])

    def _load_dutch_banking_guidelines(self):
        """Load Dutch banking-specific ESG guidelines"""
        dutch_guidelines = [
            {
                "title": "DNB Climate Risk Guidelines",
                "content": """
                Dutch National Bank climate risk guidelines for financial institutions:
                
                Climate risk categories:
                - Physical risks (acute and chronic)
                - Transition risks (policy, legal, technology, market, reputation)
                
                Risk management requirements:
                - Climate risk identification and assessment
                - Integration into risk management framework
                - Stress testing and scenario analysis
                - Monitoring and reporting
                
                Supervisory expectations:
                - Board and management oversight
                - Risk appetite and limits
                - Data quality and availability
                - Capacity building
                """,
                "metadata": {"type": "guideline", "source": "DNB", "category": "Climate_Risk", "region": "Netherlands"}
            },
            {
                "title": "Dutch Banking Association ESG Guidelines",
                "content": """
                ESG guidelines for Dutch banks (ING, Rabobank, ABN AMRO):
                
                Environmental focus:
                - Carbon footprint reduction
                - Green financing and investments
                - Climate risk management
                - Biodiversity protection
                
                Social responsibility:
                - Financial inclusion
                - Human rights due diligence
                - Labor standards
                - Community development
                
                Governance:
                - ESG integration in decision-making
                - Stakeholder engagement
                - Transparency and disclosure
                - Ethics and compliance
                """,
                "metadata": {"type": "guideline", "source": "NVB", "category": "ESG", "region": "Netherlands"}
            }
        ]
        
        for guideline in dutch_guidelines:
            self._add_document(guideline["content"], guideline["metadata"])

    def _add_document(self, content: str, metadata: Dict[str, Any]):
        """Add document to vector store"""
        try:
            # Split content into chunks
            chunks = self.text_splitter.split_text(content)
            
            # Create documents with metadata
            documents = [
                Document(
                    page_content=chunk,
                    metadata={
                        **metadata,
                        "chunk_id": i,
                        "timestamp": datetime.now().isoformat()
                    }
                )
                for i, chunk in enumerate(chunks)
            ]
            
            # Add to vector store
            self.vectorstore.add_documents(documents)
            
        except Exception as e:
            print(f"Error adding document: {str(e)}")

    async def retrieve_relevant_context(
        self, 
        query: str, 
        document_type: str = None,
        bank: str = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant context from knowledge base"""
        try:
            # Build search query with context
            search_query = query
            
            if document_type:
                search_query += f" {document_type} compliance requirements"
            
            if bank:
                search_query += f" {bank} bank specific guidelines"
            
            # Retrieve similar documents
            docs = self.vectorstore.similarity_search(
                search_query,
                k=top_k,
                filter={"type": {"$in": ["regulation", "best_practice", "guideline"]}}
            )
            
            # Format results
            context = []
            for doc in docs:
                context.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance_score": self._calculate_relevance_score(query, doc.page_content)
                })
            
            # Sort by relevance score
            context.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            return context
            
        except Exception as e:
            print(f"Error retrieving context: {str(e)}")
            return []

    def _calculate_relevance_score(self, query: str, content: str) -> float:
        """Calculate relevance score between query and content"""
        try:
            # Simple keyword-based relevance scoring
            query_words = set(query.lower().split())
            content_words = set(content.lower().split())
            
            if not query_words:
                return 0.0
            
            intersection = query_words.intersection(content_words)
            relevance = len(intersection) / len(query_words)
            
            return min(relevance, 1.0)
            
        except Exception:
            return 0.0

    async def update_knowledge_base(self, new_content: str, metadata: Dict[str, Any]):
        """Update knowledge base with new content"""
        try:
            self._add_document(new_content, metadata)
            print(f"✅ Updated knowledge base with new content: {metadata.get('title', 'Unknown')}")
            
        except Exception as e:
            print(f"❌ Error updating knowledge base: {str(e)}")

    async def get_latest_regulations(self) -> List[Dict[str, Any]]:
        """Get latest ESG regulations and updates"""
        try:
            # This would typically fetch from regulatory APIs
            # For now, return cached latest updates
            latest_updates = [
                {
                    "title": "Latest CSRD Implementation Guidelines",
                    "content": "Updated CSRD implementation guidelines for 2024...",
                    "date": "2024-01-15",
                    "source": "European Commission"
                },
                {
                    "title": "Enhanced EU Taxonomy Criteria",
                    "content": "New technical screening criteria for climate change mitigation...",
                    "date": "2024-01-10",
                    "source": "European Commission"
                }
            ]
            
            return latest_updates
            
        except Exception as e:
            print(f"Error fetching latest regulations: {str(e)}")
            return []

    async def search_esg_knowledge(
        self, 
        query: str, 
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Search ESG knowledge base with filters"""
        try:
            # Build filter for vector search
            search_filter = {}
            if filters:
                for key, value in filters.items():
                    if isinstance(value, list):
                        search_filter[key] = {"$in": value}
                    else:
                        search_filter[key] = value
            
            # Perform search
            docs = self.vectorstore.similarity_search(
                query,
                k=10,
                filter=search_filter if search_filter else None
            )
            
            # Format results
            results = []
            for doc in docs:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "source": doc.metadata.get("source", "Unknown"),
                    "category": doc.metadata.get("category", "General")
                })
            
            return results
            
        except Exception as e:
            print(f"Error searching ESG knowledge: {str(e)}")
            return []

    async def get_knowledge_statistics(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        try:
            collection = self.vectorstore._collection
            count = collection.count()
            
            # Get unique sources and categories
            results = collection.get()
            sources = set()
            categories = set()
            
            for metadata in results["metadatas"]:
                if metadata:
                    sources.add(metadata.get("source", "Unknown"))
                    categories.add(metadata.get("category", "General"))
            
            return {
                "total_documents": count,
                "unique_sources": len(sources),
                "categories": list(categories),
                "sources": list(sources),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting knowledge statistics: {str(e)}")
            return {}

    async def cleanup_old_documents(self, days_old: int = 365):
        """Clean up old documents from knowledge base"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            # This would require implementing document deletion
            # For now, just log the cleanup operation
            print(f"🧹 Cleanup operation scheduled for documents older than {days_old} days")
            
        except Exception as e:
            print(f"Error during cleanup: {str(e)}") 