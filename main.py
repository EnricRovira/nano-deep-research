import asyncio
import validators
import json
from pathlib import Path
from app.manager import ResearchManager
from dotenv import load_dotenv, find_dotenv
from app.schemas.request import CompetitorAnalysisRequest
from agents import set_default_openai_key
import os
load_dotenv(find_dotenv('.env'))

set_default_openai_key(os.getenv("KEY_OPENAI"))

async def main():
    print("Welcome to the Company Analysis Tool!")
    
    while True:
        url = input("\nPlease enter the website URL to analyze: ").strip()
        description = input("\nPlease enter a short description of the company to analyze: ").strip()
        
        if validators.url(url):
            break
        print("Invalid URL format. Please enter a valid URL (e.g., https://www.example.com)")

    print(f"\nAnalyzing {url}...")
    
    manager = ResearchManager()
    request = CompetitorAnalysisRequest(website=url, description=description)
    
    try:
        report = await manager.run(request)
        
        # Create output directory if it doesn't exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Generate filename based on domain
        domain = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(".", "_")
        output_file = output_dir / f"company_analysis_{domain}.json"
        
        # Save report to JSON file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report.dict(), f, indent=2, ensure_ascii=False)
            
        print(f"\nAnalysis complete! Report saved to: {output_file}")
        
    except Exception as e:
        print(f"\nAn error occurred during analysis: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
