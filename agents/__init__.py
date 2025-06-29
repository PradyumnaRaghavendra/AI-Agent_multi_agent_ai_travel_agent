"""
Base Agent Framework for Multi-Agent Travel Planning System
"""

import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enum import Enum

class AgentRole(Enum):
    """Define different agent roles"""
    COORDINATOR = "coordinator"
    TRAVEL_ADVISOR = "travel_advisor"
    BUDGET_OPTIMIZER = "budget_optimizer"
    WEATHER_ANALYST = "weather_analyst"
    LOCAL_EXPERT = "local_expert"
    ITINERARY_PLANNER = "itinerary_planner"

class MessageType(Enum):
    """Types of messages agents can send"""
    REQUEST = "request"
    RESPONSE = "response" 
    BROADCAST = "broadcast"
    QUERY = "query"
    RECOMMENDATION = "recommendation"

class Message:
    """Message structure for agent communication"""
    def __init__(self, sender: str, receiver: str, msg_type: MessageType, 
                 content: Dict[str, Any], timestamp: datetime = None):
        self.sender = sender
        self.receiver = receiver
        self.msg_type = msg_type
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.id = f"{sender}_{receiver}_{int(time.time() * 1000)}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'sender': self.sender,
            'receiver': self.receiver,
            'type': self.msg_type.value,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, agent_id: str, role: AgentRole, capabilities: List[str]):
        self.agent_id = agent_id
        self.role = role
        self.capabilities = capabilities
        self.message_queue: List[Message] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.is_active = True
        self.collaboration_network: Dict[str, 'BaseAgent'] = {}
        
    @abstractmethod
    def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming message and return response if needed"""
        pass
    
    @abstractmethod
    def generate_recommendation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations based on context"""
        pass
    
    def send_message(self, receiver: str, msg_type: MessageType, content: Dict[str, Any]) -> bool:
        """Send message to another agent"""
        if receiver in self.collaboration_network:
            message = Message(self.agent_id, receiver, msg_type, content)
            self.collaboration_network[receiver].receive_message(message)
            return True
        return False
    
    def receive_message(self, message: Message):
        """Receive and queue message"""
        self.message_queue.append(message)
    
    def process_message_queue(self) -> List[Message]:
        """Process all queued messages"""
        responses = []
        while self.message_queue:
            message = self.message_queue.pop(0)
            response = self.process_message(message)
            if response:
                responses.append(response)
        return responses
    
    def connect_agent(self, agent: 'BaseAgent'):
        """Connect to another agent for collaboration"""
        self.collaboration_network[agent.agent_id] = agent
        agent.collaboration_network[self.agent_id] = self
    
    def update_knowledge(self, key: str, value: Any):
        """Update agent's knowledge base"""
        self.knowledge_base[key] = value
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            'agent_id': self.agent_id,
            'role': self.role.value,
            'capabilities': self.capabilities,
            'is_active': self.is_active,
            'messages_queued': len(self.message_queue),
            'connected_agents': list(self.collaboration_network.keys()),
            'knowledge_items': len(self.knowledge_base)
        }

class AgentCommunicationHub:
    """Central hub for agent communication and coordination"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_log: List[Message] = []
        
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the hub"""
        self.agents[agent.agent_id] = agent
        
    def connect_all_agents(self):
        """Connect all agents to each other"""
        agent_list = list(self.agents.values())
        for i, agent1 in enumerate(agent_list):
            for j, agent2 in enumerate(agent_list):
                if i != j:
                    agent1.connect_agent(agent2)
    
    def broadcast_message(self, sender_id: str, content: Dict[str, Any]) -> List[Message]:
        """Broadcast message from one agent to all others"""
        responses = []
        if sender_id in self.agents:
            sender = self.agents[sender_id]
            for agent_id, agent in self.agents.items():
                if agent_id != sender_id:
                    message = Message(sender_id, agent_id, MessageType.BROADCAST, content)
                    agent.receive_message(message)
                    self.message_log.append(message)
        return responses
    
    def process_all_agents(self) -> Dict[str, List[Message]]:
        """Process message queues for all agents"""
        all_responses = {}
        for agent_id, agent in self.agents.items():
            responses = agent.process_message_queue()
            if responses:
                all_responses[agent_id] = responses
        return all_responses
    
    def get_agent_by_role(self, role: AgentRole) -> Optional[BaseAgent]:
        """Get agent by role"""
        for agent in self.agents.values():
            if agent.role == role:
                return agent
        return None
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            'total_agents': len(self.agents),
            'active_agents': len([a for a in self.agents.values() if a.is_active]),
            'total_messages': len(self.message_log),
            'agents': {aid: agent.get_status() for aid, agent in self.agents.items()}
        }

class AgentDecisionEngine:
    """Decision engine for complex multi-agent decisions"""
    
    def __init__(self, communication_hub: AgentCommunicationHub):
        self.hub = communication_hub
        
    def collaborative_decision(self, decision_context: Dict[str, Any], 
                             involved_agents: List[str]) -> Dict[str, Any]:
        """Make collaborative decision involving multiple agents"""
        
        # Step 1: Gather recommendations from involved agents
        recommendations = {}
        for agent_id in involved_agents:
            if agent_id in self.hub.agents:
                agent = self.hub.agents[agent_id]
                rec = agent.generate_recommendation(decision_context)
                recommendations[agent_id] = rec
        
        # Step 2: Analyze and synthesize recommendations
        final_decision = self._synthesize_recommendations(recommendations, decision_context)
        
        # Step 3: Broadcast final decision
        self.hub.broadcast_message("decision_engine", {
            'decision': final_decision,
            'context': decision_context,
            'contributing_agents': involved_agents
        })
        
        return final_decision
    
    def _synthesize_recommendations(self, recommendations: Dict[str, Dict], 
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize multiple agent recommendations into final decision"""
        
        # Weight recommendations based on agent expertise and context
        weights = self._calculate_agent_weights(recommendations, context)
        
        # Combine recommendations
        final_decision = {
            'primary_recommendation': None,
            'confidence_score': 0.0,
            'supporting_evidence': [],
            'alternative_options': [],
            'consensus_level': 0.0
        }
        
        # Simple consensus mechanism (can be enhanced with ML)
        if recommendations:
            # Find most common recommendations
            all_recommendations = []
            for agent_id, rec in recommendations.items():
                weight = weights.get(agent_id, 1.0)
                all_recommendations.append({
                    'agent': agent_id,
                    'recommendation': rec,
                    'weight': weight
                })
            
            # Select best recommendation based on weights and consensus
            best_rec = max(all_recommendations, key=lambda x: x['weight'])
            final_decision['primary_recommendation'] = best_rec['recommendation']
            final_decision['confidence_score'] = best_rec['weight']
            final_decision['supporting_evidence'] = [r['recommendation'] for r in all_recommendations]
            
            # Calculate consensus level
            final_decision['consensus_level'] = len(all_recommendations) / len(recommendations) if recommendations else 0
        
        return final_decision
    
    def _calculate_agent_weights(self, recommendations: Dict[str, Dict], 
                               context: Dict[str, Any]) -> Dict[str, float]:
        """Calculate weights for agent recommendations based on expertise"""
        weights = {}
        
        # Default weights based on agent roles and context
        for agent_id in recommendations.keys():
            if agent_id in self.hub.agents:
                agent = self.hub.agents[agent_id]
                base_weight = 1.0
                
                # Increase weight based on relevance to context
                if context.get('primary_concern') == 'budget' and agent.role == AgentRole.BUDGET_OPTIMIZER:
                    base_weight = 2.0
                elif context.get('primary_concern') == 'weather' and agent.role == AgentRole.WEATHER_ANALYST:
                    base_weight = 2.0
                elif context.get('primary_concern') == 'local_insights' and agent.role == AgentRole.LOCAL_EXPERT:
                    base_weight = 2.0
                
                weights[agent_id] = base_weight
        
        return weights
