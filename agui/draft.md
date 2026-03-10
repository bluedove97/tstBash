
# AG-UI 세미나

## Microsoft Agent Framework + AG‑UI
Agent‑User Interaction Protocol 소개

---

# 1. 세미나 목표

AI Agent를 실제 애플리케이션과 연결하는 방법
- AG‑UI 개념 이해
- Microsoft Agent Framework와의 관계 이해
- Tool / UI / Human-in-the-loop 구조 이해
- 실제 데모를 통해 AG‑UI 동작 확인

---

# 2. AI Agent 애플리케이션의 문제

기존 LLM 애플리케이션 구조
```
User
 ↓
Frontend (React / Web)
 ↓
Backend API
 ↓
LLM
```

문제점
- UI와 Agent 연결 표준이 없음
- Streaming 구현을 직접 해야 함
- Tool 실행 상태 표시 어려움
- Human approval workflow 구현 필요

---

# 3. AI Agent 발전 단계
AI 애플리케이션 발전
1. Chatbot
2. Tool‑using LLM
3. AI Agent
4. Agent Ecosystem

하지만 문제
> Agent가 똑똑해졌지만 UI 연결은 여전히 어렵다

---

# 4. AG‑UI란 무엇인가

Agent‑User Interaction Protocol

- Agent와 UI 사이의 표준 인터페이스
- Event 기반 통신
- Streaming 지원
- Interactive UI 지원

AG-UI목적

> Agent와 사용자 인터페이스를 연결하는 표준 프로토콜 제공

---

# 5. Agent Protocol Stack
```
User  
↑  
AG‑UI  
↑  
Agent  
↑  
MCP / Tools
```

각 Protocol 역할
| Protocol | 역할            |
| -------- | ------------- |
| AG-UI    | Agent ↔ User  |
| MCP      | Agent ↔ Tools |
| A2A      | Agent ↔ Agent |

AG-UI는 Agent 시스템의 Last Mile 역할을 한다.

---

# 6. Microsoft Agent Framework + AG‑UI

| 구성              | 역할             |
| --------------- | -------------- |
| Agent Framework | Agent Logic    |
| AG-UI           | UI Interaction |


구조

```
Frontend
   ↑
 AG-UI Protocol
   ↑
Agent Framework
   ↑
LLM + Tools
```

---

# 7. AG‑UI 주요 기능

AG-UI가 제공하는 기능
- Real-time streaming
- Tool execution 표시
- Generative UI
- Human-in-the-loop
- 상태 관리

---

# 8. AG‑UI Architecture

전체 구조
```
Frontend App
   │
   │ AG-UI Protocol
   │
AG-UI Server
   │
Agent Framework
   │
LLM + Tools
```

구성 요소
- AG-UI Server
- Agent Endpoint
- Event Streaming
- Tool Execution

---

# 9. Event 기반 구조

AG‑UI는 
> request/response가 아니라 event stream 기반

주요 이벤트
```
TEXT_MESSAGE_CONTENT
TOOL_CALL_START
TOOL_CALL_DELTA
TOOL_CALL_RESULT
STATE_UPDATE
```
Agent 실행 과정이 UI에 실시간 전달된다
---

# 10. Python AG‑UI 설치

```bash
pip install agent-framework-ag-ui --pre
```

Python 환경에서 AG‑UI integration 사용 가능

---

# 11.AG‑UI Server 개념
AG-UI Server 역할
- Agent를 HTTP endpoint로 노출
- 클라이언트는 streaming으로 결과 수신
- Web UI와 Agent를 연결

구조
```
Agent → HTTP Endpoint → UI
```
---

# 12. Demo 1 – Basic Chat

시연 목표
 - AG-UI 기본 채팅 동작 확인

시연 내용
- Python Agent 실행
- AG-UI Server 실행
- Web Client 접속
- Streaming 응답 확인

---

# 13. Backend Tool Rendering

Agent는 Tool을 실행할 수 있음

예

- Weather API
- Database Query
- Internal API

구조
```
Agent
 ↓
Tool call
 ↓
Result streaming
```
---

# 14. Tool Event 흐름
Tool 실행 과정
```
User Question
 ↓
Agent Reasoning
 ↓
Tool Call
 ↓
Tool Result
 ↓
Streaming Response
```

UI는 Tool 실행 상태를 표시할 수 있다.
```
Searching database...
Fetching weather...
```
---

# 15.Demo 2 – Tool 호출

예시 질문
```
서울 날씨 알려줘
```

동작
```
Agent → Weather Tool 호출
UI → Tool 실행 상태 표시
UI → 결과 표시
```
---

# 16.Frontend Tools
Frontend Tool이란
> Agent가 UI 기능을 호출하는 것

예
- Chart
- Table
- Modal
- Form
- Map

Agent → UI Component 생성
---

# 17.Generative UI

Agent가 UI를 생성하여 Frontend에 전달

예
```
- Stock chart
- Product card
- Data table
```
UI Payload 예시
```json
{
  "type": "chart",
  "data": {}
}
```
Frontend가 rendering 수행
---

# 18.Demo 3 – Generative UI

예시 질문
```
TSLA stock price
```
동작
```
Agent → chart UI 생성  
Frontend → chart rendering
```

---

# 19. Human‑in‑the‑loop

위험한 작업에는 사용자 승인 필요

예

- 이메일 발송
- 코드 실행
- DB 변경

따라서 필요한 기능
> Human Approval
---

# 20. Approval Workflow
Approval 흐름
```
Agent action request  
↓  
User approval  
↓  
Action 실행
```

AG-UI는 이 workflow를 기본 지원한다.

---

# 21.Demo 4 – Human Approval

Agent
```
Send email to customer
```
UI
```
Approve / Reject 버튼
```

사용자 승인 후 작업 실행
---

# 22.AG‑UI 장점
AG-UI 사용 시 장점
- UI integration 표준화
- Streaming 기본 지원
- Tool 상태 표시
- Human-in-the-loop 지원
- Generative UI

---

# 23. 기존방식 vs AG-UI
| 항목             | 기존 방식  | AG-UI    |
| -------------- | ------ | -------- |
| Streaming      | 직접 구현  | 기본 지원    |
| Tool 상태        | 직접 구현  | 이벤트      |
| Approval       | 직접 구현  | 기본 지원    |
| UI Integration | Custom | Protocol |


# 24.정리

- Agent Framework → Agent 로직
- AG‑UI → 사용자 인터페이스
- Event 기반 Agent UI 구조
- Tool + UI + Human workflow 통합


