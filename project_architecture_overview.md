# PromptIO Platform Architecture Overview

This document provides a complete mindmap of the PromptIO codebase structure, services, and modules, followed by an end-to-end execution flowchart illustrating the core prompt optimization lifecycle. Both diagrams are constructed using standard ASCII characters (`+`, `-`, `|`) as requested.

---

## 1. Codebase Structure Mindmap

The mindmap outlines the architecture of the enterprise application, separating the full stack into Web Frontend, Backend API, Background Workers, and Infrastructure layers.

```
+-------------------------------------------------------------------------------------------------+
|                                            PROMPTIO                                             |
|                             Intelligent Prompt Optimizer Platform                               |
+-------------------------------------------------------------------------------------------------+
  |
  +-- WEB FRONTEND (Next.js App Router, React, Tailwind CSS, shadcn/ui)
  |     |
  |     +-- App Routing & Layout (/web/app)
  |     |     +-- /auth              (Authentication flows: login, register)
  |     |     +-- /(dashboard)       (Authenticated user application layouts)
  |     |           +-- /dashboard       (System metrics, real-time activity feeds, usage summaries)
  |     |           +-- /prompt-studio   (Split-screen Workspace: rough inputs to framework-optimized outputs)
  |     |           +-- /evaluations     (Prompt quality analysis rubrics & multi-model comparison tables)
  |     |           +-- /templates       (Preset organization, version history, and stored templates)
  |     |           +-- /teams           (Role-based access control [RBAC] & organizational sharing)
  |     |
  |     +-- Frontend Components (/web/components)
  |     |     +-- /prompt-studio     (prompt-editor.tsx split views, framework meta menus, dynamic outputs)
  |     |     +-- /dashboard         (Quick actions, usage charts, statistics summaries)
  |     |     +-- /analytics         (Cost monitoring trackers, latency metrics matrices)
  |     |     +-- /layout & /ui      (Sidebar navigation, global header, base responsive primitives)
  |     |
  |     +-- Client State Stores (/web/store)
  |     |     +-- prompt-store.ts    (Zustand slice for workspace input buffers, active frameworks, analytics)
  |     |     +-- auth-store.ts      (Session validation tokens, user identity metadata, team mapping)
  |     |     +-- ui-store.ts        (Interface controls, theme toggles, collapse states)
  |     |
  |     +-- Integration Hooks (/web/hooks)
  |           +-- use-prompt.ts      (API gateway bridge, event-stream payload parsers, save handlers)
  |           +-- use-auth.ts        (JWT persistence handlers and route guards)
  |           +-- use-analytics.ts   (Consumption aggregation helpers)
  |
  +-- BACKEND API Engine (FastAPI Enterprise Subsystem)
  |     |
  |     +-- API Routers (/backend/apps/api/routers)
  |     |     +-- /optimize          (Core ingestion engine, Server-Sent Events [SSE] streaming handlers)
  |     |     +-- /prompts           (Prompt persistence schemas, version histories CRUD)
  |     |     +-- /evaluate          (Multi-dimensional quality scoring matrices dispatcher)
  |     |     +-- /compare           (Side-by-side framework model generation contest comparisons)
  |     |     +-- /analytics & /admin(Quota allocations, performance tracking, organization monitoring)
  |     |     +-- /audit             (GDPR-compliant security logging audit ledger)
  |     |
  |     +-- Services Layer (/backend/apps/api/services)
  |     |     +-- optimization_service.py (Multi-stage orchestration: safety -> classification -> routing -> validation)
  |     |     +-- ai_router_service.py    (Multi-model failover client: OpenRouter primary cloud / local Ollama mesh)
  |     |     +-- evaluation_service.py   (Scoring computation algorithms provider)
  |     |     +-- prompt_service.py       (Persistence layers interface)
  |     |     +-- auth_service.py         (Authorization middleware delegator)
  |     |
  |     +-- 13 Modular Optimization Frameworks (/backend/apps/api/frameworks)
  |     |     +-- Standard             (General purpose clear prompt outputs)
  |     |     +-- Reasoning            (Step-by-step logic expansion)
  |     |     +-- RACE                 (Role, Action, Context, Explanation)
  |     |     +-- CARE                 (Context, Action, Result, Example)
  |     |     +-- APE                  (Action, Purpose, Execution)
  |     |     +-- CREATE               (Character, Request, Examples, Adjustments, Type, Extras)
  |     |     +-- TAG                  (Task, Action, Goal)
  |     |     +-- CREO                 (Context, Request, Explanation, Outcome)
  |     |     +-- RISE                 (Role, Input, Steps, Execution)
  |     |     +-- PAIN                 (Problem, Action, Information, Next Steps)
  |     |     +-- COAST                (Context, Objective, Actions, Scenario, Task)
  |     |     +-- ROSES                (Role, Objective, Scenario, Expected Solution, Steps)
  |     |     +-- RESEE                (Role, Elaboration, Scenario, Elaboration, Examples)
  |     |
  |     +-- Dedicated Core Engines (/backend/apps/api/engines)
  |     |     +-- safety_engine.py        (PII regex scrubbing & policy compliance violation flagging)
  |     |     +-- intent_classifier.py    (Domain mapping & framework matching recommendation models)
  |     |     +-- evaluation_engine.py    (Clarity, specificity rubrics & final metrics assembly)
  |     |
  |     +-- Middleware Stack (/backend/apps/api/middleware)
  |     |     +-- Rate Limiting, Cross-Origin Resource Sharing [CORS], Structured Loggers, GZip Compressors
  |     |
  |     +-- Data Models & Schemas (/backend/apps/api/models & schemas)
  |           +-- Pydantic request/response layers mapping to underlying SQLAlchemy asynchronous mapped tables
  |
  +-- BACKGROUND WORKERS (Asynchronous Celery Subsystem)
  |     |
  |     +-- celery_app.py            (Broker config initialization)
  |     +-- ai_worker.py             (Offline long-tail high-token jobs queue processing)
  |     +-- evaluation_worker.py     (Deferred execution matrices evaluation worker)
  |     +-- compliance_worker.py     (Periodic automated background policy compliance re-audits)
  |
  +-- INFRASTRUCTURE & PERSISTENCE
        |
        +-- Container & Proxy Layers (/backend/infra)
        |     +-- Dockerfile.api & docker-compose.yml (Declarative microservice orchestration)
        |     +-- nginx.conf                          (High-throughput load balancing ingress proxy)
        |
        +-- Database Layers
              +-- PostgreSQL Engine via Asyncpg driver (Transactional records, audit histories, version trees)
```

---

## 2. Core Optimization Lifecycle Flowchart

This flowchart visualizes the pipeline executed when a user enters a rough prompt in the workspace and clicks "Optimize Prompt". The backend routes the data through validation engines, constructs customized payloads based on the chosen framework, dispatches to AI endpoints with automatic local failovers, and returns actionable metrics back to the interface.

```
+-------------------------------------------------------------------------------------------------+
|                            USER INPUT: Rough Prompt in Web Studio                               |
+-------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+-------------------------------------------------------------------------------------------------+
|                       Frontend Client invokes REST call: POST /optimize                         |
+-------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+-------------------------------------------------------------------------------------------------+
|                   FastAPI Router Entrypoint delegates to OptimizationService                    |
+-------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+-------------------------------------------------------------------------------------------------+
|                Stage 1: Safety Engine Pre-flight Analysis (Check PII & Policy)                  |
+-------------------------------------------------------------------------------------------------+
                                                 |
                       +-------------------------+-------------------------+
                       | (Unsafe Content)                                  | (Safe Content)
                       v                                                   v
+----------------------------------------------+     +--------------------------------------------+
| Abort Workflow: Return HTTP 400 Bad Request  |     | Stage 2: Optional Intent Classification    |
| containing specific compliance flag alerts   |     | (Auto-detect framework if user requested)  |
+----------------------------------------------+     +--------------------------------------------+
                                                                           |
                                                                           v
                                                     +--------------------------------------------+
                                                     | Stage 3: Inject Specific Framework Engine  |
                                                     | (e.g. RACE, CREATE, COAST, RESEE, Standard)|
                                                     +--------------------------------------------+
                                                                           |
                                                                           v
                                                     +--------------------------------------------+
                                                     | Stage 4: AI Router Dispatch Orchestration  |
                                                     | Determines target execution platform       |
                                                     +--------------------------------------------+
                                                                           |
                         +-------------------------------------------------+-------------------------------------------------+
                         | (Cloud Mode Selected)                                                                             | (Local/Offline Mode Selected)
                         v                                                                                                   v
+-----------------------------------------------------------------+                                 +-----------------------------------------------------------------+
| Dispatch HTTP POST request to OpenRouter API Endpoint           |                                 | Dispatch HTTP POST request to Local Ollama Server               |
| Request JSON object structure, tracking input/completion tokens |                                 | Target local execution port (http://localhost:11434/api/chat)   |
+-----------------------------------------------------------------+                                 +-----------------------------------------------------------------+
                         |                                                                                                   |
                         +-------------------------------------------------+-------------------------------------------------+
                                                                           |
                                                                           v
                                                     +--------------------------------------------+
                                                     | Stage 5: Structured Payload Parsing        |
                                                     | Strip markdown blocks, validate JSON model |
                                                     +--------------------------------------------+
                                                                           |
                                                                           v
                                                     +--------------------------------------------+
                                                     | Stage 6: Output Safety & Quality Analysis  |
                                                     | Evaluate Clarity, Specificity, Complexity  |
                                                     +--------------------------------------------+
                                                                           |
                                                                           v
                                                     +--------------------------------------------+
                                                     | Stage 7: Persistence & Audit Tracking      |
                                                     | Store version tree, log telemetry costs    |
                                                     +--------------------------------------------+
                                                                           |
                                                                           v
                                                     +--------------------------------------------+
                                                     |      Frontend Receives JSON Payload        |
                                                     | Renders dynamic preview & quality metrics  |
                                                     +--------------------------------------------+
```
