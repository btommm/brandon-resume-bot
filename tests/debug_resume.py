#!/usr/bin/env python3
"""
Simple debug script to check resume loading
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from brandon_bot.document_processor import document_processor
from brandon_bot.bot import resume_bot
from brandon_bot.config import config

def main():
    print("🔍 DEBUGGING RESUME LOADING")
    print("=" * 50)
    
    # 1. Check if data directory exists
    print(f"1. Data directory: {config.DATA_DIR}")
    if os.path.exists(config.DATA_DIR):
        print("   ✅ Data directory exists")
        files = os.listdir(config.DATA_DIR)
        print(f"   Files found: {files}")
    else:
        print("   ❌ Data directory missing!")
        return
    
    # 2. Load documents
    print("\n2. Loading documents...")
    documents = document_processor.load_all_documents()
    print(f"   Loaded {len(documents)} documents")
    for name, content in documents.items():
        print(f"   📄 {name}: {len(content)} characters")
    
    # 3. Check processed content
    print("\n3. Processed content:")
    if document_processor.processed_content:
        content = document_processor.processed_content
        print(f"   Length: {len(content)} characters")
        print(f"   First 200 chars: {content[:200]}...")
        
        # Check for key terms
        content_lower = content.lower()
        print(f"\n   Key terms found:")
        print(f"   - 'education': {'✅' if 'education' in content_lower else '❌'}")
        print(f"   - 'university': {'✅' if 'university' in content_lower else '❌'}")
        print(f"   - 'college': {'✅' if 'college' in content_lower else '❌'}")
        print(f"   - 'school': {'✅' if 'school' in content_lower else '❌'}")
        print(f"   - 'degree': {'✅' if 'degree' in content_lower else '❌'}")
        
    else:
        print("   ❌ No processed content!")
    
    # 4. Check bot system instructions
    print("\n4. Bot system instructions:")
    try:
        instructions = resume_bot._build_system_instructions()
        print(f"   Instructions length: {len(instructions)} characters")
        if "Brandon's resume" in instructions:
            print("   ✅ Resume content included in instructions")
        else:
            print("   ❌ Resume content NOT included in instructions")
            
        # Show a snippet of the instructions
        print(f"   Instructions snippet: {instructions[:300]}...")
        
    except Exception as e:
        print(f"   ❌ Error building instructions: {e}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
