
# AG-UI 세미나

## Microsoft Agent Framework + AG‑UI
Agent‑User Interaction Protocol 소개

---

# 세미나 목표

- AG‑UI 개념 이해
- Microsoft Agent Framework와의 관계 이해
- Tool / UI / Human-in-the-loop 구조 이해
- 실제 데모를 통해 AG‑UI 동작 확인

---

# AI Agent 애플리케이션의 문제

- UI와 Agent 연결 표준이 없음
- Streaming 구현을 직접 해야 함
- Tool 실행 상태 표시 어려움
- Human approval workflow 구현 필요

---

# AI Agent 발전 단계

1. Chatbot
2. Tool‑using LLM
3. AI Agent
4. Agent Ecosystem

→ Agent가 똑똑해졌지만 UI 연결은 여전히 어렵다

---

# AG‑UI란 무엇인가

Agent‑User Interaction Protocol

- Agent와 UI 사이의 표준 인터페이스
- Event 기반 통신
- Streaming 지원
- Interactive UI 지원

---

# Agent Protocol Stack

User  
↑  
AG‑UI  
↑  
Agent  
↑  
MCP / Tools

---

# Microsoft Agent Framework + AG‑UI

- Agent Framework → Agent logic
- AG‑UI → User interaction

구조

Frontend ↔ AG‑UI ↔ Agent Framework ↔ LLM

---

# AG‑UI 주요 기능

- Real-time streaming
- Tool execution 표시
- Generative UI
- Human-in-the-loop
- 상태 관리

---

# AG‑UI Architecture

Frontend  
↓  
AG‑UI Protocol  
↓  
AG‑UI Server  
↓  
Agent Framework  
↓  
LLM + Tools

---

# Event 기반 구조

AG‑UI는 request/response가 아니라 event stream 기반

주요 이벤트

- TEXT_MESSAGE_CONTENT
- TOOL_CALL_START
- TOOL_CALL_RESULT
- STATE_UPDATE

---

# Python AG‑UI 설치

```bash
pip install agent-framework-ag-ui --pre
```

Python 환경에서 AG‑UI integration 사용 가능

---

# AG‑UI Server 개념

- Agent를 HTTP endpoint로 노출
- 클라이언트는 streaming으로 결과 수신
- Web UI와 Agent를 연결

---

# Demo 1 – Basic Chat

시연 내용

- AG‑UI Agent 실행
- Web client 연결
- Streaming 응답 확인

---

# Backend Tool Rendering

Agent는 Tool을 실행할 수 있음

예

- Weather API
- Database Query
- Internal API

---

# Tool Event 흐름

User 질문  
↓  
Agent reasoning  
↓  
Tool call  
↓  
Tool result  
↓  
User에게 streaming

---

# Demo 2 – Tool 호출

예시 질문

서울 날씨 알려줘

Agent → Weather Tool 호출  
UI → Tool 실행 상태 표시

---

# Frontend Tools

Agent가 UI 컴포넌트를 생성

예

- Chart
- Table
- Modal
- Form

---

# Generative UI

Agent가 UI를 생성하여 Frontend에 전달

예

- Stock chart
- Product card
- Data table

---

# Demo 3 – Generative UI

예시

TSLA stock price

Agent → chart UI 생성  
Frontend → chart rendering

---

# Human‑in‑the‑loop

위험한 작업에는 사용자 승인 필요

예

- 이메일 발송
- 코드 실행
- DB 변경

---

# Approval Workflow

Agent action request  
↓  
User approval  
↓  
Action 실행

---

# Demo 4 – Human Approval

Agent

Send email to customer

UI

Approve / Reject 버튼

---

# AG‑UI 장점

- UI integration 표준화
- Streaming 기본 지원
- Tool 상태 표시
- Human-in-the-loop 지원
- Generative UI

---

# 정리

- Agent Framework → Agent 로직
- AG‑UI → 사용자 인터페이스
- Event 기반 Agent UI 구조
- Tool + UI + Human workflow 통합

---

# Q&A

질문 있으신가요?
