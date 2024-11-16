import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st
from typing import List, Dict
import json
from dotenv import load_dotenv
import time
from groq import Groq

load_dotenv()

class AIWebSearchAgent:
    def __init__(self):
        # Initialize Groq client
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def search_web(self, query: str, num_results: int = 3) -> str:
        """
        Performs a web search using DuckDuckGo.
        """
        try:
            url = f'https://html.duckduckgo.com/html/?q={query}'
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for result in soup.select('.result__body')[:num_results]:
                title = result.select_one('.result__title')
                snippet = result.select_one('.result__snippet')
                if title and snippet:
                    results.append(f"Title: {title.get_text()}\nSnippet: {snippet.get_text()}\n")
            
            return '\n'.join(results)
        except Exception as e:
            return f"Search error: {str(e)}"

    def extract_info_with_llm(self, query: str, search_results: str) -> Dict:
        """
        Uses Groq's LLM to extract structured information from search results based on the query.
        """
        prompt = f"""
        ### Context
        Query: {query}
        Search Results: {search_results}

        ### Task
        Analyze the search results and extract relevant information that answers the query.
        Provide a response in JSON format with the following structure:
        {{
            "extracted_info": "main findings or relevant information",
            "key_points": ["list", "of", "important", "points"],
            "source_quality": "assessment of source reliability (high/medium/low)",
            "confidence": "confidence in findings (high/medium/low)",
            "additional_notes": "any caveats or important context"
        }}

        The JSON must be valid and properly formatted.
        """

        try:
            completion = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",  # Using Mixtral for better performance
                messages=[
                    {"role": "system", "content": "You are a precise data extraction assistant. Always provide responses in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=1000
            )
            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            return {
                "error": f"LLM processing error: {str(e)}",
                "extracted_info": None,
                "key_points": [],
                "source_quality": "error",
                "confidence": "none",
                "additional_notes": "Failed to process with LLM"
            }

    def process_data(self, data: pd.DataFrame, query_col: str, template: str) -> List[Dict]:
        """
        Process the data with web search and LLM analysis.
        """
        results = []
        total_rows = len(data)
        
        # Create columns for status display
        col1, col2 = st.columns([3, 1])
        progress_bar = col1.progress(0)
        status_text = col2.empty()
        
        for idx, row in data.iterrows():
            entity = row[query_col]
            search_query = template.format(entity=entity)
            
            # Update progress
            progress = (idx + 1) / total_rows
            progress_bar.progress(progress)
            status_text.text(f"Processing {idx + 1}/{total_rows}")
            
            try:
                # Perform search
                search_results = self.search_web(search_query)
                
                # Extract information using LLM
                extracted_info = self.extract_info_with_llm(search_query, search_results)
                
                # Store results
                results.append({
                    "entity": entity,
                    "search_query": search_query,
                    "analysis": extracted_info,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                
            except Exception as e:
                results.append({
                    "entity": entity,
                    "error": str(e),
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
            
            # Add delay to prevent rate limiting
            time.sleep(2)
        
        progress_bar.empty()
        status_text.empty()
        return results

def display_results(results: List[Dict]):
    """
    Display results in a structured format.
    """
    st.subheader("Analysis Results")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Summary View", "Detailed View"])
    
    with tab1:
        # Summary table
        summary_data = []
        for r in results:
            if "analysis" in r:
                summary_data.append({
                    "Entity": r["entity"],
                    "Main Findings": r["analysis"].get("extracted_info", "N/A"),
                    "Confidence": r["analysis"].get("confidence", "N/A"),
                    "Source Quality": r["analysis"].get("source_quality", "N/A")
                })
        
        if summary_data:
            st.dataframe(pd.DataFrame(summary_data))
    
    with tab2:
        # Detailed expandable view
        for r in results:
            with st.expander(f"Details for: {r['entity']}"):
                st.json(r)

def main():
    st.set_page_config(page_title="AI Web Search & Analysis", layout="wide")
    st.title("🔍 AI Web Research Assistant")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Settings")
        st.markdown("""
        This tool helps you:
        1. Process data from your CSV file
        2. Perform web searches for each entry
        3. Extract relevant information using AI
        """)
    
    # Initialize the agent
    agent = AIWebSearchAgent()
    
    # File upload
    uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=['csv'])
    
    if uploaded_file:
        # Read and display the data
        df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(df.head())
        
        # Configuration
        col1, col2 = st.columns(2)
        with col1:
            query_column = st.selectbox("Select column for queries:", df.columns)
        with col2:
            search_template = st.text_area(
                "Enter search template (use {entity} as placeholder):",
                value="Latest developments and news about {entity}",
                height=100
            )
        
        # Process button
        if st.button("Start Analysis", type="primary"):
            try:
                with st.spinner("Processing... This may take a few minutes."):
                    results = agent.process_data(df, query_column, search_template)
                    
                    # Display results
                    display_results(results)
                    
                    # Download option
                    results_df = pd.json_normalize(results)
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results (CSV)",
                        data=csv,
                        file_name="ai_research_results.csv",
                        mime="text/csv"
                    )
                    
                    # Save JSON option
                    st.download_button(
                        label="📥 Download Results (JSON)",
                        data=json.dumps(results, indent=2),
                        file_name="ai_research_results.json",
                        mime="application/json"
                    )
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()