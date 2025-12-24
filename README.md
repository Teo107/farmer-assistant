# CO2 Angels Farmer Assistant
This project implements a functional farmer-assistant chatbot using a simulated WhatsApp-style web interface.  
Farmers can link their identity, view parcels, request parcel details, receive health summaries, and configure periodic reports.

## Tech Stack

| Layer | Technology |
|------|------------|
| Backend | FastAPI (Python) |
| Frontend | HTML + CSS + JavaScript |
| Data Storage | JSON files (mock database) |
| Runtime State | In-memory Python dictionaries |
| AI (optional) | Gemini AI |
| CORS | FastAPI Middleware |

---

## 
#### Clone repo
[[git clone https://github.com/Teo107/farmer-assistant-chatbot.git](https://github.com/Teo107/farmer-assistant)  ](https://github.com/Teo107/farmer-assistant)  
```cd farmer-assistant-chatbot```

Create virtual environment  
```
python -m venv venv
```
activate venv Mac / Linux  
```
source venv/bin/activate
```
activate venv Windows  
```
venv\Scripts\activate
```

#### Install dependencies
```
pip install -r requirements.txt
```

#### (optional) Enable AI mode
create .env in root and add:
```GEMINI_API_KEY=your_key_here```  
then in` message_router.py` set: `USE_AI = True`


#### Start backend
```
uvicorn app.main:app --reload
```
Backend runs at: `http://127.0.0.1:8000`


#### Start frontend
open file: frontend/index.html  
in browser (right-click -> `Open in Browser`)

---


#### API Testing (without UI)

Swagger Docs:
`http://127.0.0.1:8000/docs`

POST /message  
Sends a chat message to backend.

GET /debug/state  
Returns linked phones + report frequency state.  
you can go to `http://127.0.0.1:8000/debug/state`

POST /generate-reports  
Simulates scheduled notifications.

---

## Architecture Summary

#### Frontend:
- WhatsApp-style UI (HTML + CSS + JS)
- Sends messages to backend via REST
- Renders chatbot replies in chat format

#### Backend (FastAPI):
- /message -> main chatbot endpoint
- /generate-reports -> simulate scheduled reports
- /debug/state -> inspect runtime state
- Handles account linking, parcel queries, summaries, report setup

#### Data Layer:
- JSON -> farmers, parcels, monitoring data
- In-memory store -> phone linking + report frequency

#### AI (optional):
- Gemini intent detection and reply generation
- Can be disabled to use rule-based only

---
  
## Future Extensions

#### WhatsApp Real Integration
Currently, the chatbot runs in a **browser-based WhatsApp-style UI**, only simulating how a farmer would chat.  
A future production version would integrate with the **Meta WhatsApp Cloud API**, so the system can:
- Receive real WhatsApp messages from farmers  
- Send replies directly to their WhatsApp conversations  
- Use real phone-number verification and farmer onboarding  
- Become a real conversational support system, not just a simulation  


#### Persistent Storage
Right now, the project intentionally keeps things lightweight:
- JSON files store static farmer and parcel data  
- In-memory Python dictionaries store runtime state  
  (linked phone numbers, report frequency, last sent reports)

This is good for a prototype but resets when the backend restarts.

A production-ready version would move to:
- **PostgreSQL** (or another SQL DB) for farmers, parcels, soil data, monitoring history  


#### ✔️ Real Scheduling
Right now, periodic report sending is triggered manually by calling an endpoint.  
In a real deployment, reports should be sent automatically (daily / weekly / monthly) using:
- **APScheduler**
- or system cron scheduling

This would transform reporting into a fully automated notification system.

---

#### ✔️ Smarter AI Assistant
AI support is implemented but intentionally simple.  
Currently:
- Gemini detects user intent  
- Generates friendly natural-language replies  
- It works, but can sometimes misunderstand unstructured or vague messages

Planned improvements:
- Better structured prompting
- Safer fallback to rule-based logic when AI is uncertain
- Conversational context memory
- More agronomic intelligence (alerts, recommendations, warnings)

This would make the assistant more natural, reliable, and genuinely helpful in real-world farming.


