# ONGISA

> **AI-powered codebase intelligence for understanding, analyzing, and improving software architecture.**

ONGISA is a developer tool designed to give developers a clear view of how a software project is built.

It analyzes a codebase, maps its files, modules, imports, and dependencies, detects architectural problems, visualizes the structure as a dependency graph, and uses AI to help developers understand and improve the system.

Large codebases can become difficult to understand as the number of files, modules, and dependencies grows. Instead of manually searching through files and tracing connections, ONGISA builds an architectural picture of the project and helps developers answer questions such as:

* What does this file depend on?
* What depends on this module?
* Which modules are highly connected?
* Are there circular dependencies?
* Which parts of the codebase are becoming too large or complex?
* Where are the architectural smells?
* What could be refactored?
* What parts of the system could be affected by a change?

> **The goal: give developers an X-ray of their codebase — from structure and dependencies to architectural problems and possible improvements.**


---

# ✨ What ONGISA Does

ONGISA combines several capabilities into one developer platform:

* 🔎 Static code analysis
* 📁 Repository structure analysis
* 🔗 Dependency analysis
* 🕸️ Dependency graph generation
* 📊 Code and structural metrics
* 🚨 Architectural smell detection
* 🏢 God-module detection
* 🔄 Circular dependency detection
* 🗑️ Disconnected/orphan module detection
* 📦 ZIP-based repository ingestion
* 🌐 Web-based architecture dashboard
* 🤖 Gemini-powered architecture assistance
* 💬 Conversational AI Architecture Assistant
* 📥 Markdown architecture/code audit reports
* 🔧 AI-assisted refactoring workflows
* 🐳 Docker development configuration
* ⚙️ GitHub Actions CI pipeline

---

# 🧠 How ONGISA Works

ONGISA follows a pipeline that converts a software repository into an architectural model.

```text
                     PROJECT
                        │
                        ▼
                ┌─────────────────┐
                │   ONGISA CORE   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │     ANALYZE     │
                │                 │
                │ Files           │
                │ Functions       │
                │ Classes         │
                │ Imports         │
                │ Dependencies    │
                │ Metrics         │
                └────────┬────────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
        DEPENDENCY   ARCHITECTURE   CALL
           GRAPH       ANALYSIS     ANALYSIS
              │          │          │
              └──────────┼──────────┘
                         ▼
                ┌─────────────────┐
                │  WEB DASHBOARD  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   GEMINI AI     │
                │    + RAG        │
                └────────┬────────┘
                         │
                         ▼
                 AI EXPLANATIONS
                         │
                         ▼
                  REFACTOR PLANS
```

---

# 🔎 Static Codebase Analysis

ONGISA analyzes source files and extracts structural information from the project.

The analyzer can work with information such as:

* Files
* Directories
* Functions
* Classes
* Methods
* Imports
* Exports
* Symbols
* Module relationships
* Dependency relationships
* File metrics

For example:

```text
src/
├── auth/
│   ├── login.ts
│   └── register.ts
│
├── users/
│   └── userService.ts
│
├── payments/
│   ├── payment.ts
│   └── stripe.ts
│
└── database/
    └── database.ts
```

ONGISA does not simply treat these as isolated files.

It builds relationships between them:

```text
login.ts
   │
   └──→ userService.ts
             │
             └──→ database.ts


payment.ts
   │
   └──→ stripe.ts
             │
             └──→ database.ts
```

---

# 🕸️ Dependency Graph

One of ONGISA's core features is converting imports and module relationships into a visual dependency graph.

Example:

```text
                 app.ts
                /     \
               ▼       ▼
           auth.ts   users.ts
               │       │
               └───┬───┘
                   ▼
              database.ts
```

The graph helps developers understand:

* Which files depend on a module
* Which modules have many dependents
* Which modules are isolated
* Where dependencies are concentrated
* Where circular dependencies exist
* How changes may propagate through the project

ONGISA can also generate graph data such as:

```text
graph.json
```

The web dashboard uses this information to create an interactive architecture view.

---

# 🚨 Architectural Smell Detection

ONGISA analyzes structural relationships and metrics to identify potential architectural problems.

## 🏢 God Modules

A **God Module** is a file or module that has accumulated too many responsibilities.

For example:

```text
UserManager.ts

├── Authentication
├── Database operations
├── Email notifications
├── Payment processing
├── Validation
└── User management
```

ONGISA can use structural information such as:

* File size
* Symbol count
* Import count
* Dependency relationships
* Structural complexity

to identify modules that deserve investigation.

Example:

```text
🔴 God Module Detected

File:
src/services/UserManager.ts

Metrics:
2,800 lines
67 functions
32 imports

Recommendation:
Consider separating authentication,
database access, notifications,
and user management.
```

---

## 🔄 Circular Dependencies

ONGISA can identify dependency cycles such as:

```text
A → B
↑   ↓
└── C
```

Or:

```text
auth.ts
   ↓
users.ts
   ↓
database.ts
   ↓
auth.ts
```

Circular dependencies can make a project harder to understand, test, and modify.

---

## 🗑️ Disconnected / Orphan Modules

ONGISA can identify files that appear disconnected from the main application dependency graph.

Example:

```text
Application
│
├── auth.ts
├── users.ts
├── payments.ts
└── database.ts

legacyPayments.ts
```

A disconnected module can then be investigated to determine whether it is unused, obsolete, or intentionally isolated.

---

# 📦 Repository Ingestion

ONGISA supports analyzing uploaded project archives through the web dashboard.

The current workflow allows a developer to:

```text
Project
   │
   ▼
ZIP Upload
   │
   ▼
Archive Extraction
   │
   ▼
Source Analysis
   │
   ▼
Dependency Graph
   │
   ▼
Architecture Dashboard
```

The web application includes an upload interface for sending project archives to the backend analyzer.

Repository cloning and broader Git-based ingestion are part of the project's ongoing development.

---

## 🤖 AI Codebase Intelligence

ONGISA includes an AI layer powered by Google's Gemini API.

Rather than blindly sending an entire repository to an LLM, the AI layer works with the **structured information produced by ONGISA's analysis pipeline**.

The AI can reason over information such as:

* Repository structure
* Files and modules
* Symbols
* Imports
* Dependencies
* Graph relationships
* Architectural issues
* Code smells
* Analysis results

This allows ONGISA to provide **architecture-focused answers grounded in the actual structure and analysis of the project**, helping developers understand how different parts of the codebase are connected and where potential problems exist.

# 💬 Architecture AI Assistant

The web dashboard includes a conversational **Architecture AI Assistant**.

A floating chat interface allows developers to ask questions about the analyzed codebase.

Example questions:

```text
Where is data validation handled?

Which files depend on this module?

Why is this module highly connected?

What architectural problems were detected?

Explain the current dependency structure.

What could be causing this coupling?

How could this module be refactored?
```

The request flows through the web application to the ONGISA AI backend and then to Gemini.

```text
Developer Question
        │
        ▼
Architecture Chat Drawer
        │
        ▼
Next.js API Route
        │
        ▼
ONGISA AI Engine
        │
        ▼
Gemini
        │
        ▼
Architecture Response
```

---

# 📥 Architecture Audit Reports

ONGISA can generate Markdown architecture and code audit reports from analysis results.

Reports can contain information such as:

* Total tracked files
* Dependency information
* Detected architectural issues
* Code smells
* Issue severity
* Structural recommendations

Example:

```text
ONGISA Architecture & Code Audit Report

Overview
├── Total tracked files
├── Detected issues
└── Architectural observations

Detected Issues
├── God modules
├── Circular dependencies
└── Other structural smells

Recommendations
└── Suggested architectural improvements
```

Reports can be exported directly from the web dashboard.

---

# 🔧 AI-Assisted Refactoring

ONGISA is designed to use analyzer results to assist with refactoring.

Instead of asking an AI model to modify a project without understanding its architecture, ONGISA first gathers structural information.

Example request:

```text
Refactor UserManager.ts so that
authentication, database access,
and notifications are separated.
```

The intended workflow is:

```text
Developer Request
        │
        ▼
Analyzer Diagnostics
        │
        ▼
Architecture Context
        │
        ▼
Gemini
        │
        ▼
Refactoring Plan
        │
        ▼
Proposed Changes
        │
        ▼
Developer Review
```

The project uses a **dry-run approach** so proposed changes can be inspected before being applied.

---

# 🖥️ CLI

ONGISA includes a developer-facing CLI architecture.

Current commands include:

```bash
forge analyze
```

Analyzes a project and generates structural and dependency information.

```bash
forge chat
```

Starts an AI-assisted conversation with the codebase.

```bash
forge refactor
```

Runs the refactoring workflow using analyzer diagnostics and developer instructions.

---

# 🌐 Web Dashboard

The ONGISA web dashboard is built with Next.js and React.

The dashboard provides a visual interface for exploring analyzed projects.

Current capabilities include:

* Interactive dependency topology
* Repository/project upload
* Architecture analysis
* Code smell visualization
* Dependency exploration
* Analysis results
* AI Architecture Chat Assistant
* Markdown audit report export
* Refactoring workflow interface

The dashboard is designed around the idea that developers should be able to **see the architecture before changing it**.

---

# 🏗️ Project Architecture

ONGISA is organized as a modular monorepo.

```text
ONGISA/
│
├── packages/
│   │
│   ├── forge-core/
│   │   ├── schemas/
│   │   ├── models/
│   │   ├── repository/
│   │   └── cloner.py
│   │
│   ├── forge-analyzer/
│   │   ├── parsers/
│   │   ├── analysis/
│   │   ├── metrics/
│   │   ├── graph/
│   │   └── callgraph.py
│   │
│   ├── forge-ai/
│   │   ├── embeddings/
│   │   ├── retrieval/
│   │   ├── vector_store/
│   │   ├── agent.py
│   │   └── gemini/
│   │
│   └── forge-refactor/
│       ├── planning/
│       ├── transformations/
│       └── jobs/
│
├── CLI/
│   └── forge-cli/
│
├── apps/
│   └── forge-web/
│       ├── app/
│       │   └── api/
│       │       ├── chat/
│       │       ├── export/
│       │       └── graph/
│       │
│       └── components/
│           ├── DependencyGraph.tsx
│           ├── UploadDropzone.tsx
│           ├── AnalysisResult.tsx
│           └── ArchitectureChatDrawer.tsx
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# 📦 Core Components

## `forge-core`

The shared foundation of ONGISA.

Responsibilities include:

* Shared schemas
* Repository models
* AST metadata
* Analysis result structures
* Repository utilities
* Repository cloning functionality
* Shared interfaces

---

## `forge-analyzer`

The static analysis engine.

Responsibilities include:

* Source parsing
* AST analysis
* Function extraction
* Class extraction
* Import analysis
* Dependency tracking
* File metrics
* Structural diagnostics
* Dependency graph generation
* Call-graph analysis

This package provides the structural intelligence used by the rest of ONGISA.

---

## `forge-ai`

The AI intelligence layer.

Responsibilities include:

* Gemini integration
* AI architecture questions
* Codebase context construction
* Retrieval architecture
* Embeddings
* Vector storage
* AI explanations
* Architecture chat

---

## `forge-refactor`

The refactoring engine.

Responsibilities include:

* Refactoring job management
* Analyzer diagnostic integration
* AI refactoring prompts
* Transformation planning
* Dry-run workflows
* Proposed file modifications

---

## `forge-cli`

The developer-facing terminal interface.

It provides commands such as:

```bash
forge analyze
forge chat
forge refactor
```

---

## `forge-web`

The Next.js web application.

It provides:

* Architecture visualization
* Dependency graph interaction
* Repository upload
* Analysis results
* Architecture chat
* Audit report export
* Refactoring workflows

---

# 🔄 Typical ONGISA Workflow

A typical analysis session looks like this:

### 1. Upload a project

```text
Developer
    │
    ▼
ZIP Repository
    │
    ▼
ONGISA
```

### 2. Analyze the codebase

```text
Source Code
    ↓
Parser
    ↓
AST / Structure
    ↓
Symbols + Imports + Metrics
```

### 3. Build the dependency graph

```text
Files
  ↓
Imports
  ↓
Dependencies
  ↓
Graph
```

### 4. Detect architectural problems

```text
Graph + Metrics
       ↓
Architecture Analysis
       ↓
├── God Modules
├── Circular Dependencies
├── Disconnected Modules
└── Other Structural Issues
```

### 5. Visualize the architecture

```text
Analysis Results
       ↓
React Flow
       ↓
Interactive Dashboard
```

### 6. Ask the AI

```text
Developer Question
       ↓
Architecture Context
       ↓
ONGISA AI Engine
       ↓
Gemini
       ↓
AI Explanation
```

### 7. Generate a report

```text
Analysis Results
       ↓
Audit Report Generator
       ↓
Markdown Report
       ↓
Download
```

### 8. Plan a refactor

```text
Architecture Problem
       ↓
Analyzer Diagnostics
       ↓
Gemini
       ↓
Refactoring Plan
       ↓
Developer Review
```

---

# 🛠️ Technology Stack

## Backend

* Python
* FastAPI
* Pydantic
* Python AST
* Tree-sitter
* Static analysis

## AI

* Google Gemini API
* `google-generativeai`
* Retrieval-Augmented Generation architecture
* Embeddings
* Vector storage

## Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS
* React Flow

## CLI

* Python
* Typer
* Rich

## Infrastructure

* Docker
* Docker Compose
* Git
* GitHub Actions

---

# ⚙️ Development Setup

Clone the repository:

```bash
git clone <repository-url>
cd ONGISA
```

Create/activate the Python environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Set the Gemini API key:

```powershell
$env:GEMINI_API_KEY="your_gemini_api_key"
```

Set the Python package paths:

```powershell
$env:PYTHONPATH="packages/forge-core/src;packages/forge-analyzer/src;packages/forge-ai/src"
```

Start the backend:

```powershell
uvicorn forge_ai.main:app --reload --port 8000
```

In another terminal, start the web dashboard:

```powershell
npm run dev --prefix apps/forge-web
```

The project can also be developed using Docker when Docker Desktop is available.

---

# 🧪 Testing

ONGISA includes automated Python tests and a Next.js build check through GitHub Actions.

The Python test suite can be run with:

```powershell
$env:PYTHONPATH="packages/forge-core/src;packages/forge-analyzer/src;packages/forge-ai/src"

python -m pytest packages/forge-core/tests packages/forge-analyzer/tests packages/forge-ai/tests
```

The web application can be checked with:

```powershell
npm run build --prefix apps/forge-web
```

GitHub Actions is configured to automatically run project checks on pushes and pull requests.

> The CI configuration is still being refined as the project evolves.

---

# 🚧 Current Project Status

ONGISA is actively under development.

### Completed / Implemented

* [x] Monorepo project structure
* [x] Core package architecture
* [x] Repository analysis foundation
* [x] Static code analysis
* [x] Import/dependency analysis
* [x] Symbol extraction
* [x] Dependency graph generation
* [x] Architecture visualization
* [x] React Flow topology dashboard
* [x] ZIP repository upload
* [x] Upload/dropzone interface
* [x] Architectural smell analysis
* [x] God-module detection
* [x] Circular dependency analysis
* [x] Disconnected module analysis
* [x] FastAPI backend
* [x] Next.js web dashboard
* [x] Gemini AI integration
* [x] Architecture AI chat endpoint
* [x] Architecture Chat Drawer
* [x] Markdown architecture report export
* [x] Docker configuration
* [x] GitHub Actions CI foundation
* [x] Refactoring workflow foundation

### In Progress

* [ ] More robust multi-language analysis
* [ ] More advanced call-graph analysis
* [ ] Deeper cross-language dependency analysis
* [ ] More sophisticated architectural smell detection
* [ ] Improved AI/RAG reasoning
* [ ] More advanced refactoring transformations
* [ ] Improved repository ingestion
* [ ] Expanded automated test coverage
* [ ] Production-ready GitHub repository ingestion

---

# 🔮 Roadmap

## Phase 1 — Static Analysis

* Multi-language parsing
* Improved AST analysis
* Better symbol resolution
* Advanced dependency tracking
* More code metrics

## Phase 2 — Architecture Intelligence

* More architectural smell detectors
* Module coupling analysis
* Change-impact analysis
* Dependency risk analysis
* Architecture health metrics

## Phase 3 — AI Intelligence

* Better RAG retrieval
* Architecture-aware prompting
* Deeper codebase reasoning
* Natural-language architecture exploration
* More precise refactoring recommendations

## Phase 4 — Automated Refactoring

* Multi-file transformations
* Dependency-aware refactoring
* Refactoring previews
* Patch generation
* Safe rollback
* Automated tests after changes

## Phase 5 — Developer Platform

* GitHub repository integration
* Repository history analysis
* Pull-request architecture analysis
* CI/CD integration
* Team dashboards
* Continuous architecture monitoring

---

## 🔐 Design Philosophy

ONGISA is built around a few core principles that guide how the system analyzes codebases and assists developers.

### 1. Understand Before Changing

ONGISA should first understand the structure, dependencies, and architecture of a codebase before suggesting changes.

### 2. Analyze Before Generating

AI should work from the context produced by static analysis. Structural information should be established before AI recommendations or generation take place.

### 3. Explain Recommendations

Developers should be able to understand **why** a particular architectural issue or refactoring is being suggested, rather than receiving unexplained changes.

### 4. Refactor Safely

Refactoring should be treated as a controlled process. ONGISA favors analysis, previews, dry runs, and developer approval before changes are applied.

### 5. Keep the Developer in Control

ONGISA is designed to **assist developers, not replace their decisions**. Developers remain in control of what changes are accepted, rejected, or applied to their codebase.


# 🎯 The Problem ONGISA Solves

As software projects grow, understanding the architecture becomes increasingly difficult.

A project can grow from:

```text
10 files
   ↓
50 files
   ↓
500 files
   ↓
5,000+ files
```

At that point, developers may struggle to answer:

```text
What depends on this file?

Where is this function being used?

Why is this module so large?

Are there circular dependencies?

Which modules are highly connected?

What could break if I change this?

Where should this functionality live?

How should this part of the system be refactored?
```

ONGISA aims to answer these questions using actual structural information from the codebase.

---

# 💡 Why ONGISA?

Traditional static-analysis tools are useful for finding individual structural problems.

AI coding assistants are useful for explaining and generating code.

ONGISA combines the two:

```text
STATIC ANALYSIS
       +
DEPENDENCY GRAPH
       +
ARCHITECTURE ANALYSIS
       +
CODEBASE CONTEXT
       +
GENERATIVE AI
       =
CODEBASE INTELLIGENCE
```

The analyzer provides the structural facts.

The AI provides interpretation and explanations.

Together, they create a system designed specifically around understanding software architecture.

---

# 📄 License

ONGISA is currently still under active development.

License information will be added before the first official public release.

---

# 👨‍💻 Vision

The long-term vision for ONGISA is to make large software systems easier to understand.

Instead of developers spending hours manually tracing files, imports, dependencies, and architectural problems, they should be able to ask:

```text
"What is wrong with my architecture?"

"Why is this module so complicated?"

"What depends on this file?"

"What could be affected by this change?"

"How should I refactor this?"

"Why does this dependency exist?"
```

ONGISA should answer those questions using the **actual architecture and structural information of the codebase**, rather than guessing from isolated pieces of source code.

---

# ⭐ ONGISA

**Analyze. Understand. Visualize. Refactor.**

> **Your codebase has an architecture. ONGISA makes it visible.**
