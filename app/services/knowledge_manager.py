import asyncio
import aiohttp
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import feedparser
from bs4 import BeautifulSoup
import hashlib
import os

from .rag_service import RAGService
from ..utils.config import settings

class KnowledgeManager:
    def __init__(self):
        self.rag_service = RAGService()
        self._initialized = False
        self.update_interval = 3600  # 1 hour

    async def initialize(self):
        """Initialize the knowledge manager"""
        if not self._initialized:
            await self.rag_service.initialize_knowledge_base()
            self._initialized = True
        self.last_update = None
        self.update_sources = {
            "regulatory": [
                "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2464",
                "https://www.eba.europa.eu/regulation-and-policy/sustainable-finance",
                "https://www.dnb.nl/en/",
            ],
            "news": [
                "https://www.reuters.com/topic/sustainable-finance",
                "https://www.bloomberg.com/topics/sustainable-finance",
                "https://www.ft.com/sustainable-finance",
            ],
            "research": [
                "https://www.unpri.org/",
                "https://www.sasb.org/",
                "https://www.cdp.net/",
            ]
        }

    async def start_auto_updates(self):
        """Start automatic knowledge base updates"""
        while True:
            try:
                await self.update_knowledge_base()
                await asyncio.sleep(self.update_interval)
            except Exception as e:
                print(f"Error in auto-update: {str(e)}")
                await asyncio.sleep(300)  # Wait 5 minutes before retrying

    async def update_knowledge_base(self):
        """Update knowledge base with latest information"""
        try:
            print("🔄 Starting knowledge base update...")
            
            # Get latest regulatory updates
            regulatory_updates = await self._fetch_regulatory_updates()
            
            # Get latest news and insights
            news_updates = await self._fetch_news_updates()
            
            # Get latest research and best practices
            research_updates = await self._fetch_research_updates()
            
            # Combine all updates
            all_updates = regulatory_updates + news_updates + research_updates
            
            # Add updates to knowledge base
            for update in all_updates:
                await self.rag_service.update_knowledge_base(
                    new_content=update["content"],
                    metadata=update["metadata"]
                )
            
            self.last_update = datetime.now()
            print(f"✅ Knowledge base updated with {len(all_updates)} new items")
            
        except Exception as e:
            print(f"❌ Error updating knowledge base: {str(e)}")

    async def _fetch_regulatory_updates(self) -> List[Dict[str, Any]]:
        """Fetch latest regulatory updates"""
        updates = []
        
        try:
            # CSRD updates
            csrd_content = await self._fetch_web_content(
                "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2464"
            )
            if csrd_content:
                updates.append({
                    "content": csrd_content,
                    "metadata": {
                        "type": "regulation",
                        "source": "EU",
                        "category": "CSRD",
                        "title": "CSRD Implementation Updates",
                        "timestamp": datetime.now().isoformat(),
                        "priority": "High"
                    }
                })
            
            # EBA guidelines
            eba_content = await self._fetch_web_content(
                "https://www.eba.europa.eu/regulation-and-policy/sustainable-finance"
            )
            if eba_content:
                updates.append({
                    "content": eba_content,
                    "metadata": {
                        "type": "guideline",
                        "source": "EBA",
                        "category": "Sustainable_Finance",
                        "title": "EBA Sustainable Finance Guidelines",
                        "timestamp": datetime.now().isoformat(),
                        "priority": "High"
                    }
                })
            
            # DNB updates
            dnb_content = await self._fetch_web_content(
                "https://www.dnb.nl/en/"
            )
            if dnb_content:
                updates.append({
                    "content": dnb_content,
                    "metadata": {
                        "type": "guideline",
                        "source": "DNB",
                        "category": "Climate_Risk",
                        "title": "DNB Climate Risk Guidelines",
                        "timestamp": datetime.now().isoformat(),
                        "priority": "High",
                        "region": "Netherlands"
                    }
                })
            
        except Exception as e:
            print(f"Error fetching regulatory updates: {str(e)}")
        
        return updates

    async def _fetch_news_updates(self) -> List[Dict[str, Any]]:
        """Fetch latest ESG news and insights"""
        updates = []
        
        try:
            # Reuters sustainable finance news
            reuters_content = await self._fetch_web_content(
                "https://www.reuters.com/topic/sustainable-finance"
            )
            if reuters_content:
                updates.append({
                    "content": reuters_content,
                    "metadata": {
                        "type": "news",
                        "source": "Reuters",
                        "category": "Sustainable_Finance",
                        "title": "Latest Sustainable Finance News",
                        "timestamp": datetime.now().isoformat(),
                        "priority": "Medium"
                    }
                })
            
            # Bloomberg ESG insights
            bloomberg_content = await self._fetch_web_content(
                "https://www.bloomberg.com/topics/sustainable-finance"
            )
            if bloomberg_content:
                updates.append({
                    "content": bloomberg_content,
                    "metadata": {
                        "type": "news",
                        "source": "Bloomberg",
                        "category": "ESG_Insights",
                        "title": "Bloomberg ESG Insights",
                        "timestamp": datetime.now().isoformat(),
                        "priority": "Medium"
                    }
                })
            
        except Exception as e:
            print(f"Error fetching news updates: {str(e)}")
        
        return updates

    async def _fetch_research_updates(self) -> List[Dict[str, Any]]:
        """Fetch latest research and best practices"""
        updates = []
        
        try:
            # UN PRI updates
            unpri_content = await self._fetch_web_content(
                "https://www.unpri.org/"
            )
            if unpri_content:
                updates.append({
                    "content": unpri_content,
                    "metadata": {
                        "type": "best_practice",
                        "source": "UNPRI",
                        "category": "Responsible_Investment",
                        "title": "UN PRI Best Practices",
                        "timestamp": datetime.now().isoformat(),
                        "priority": "High"
                    }
                })
            
            # SASB standards
            sasb_content = await self._fetch_web_content(
                "https://www.sasb.org/"
            )
            if sasb_content:
                updates.append({
                    "content": sasb_content,
                    "metadata": {
                        "type": "best_practice",
                        "source": "SASB",
                        "category": "Sustainability_Accounting",
                        "title": "SASB Standards",
                        "timestamp": datetime.now().isoformat(),
                        "priority": "High"
                    }
                })
            
        except Exception as e:
            print(f"Error fetching research updates: {str(e)}")
        
        return updates

    async def _fetch_web_content(self, url: str) -> Optional[str]:
        """Fetch content from web URL"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Parse HTML and extract relevant text
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # Remove script and style elements
                        for script in soup(["script", "style"]):
                            script.decompose()
                        
                        # Extract text
                        text = soup.get_text()
                        
                        # Clean up text
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        text = ' '.join(chunk for chunk in chunks if chunk)
                        
                        return text[:5000]  # Limit content length
                    
        except Exception as e:
            print(f"Error fetching content from {url}: {str(e)}")
        
        return None

    async def add_custom_knowledge(
        self, 
        content: str, 
        title: str, 
        source: str, 
        category: str,
        priority: str = "Medium"
    ):
        """Add custom knowledge to the knowledge base"""
        try:
            metadata = {
                "type": "custom",
                "source": source,
                "category": category,
                "title": title,
                "timestamp": datetime.now().isoformat(),
                "priority": priority
            }
            
            await self.rag_service.update_knowledge_base(content, metadata)
            print(f"✅ Added custom knowledge: {title}")
            
        except Exception as e:
            print(f"❌ Error adding custom knowledge: {str(e)}")

    async def get_update_status(self) -> Dict[str, Any]:
        """Get knowledge base update status"""
        return {
            "last_update": self.last_update.isoformat() if self.last_update else None,
            "update_interval": self.update_interval,
            "next_update": (self.last_update + timedelta(seconds=self.update_interval)).isoformat() if self.last_update else None,
            "auto_update_enabled": True,
            "update_sources": list(self.update_sources.keys())
        }

    async def force_update(self):
        """Force immediate knowledge base update"""
        await self.update_knowledge_base()

    async def get_knowledge_summary(self) -> Dict[str, Any]:
        """Get summary of knowledge base content"""
        try:
            stats = await self.rag_service.get_knowledge_statistics()
            
            # Get recent updates
            recent_updates = await self._get_recent_updates()
            
            return {
                "statistics": stats,
                "recent_updates": recent_updates,
                "update_status": await self.get_update_status()
            }
            
        except Exception as e:
            print(f"Error getting knowledge summary: {str(e)}")
            return {}

    async def _get_recent_updates(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent knowledge base updates"""
        try:
            # This would typically query the vector store for recent documents
            # For now, return a mock list
            return [
                {
                    "title": "CSRD Implementation Guidelines",
                    "source": "EU",
                    "category": "CSRD",
                    "timestamp": datetime.now().isoformat(),
                    "priority": "High"
                },
                {
                    "title": "Latest Climate Risk Requirements",
                    "source": "DNB",
                    "category": "Climate_Risk",
                    "timestamp": datetime.now().isoformat(),
                    "priority": "High"
                }
            ]
            
        except Exception as e:
            print(f"Error getting recent updates: {str(e)}")
            return []

    async def search_knowledge_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Search knowledge base by date range"""
        try:
            # This would typically query the vector store with date filters
            # For now, return mock data
            return [
                {
                    "title": "Knowledge item in date range",
                    "content": "Content summary",
                    "metadata": {
                        "timestamp": start_date.isoformat(),
                        "source": "EU",
                        "category": "Regulation"
                    }
                }
            ]
            
        except Exception as e:
            print(f"Error searching by date range: {str(e)}")
            return []

    async def export_knowledge_base(self, format: str = "json") -> str:
        """Export knowledge base in specified format"""
        try:
            if format == "json":
                stats = await self.rag_service.get_knowledge_statistics()
                return json.dumps(stats, indent=2)
            else:
                raise ValueError(f"Unsupported export format: {format}")
                
        except Exception as e:
            print(f"Error exporting knowledge base: {str(e)}")
            return ""

    async def cleanup_old_knowledge(self, days_old: int = 365):
        """Clean up old knowledge base entries"""
        try:
            await self.rag_service.cleanup_old_documents(days_old)
            print(f"🧹 Cleaned up knowledge base entries older than {days_old} days")
            
        except Exception as e:
            print(f"Error cleaning up knowledge base: {str(e)}") 