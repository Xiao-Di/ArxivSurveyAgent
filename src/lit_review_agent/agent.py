"""Main Literature Review Agent class integrating all modules."""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import re
import platform

from .ai_core.llm_manager import LLMManager
from .processing.text_processor import TextProcessor
from .processing.vector_store import VectorStore
from .retrieval.arxiv_client import ArxivClient
from .retrieval.base_retriever import LiteratureItem
from .retrieval.pdf_processor import PDFProcessor
# Semantic Scholar removed - using ArXiv only
from .utils.config import Config
from .utils.logger import LoggerMixin, get_logger, setup_logger
from .utils.display import display, print_status, print_error, print_success
from .ai_core.summarizer import Summarizer

logger = get_logger(__name__)


def get_emoji_safe(emoji: str, fallback: str = "*") -> str:
    """Get emoji or fallback character for Windows compatibility."""
    return emoji if platform.system() != 'Windows' else fallback


class LiteratureAgent(LoggerMixin):
    """Main agent for automated literature review and summarization."""

    def __init__(self, config: Config | None = None):
        """
        Initialize the Literature Agent.

        Args:
            config: Configuration object (uses default if None)
        """
        super().__init__()
        self.config = config if config else Config()

        # Initialize components
        self.llm_manager = LLMManager(config=self.config)

        self.text_processor = TextProcessor(
            spacy_model=self.config.spacy_model_name,
            sentence_model=self.config.sentence_transformer_model,
        )

        self.vector_store = VectorStore(
            persist_directory=self.config.chroma_persist_directory,
            collection_name=self.config.chroma_collection_name,
            embedding_model=self.config.sentence_transformer_model,
        )

        self.arxiv_client = ArxivClient(
            api_url=self.config.arxiv_api_url, max_results=self.config.arxiv_max_results
        )

        self.pdf_processor = PDFProcessor()

        # Semantic Scholar removed - using ArXiv only
        # self.semantic_scholar_client = SemanticScholarClient(config=self.config)

        self.summarizer = Summarizer(
            llm_manager=self.llm_manager, config=self.config)

        self.logger.info("Initialized Literature Agent")

    def _generate_basic_action_plan(self, params: dict) -> List[str]:
        """
        Generate a basic action plan based on extracted parameters.

        Args:
            params: Dictionary containing extracted parameters and search settings

        Returns:
            List of action plan steps as strings
        """
        plan = []

        # Step 1: Parameter analysis
        topic = params.get("topic", "未指定主题")
        time_limit = params.get("time_limit")
        focus = params.get("focus")
        year_start = params.get("year_start")
        year_end = params.get("year_end")
        max_papers = params.get("max_papers", 20)
        sources = params.get("sources", [])
        retrieve_full_text = params.get("retrieve_full_text", False)

        # Generate plan steps
        plan.append(f"{get_emoji_safe('🎯', '1.')} 确定研究主题：{topic}")

        # Time constraint step
        if time_limit or year_start or year_end:
            time_desc = ""
            if year_start and year_end:
                time_desc = f"{year_start}-{year_end}年"
            elif year_start:
                time_desc = f"{year_start}年至今"
            elif time_limit:
                time_desc = time_limit
            plan.append(f"{get_emoji_safe('📅', '2.')} 设定时间范围：{time_desc}")

        # Focus area step
        if focus:
            plan.append(f"{get_emoji_safe('🔍', '3.')} 重点关注领域：{focus}")

        # Data sources step
        sources_str = "、".join(sources) if sources else "默认数据源"
        plan.append(f"{get_emoji_safe('📚', '4.')} 选择数据源：{sources_str}")

        # Search strategy step
        search_strategy = f"检索最多{max_papers}篇相关论文"
        if retrieve_full_text:
            search_strategy += "，并获取全文内容"
        plan.append(f"{get_emoji_safe('🔎', '5.')} 执行检索策略：{search_strategy}")

        # Processing steps
        plan.append(f"{get_emoji_safe('📊', '6.')} 分析论文元数据：标题、作者、摘要、引用数等")
        plan.append(f"{get_emoji_safe('📈', '7.')} 识别研究趋势：发表时间分布、热点关键词")

        if retrieve_full_text:
            plan.append(f"{get_emoji_safe('📄', '8.')} 处理全文内容：提取关键信息和核心观点")

        plan.append(f"{get_emoji_safe('🤖', '9.')} AI智能分析：生成综合性研究洞察")
        plan.append(f"{get_emoji_safe('📝', '10.')} 生成最终报告：整理发现和建议")

        return plan

    async def conduct_literature_review(
        self,
        research_topic: str = None,
        raw_query: str = None,
        max_papers: int = 20,
        sources: Optional[List[str]] = None,
        retrieve_full_text: bool = False,
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
    ) -> dict:
        """
        Conducts a comprehensive literature review for a given research topic.

        Args:
            research_topic: The topic to search for (legacy parameter).
            raw_query: Natural language query from user (new parameter).
            max_papers: Maximum number of papers to retrieve and process overall.
            sources: A list of sources to use (e.g., ['arxiv', 'semantic_scholar']).
                     Defaults to sources defined in config if None.
            retrieve_full_text: Whether to attempt to download and process full PDF texts.
            year_start: Optional start year for filtering publications.
            year_end: Optional end year for filtering publications.

        Returns:
            A dictionary containing the review results, including retrieved papers,
            analysis, and potentially identified trends.
        """
        # Handle natural language query processing
        if raw_query and not research_topic:
            # Extract parameters from natural language query
            self.logger.info(f"Received raw query: '{raw_query}'")
            display.print_header(f"Processing query: {raw_query}")

            # Extract core research parameters using LLM
            parsed_params = await self.llm_manager.extract_core_research_params(
                raw_query
            )
            self.logger.info(f"Parsed parameters: {parsed_params}")
            print_status(f"Interpreted parameters: {parsed_params}")

            research_topic = parsed_params.get("topic")
            if not research_topic:
                print_error(
                    "Could not determine the main research topic from the query."
                )
                return {"error": "Missing research topic"}

            # Handle time constraints if specified
            time_limit = parsed_params.get("time_limit")
            if time_limit and not year_start and not year_end:
                # Simple time parsing - can be enhanced later
                current_year = datetime.now().year

                if "last year" in time_limit.lower():
                    year_start = current_year - 1
                    year_end = current_year
                elif "recent" in time_limit.lower():
                    year_start = current_year - 3
                    year_end = current_year
                elif "since" in time_limit.lower():
                    # Try to extract year from "since YYYY"
                    year_match = re.search(
                        r"since\s+(\d{4})", time_limit.lower())
                    if year_match:
                        year_start = int(year_match.group(1))
                        year_end = current_year
                else:
                    # Handle "YYYY to YYYY" format and other patterns
                    if re.search(r"\d{4}\s+to\s+\d{4}", time_limit.lower()):
                        years = re.findall(r"\d{4}", time_limit)
                        if len(years) >= 2:
                            year_start = int(years[0])
                            year_end = int(years[1])

            # Handle focus keywords - could be used to enhance search query
            focus = parsed_params.get("focus")
            if focus:
                # Enhance the research topic with focus keywords
                research_topic = f"{research_topic} {focus}"
                print_status(
                    f"Enhanced search query with focus: {research_topic}")

        elif research_topic and not raw_query:
            # Legacy mode - use research_topic directly
            pass
        else:
            print_error("Either research_topic or raw_query must be provided.")
            return {"error": "Missing query parameters"}

        # Display enhanced header
        display.print_header(
            f"Literature Review: {research_topic}",
            f"Max Papers: {max_papers} | Full Text: {'Yes' if retrieve_full_text else 'No'}",
        )

        self.logger.info(
            f"Starting literature review for topic: '{research_topic}'")
        self.logger.debug(
            f"Parameters: max_papers={max_papers}, sources={sources}, retrieve_full_text={retrieve_full_text}, "
            f"year_start={year_start}, year_end={year_end}"
        )

        # Generate action plan based on extracted parameters
        # Initialize variables to avoid scope issues
        time_limit = locals().get("time_limit")
        focus = locals().get("focus")

        action_plan = self._generate_basic_action_plan(
            {
                "topic": research_topic,
                "time_limit": time_limit,
                "focus": focus,
                "year_start": year_start,
                "year_end": year_end,
                "max_papers": max_papers,
                "sources": sources or ["arxiv", "semantic_scholar"],
                "retrieve_full_text": retrieve_full_text,
            }
        )

        # Display action plan
        print_status(f"{get_emoji_safe('📋', 'Plan:')} 生成的行动计划:")
        for i, step in enumerate(action_plan, 1):
            print(f"  {i}. {step}")

        self.logger.info(
            f"Generated action plan with {len(action_plan)} steps")

        if sources is None:
            sources = self.config.default_retrieval_sources
            print_status(f"Using default sources: {sources}")
            self.logger.info(
                f"No sources specified, using default sources from config: {sources}"
            )

        # Ensure sources is a list, even if it's from config as a string
        if isinstance(sources, str):
            sources = [s.strip().lower()
                       for s in sources.split(",") if s.strip()]

        retrieved_items: List[LiteratureItem] = []
        processed_papers = []

        active_sources_count = 0
        if "arxiv" in sources and self.arxiv_client:
            active_sources_count += 1
        # Semantic Scholar removed - using ArXiv only
        # Add other sources here when they are implemented

        papers_per_source = (
            max_papers // active_sources_count
            if active_sources_count > 0
            else max_papers
        )
        if papers_per_source == 0 and max_papers > 0:
            papers_per_source = 1

        print_status(
            f"Active sources: {active_sources_count}, Papers per source: {papers_per_source}"
        )
        self.logger.debug(
            f"Active sources: {active_sources_count}, Papers per source: {papers_per_source}"
        )

        # Create progress bar for retrieval
        total_steps = len([s for s in sources if s in [
                          "arxiv", "semantic_scholar"]])
        if retrieve_full_text:
            total_steps += 1  # Add step for full text processing
        total_steps += 1  # Add step for AI processing

        progress = display.create_progress_bar(
            "Retrieving literature...", total=total_steps
        )
        progress.start()

        try:
            if "arxiv" in sources and self.arxiv_client:
                try:
                    display.update_progress(
                        description=f"{get_emoji_safe('🔍', '>')} Searching arXiv...")
                    print_status(
                        f"Retrieving up to {papers_per_source} papers from arXiv..."
                    )
                    self.logger.info(
                        f"Retrieving up to {papers_per_source} papers from arXiv for topic: '{research_topic}'"
                    )

                    arxiv_papers_items = await self.arxiv_client.search(
                        query=research_topic, max_results=papers_per_source
                    )
                    retrieved_items.extend(arxiv_papers_items)
                    print_success(
                        f"Retrieved {len(arxiv_papers_items)} items from arXiv"
                    )
                    self.logger.info(
                        f"Retrieved {len(arxiv_papers_items)} items from arXiv."
                    )
                    display.update_progress(advance=1)
                except Exception as e:
                    print_error(f"Error retrieving from arXiv: {e}")
                    self.logger.error(
                        f"Error retrieving from arXiv: {e}", exc_info=True
                    )

            # Semantic Scholar removed - using ArXiv only

            display.update_progress(
                description=f"{get_emoji_safe('🔄', '>')} Processing and deduplicating results..."
            )
            print_status(
                f"Total items retrieved from all sources: {len(retrieved_items)}"
            )
            self.logger.info(
                f"Total items retrieved from all sources before deduplication: {len(retrieved_items)}"
            )

            # Deduplication Stage 1: Based on unique identifiers (DOI, ArXiv ID)
            temp_deduped_items_by_id: List[LiteratureItem] = []
            seen_ids_for_dedup = set()
            for item in retrieved_items:
                unique_id = None
                if item.doi:
                    unique_id = item.doi.lower()
                # Ensure arxiv_id from S2 is comparable to arxiv_client's (e.g. no "arxiv:" prefix for s2's internal)
                elif item.arxiv_id:
                    # ArxivClient stores arxiv_id without prefix. S2 Client also stores it without prefix after parsing.
                    unique_id = item.arxiv_id.lower()
                # If item.id is already prefixed (e.g. "arxiv:xxxx" or "s2:yyyy"), consider using it as part of dedup key
                # For now, DOI and ArXiv ID are primary for cross-source deduplication.

                if unique_id and unique_id in seen_ids_for_dedup:
                    self.logger.debug(
                        f"Deduplicating item by ID ({unique_id}): '{item.title}'"
                    )
                    continue
                if unique_id:
                    seen_ids_for_dedup.add(unique_id)
                temp_deduped_items_by_id.append(item)
            retrieved_items = temp_deduped_items_by_id
            print_status(
                f"{len(retrieved_items)} items after ID-based deduplication")
            self.logger.info(
                f"{len(retrieved_items)} items after ID-based deduplication (DOI/ArXiv ID)."
            )

            # Deduplication Stage 2: Softer deduplication (e.g., normalized title and first author name)
            final_deduped_items: List[LiteratureItem] = []
            seen_title_author_hash = set()
            for item in retrieved_items:
                norm_title = "".join(
                    e for e in item.title.lower() if e.isalnum() or e.isspace()
                ).strip()
                first_author_norm = (
                    item.authors[0].lower().strip()
                    if item.authors
                    else "unknown_author"
                )
                # Create a hash or tuple for the pair
                title_author_key = hash((norm_title, first_author_norm))

                if title_author_key in seen_title_author_hash:
                    self.logger.debug(
                        f"Deduplicating item by title/author ('{norm_title}' / '{first_author_norm}'): '{item.title}'"
                    )
                    continue
                seen_title_author_hash.add(title_author_key)
                final_deduped_items.append(item)
            retrieved_items = final_deduped_items
            print_success(
                f"{len(retrieved_items)} unique items after complete deduplication"
            )
            self.logger.info(
                f"{len(retrieved_items)} items after title/author soft deduplication."
            )

            if len(retrieved_items) > max_papers:
                print_status(
                    f"Limiting {len(retrieved_items)} deduplicated items to {max_papers}"
                )
                self.logger.info(
                    f"Limiting {len(retrieved_items)} deduplicated items to {max_papers}."
                )
                # TODO: Implement sorting by relevance or date before truncating if needed.
                # For now, just take the first N. A more sophisticated approach might involve scoring.
                retrieved_items = retrieved_items[:max_papers]

            if retrieve_full_text:
                display.update_progress(
                    description=f"{get_emoji_safe('📄', '>')} Retrieving full text content..."
                )
                print_status(
                    f"Attempting to retrieve full text for {len(retrieved_items)} items..."
                )
                self.logger.info(
                    f"Attempting to retrieve full text for {len(retrieved_items)} items..."
                )

                success_count = 0
                for i, item in enumerate(retrieved_items):
                    display.update_progress(
                        description=f"{get_emoji_safe('📄', '>')} Processing PDF {i+1}/{len(retrieved_items)}: {item.title[:25]}..."
                    )

                    if item.pdf_url:
                        self.logger.debug(
                            f"Processing PDF for: '{item.title}' from {item.pdf_url}"
                        )
                        try:
                            full_text_content = (
                                await self.pdf_processor.extract_text_from_url(
                                    item.pdf_url
                                )
                            )
                            if full_text_content:
                                retrieved_items[i].full_text = full_text_content
                                success_count += 1
                                self.logger.info(
                                    f"Extracted full text for: '{item.title}' ({len(full_text_content)} chars)"
                                )
                            else:
                                self.logger.warning(
                                    f"Could not extract full text for: '{item.title}' (empty content from PDF processor). URL: {item.pdf_url}"
                                )
                        except Exception as pdf_e:
                            self.logger.error(
                                f"Error processing PDF for '{item.title}' from {item.pdf_url}: {pdf_e}",
                                exc_info=False,
                            )
                    # If full_text wasn't already populated by the retriever (e.g. arXiv summary sometimes is in full_text)
                    elif not item.full_text:
                        self.logger.debug(
                            f"No PDF URL for item: '{item.title}', skipping full text retrieval."
                        )

                print_success(
                    f"Successfully extracted full text for {success_count}/{len(retrieved_items)} papers"
                )
                display.update_progress(advance=1)

            # AI Processing stage
            display.update_progress(
                description=f"{get_emoji_safe('🤖', '>')} Processing with AI...")
            print_status(
                f"Starting AI processing for {len(retrieved_items)} papers...")

            for i, item in enumerate(retrieved_items):
                display.update_progress(
                    description=f"{get_emoji_safe('🤖', '>')} AI processing {i+1}/{len(retrieved_items)}: {item.title[:25]}..."
                )
                self.logger.debug(
                    f"Final processing stage for item: '{item.title}' (ID: {item.id})"
                )
                text_for_ai = item.full_text if item.full_text else item.abstract
                if not text_for_ai:
                    self.logger.warning(
                        f"No text (full or abstract) available for AI processing of '{item.title}'."
                    )
                    ai_summary = "No text content available for summarization."
                    keywords = []
                else:
                    self.logger.debug(
                        f"Using text (len: {len(text_for_ai)}) for AI processing of '{item.title}'. Full text used: {bool(item.full_text)}."
                    )
                    try:
                        keywords = self.text_processor.extract_research_keywords(
                            text_for_ai, max_keywords=10
                        )
                    except Exception as kw_e:
                        self.logger.error(
                            f"Error extracting keywords for {item.title}: {kw_e}",
                            exc_info=True,
                        )
                        keywords = []
                    try:
                        summary_type_for_llm = (
                            "key_findings" if item.full_text else "abstract_enhancement"
                        )
                        self.logger.debug(
                            f"Requesting '{summary_type_for_llm}' summary for '{item.title}'"
                        )
                        ai_summary = await self.summarizer.summarize_text(
                            text=text_for_ai,
                            summary_type=summary_type_for_llm,
                        )
                    except Exception as summ_e:
                        self.logger.error(
                            f"Error using Summarizer for {item.title}: {summ_e}",
                            exc_info=True,
                        )
                        ai_summary = "AI summary generation failed."

                processed_papers.append(
                    {
                        "title": item.title,
                        "authors": item.authors if item.authors else [],
                        "published_date": (
                            item.publication_date.isoformat()
                            if item.publication_date
                            else ""
                        ),
                        "url": item.url,
                        "pdf_url": item.pdf_url,
                        "original_summary": item.abstract,
                        "ai_enhanced_summary": ai_summary,
                        "full_text_retrieved": bool(item.full_text),
                        "full_text_snippet": (
                            item.full_text[:200] +
                            "..." if item.full_text else None
                        ),
                        "keywords": keywords,
                        "source": item.source,
                        "item_id_internal": item.id,
                    }
                )

            display.update_progress(advance=1)

        except Exception as e:
            print_error(f"Error during literature review: {e}")
            self.logger.error(
                f"Error during literature review: {e}", exc_info=True)
        finally:
            display.finish_progress()

        # Display final results
        results = {
            "research_topic": research_topic,
            "action_plan": action_plan,
            "retrieved_items": [item.model_dump() for item in retrieved_items],
            "processed_papers": processed_papers,
            "num_papers_processed": len(processed_papers),
        }

        # Show summary panel
        try:
            summary_panel = display.create_summary_panel(results)
            display.console.print(summary_panel)
        except UnicodeEncodeError:
            print(
                f"[SUMMARY] Literature review completed for: {research_topic}")
            print(f"Papers processed: {len(processed_papers)}")

        # Show papers table
        if processed_papers:
            try:
                papers_table = display.create_papers_table(processed_papers)
                display.console.print(papers_table)
            except UnicodeEncodeError:
                print("[PAPERS] Paper list display skipped due to encoding issues")

        print_success(
            f"Literature review completed! Processed {len(processed_papers)} papers"
        )
        self.logger.info(
            f"Literature review completed. Processed {len(processed_papers)} papers."
        )

        return results

    async def search_similar_papers(
        self, query: str, n_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for papers similar to a query using vector similarity.

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            List of similar papers
        """
        try:
            self.logger.info(f"Searching for similar papers: {query}")

            results = self.vector_store.search_similar(
                query=query, n_results=n_results)

            self.logger.info(f"Found {len(results)} similar papers")
            return results

        except Exception as e:
            self.logger.error(f"Error searching similar papers: {e}")
            return []

    async def generate_custom_summary(
        self, paper_ids: List[str], summary_type: str = "executive"
    ) -> Optional[str]:
        """
        Generate a custom summary for specific papers.

        Args:
            paper_ids: List of paper IDs
            summary_type: Type of summary to generate

        Returns:
            Generated summary or None if failed
        """
        try:
            self.logger.info(
                f"Generating custom summary for {len(paper_ids)} papers")

            # Retrieve papers from vector store
            paper_texts = []
            for paper_id in paper_ids:
                paper_data = self.vector_store.get_item_by_id(paper_id)
                if paper_data and paper_data["document"]:
                    paper_texts.append(paper_data["document"])

            if not paper_texts:
                self.logger.warning(
                    "No paper texts found for summary generation")
                return None

            # Combine texts
            combined_text = "\n\n---\n\n".join(paper_texts)

            # Generate summary using the summarizer
            summary = await self.summarizer.summarize_text(
                text=combined_text, summary_type=summary_type, max_tokens=1000
            )

            self.logger.info("Custom summary generated successfully")
            return summary

        except Exception as e:
            self.logger.error(f"Error generating custom summary: {e}")
            return None

    async def export_results(
        self,
        results: Dict[str, Any],
        output_format: str = "markdown",
        output_file: Optional[str] = None,
    ) -> bool:
        """
        Export literature review results to file.

        Args:
            results: Literature review results
            output_format: Output format (markdown, json, txt)
            output_file: Output file path (auto-generated if None)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate output filename if not provided
            if not output_file:
                from datetime import timezone

                timestamp = datetime.now(
                    timezone.utc).strftime("%Y%m%d_%H%M%S")
                topic_safe = "".join(
                    c
                    for c in results.get("topic", "review")
                    if c.isalnum() or c in (" ", "-", "_")
                ).rstrip()
                topic_safe = topic_safe.replace(" ", "_")[:50]

                output_file = f"{self.config.output_dir}/literature_review_{topic_safe}_{timestamp}.{output_format}"

            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate content based on format
            if output_format == "markdown":
                content = self._generate_markdown_report(results)
            elif output_format == "json":
                import json

                content = json.dumps(results, indent=2, ensure_ascii=False)
            else:  # txt
                content = self._generate_text_report(results)

            # Write to file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

            self.logger.info(f"Results exported to: {output_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error exporting results: {e}")
            return False

    async def generate_full_report(
        self, papers: List, topic: str, output_format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        Generates a comprehensive literature review report using ReportGenerator.

        Args:
            papers: List of literature items.
            topic: The research topic.
            output_format: The desired output format (markdown, html, latex).

        Returns:
            A dictionary containing the report content and metadata.
        """
        self.logger.info(
            f"Generating full report for topic '{topic}' in {output_format} format."
        )

        try:
            # Import ReportGenerator and TrendAnalyzer here to avoid circular imports
            from .ai_core.report_generator import ReportGenerator
            from .ai_core.trend_analyzer import TrendAnalyzer

            # Initialize trend analyzer
            trend_analyzer = TrendAnalyzer(
                llm_manager=self.llm_manager, text_processor=self.text_processor
            )

            # Initialize report generator
            report_generator = ReportGenerator(
                llm_manager=self.llm_manager,
                summarizer=self.summarizer,
                trend_analyzer=trend_analyzer,
            )

            # Generate comprehensive report
            report_data = await report_generator.generate_comprehensive_report(
                papers=papers, topic=topic, output_format=output_format
            )
            self.logger.info(
                f"Successfully generated full report for topic '{topic}'.")
            return report_data
        except Exception as e:
            self.logger.error(f"Error generating full report: {e}")
            return {"error": str(e)}

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get agent statistics.

        Returns:
            Dictionary with agent statistics
        """
        try:
            vector_stats = self.vector_store.get_collection_stats()

            return {
                "vector_store": vector_stats,
                "llm_requests": getattr(self.llm_manager, "request_count", 0),
                "config": {
                    "model": self.config.openai_model,
                    "max_papers": self.config.arxiv_max_results,
                },
            }
        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {}

    def _generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generate a markdown report from results."""
        lines = []

        lines.append(
            f"# Literature Review: {results.get('topic', 'Unknown Topic')}")
        lines.append(f"\nGenerated on: {results.get('timestamp', 'Unknown')}")
        lines.append("\n---\n")

        # Summary
        if results.get("summary"):
            lines.append("## Executive Summary\n")
            lines.append(results["summary"])
            lines.append("\n")

        # Key Insights
        if results.get("key_insights"):
            lines.append("## Key Insights\n")
            for i, insight in enumerate(results["key_insights"], 1):
                lines.append(f"{i}. {insight}")
            lines.append("\n")

        # Research Gaps
        if results.get("research_gaps"):
            lines.append("## Research Gaps and Future Opportunities\n")
            for i, gap in enumerate(results["research_gaps"], 1):
                lines.append(f"{i}. {gap}")
            lines.append("\n")

        # Statistics
        if results.get("statistics"):
            stats = results["statistics"]
            lines.append("## Statistics\n")
            lines.append(f"- Total Papers: {stats.get('total_papers', 0)}")

            if stats.get("date_range"):
                dr = stats["date_range"]
                lines.append(
                    f"- Date Range: {dr.get('earliest', 'Unknown')} - {dr.get('latest', 'Unknown')}"
                )

            if stats.get("top_categories"):
                lines.append("\n### Top Categories")
                for category, count in stats["top_categories"][:5]:
                    lines.append(f"- {category}: {count} papers")

            lines.append("\n")

        # Papers
        if results.get("papers"):
            lines.append("## Papers Reviewed\n")
            for i, paper in enumerate(results["papers"], 1):
                lines.append(f"### {i}. {paper.get('title', 'Unknown Title')}")

                if paper.get("authors"):
                    authors = ", ".join(paper["authors"][:3])
                    if len(paper["authors"]) > 3:
                        authors += " et al."
                    lines.append(f"**Authors:** {authors}")

                if paper.get("publication_date"):
                    lines.append(f"**Date:** {paper['publication_date']}")

                if paper.get("summary"):
                    lines.append(f"**Summary:** {paper['summary']}")

                if paper.get("url"):
                    lines.append(f"**URL:** {paper['url']}")

                lines.append("\n")

        return "\n".join(lines)

    def _generate_text_report(self, results: Dict[str, Any]) -> str:
        """Generate a plain text report from results."""
        lines = []

        lines.append(
            f"LITERATURE REVIEW: {results.get('topic', 'Unknown Topic').upper()}"
        )
        lines.append("=" * 80)
        lines.append(f"Generated on: {results.get('timestamp', 'Unknown')}")
        lines.append("")

        # Summary
        if results.get("summary"):
            lines.append("EXECUTIVE SUMMARY")
            lines.append("-" * 40)
            lines.append(results["summary"])
            lines.append("")

        # Key Insights
        if results.get("key_insights"):
            lines.append("KEY INSIGHTS")
            lines.append("-" * 40)
            for i, insight in enumerate(results["key_insights"], 1):
                lines.append(f"{i}. {insight}")
            lines.append("")

        # Research Gaps
        if results.get("research_gaps"):
            lines.append("RESEARCH GAPS AND FUTURE OPPORTUNITIES")
            lines.append("-" * 40)
            for i, gap in enumerate(results["research_gaps"], 1):
                lines.append(f"{i}. {gap}")
            lines.append("")

        # Statistics
        if results.get("statistics"):
            stats = results["statistics"]
            lines.append("STATISTICS")
            lines.append("-" * 40)
            lines.append(f"Total Papers: {stats.get('total_papers', 0)}")

            if stats.get("date_range"):
                dr = stats["date_range"]
                lines.append(
                    f"Date Range: {dr.get('earliest', 'Unknown')} - {dr.get('latest', 'Unknown')}"
                )

            lines.append("")

        return "\n".join(lines)


if __name__ == "__main__":
    import asyncio

    async def main():
        # Setup enhanced display
        display.print_header(
            "Literature Review Agent - Testing Mode",
            "Enhanced CLI with Rich Display Support",
        )

        print_status("Initializing Literature Agent...")

        custom_config = Config(
            arxiv_api_url="http://export.arxiv.org/api/",
            spacy_model_name="en_core_web_sm",
            log_level="INFO",  # Changed to INFO for cleaner demo output
            # Ensure SEMANTIC_SCHOLAR_API_KEY is set in .env or here if needed for non-mock tests
            # semantic_scholar_api_key="YOUR_S2_KEY_HERE_IF_NEEDED"
        )
        setup_logger(log_level=custom_config.log_level.upper(), use_rich=True)
        agent = LiteratureAgent(config=custom_config)

        print_success("Agent initialized successfully!")

        topic = "transformers in natural language processing"
        print_status(f"Starting literature review for: '{topic}'")
        print_status(
            f"Using sources: {custom_config.default_retrieval_sources}")

        # The conduct_literature_review method now handles all the display automatically
        review_results = await agent.conduct_literature_review(
            topic,
            max_papers=6,
            retrieve_full_text=False,  # Set to True to test PDF processing too
            # Test with default sources (arxiv, s2)
            sources=custom_config.default_retrieval_sources,
            year_start=2022,
            year_end=2023,
        )

        # Display detailed paper information if requested
        if review_results.get("processed_papers"):
            display.print_rule("Detailed Paper Information")

            # Show only first 3 in detail
            for i, paper in enumerate(review_results["processed_papers"][:3], 1):
                display.print_paper_details(paper, i)

        # Show completion message
        display.print_rule("Review Complete")
        print_success("Literature review process completed successfully!")

    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            print_error(
                "Could not run asyncio.run(main()) directly, possibly due to existing event loop."
            )
        else:
            print_error(f"Runtime error: {e}")
            raise e
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        raise e
