#!/usr/bin/env python3
"""
LangGraph Multi-Agent AI Travel Planning System
Advanced travel planning using LangGraph framework with Google Gemini and DuckDuckGo search
"""

import sys
import os
import asyncio
from datetime import datetime, timedelta
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.langgraph_agents import LangGraphTravelAgents
from modules.user_input import UserInputHandler
from config.langgraph_config import langgraph_config as config

def display_langgraph_header():
    """Display header for LangGraph system"""
    print("\n" + "="*80)
    print("🚀 LANGGRAPH MULTI-AGENT AI TRAVEL PLANNER")
    print("="*80)
    print("🤖 Powered by Google Gemini Flash-2.0 & DuckDuckGo Search")
    print("="*80)
    print("\n🎯 AI AGENT TEAM (LangGraph Framework):")
    print("   🎯 Coordinator Agent     - Workflow orchestration & decision synthesis")
    print("   ✈️  Travel Advisor       - Destination expertise with live search")
    print("   💰 Budget Optimizer      - Cost analysis with real-time pricing")
    print("   🌤️  Weather Analyst      - Weather intelligence with current data")
    print("   🏠 Local Expert          - Insider knowledge with live local info")
    print("   📅 Itinerary Planner     - Schedule optimization & logistics")
    print("\n🔧 ENHANCED CAPABILITIES:")
    print("   • Google Gemini Flash-2.0 for all AI interactions")
    print("   • DuckDuckGo search for real-time information")
    print("   • LangGraph state management and workflow")
    print("   • Advanced tool integration and execution")
    print("   • Asynchronous multi-agent collaboration")
    print("="*80)

def validate_environment():
    """Validate environment setup"""
    print("🔍 Validating Environment...")
    
    # Check Gemini API key
    if not config.GEMINI_API_KEY:
        print("❌ Error: GEMINI_API_KEY not found in environment")
        print("Please set your Google Gemini API key in .env file:")
        print("GEMINI_API_KEY=your_api_key_here")
        print("\nGet your API key from: https://makersuite.google.com/app/apikey")
        return False
    
    print(f"✅ Gemini API Key: {'*' * 10}{config.GEMINI_API_KEY[-4:]}")
    print(f"✅ Model: {config.GEMINI_MODEL}")
    print(f"✅ DuckDuckGo Search: Enabled")
    
    return True

def create_sample_request():
    """Create a sample travel request for demonstration"""
    return {
        "destination": "Tokyo",
        "duration": 5,
        "budget_range": "mid-range",
        "interests": ["culture", "food", "technology", "history"],
        "group_size": 2,
        "travel_dates": "2024-04-15 to 2024-04-20"
    }

def demonstrate_langgraph_system():
    """Demonstrate the LangGraph multi-agent system"""
    print("\n" + "🎭 LANGGRAPH SYSTEM DEMONSTRATION")
    print("-" * 60)
    
    print("📋 Sample Travel Request:")
    sample_request = create_sample_request()
    for key, value in sample_request.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    print(f"\n🚀 Initializing LangGraph Multi-Agent System...")
    
    try:
        # Initialize the system
        travel_agents = LangGraphTravelAgents()
        print("✅ LangGraph workflow compiled successfully")
        
        print(f"\n🤝 Starting Multi-Agent Collaboration...")
        print("   This may take 1-2 minutes for complete analysis...")
        
        # Run the planning
        result = travel_agents.run_travel_planning(sample_request)
        
        if result["success"]:
            print(f"\n✅ Planning completed successfully!")
            print(f"   Total iterations: {result['total_iterations']}")
            print(f"   Agents involved: {len(result['agent_outputs'])}")
            
            # Display agent contributions
            print(f"\n🤖 AGENT CONTRIBUTIONS:")
            for agent_name, output in result["agent_outputs"].items():
                status = output.get("status", "unknown")
                timestamp = output.get("timestamp", "")
                print(f"   {agent_name.replace('_', ' ').title():<20}: {status.upper()} ({timestamp[:19]})")
            
            # Display final plan summary
            travel_plan = result["travel_plan"]
            print(f"\n📋 TRAVEL PLAN SUMMARY:")
            print(f"   Destination: {travel_plan.get('destination')}")
            print(f"   Duration: {travel_plan.get('duration')} days")
            print(f"   Planning Method: {travel_plan.get('planning_method')}")
            
            print(f"\n🎉 DEMONSTRATION COMPLETED SUCCESSFULLY!")
            return True
            
        else:
            print(f"❌ Planning failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ System error: {str(e)}")
        return False

def run_interactive_planning():
    """Run interactive travel planning with user input"""
    print("\n" + "="*80)
    print("🎯 INTERACTIVE TRAVEL PLANNING")
    print("="*80)
    
    # Get user input
    input_handler = UserInputHandler()
    user_data = input_handler.get_trip_details()
    
    if not user_data:
        print("❌ Planning cancelled by user")
        return
    
    # Convert user data to LangGraph format
    travel_request = {
        "destination": user_data.get("destination", ""),
        "duration": user_data.get("duration", 3),
        "budget_range": user_data.get("budget_range", "mid-range"),
        "interests": user_data.get("interests", []),
        "group_size": user_data.get("group_size", 1),
        "travel_dates": f"{user_data.get('start_date', '')} to {user_data.get('end_date', '')}"
    }
    
    print(f"\n🚀 Starting LangGraph Multi-Agent Planning...")
    print("   This process uses multiple AI agents collaborating in real-time")
    print("   Each agent will search for current information and provide expertise")
    
    try:
        # Initialize and run the system
        travel_agents = LangGraphTravelAgents()
        result = travel_agents.run_travel_planning(travel_request)
        
        if result["success"]:
            display_planning_results(result, travel_request)
            
            # Save results
            save_results = input("\n💾 Save complete travel plan to file? (y/n): ").lower().strip()
            if save_results == 'y':
                save_langgraph_results(result, travel_request)
        else:
            print(f"❌ Planning failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ System error: {str(e)}")

def display_planning_results(result: dict, request: dict):
    """Display comprehensive planning results"""
    print("\n" + "="*80)
    print("📋 LANGGRAPH MULTI-AGENT PLANNING RESULTS")
    print("="*80)
    
    travel_plan = result["travel_plan"]
    
    # Trip Overview
    print(f"🌍 TRIP OVERVIEW:")
    print(f"   Destination: {travel_plan.get('destination')}")
    print(f"   Duration: {travel_plan.get('duration')} days")
    print(f"   Group Size: {travel_plan.get('group_size')} people")
    print(f"   Budget Range: {travel_plan.get('budget_range').title()}")
    print(f"   Interests: {', '.join(travel_plan.get('interests', []))}")
    
    # System Performance
    print(f"\n🤖 SYSTEM PERFORMANCE:")
    print(f"   Planning Method: {travel_plan.get('planning_method')}")
    print(f"   Total Iterations: {result.get('total_iterations')}")
    print(f"   Agents Involved: {len(result['agent_outputs'])}")
    print(f"   Planning Status: {'✅ Complete' if result.get('planning_complete') else '⚠️ Partial'}")
    
    # Agent Contributions
    print(f"\n🎯 AGENT CONTRIBUTIONS:")
    agent_outputs = result.get("agent_outputs", {})
    for agent_name, output in agent_outputs.items():
        print(f"\n   {agent_name.replace('_', ' ').title().upper()}:")
        contribution = output.get("response", "No output available")
        # Truncate long responses for display
        if len(contribution) > 300:
            contribution = contribution[:300] + "..."
        print(f"   {contribution}")
    
    print("\n" + "="*80)

def save_langgraph_results(result: dict, request: dict):
    """Save LangGraph results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = request.get('destination', 'unknown').replace(' ', '_').lower()
    filename = f"langgraph_travel_plan_{destination}_{timestamp}.txt"
    
    content = []
    content.append("="*80)
    content.append("LANGGRAPH MULTI-AGENT AI TRAVEL PLANNING REPORT")
    content.append("="*80)
    content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    content.append(f"System: LangGraph Framework with Google Gemini & DuckDuckGo")
    content.append("")
    
    # Trip details
    travel_plan = result["travel_plan"]
    content.append("TRIP OVERVIEW:")
    content.append("-" * 40)
    content.append(f"Destination: {travel_plan.get('destination')}")
    content.append(f"Duration: {travel_plan.get('duration')} days")
    content.append(f"Group Size: {travel_plan.get('group_size')} people")
    content.append(f"Budget Range: {travel_plan.get('budget_range')}")
    content.append(f"Interests: {', '.join(travel_plan.get('interests', []))}")
    content.append("")
    
    # System performance
    content.append("SYSTEM PERFORMANCE:")
    content.append("-" * 40)
    content.append(f"Planning Method: {travel_plan.get('planning_method')}")
    content.append(f"Total Iterations: {result.get('total_iterations')}")
    content.append(f"Agents Involved: {len(result['agent_outputs'])}")
    content.append("")
    
    # Agent contributions
    content.append("AGENT CONTRIBUTIONS:")
    content.append("-" * 40)
    agent_outputs = result.get("agent_outputs", {})
    for agent_name, output in agent_outputs.items():
        content.append(f"\n{agent_name.replace('_', ' ').title().upper()}:")
        content.append(f"Status: {output.get('status', 'Unknown')}")
        content.append(f"Timestamp: {output.get('timestamp', 'Unknown')}")
        content.append(f"Response: {output.get('response', 'No output available')}")
        content.append("")
    
    content.append("="*80)
    content.append("End of LangGraph Multi-Agent Travel Planning Report")
    content.append("="*80)
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        print(f"✅ Travel plan saved as: {filename}")
    except Exception as e:
        print(f"❌ Error saving file: {str(e)}")

def main():
    """Main entry point for LangGraph travel planning system"""
    try:
        # Display header
        display_langgraph_header()
        
        # Validate environment
        if not validate_environment():
            return
        
        print("\n" + "="*60)
        print("Choose your experience:")
        print("1. 🎭 Quick Demonstration (Tokyo sample trip)")
        print("2. 🎯 Interactive Travel Planning (Custom trip)")
        print("3. ❌ Exit")
        
        while True:
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == '1':
                print("\n🎭 Starting LangGraph System Demonstration...")
                if demonstrate_langgraph_system():
                    print("\n🎉 Demonstration completed successfully!")
                break
                
            elif choice == '2':
                print("\n🎯 Starting Interactive Planning...")
                run_interactive_planning()
                break
                
            elif choice == '3':
                print("\n👋 Thank you for trying the LangGraph Travel Planning System!")
                break
                
            else:
                print("Please enter 1, 2, or 3.")
        
    except KeyboardInterrupt:
        print("\n\n❌ Planning interrupted by user.")
    except Exception as e:
        print(f"\n❌ System error: {str(e)}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()
