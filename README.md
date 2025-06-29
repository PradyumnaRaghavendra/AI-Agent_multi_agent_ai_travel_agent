
# 🚀 AI Travel Agent & Expense Planner - LangGraph Multi-Agent System

## Overview

A state-of-the-art multi-agent travel planning system built with **LangGraph**, **Google Gemini Flash-2.0**, and **DuckDuckGo Search**. The system offers three different planning approaches, from traditional single-agent to cutting-edge multi-agent collaboration using modern industry frameworks.

## 🤖 Planning Options

Choose from three different planning experiences:

### 1. 🔧 Single-Agent Planning (Classic)
- Traditional single AI agent approach
- Direct planning methodology
- Proven reliability and efficiency

### 2. 🚀 Legacy Multi-Agent (Custom Framework)
- 6 specialized AI agents working together
- Custom multi-agent framework
- Enhanced recommendations through collaboration

### 3. 🌟 LangGraph Multi-Agent (Advanced) ⭐ **RECOMMENDED**
- **Google Gemini Flash-2.0** powered agents
- **DuckDuckGo real-time search** integration
- **LangGraph workflow** orchestration
- State-of-the-art multi-agent collaboration

## 🏗️ LangGraph System Architecture
![](https://github.com/abh2050/langraph_multi_agent_ai_travel_agent/blob/main/Editor%20_%20Mermaid%20Chart-2025-06-20-183945.png)

### Framework Components
- **LangGraph StateGraph**: Workflow orchestration and state management
- **Google Gemini Flash-2.0**: Advanced AI reasoning and natural language processing
- **DuckDuckGo Search**: Real-time information retrieval (no API key needed)
- **Pydantic**: Type safety and data validation
- **Custom Agent Protocols**: Specialized communication between agents

### 🤖 AI Agent Network

| Agent | Role | Capabilities |
|-------|------|-------------|
| **Coordinator** | Workflow orchestration & decision synthesis | Master planning, task delegation, consensus building |
| **Travel Advisor** | Destination expertise with live search | Attraction research, destination insights, cultural guidance |
| **Weather Analyst** | Weather intelligence with current data | Weather forecasting, climate analysis, packing advice |
| **Budget Optimizer** | Cost analysis with real-time pricing | Budget planning, cost optimization, savings strategies |
| **Local Expert** | Insider knowledge with local info | Local tips, hidden gems, cultural etiquette |
| **Itinerary Planner** | Schedule optimization & logistics | Day-by-day planning, route optimization, timing |

## 🎯 Key Features

### Advanced Capabilities
- ✅ **Real-time Search Integration**: Live data from DuckDuckGo
- ✅ **State Management**: Persistent conversation state across agents
- ✅ **Tool-Augmented Agents**: Each agent has specialized search tools
- ✅ **Collaborative Decision Making**: Agents work together to create optimal plans
- ✅ **Workflow Orchestration**: LangGraph manages complex agent interactions
- ✅ **Error Handling**: Robust error recovery and fallback mechanisms

### Search Tools
1. **Destination Information**: General destination research
2. **Weather Intelligence**: Current and forecasted weather data
3. **Attraction Discovery**: Top attractions and activities
4. **Hotel Research**: Accommodation options and pricing
5. **Restaurant Finder**: Dining recommendations and reviews
6. **Local Insights**: Cultural tips and insider knowledge
7. **Budget Analysis**: Cost estimates and budget planning
## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.8+
pip install -r requirements.txt
```

### Setup
1. **Get Gemini API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Configure Environment**: Add your API key to `.env` file
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. **Verify Installation**: Run the test script
   ```bash
   python test_langgraph_system.py
   ```

### Running the System

#### Option 1: Main Menu (All 3 Systems)
```bash
python main.py
# Select option 3 for LangGraph (Recommended)
# Select option 2 for Legacy Multi-Agent
# Select option 1 for Single-Agent
```

#### Option 2: Direct LangGraph System
```bash
python langgraph_main.py
```

#### Option 3: Test Without API Key
```bash
python test_langgraph_system.py
```

## 📊 Usage Examples

### Demo Mode
```bash
python langgraph_main.py
# Select option 1 for Tokyo demonstration
```

### Interactive Planning
```bash
python langgraph_main.py
# Select option 2 for custom trip planning
```

### System Validation
```bash
python test_langgraph_system.py
# Tests all components without API calls
```

## 🛠️ Configuration

### Environment Variables
```bash
# Required for LangGraph System
GEMINI_API_KEY=your_gemini_api_key

# Optional (for legacy systems)
OPENWEATHER_API_KEY=your_weather_api_key
GOOGLE_PLACES_API_KEY=your_places_api_key
EXCHANGERATE_API_KEY=your_exchange_rate_api_key
```

### Model Configuration
```python
class LangGraphConfig:
    GEMINI_MODEL = "gemini-2.0-flash"
    TEMPERATURE = 0.7
    MAX_TOKENS = 4000
    TOP_P = 0.9
```

### API Configuration (Optional)
For enhanced legacy functionality, obtain free API keys:

1. **Google Gemini API** (Required for LangGraph system)
   - Get key: https://makersuite.google.com/app/apikey
   - Add to .env: `GEMINI_API_KEY=your_key`

2. **OpenWeather API** (Legacy weather data)
   - Get key: https://openweathermap.org/api
   - Add to .env: `OPENWEATHER_API_KEY=your_key`

3. **Google Places API** (Legacy attractions/hotels)
   - Get key: Google Cloud Console
   - Add to .env: `GOOGLE_PLACES_API_KEY=your_key`

4. **Exchange Rate API** (Legacy currency conversion)
   - Get key: https://exchangerate-api.com/
   - Add to .env: `EXCHANGERATE_API_KEY=your_key`

**Note**: The LangGraph system uses DuckDuckGo search (no API key needed) and works independently of legacy APIs.

## Example Usage

```
🌍 AI Travel Agent & Expense Planner
====================================

Enter destination: London
Start date: 2025-12-25
End date: 2025-12-30
Budget range: Mid-range
Currency: CAD
Group size: 2
Interests: museums, food, culture

→ Generates complete 5-day London itinerary with:
   • Weather forecasts
   • Museum and restaurant recommendations
   • Hotel options
   • Daily cost breakdowns
   • Currency-converted expenses
```
## Sample Report
```
================================================================================
LANGGRAPH MULTI-AGENT AI TRAVEL PLANNING REPORT
================================================================================
Generated: 2025-06-20 12:58:25
System: LangGraph Framework with Google Gemini & DuckDuckGo

TRIP OVERVIEW:
----------------------------------------
Destination: Delhi
Duration: 3 days
Group Size: 3 people
Budget Range: mid-range
Interests: 

SYSTEM PERFORMANCE:
----------------------------------------
Planning Method: LangGraph Multi-Agent Collaboration
Total Iterations: 7
Agents Involved: 5

AGENT CONTRIBUTIONS:
----------------------------------------

TRAVEL ADVISOR:
Status: completed
Timestamp: 2025-06-20T12:57:24.431678
Response: _agent: Okay, I can help you plan a 3-day trip to Delhi for 3 people, with a mid-range budget, sometime between July 21st and July 30th, 2025. Since you haven't specified any particular interests, I'll create a well-rounded itinerary covering historical sites, cultural experiences, and local flavors. Here's a possible plan:

**General Advice & Considerations:**

*   **Best Time to Visit:** While your travel dates are in July, keep in mind that Delhi experiences its monsoon season around that time. Expect high humidity and occasional heavy rainfall. Pack accordingly (light, quick-drying clothes, umbrella/raincoat).
*   **Transportation:** Delhi has a well-developed metro system which is efficient and cost-effective for getting around. Auto-rickshaws and taxis (Ola/Uber) are also readily available. Negotiate fares with auto-rickshaws beforehand.
*   **Accommodation:** I'll suggest areas with a range of mid-range hotel options.
*   **Food:** Delhi is a food lover's paradise! Be adventurous and try local street food, but ensure hygiene. Stick to reputable vendors and bottled water.
*   **Safety:** Be aware of your surroundings, especially in crowded areas. Keep valuables secure.

**Top Attractions and Must-See Places:**

*   **Historical Monuments:** Red Fort, Humayun's Tomb, Qutub Minar, India Gate
*   **Religious Sites:** Lotus Temple, Akshardham Temple, Jama Masjid
*   **Museums:** National Museum, National Rail Museum
*   **Gardens:** Lodhi Garden, Garden of Five Senses
*   **Markets:** Chandni Chowk, Dilli Haat, Khan Market

**Cultural Insights and Etiquette Tips:**

*   **Dress Code:** Dress modestly, especially when visiting religious sites. Shoulders and knees should be covered.
*   **Greetings:** "Namaste" is a respectful greeting.
*   **Photography:** Ask for permission before taking photos of people, especially women.
*   **Shoes:** Remove shoes before entering temples and mosques.
*   **Tipping:** Tipping is customary in restaurants and for services.
*   **Bargaining:** Bargaining is common in markets.

**Best Areas to Stay and Explore (Mid-Range Budget):**

*   **Connaught Place (CP):** Central location, good connectivity, lots of restaurants and shopping.
*   **Karol Bagh:** More budget-friendly than CP, bustling market area.
*   **South Delhi (Hauz Khas, Green Park):** Quieter, more residential, with trendy cafes and boutiques.
*   **Paharganj:** Very budget-friendly, close to the New Delhi Railway Station, but can be crowded and overwhelming.

**Possible 3-Day Itinerary:**

**Day 1: Old Delhi & Central Delhi**

*   **Morning:** Explore **Old Delhi**. Take a rickshaw ride through **Chandni Chowk**, visit **Jama Masjid** (one of India's largest mosques), and sample street food (parathe, jalebi).
*   **Afternoon:** Visit the **Red Fort**, a UNESCO World Heritage Site.
*   **Evening:** Stroll through **Connaught Place**, have dinner at a restaurant of your choice.

**Day 2: New Delhi & Historical Sites**

*   **Morning:** Visit **Humayun's Tomb**, a precursor to the Taj Mahal.
*   **Afternoon:** Explore **Qutub Minar**, another UNESCO World Heritage Site.
*   **Late Afternoon:** Drive past **India Gate** and **Presidential Palace**.
*   **Evening:** Visit **Dilli Haat** (an open-air crafts bazaar) for shopping and cultural performances. Have dinner there.

**Day 3: Temples & Gardens**

*   **Morning:** Visit **Lotus Temple**, a Baháʼí House of Worship known for its distinctive lotus-like shape.
*   **Afternoon:** Explore **Akshardham Temple**, a sprawling complex dedicated to Swaminarayan. (Note: Allow ample time for security checks).
*   **Evening:** Relax in **Lodhi Garden**, a historical garden with tombs and monuments. Have a farewell dinner at a restaurant in Hauz Khas Village.

**Activity Recommendations Based on Interests (Since None Were Specified):**

*   **Food Tour:** If you're foodies, consider a guided food tour of Delhi.
*   **Cooking Class:** Learn to cook authentic Indian dishes.
*   **Yoga/Meditation:** Find a yoga class or meditation session for relaxation.
*   **Shopping:** Explore different markets for souvenirs and handicrafts.
*   **Sufi Music:** Experience a Sufi music performance at Nizamuddin Dargah (Thursday evenings are particularly popular).

**Mid-Range Budget Considerations:**

*   **Accommodation:** Expect to pay around INR 3,000-6,000 per night for a decent mid-range hotel room for three people.
*   **Food:** Meals can range from INR 300-1,000 per person per meal, depending on the restaurant.
*   **Transportation:** Metro is very affordable. Budget around INR 500-1000 per day for taxis/auto-rickshaws, depending on usage.
*   **Entrance Fees:** Monument entrance fees can add up. Factor in around INR 1,000-2,000 per person for all the sites.

This is a flexible itinerary that can be adjusted to your preferences. Once you provide more specific interests, I can tailor the plan further. Let me know if you have any questions!


WEATHER ANALYST:
Status: completed
Timestamp: 2025-06-20T12:57:26.070786
Response: Okay, thanks for the detailed itinerary. To make it weather-intelligent and provide the best recommendations, I need to understand the expected weather conditions during your travel dates (July 21st - July 30th, 2025) in Delhi.

NEED_SEARCH: average weather conditions in Delhi between July 21 and July 30


BUDGET OPTIMIZER:
Status: completed
Timestamp: 2025-06-20T12:57:36.309040
Response: Okay, here's a budget optimization plan for a 3-day trip to Delhi for 3 people on a mid-range budget.

**Estimated Daily and Total Costs:**

*   **Estimated Daily Cost (per person):** ₹3,000 - ₹5,000 (This is a broad range, and we'll refine it below)
*   **Estimated Total Cost (for 3 people, 3 days):** ₹27,000 - ₹45,000

**Budget Breakdown by Category (for 3 people, 3 days - flexible based on your preferences):**

| Category      | Percentage | Estimated Cost (Lower End - ₹27,000) | Estimated Cost (Higher End - ₹45,000) | Notes                                                                                                                                                                                             |
|---------------|------------|--------------------------------------|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Accommodation | 30%        | ₹8,100                                 | ₹13,500                                  | Mid-range hotels or well-reviewed guesthouses/Airbnb. Aim for ₹900-₹1500 per room per night.                                                                                               |
| Food          | 30%        | ₹8,100                                 | ₹13,500                                  | Mix of street food, local restaurants, and a few nicer meals. Budget ₹900-₹1500 per person per day.                                                                                                |
| Activities    | 20%        | ₹5,400                                 | ₹9,000                                   | Entrance fees to monuments, guided tours, and other experiences. Prioritize must-see sites.                                                                                                |
| Transport     | 10%        | ₹2,700                                 | ₹4,500                                   | Metro, auto-rickshaws, and ride-sharing apps. The Delhi Metro is very efficient and affordable.                                                                                             |
| Miscellaneous | 10%        | ₹2,700                                 | ₹4,500                                   | Souvenirs, tips, unexpected expenses. Always good to have a buffer.                                                                                                                     |

**Money-Saving Tips and Strategies:**

*   **Accommodation:**
    *   **Travel during the shoulder season (spring or autumn):** You'll find better deals on accommodation and fewer crowds.
    *   **Consider guesthouses or homestays:** Often cheaper than hotels and offer a more authentic experience. Look for well-reviewed options on platforms like Booking.com or Airbnb. Negotiate the price if possible.
    *   **Book in advance:** Secure better rates, especially if traveling during peak season.
*   **Food:**
    *   **Eat like a local:** Street food and local restaurants are much cheaper than tourist-oriented establishments. Be mindful of hygiene; choose vendors with high turnover and visible cleanliness.
    *   **Lunch thalis:** A great value for money, offering a variety of dishes at a fixed price.
    *   **Carry a reusable water bottle:** Refill it whenever possible to avoid buying bottled water.
*   **Activities:**
    *   **Take advantage of free activities:** Many parks, gardens, and religious sites (like Bangla Sahib Gurudwara) are free to enter.
    *   **Consider a Delhi Tourism hop-on-hop-off bus:** A cost-effective way to see many of the major attractions.  Check reviews before booking.
    *   **Group discounts:** Inquire about group discounts at monuments and museums.
*   **Transport:**
    *   **Use the Delhi Metro extensively:** It's clean, efficient, and very affordable. Buy a tourist card for unlimited travel.
    *   **Negotiate auto-rickshaw fares:** Always agree on a price before getting in. Use ride-sharing apps like Uber or Ola for predictable pricing.
    *   **Avoid taxis for short distances:** They are generally more expensive than auto-rickshaws or ride-sharing.
*   **General:**
    *   **Bargain respectfully:** Bargaining is common in markets and with auto-rickshaw drivers. Be polite and respectful.
    *   **Travel in the off-season or shoulder season:** You'll find better deals on flights and accommodation.
    *   **Use credit cards with no foreign transaction fees:** This can save you money on exchange rates.
    *   **Alert your bank:** Inform your bank of your travel dates to avoid having your cards blocked.

**Cost-Effective Alternatives for Expensive Activities:**

*   **Instead of hiring a private car for sightseeing:** Use the Delhi Metro and auto-rickshaws.
*   **Instead of eating at fancy restaurants every night:** Explore street food markets and local dhabas.
*   **Instead of guided tours at every monument:** Read up on the history and significance of the sites beforehand and explore on your own. Consider hiring a local guide at one or two key sites.
*   **Instead of buying expensive souvenirs:** Look for unique, locally made crafts in markets like Dilli Haat (though entrance fee applies, the variety and authenticity are worth it).

To give you even more specific recommendations, I need a little more information:

*   **What are your "must-see" attractions in Delhi?**
*   **What kind of food are you interested in trying?**
*   **What is your preferred accommodation style (hotel, guesthouse, Airbnb)?**

Once I have this, I can refine the budget further and suggest specific places to visit and eat.


LOCAL EXPERT:
Status: completed
Timestamp: 2025-06-20T12:57:47.676662
Response: Great! Knowing your interests helps me tailor the recommendations. Here's a more specific plan for a 3-day trip to Delhi for 3 people, focusing on history, culture, and food, while optimizing for a mid-range budget:

**Refined Budget Breakdown (Based on Interests):**

Let's assume you're aiming for the lower end of the initial budget range (₹27,000 total for 3 people, 3 days). We can adjust the percentages slightly to prioritize activities related to history and culture.

| Category      | Percentage | Estimated Cost (₹27,000 Total) | Notes                                                                                                                                                     |
|---------------|------------|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Accommodation | 30%        | ₹8,100                        | Focus on well-reviewed guesthouses or budget-friendly hotels in central locations like Paharganj (budget) or Karol Bagh (mid-range).                     |
| Food          | 30%        | ₹8,100                        | Prioritize street food experiences and local restaurants.                                                                                                |
| Activities    | 25%        | ₹6,750                        | Allocate more for entrance fees to historical sites and potentially a guided tour or two.                                                               |
| Transport     | 10%        | ₹2,700                        | Metro and auto-rickshaws.                                                                                                                               |
| Miscellaneous | 5%         | ₹1,350                        | Buffer for unexpected expenses, small souvenirs.                                                                                                           |

**Detailed Itinerary and Recommendations:**

**Day 1: Old Delhi Immersion**

*   **Morning (Historical):**
    *   **Red Fort (Lal Qila):** Explore this UNESCO World Heritage Site. Allocate 2-3 hours. Entrance fee: ₹60 for Indians, ₹800 for foreigners.
    *   **Budget Tip:** Hire a government-approved guide at the entrance for a more enriching experience (negotiate the price beforehand).
*   **Lunch (Food):**
    *   **Karim's (near Jama Masjid):** Iconic Mughlai restaurant. Try their kebabs, biryani, and nahari. (₹500-₹800 for 3 people)
*   **Afternoon (Cultural/Spiritual):**
    *   **Jama Masjid:** One of India's largest mosques. Dress modestly (cover shoulders and knees). Entrance is free, but there's a small fee for photography.
    *   **Chandni Chowk:** Explore the bustling market. Sample street food like *parathe* (stuffed flatbreads) at Parathe Wali Gali, *jalebi* (sweet fried dough), and *lassi* (yogurt drink). Be mindful of hygiene.
*   **Evening (Cultural):**
    *   **Sound and Light Show at Red Fort (optional):** Check timings and book tickets in advance (₹600-₹800 for 3 people).
    *   **Dinner:** Continue exploring street food in Chandni Chowk or find a local restaurant in the area.

**Day 2: New Delhi Exploration**

*   **Morning (Historical):**
    *   **Humayun's Tomb:** A precursor to the Taj Mahal. Beautiful Mughal architecture. Entrance fee: ₹40 for Indians, ₹600 for foreigners.
    *   **Budget Tip:** Take the metro to JLN Stadium station and then an auto-rickshaw to the tomb (₹50-₹80).
*   **Lunch (Food):**
    *   **Khan Market:** Upscale market with a variety of restaurants. Explore options like *Big Yellow Door* (casual cafe) or *SodaBottleOpenerWala* (Parsi cuisine). (₹800-₹1200 for 3 people)
*   **Afternoon (Historical/Cultural):**
    *   **Qutub Minar:** Another UNESCO World Heritage Site. A towering minaret with intricate carvings. Entrance fee: ₹40 for Indians, ₹600 for foreigners.
    *   **Mehrauli Archaeological Park (adjacent to Qutub Minar):** Explore historical ruins and tombs (free entry).
*   **Evening (Spiritual/Cultural):**
    *   **Lotus Temple:** A Baháʼí House of Worship. Striking architectural design. Free entry.
    *   **Dinner:** Explore Hauz Khas Village for a variety of dining options (from budget to mid-range).

**Day 3: Museums and Markets**

*   **Morning (Cultural/Historical):**
    *   **National Museum:** Extensive collection of Indian art, artifacts, and historical exhibits. Entrance fee: ₹20 for Indians, ₹650 for foreigners.
    *   **Budget Tip:** Check for student discounts if applicable.
*   **Lunch (Food):**
    *   **Connaught Place (CP):** Central business district with numerous restaurants. Explore options for North Indian, South Indian, or international cuisine. (₹700-₹1000 for 3 people)
*   **Afternoon (Shopping/Cultural):**
    *   **Dilli Haat (INA):** A crafts village showcasing handicrafts and cuisine from different states of India. Entrance fee: ₹30.
    *   **Janpath Market (near CP):** Bargain for clothes, jewelry, and souvenirs.
*   **Evening (Relaxation/Departure):**
    *   **India Gate:** Visit this iconic war memorial. Enjoy a walk around the area.
    *   **Dinner:** Depending on your departure time, have a final meal at a restaurant near your hotel or the airport.

**Local Dining Recommendations (Beyond the Itinerary):**

*   **Street Food:**
    *   **Rajinder Da Dhaba (Safdarjung Enclave):** Famous for its non-vegetarian kebabs and curries (budget-friendly).
    *   **Dolma Aunty Momos (Lajpat Nagar):** Delicious and affordable momos (dumplings).
*   **Local Restaurants:**
    *   **Andhra Bhavan (near India Gate):** Authentic Andhra cuisine (South Indian) at very reasonable prices.
    *   **Bukhara (ITC Maurya):** High-end, but iconic for its Dal Bukhara and tandoori dishes (splurge).
    *   **Gulati (Pandara Road Market):** Popular for North Indian cuisine, especially butter chicken and dal makhani.

**Cultural Etiquette and Customs:**

*   **Dress Modestly:** Especially when visiting religious sites. Cover shoulders and knees.
*   **Remove Shoes:** Before entering temples, mosques, and some homes.
*   **Use Your Right Hand:** For eating and giving/receiving things.
*   **Bargain Respectfully:** It's expected in markets, but do so politely.
*   **Avoid Public Displays of Affection:** While attitudes are changing, it's still generally considered inappropriate.
*   **Be Mindful of Personal Space:** Crowded areas are common.
*   **Learn a Few Basic Hindi Phrases:** "Namaste" (hello), "Shukriya" (thank you), "Kitna hai?" (how much?).

**Insider Tips:**

*   **Stay Hydrated:** Delhi can get very hot and humid, especially in the summer.
*   **Be Aware of Scams:** Be cautious of touts and unsolicited offers.
*   **Download Ride-Sharing Apps:** Uber and Ola are widely used and convenient.
*   **Use Google Maps:** For navigation and public transport directions.
*   **Carry Small Denomination Bills:** For auto-rickshaws and street vendors.
*   **Beware of Pickpockets:** Be vigilant in crowded areas.
*   **Learn to Say "No" Firmly:** To avoid being pressured into buying things you don't want.
*   **Check the Weather Forecast:** Plan your activities accordingly.
*   **Be Prepared for Traffic:** Delhi traffic can be chaotic.

This itinerary is a suggestion, feel free to customize it based on your preferences and energy levels. Enjoy your trip to Delhi!


ITINERARY PLANNER:
Status: completed
Timestamp: 2025-06-20T12:57:55.320014
Response: This is an excellent refined itinerary, incorporating budget considerations, specific restaurant recommendations, cultural tips, and practical advice. Here are a few minor suggestions to further enhance its usefulness:

**1.  Transportation Specifics & Optimization:**

*   **Day 1:**
    *   "Take the metro to Chawri Bazaar station" before heading to Jama Masjid and Chandni Chowk. This is the most efficient way to reach that area.  Specify that auto-rickshaws are readily available from the metro station if they prefer not to walk.
    *   Add: "Consider taking a cycle rickshaw tour of Chandni Chowk for a unique experience (negotiate the price beforehand)." This provides a specific alternative activity within the area.
*   **Day 2:**
    *   Specify which metro station is closest to Khan Market (Khan Market station).
    *   Add a note about the distance between Qutub Minar and Mehrauli Archaeological Park (walking distance vs. auto-rickshaw).
*   **Day 3:**
    *   Specify the metro station for Dilli Haat (INA station).
    *   Mention that Janpath Market is walking distance from Connaught Place.

**2.  Timing Considerations:**

*   **General:** Emphasize the importance of starting early, especially during peak season or hot weather, to avoid crowds and heat exhaustion.  Suggest starting activities around 9:00 AM each day.
*   **Red Fort (Day 1):** Suggest arriving right at opening time (usually 9:30 AM) to avoid the biggest crowds.
*   **Lotus Temple (Day 2):**  Mention that there can be long queues, especially on weekends.  Suggest visiting during off-peak hours (e.g., late afternoon).

**3.  Alternative Activities (Contingency Planning):**

*   Have a backup plan for each day in case of unexpected closures (e.g., strikes, holidays). Examples:
    *   **Day 1 (Alternative):** If Red Fort is unexpectedly closed, visit the National Gandhi Museum near Raj Ghat.
    *   **Day 2 (Alternative):** If Humayun's Tomb is too crowded, visit Safdarjung's Tomb, another Mughal-era tomb with similar architecture but fewer visitors.
    *   **Day 3 (Alternative):** If Dilli Haat is not appealing, consider visiting the State Emporia Complex on Baba Kharak Singh Marg for fixed-price handicrafts.

**4.  Food Considerations:**

*   **Dietary Restrictions:**  Include a brief sentence about how Delhi caters to various dietary restrictions (vegetarian, vegan, gluten-free) and how to communicate those needs to restaurants.
*   **Water:** Reinforce the importance of drinking bottled water or filtered water only.

**5.  Safety and Health:**

*   **Mosquito Repellent:**  Recommend using mosquito repellent, especially in the evenings.
*   **Air Pollution:**  Briefly mention the air quality in Delhi and suggest checking the Air Quality Index (AQI) and taking precautions if necessary (e.g., wearing a mask on particularly bad days).

**Revised Snippets Incorporating Suggestions:**

*   **Day 1: Old Delhi Immersion**
    *   **Morning:** "...Take the metro to *Chawri Bazaar* station. From the station, auto-rickshaws are readily available if you prefer not to walk to Jama Masjid and Chandni Chowk. Consider taking a cycle rickshaw tour of Chandni Chowk for a unique experience (negotiate the price beforehand)."

*   **Day 2: New Delhi Exploration**
    *   **Morning:** "...Take the metro to *JLN Stadium* station and then an auto-rickshaw to the tomb (₹50-₹80)."
    *   **Lunch:** "...Khan Market (metro station: *Khan Market*)."
    *   **Afternoon:** "...Mehrauli Archaeological Park (adjacent to Qutub Minar): Explore historical ruins and tombs (free entry). The park is within walking distance of Qutub Minar, or a short auto-rickshaw ride."
    *   **Alternative:** If Humayun's Tomb is too crowded, visit Safdarjung's Tomb, another Mughal-era tomb with similar architecture but fewer visitors.

*   **Day 3: Museums and Markets**
    *   **Afternoon:** "...Dilli Haat (INA) (metro station: *INA*)...Janpath Market (near CP): Bargain for clothes, jewelry, and souvenirs. Janpath Market is within walking distance from Connaught Place."

*   **General Timing:** "To avoid the biggest crowds and the heat, aim to start your sightseeing around 9:00 AM each day."

*   **Food Considerations:** "Delhi caters well to various dietary restrictions (vegetarian, vegan, gluten-free). Don't hesitate to communicate your needs to restaurant staff. Always drink bottled or filtered water."

*   **Safety and Health:** "Remember to use mosquito repellent, especially in the evenings. Check the Air Quality Index (AQI) daily and consider wearing a mask on days with high pollution levels."

By incorporating these minor adjustments, you'll make the itinerary even more practical, informative, and user-friendly.  Great work!

================================================================================
End of LangGraph Multi-Agent Travel Planning Report
================================================================================
```

## 🏗️ Architecture

### Project Structure
```
📁 ai_travel_agent/
├── main.py                    # Multi-system entry point
├── langgraph_main.py         # LangGraph system entry
├── test_langgraph_system.py  # Comprehensive testing
├── agents/                   # Agent implementations
│   ├── langgraph_agents.py   # LangGraph agent system
│   ├── multi_agent_orchestrator.py # Legacy multi-agent
│   └── travel_agents.py      # Individual agent classes
├── config/                   # Configuration management
│   ├── langgraph_config.py   # LangGraph configuration
│   ├── api_config.py         # Legacy API settings
│   └── app_config.py         # Application settings
├── tools/                    # LangGraph tools
│   └── travel_tools.py       # 7 DuckDuckGo search tools
├── data/                     # Data models
│   └── models.py             # Data classes
├── modules/                  # Legacy business logic
│   ├── user_input.py         # Input handling & validation
│   ├── weather_service.py    # Weather data integration
│   ├── attraction_finder.py  # Attraction discovery
│   ├── hotel_estimator.py    # Accommodation estimation
│   ├── currency_converter.py # Currency conversion
│   ├── expense_calculator.py # Cost calculations
│   ├── itinerary_planner.py  # Day-by-day planning
│   └── trip_summary.py       # Report generation
└── utils/                    # Utility functions
    └── helpers.py            # Common helper functions
```

### System Comparison

| Feature | Single-Agent | Legacy Multi-Agent | LangGraph System |
|---------|-------------|-------------------|------------------|
| **Framework** | Custom | Custom | LangGraph + LangChain |
| **LLM** | Mock/Static | Mock/Static | Google Gemini Flash-2.0 |
| **Search** | Static Data | Static Data | DuckDuckGo Real-time |
| **State Management** | None | Basic | Advanced (StateGraph) |
| **Tool Integration** | Limited | Limited | Full Tool Ecosystem |
| **Collaboration** | None | Basic | Advanced Workflows |
| **Scalability** | Low | Medium | High |
| **Maintainability** | Low | Medium | High |

## Dependencies

### Required Packages
```
requests>=2.31.0    # HTTP requests for API calls
python-dotenv>=1.0.0 # Environment variable management
```

### External APIs (Optional)
- OpenWeather API: Weather forecasts
- Google Places API: Attractions and hotels
- Exchange Rate API: Currency conversion

## 🧪 Testing

### Run Tests
```bash
# LangGraph system validation (no API key needed)
python test_langgraph_system.py

# Legacy system tests
python -m pytest tests/ (if tests directory exists)
```

### System Validation
The `test_langgraph_system.py` script validates:
- All LangGraph components
- Tool integrations
- Configuration management
- Import compatibility
- System readiness

## 🚨 Troubleshooting

### Common Issues

1. **API Quota Exceeded**
   ```
   Error: 429 You exceeded your current quota
   Solution: Wait for quota reset or upgrade API plan
   ```

2. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration Issues**
   ```bash
   python test_langgraph_system.py
   ```

4. **Missing API Key**
   ```
   Error: GEMINI_API_KEY not found
   Solution: Add your API key to .env file
   ```

### Debug Mode
```bash
export DEBUG=true
python langgraph_main.py
```

## Features in Detail

### 🌤️ Weather Integration
- 5-day weather forecasts
- Temperature, conditions, humidity
- Weather-based activity recommendations
- Packing suggestions

### 🏛️ Attraction Discovery
- Museums and cultural sites
- Restaurants by cuisine type
- Activities based on interests
- Rating and cost information

### 🏨 Accommodation
- Budget-appropriate hotel recommendations
- Price per night calculations
- Amenity listings
- Group accommodation options

### 💱 Currency Support
- Real-time exchange rates
- 10+ international currencies
- Automatic cost conversion
- Rate caching for performance

### 📅 Itinerary Planning
- Day-by-day schedules
- Weather-optimized activity ordering
- Transportation suggestions
- Timing recommendations

### 📊 Expense Management
- Detailed cost breakdowns
- Budget vs actual tracking
- Group cost calculations
- Cost-saving recommendations

## Contributing

### Code Structure
- Follow object-oriented design principles
- Maintain modular architecture
- Include comprehensive error handling
- Add unit tests for new features

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run validation
python validate.py

# Test specific modules
python -m pytest tests/test_attraction.py
```

## License

This project is for educational purposes as part of the AI Agents assignment.

## Support

For issues or questions:
1. Check the validation script: `python validate.py`
2. Review error messages and logs
3. Verify API key configuration (if using external APIs)

---

