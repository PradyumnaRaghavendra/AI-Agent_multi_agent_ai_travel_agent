# LangGraph Travel Planning Agents
from typing import Dict, Any, List, Optional, TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import json
from datetime import datetime

from config.langgraph_config import langgraph_config as config

# Define the state structure for the multi-agent system
class TravelPlanState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage | SystemMessage], add_messages]
    destination: str
    duration: int
    budget_range: str
    interests: List[str]
    group_size: int
    travel_dates: str
    current_agent: str
    agent_outputs: Dict[str, Any]
    final_plan: Dict[str, Any]
    iteration_count: int

class LangGraphTravelAgents:
    """LangGraph-based multi-agent travel planning system"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=config.GEMINI_MODEL,
            google_api_key=config.GEMINI_API_KEY,
            temperature=config.TEMPERATURE,
            max_output_tokens=config.MAX_TOKENS,
            top_p=config.TOP_P,
        )
        
        # Initialize the graph
        self.graph = self._create_agent_graph()
    
    def _create_agent_graph(self) -> StateGraph:
        """Create the LangGraph multi-agent workflow"""
        
        # Define the workflow graph
        workflow = StateGraph(TravelPlanState)
        
        # Add agent nodes
        workflow.add_node("travel_advisor", self._travel_advisor_agent)
        workflow.add_node("weather_analyst", self._weather_analyst_agent)
        workflow.add_node("budget_optimizer", self._budget_optimizer_agent)
        workflow.add_node("local_expert", self._local_expert_agent)
        workflow.add_node("itinerary_planner", self._itinerary_planner_agent)
        workflow.add_node("coordinator", self._coordinator_agent)
        workflow.add_node("tools", self._tool_executor_node)
        
        # Define the workflow edges
        workflow.set_entry_point("coordinator")
        
        # Coordinator decides which agents to call
        workflow.add_conditional_edges(
            "coordinator",
            self._coordinator_router,
            {
                "travel_advisor": "travel_advisor",
                "weather_analyst": "weather_analyst", 
                "budget_optimizer": "budget_optimizer",
                "local_expert": "local_expert",
                "itinerary_planner": "itinerary_planner",
                "tools": "tools",
                "end": END
            }
        )
        
        # Each agent can either use tools or return to coordinator
        for agent in ["travel_advisor", "weather_analyst", "budget_optimizer", "local_expert", "itinerary_planner"]:
            workflow.add_conditional_edges(
                agent,
                self._agent_router,
                {
                    "tools": "tools",
                    "coordinator": "coordinator",
                    "end": END
                }
            )
        
        # Tools always return to coordinator
        workflow.add_edge("tools", "coordinator")
        
        return workflow.compile()
    
    def _coordinator_agent(self, state: TravelPlanState) -> TravelPlanState:
        """Coordinator agent that orchestrates the multi-agent workflow"""
        
        system_prompt = f"""You are the Coordinator Agent for a multi-agent travel planning system.

Your role is to:
1. Analyze the travel planning request
2. Determine which specialized agents need to contribute
3. Coordinate the workflow between agents
4. Synthesize final recommendations

Current request:
- Destination: {state.get('destination', 'Not specified')}
- Duration: {state.get('duration', 'Not specified')} days
- Budget: {state.get('budget_range', 'Not specified')}
- Interests: {', '.join(state.get('interests', []))}
- Group size: {state.get('group_size', 1)}
- Travel dates: {state.get('travel_dates', 'Not specified')}

Available agents:
- travel_advisor: Destination expertise and attraction recommendations
- weather_analyst: Weather forecasting and activity planning
- budget_optimizer: Cost analysis and money-saving strategies
- local_expert: Local insights and cultural tips
- itinerary_planner: Schedule optimization and logistics

Agent outputs so far: {json.dumps(state.get('agent_outputs', {}), indent=2)}

Based on the current state, decide what to do next:
1. If you need more information, specify which agent should work next
2. If you have enough information from all relevant agents, synthesize the final plan
3. Respond with either an agent name or 'FINAL_PLAN' if ready to conclude

Your response should be either:
- Agent name to call next (travel_advisor, weather_analyst, budget_optimizer, local_expert, itinerary_planner)
- 'FINAL_PLAN' if ready to create the comprehensive travel plan
- 'SEARCH' if you need to search for information first
"""
        
        messages = [SystemMessage(content=system_prompt)]
        if state.get("messages"):
            messages.extend(state["messages"][-3:])  # Keep recent context
        
        response = self.llm.invoke(messages)
        
        # Update state
        new_state = state.copy()
        new_state["messages"] = state.get("messages", []) + [response]
        new_state["current_agent"] = "coordinator"
        new_state["iteration_count"] = state.get("iteration_count", 0) + 1
        
        return new_state
    
    def _travel_advisor_agent(self, state: TravelPlanState) -> TravelPlanState:
        """Travel advisor agent with destination expertise"""
        
        system_prompt = f"""You are the Travel Advisor Agent, specialized in destination expertise and recommendations.

Your expertise includes:
- Destination knowledge and highlights
- Attraction recommendations
- Cultural insights and tips
- Best practices for travelers

Current planning request:
- Destination: {state.get('destination')}
- Duration: {state.get('duration')} days
- Interests: {', '.join(state.get('interests', []))}
- Group size: {state.get('group_size')}

Your task: Provide comprehensive destination advice including:
1. Top attractions and must-see places
2. Cultural insights and etiquette tips
3. Best areas to stay and explore
4. Activity recommendations based on interests

If you need to search for current information about the destination, respond with 'NEED_SEARCH: [search query]'
Otherwise, provide your expert recommendations based on your knowledge.
"""
        
        messages = [SystemMessage(content=system_prompt)]
        if state.get("messages"):
            messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        # Store agent output
        agent_outputs = state.get("agent_outputs", {})
        agent_outputs["travel_advisor"] = {
            "response": response.content,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        new_state = state.copy()
        new_state["messages"] = state.get("messages", []) + [response]
        new_state["current_agent"] = "travel_advisor"
        new_state["agent_outputs"] = agent_outputs
        
        return new_state
    
    def _weather_analyst_agent(self, state: TravelPlanState) -> TravelPlanState:
        """Weather analyst agent for climate and weather planning"""
        
        system_prompt = f"""You are the Weather Analyst Agent, specialized in weather intelligence and climate-aware planning.

Your expertise includes:
- Weather pattern analysis
- Seasonal travel recommendations
- Activity planning based on weather conditions
- Climate considerations for destinations

Current planning request:
- Destination: {state.get('destination')}
- Travel dates: {state.get('travel_dates')}
- Duration: {state.get('duration')} days
- Planned activities: {', '.join(state.get('interests', []))}

Your task: Provide weather-intelligent recommendations including:
1. Expected weather conditions during travel dates
2. Best times of day for outdoor activities
3. Weather-appropriate activity suggestions
4. Packing recommendations based on climate

If you need current weather data, respond with 'NEED_SEARCH: [weather search query]'
Otherwise, provide your analysis based on climate knowledge.
"""
        
        messages = [SystemMessage(content=system_prompt)]
        if state.get("messages"):
            messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        # Store agent output
        agent_outputs = state.get("agent_outputs", {})
        agent_outputs["weather_analyst"] = {
            "response": response.content,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        new_state = state.copy()
        new_state["messages"] = state.get("messages", []) + [response]
        new_state["current_agent"] = "weather_analyst"
        new_state["agent_outputs"] = agent_outputs
        
        return new_state
    
    def _budget_optimizer_agent(self, state: TravelPlanState) -> TravelPlanState:
        """Budget optimizer agent for cost analysis and optimization"""
        
        system_prompt = f"""You are the Budget Optimizer Agent, specialized in cost analysis and money-saving strategies.

Your expertise includes:
- Travel cost analysis and budgeting
- Money-saving tips and strategies
- Budget allocation recommendations
- Cost-effective alternatives

Current planning request:
- Destination: {state.get('destination')}
- Duration: {state.get('duration')} days
- Budget range: {state.get('budget_range')}
- Group size: {state.get('group_size')}

Your task: Provide budget optimization recommendations including:
1. Estimated daily and total costs
2. Budget breakdown by category (accommodation, food, activities, transport)
3. Money-saving tips and strategies
4. Cost-effective alternatives for expensive activities

If you need current pricing information, respond with 'NEED_SEARCH: [budget search query]'
Otherwise, provide your budget analysis and recommendations.
"""
        
        messages = [SystemMessage(content=system_prompt)]
        if state.get("messages"):
            messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        # Store agent output
        agent_outputs = state.get("agent_outputs", {})
        agent_outputs["budget_optimizer"] = {
            "response": response.content,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        new_state = state.copy()
        new_state["messages"] = state.get("messages", []) + [response]
        new_state["current_agent"] = "budget_optimizer"
        new_state["agent_outputs"] = agent_outputs
        
        return new_state
    
    def _local_expert_agent(self, state: TravelPlanState) -> TravelPlanState:
        """Local expert agent with insider knowledge"""
        
        system_prompt = f"""You are the Local Expert Agent, specialized in insider knowledge and local insights.

Your expertise includes:
- Local customs and cultural nuances
- Hidden gems and off-the-beaten-path recommendations
- Local dining and entertainment scene
- Practical local tips and advice

Current planning request:
- Destination: {state.get('destination')}
- Interests: {', '.join(state.get('interests', []))}
- Duration: {state.get('duration')} days

Your task: Provide local expert insights including:
1. Hidden gems and local favorites
2. Cultural etiquette and customs
3. Local dining recommendations
4. Insider tips for getting around and saving money

If you need current local information, respond with 'NEED_SEARCH: [local tips search query]'
Otherwise, provide your local expertise and insights.
"""
        
        messages = [SystemMessage(content=system_prompt)]
        if state.get("messages"):
            messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        # Store agent output
        agent_outputs = state.get("agent_outputs", {})
        agent_outputs["local_expert"] = {
            "response": response.content,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        new_state = state.copy()
        new_state["messages"] = state.get("messages", []) + [response]
        new_state["current_agent"] = "local_expert"
        new_state["agent_outputs"] = agent_outputs
        
        return new_state
    
    def _itinerary_planner_agent(self, state: TravelPlanState) -> TravelPlanState:
        """Itinerary planner agent for schedule optimization"""
        
        system_prompt = f"""You are the Itinerary Planner Agent, specialized in schedule optimization and logistics.

Your expertise includes:
- Daily itinerary planning and optimization
- Transportation and logistics coordination
- Time management and scheduling
- Activity sequencing and routing

Current planning request:
- Destination: {state.get('destination')}
- Duration: {state.get('duration')} days
- Group size: {state.get('group_size')}
- Available agent insights: {list(state.get('agent_outputs', {}).keys())}

Your task: Create an optimized itinerary including:
1. Day-by-day schedule recommendations
2. Optimal timing for activities
3. Transportation suggestions between locations
4. Rest periods and meal breaks

Consider the recommendations from other agents when creating the itinerary.
Provide a structured daily plan that maximizes the travel experience.
"""
        
        messages = [SystemMessage(content=system_prompt)]
        if state.get("messages"):
            messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        # Store agent output
        agent_outputs = state.get("agent_outputs", {})
        agent_outputs["itinerary_planner"] = {
            "response": response.content,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        new_state = state.copy()
        new_state["messages"] = state.get("messages", []) + [response]
        new_state["current_agent"] = "itinerary_planner"
        new_state["agent_outputs"] = agent_outputs
        
        return new_state
    
    def _tool_executor_node(self, state: TravelPlanState) -> TravelPlanState:
        """Execute tools based on agent requests"""
        
        last_message = state["messages"][-1] if state.get("messages") else None
        if not last_message:
            return state
        
        # Check if the last message requests a search
        content = last_message.content
        if "NEED_SEARCH:" in content:
            search_query = content.split("NEED_SEARCH:")[-1].strip()
            
            # Determine which tool to use based on the current agent and query
            current_agent = state.get("current_agent", "")
            
            try:
                if "weather" in search_query.lower() or current_agent == "weather_analyst":
                    from tools.travel_tools import search_weather_info
                    tool_result = search_weather_info.invoke({
                        "destination": state.get("destination", ""), 
                        "dates": state.get("travel_dates", "")
                    })
                elif "attraction" in search_query.lower() or "activity" in search_query.lower():
                    from tools.travel_tools import search_attractions
                    tool_result = search_attractions.invoke({
                        "destination": state.get("destination", ""), 
                        "interests": " ".join(state.get("interests", []))
                    })
                elif "budget" in search_query.lower() or "cost" in search_query.lower():
                    from tools.travel_tools import search_budget_info
                    tool_result = search_budget_info.invoke({
                        "destination": state.get("destination", ""), 
                        "duration": str(state.get("duration", ""))
                    })
                elif "hotel" in search_query.lower() or "accommodation" in search_query.lower():
                    from tools.travel_tools import search_hotels
                    tool_result = search_hotels.invoke({
                        "destination": state.get("destination", ""), 
                        "budget": state.get("budget_range", "mid-range")
                    })
                elif "restaurant" in search_query.lower() or "food" in search_query.lower():
                    from tools.travel_tools import search_restaurants
                    tool_result = search_restaurants.invoke({
                        "destination": state.get("destination", "")
                    })
                elif "local" in search_query.lower() or "tip" in search_query.lower():
                    from tools.travel_tools import search_local_tips
                    tool_result = search_local_tips.invoke({
                        "destination": state.get("destination", "")
                    })
                else:
                    # Default to destination info search
                    from tools.travel_tools import search_destination_info
                    tool_result = search_destination_info.invoke({
                        "query": state.get("destination", "")
                    })
                
                # Add tool result to messages
                tool_message = AIMessage(content=f"Search results: {tool_result}")
                new_state = state.copy()
                new_state["messages"] = state.get("messages", []) + [tool_message]
                return new_state
                
            except Exception as e:
                # Add error message if tool execution fails
                error_message = AIMessage(content=f"Tool execution error: {str(e)}")
                new_state = state.copy()
                new_state["messages"] = state.get("messages", []) + [error_message]
                return new_state
        
        return state
    
    def _coordinator_router(self, state: TravelPlanState) -> str:
        """Route from coordinator to appropriate next step"""
        
        last_message = state.get("messages", [])[-1] if state.get("messages") else None
        if not last_message:
            return "end"
        
        content = last_message.content.lower()
        
        # Check if coordinator wants to search
        if "search" in content or "need_search" in content:
            return "tools"
        
        # Check if coordinator is requesting a specific agent
        if "travel_advisor" in content:
            return "travel_advisor"
        elif "weather_analyst" in content:
            return "weather_analyst"
        elif "budget_optimizer" in content:
            return "budget_optimizer"
        elif "local_expert" in content:
            return "local_expert"
        elif "itinerary_planner" in content:
            return "itinerary_planner"
        elif "final_plan" in content:
            return "end"
        
        # Default: check which agents haven't contributed yet
        agent_outputs = state.get("agent_outputs", {})
        required_agents = ["travel_advisor", "weather_analyst", "budget_optimizer", "local_expert", "itinerary_planner"]
        
        for agent in required_agents:
            if agent not in agent_outputs:
                return agent
        
        # If all agents have contributed, end
        return "end"
    
    def _agent_router(self, state: TravelPlanState) -> str:
        """Route from agents to next step"""
        
        last_message = state.get("messages", [])[-1] if state.get("messages") else None
        if not last_message:
            return "coordinator"
        
        content = last_message.content
        
        # Check if agent needs to search
        if "NEED_SEARCH:" in content:
            return "tools"
        
        # Otherwise return to coordinator
        return "coordinator"
    
    def run_travel_planning(self, travel_request: Dict[str, Any]) -> Dict[str, Any]:
        """Run the complete multi-agent travel planning workflow"""
        
        # Initialize state
        initial_state = TravelPlanState(
            messages=[HumanMessage(content=f"Plan a trip with these requirements: {json.dumps(travel_request)}")],
            destination=travel_request.get("destination", ""),
            duration=travel_request.get("duration", 3),
            budget_range=travel_request.get("budget_range", "mid-range"),
            interests=travel_request.get("interests", []),
            group_size=travel_request.get("group_size", 1),
            travel_dates=travel_request.get("travel_dates", ""),
            current_agent="",
            agent_outputs={},
            final_plan={},
            iteration_count=0
        )
        
        # Run the workflow
        try:
            final_state = self.graph.invoke(initial_state)
            
            # Compile final travel plan
            final_plan = self._compile_final_plan(final_state)
            
            return {
                "success": True,
                "travel_plan": final_plan,
                "agent_outputs": final_state.get("agent_outputs", {}),
                "total_iterations": final_state.get("iteration_count", 0),
                "planning_complete": True
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "travel_plan": {},
                "agent_outputs": {},
                "total_iterations": 0,
                "planning_complete": False
            }
    
    def _compile_final_plan(self, state: TravelPlanState) -> Dict[str, Any]:
        """Compile the final travel plan from all agent outputs"""
        
        agent_outputs = state.get("agent_outputs", {})
        
        final_plan = {
            "destination": state.get("destination"),
            "duration": state.get("duration"),
            "travel_dates": state.get("travel_dates"),
            "group_size": state.get("group_size"),
            "budget_range": state.get("budget_range"),
            "interests": state.get("interests"),
            "planning_method": "LangGraph Multi-Agent Collaboration",
            "agent_contributions": {},
            "recommendations": {},
            "summary": "Multi-agent collaborative travel plan generated using LangGraph framework"
        }
        
        # Extract key information from each agent
        for agent_name, output in agent_outputs.items():
            final_plan["agent_contributions"][agent_name] = {
                "contribution": output.get("response", ""),
                "timestamp": output.get("timestamp", ""),
                "status": output.get("status", "")
            }
        
        # Generate summary recommendations
        if agent_outputs:
            final_plan["recommendations"] = {
                "destination_highlights": "See travel advisor recommendations",
                "weather_considerations": "Check weather analyst insights",
                "budget_breakdown": "Review budget optimizer analysis",
                "local_insights": "Follow local expert tips",
                "daily_itinerary": "Use itinerary planner schedule"
            }
        
        return final_plan
