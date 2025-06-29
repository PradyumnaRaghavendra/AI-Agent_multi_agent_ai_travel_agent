"""
Multi-Agent AI Travel Planning System - Main Entry Point
Enhanced collaborative travel planning with specialized AI agents
"""

import sys
import os
from datetime import datetime, timedelta
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.multi_agent_orchestrator import MultiAgentTravelOrchestrator
from modules.user_input import UserInputHandler
from utils.helpers import display_header, save_to_file

def main():
    """Main function for multi-agent travel planning system"""
    
    # Display enhanced header
    display_multi_agent_header()
    
    try:
        # Initialize the multi-agent system
        print("🚀 Initializing Multi-Agent Travel Planning System...")
        orchestrator = MultiAgentTravelOrchestrator()
        
        # Show system status
        system_status = orchestrator.get_system_status()
        print(f"✅ System Ready: {system_status['active_agents']}/{system_status['total_agents']} agents online")
        print()
        
        # Demonstrate agent collaboration capabilities
        show_agent_collaboration_demo = input("Would you like to see the multi-agent collaboration demo? (y/n): ").lower().strip()
        if show_agent_collaboration_demo == 'y':
            demonstrate_system_capabilities(orchestrator)
        
        # Get user input
        print("\n" + "="*80)
        print("🎯 TRIP PLANNING INPUT")
        print("="*80)
        
        user_input_handler = UserInputHandler()
        user_data = user_input_handler.get_comprehensive_trip_details()
        
        if not user_data:
            print("❌ Trip planning cancelled.")
            return
        
        print("\n" + "="*80)
        print("🤖 MULTI-AGENT COLLABORATIVE PLANNING")
        print("="*80)
        
        # Execute multi-agent planning
        comprehensive_plan = orchestrator.plan_comprehensive_trip(user_data)
        
        # Display results
        display_multi_agent_results(comprehensive_plan)
        
        # Save results
        save_results = input("\n💾 Save complete multi-agent report to file? (y/n): ").lower().strip()
        if save_results == 'y':
            save_multi_agent_results(comprehensive_plan, user_data)
        
        # Show system performance metrics
        show_metrics = input("\n📊 View system performance metrics? (y/n): ").lower().strip()
        if show_metrics == 'y':
            display_system_metrics(orchestrator, comprehensive_plan)
        
        print("\n🎉 Multi-Agent Travel Planning Complete!")
        print("Thank you for using our collaborative AI travel planning system!")
        
    except KeyboardInterrupt:
        print("\n\n❌ Multi-agent planning interrupted by user.")
    except Exception as e:
        print(f"\n❌ An error occurred in the multi-agent system: {str(e)}")
        print("Please check your inputs and try again.")

def display_multi_agent_header():
    """Display enhanced header for multi-agent system"""
    print("\n" + "="*80)
    print("🤖 MULTI-AGENT AI TRAVEL PLANNER & EXPENSE CALCULATOR")
    print("="*80)
    print("🎯 Collaborative Intelligence: 6 Specialized AI Agents Working Together")
    print("="*80)
    print("\n🧠 AI AGENT TEAM:")
    print("   🎯 Coordinator Agent     - Master orchestration & decision synthesis")
    print("   ✈️  Travel Advisor       - Destination expertise & recommendations")
    print("   💰 Budget Optimizer      - Cost analysis & money-saving strategies")
    print("   🌤️  Weather Analyst      - Weather intelligence & planning")
    print("   🏠 Local Expert          - Insider knowledge & real-time insights")
    print("   📅 Itinerary Planner     - Schedule optimization & logistics")
    print("\n🚀 ENHANCED CAPABILITIES:")
    print("   • Collaborative decision-making with agent consensus")
    print("   • Multi-dimensional optimization (cost, weather, logistics)")
    print("   • Real-time conflict resolution between recommendations")
    print("   • Adaptive planning based on your priorities")
    print("   • Comprehensive validation and quality assurance")
    print("="*80)

def demonstrate_system_capabilities(orchestrator: MultiAgentTravelOrchestrator):
    """Demonstrate the multi-agent system capabilities"""
    print("\n" + "="*60)
    print("🎭 MULTI-AGENT COLLABORATION DEMONSTRATION")
    print("="*60)
    
    demo_data = orchestrator.demonstrate_agent_collaboration()
    
    print("\n🤖 AGENT NETWORK:")
    for agent_id, info in demo_data['agent_network'].items():
        print(f"   {agent_id.replace('_', ' ').title():<25} | Role: {info['role']:<15} | Capabilities: {len(info['capabilities'])}")
    
    print(f"\n📡 COMMUNICATION INFRASTRUCTURE:")
    comm_patterns = demo_data['communication_patterns']
    print(f"   • Registered Agents: {comm_patterns['hub_registered_agents']}")
    print(f"   • Message Types: {', '.join(comm_patterns['message_types_supported'])}")
    print(f"   • Features: {', '.join(comm_patterns['collaborative_features'])}")
    
    print(f"\n🧠 DECISION MAKING ENGINE:")
    decision_info = demo_data['decision_making_process']
    print(f"   • Engine: {decision_info['synthesis_engine']}")
    print(f"   • Consensus Methods: {', '.join(decision_info['consensus_mechanisms'])}")
    print(f"   • Quality Assurance: {', '.join(decision_info['quality_assurance'])}")
    
    print(f"\n✨ SYSTEM CAPABILITIES:")
    for capability in demo_data['system_capabilities']:
        print(f"   • {capability}")
    
    print("="*60)
    input("\nPress Enter to continue to trip planning...")

def display_multi_agent_results(comprehensive_plan: dict):
    """Display comprehensive multi-agent planning results"""
    print("\n" + "="*80)
    print("📋 MULTI-AGENT TRAVEL PLANNING RESULTS")
    print("="*80)
    
    # Trip Summary
    trip_summary = comprehensive_plan.get('trip_summary', {})
    print(f"🎯 TRIP OVERVIEW:")
    print(f"   Destination: {trip_summary.get('destination', 'N/A')}")
    print(f"   Duration: {trip_summary.get('duration', 'N/A')} days")
    print(f"   Dates: {trip_summary.get('dates', 'N/A')}")
    print(f"   Group Size: {trip_summary.get('group_size', 'N/A')} people")
    print(f"   Planning Method: {trip_summary.get('planning_approach', 'N/A')}")
    
    # Agent Contributions
    print(f"\n🤖 AI AGENT CONTRIBUTIONS:")
    agent_contributions = comprehensive_plan.get('agent_contributions', {})
    for agent_type, contribution in agent_contributions.items():
        print(f"   {agent_type.replace('_', ' ').title():<20}: {contribution}")
    
    # System Performance
    print(f"\n📊 SYSTEM PERFORMANCE:")
    performance = comprehensive_plan.get('system_performance', {})
    print(f"   Agents Consulted: {performance.get('agents_consulted', 0)}")
    print(f"   Consensus Level: {performance.get('consensus_achieved', 0):.1%}")
    print(f"   Confidence Score: {performance.get('confidence_score', 0):.1%}")
    print(f"   Processing: {performance.get('processing_time', 'N/A')}")
    
    # Multi-Agent Summary
    print(f"\n🎯 COLLABORATION SUMMARY:")
    ma_summary = comprehensive_plan.get('multi_agent_summary', {})
    print(f"   Coordination Success: {'✅' if ma_summary.get('coordination_success') else '❌'}")
    print(f"   All Agents Contributed: {'✅' if ma_summary.get('all_agents_contributed') else '❌'}")
    print(f"   Conflicts Resolved: {ma_summary.get('decision_conflicts_resolved', 0)}")
    print(f"   Recommendation Quality: {ma_summary.get('recommendation_quality', 'N/A')}")
    print(f"   Predicted Satisfaction: {ma_summary.get('user_satisfaction_prediction', 'N/A')}")
    
    # Detailed Insights
    detailed_insights = comprehensive_plan.get('detailed_insights', {})
    
    if detailed_insights.get('destination_highlights'):
        print(f"\n🏛️ DESTINATION HIGHLIGHTS:")
        for highlight in detailed_insights['destination_highlights']:
            print(f"   • {highlight}")
    
    if detailed_insights.get('budget_breakdown'):
        print(f"\n💰 BUDGET BREAKDOWN:")
        for category, percentage in detailed_insights['budget_breakdown'].items():
            print(f"   {category.title():<15}: {percentage}")
    
    if detailed_insights.get('weather_considerations'):
        print(f"\n🌤️ WEATHER INTELLIGENCE:")
        for consideration in detailed_insights['weather_considerations']:
            print(f"   • {consideration}")
    
    if detailed_insights.get('local_tips'):
        print(f"\n🏠 LOCAL EXPERT INSIGHTS:")
        for tip in detailed_insights['local_tips']:
            print(f"   • {tip}")
    
    if detailed_insights.get('optimized_itinerary'):
        print(f"\n📅 ITINERARY OPTIMIZATION:")
        for optimization in detailed_insights['optimized_itinerary']:
            print(f"   • {optimization}")
    
    if detailed_insights.get('contingency_plans'):
        print(f"\n🛡️ CONTINGENCY PLANNING:")
        for plan in detailed_insights['contingency_plans']:
            print(f"   • {plan}")

def save_multi_agent_results(comprehensive_plan: dict, user_data: dict):
    """Save multi-agent results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = user_data.get('destination', 'unknown').replace(' ', '_').lower()
    filename = f"multi_agent_trip_plan_{destination}_{timestamp}.txt"
    
    content = []
    content.append("="*80)
    content.append("MULTI-AGENT AI TRAVEL PLANNING REPORT")
    content.append("="*80)
    content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    content.append(f"Planning System: Multi-Agent Collaborative Intelligence")
    content.append("")
    
    # Trip Summary
    trip_summary = comprehensive_plan.get('trip_summary', {})
    content.append("TRIP OVERVIEW:")
    content.append("-" * 40)
    for key, value in trip_summary.items():
        content.append(f"{key.replace('_', ' ').title()}: {value}")
    content.append("")
    
    # Agent Contributions
    content.append("AI AGENT CONTRIBUTIONS:")
    content.append("-" * 40)
    agent_contributions = comprehensive_plan.get('agent_contributions', {})
    for agent_type, contribution in agent_contributions.items():
        content.append(f"{agent_type.replace('_', ' ').title()}: {contribution}")
    content.append("")
    
    # System Performance
    content.append("SYSTEM PERFORMANCE METRICS:")
    content.append("-" * 40)
    performance = comprehensive_plan.get('system_performance', {})
    for key, value in performance.items():
        if key != 'quality_metrics':
            content.append(f"{key.replace('_', ' ').title()}: {value}")
    
    # Quality Metrics
    quality_metrics = performance.get('quality_metrics', {})
    if quality_metrics:
        content.append("\nQuality Metrics:")
        for metric, score in quality_metrics.items():
            content.append(f"  {metric.replace('_', ' ').title()}: {score:.1%}")
    content.append("")
    
    # Detailed Insights
    detailed_insights = comprehensive_plan.get('detailed_insights', {})
    for section, items in detailed_insights.items():
        if items:
            content.append(f"{section.replace('_', ' ').upper()}:")
            content.append("-" * 40)
            if isinstance(items, list):
                for item in items:
                    content.append(f"• {item}")
            elif isinstance(items, dict):
                for key, value in items.items():
                    content.append(f"• {key.title()}: {value}")
            content.append("")
    
    # Multi-Agent Summary
    ma_summary = comprehensive_plan.get('multi_agent_summary', {})
    content.append("MULTI-AGENT COLLABORATION SUMMARY:")
    content.append("-" * 40)
    for key, value in ma_summary.items():
        content.append(f"{key.replace('_', ' ').title()}: {value}")
    content.append("")
    
    content.append("="*80)
    content.append("End of Multi-Agent Travel Planning Report")
    content.append("="*80)
    
    # Save to file
    try:
        full_content = "\n".join(content)
        save_to_file(full_content, filename)
        print(f"✅ Multi-agent report saved as: {filename}")
    except Exception as e:
        print(f"❌ Error saving file: {str(e)}")

def display_system_metrics(orchestrator: MultiAgentTravelOrchestrator, comprehensive_plan: dict):
    """Display detailed system performance metrics"""
    print("\n" + "="*60)
    print("📊 SYSTEM PERFORMANCE METRICS")
    print("="*60)
    
    system_status = orchestrator.get_system_status()
    
    print("🖥️ SYSTEM STATUS:")
    print(f"   Overall Status: {system_status['system_status'].title()}")
    print(f"   Active Agents: {system_status['active_agents']}/{system_status['total_agents']}")
    print(f"   Network Health: {system_status['agent_network_health']}")
    print(f"   Planning Sessions: {system_status['planning_sessions_completed']}")
    
    print("\n📡 COMMUNICATION HUB:")
    hub_status = system_status.get('communication_hub_status', {})
    print(f"   Total Agents: {hub_status.get('total_agents', 0)}")
    print(f"   Active Agents: {hub_status.get('active_agents', 0)}")
    print(f"   Messages Processed: {hub_status.get('total_messages', 0)}")
    
    print("\n🎯 PLANNING QUALITY:")
    performance = comprehensive_plan.get('system_performance', {})
    quality_metrics = performance.get('quality_metrics', {})
    for metric, score in quality_metrics.items():
        print(f"   {metric.replace('_', ' ').title()}: {score:.1%}")
    
    print("\n🤖 AGENT PERFORMANCE:")
    hub_agents = hub_status.get('agents', {})
    for agent_id, agent_info in hub_agents.items():
        print(f"   {agent_id.replace('_', ' ').title():<20}: "
              f"Active: {'✅' if agent_info.get('is_active') else '❌'} | "
              f"Connections: {len(agent_info.get('connected_agents', []))}")
    
    print("="*60)

if __name__ == "__main__":
    main()
