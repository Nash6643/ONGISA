# ONGISA

> **AI-powered static codebase analysis, architecture visualization, and intelligent refactoring.**

ONGISA is a developer tool that analyzes entire software projects, maps their structure and dependencies, detects architectural problems, and uses AI to explain issues and suggest safe refactoring strategies.

Instead of manually tracing hundreds of files and imports, ONGISA gives developers a clear picture of **how their codebase is structured, how its components depend on each other, where architectural problems exist, and how those problems can be improved.**

---

## ✨ What ONGISA Does

ONGISA combines **static code analysis**, **dependency mapping**, **architecture visualization**, and **AI-powered code understanding** into one platform.

You can point ONGISA at a project and discover:

* 📁 Project and directory structure
* 🔗 File and module dependencies
* 📦 Import relationships
* 🔍 Functions, classes, and symbols
* 📊 File and code complexity metrics
* 🗑️ Potentially unused or disconnected modules
* 🔄 Circular dependencies
* 🏢 Overly large or complex "God Modules"
* ⚠️ Architectural smells and structural problems
* 🤖 AI explanations of detected issues
* 🔧 AI-generated refactoring suggestions

The goal is simple:

> **Give developers an X-ray of their entire codebase.**

---

# 🧠 How It Works

ONGISA follows a pipeline that turns a source code repository into an understandable architectural model.

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
              ┌────────┴────────┐
              ▼                 ▼
       DEPENDENCY GRAPH    ARCHITECTURE
                              ANALYSIS
              │                 │
              └────────┬────────┘
                       ▼
                ┌──────────────┐
                │  WEB DASHBOARD│
                └──────┬───────┘
                       │
                       ▼
                 ┌───────────┐
                 │    AI     │
                 │   + RAG   │
                 └─────┬─────┘
                       │
                       ▼
               REFACTOR PLAN
                       │
                       ▼
                PROPOSED CHANGES
```

---

# 🔎 Static Codebase Analysis

ONGISA analyzes source files and extracts structural information from the project.

Depending on the supported language, it can identify:

* Files
* Directories
* Functions
* Classes
* Methods
* Imports
* Exports
* Module relationships
* Symbol relationships
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

ONGISA doesn't just see these as files.

It builds a structural representation of the project and understands relationships such as:

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

One of ONGISA's core capabilities is turning imports and relationships into a dependency graph.

For example:

```text
              app.ts
             /     \
            ▼       ▼
        auth.ts   users.ts
           │         │
           └────┬────┘
                ▼
          database.ts
```

This allows developers to quickly understand:

* Which files depend on a particular module
* Which modules have many dependents
* Which modules are isolated
* Where dependencies are concentrated
* Where circular dependencies exist
* How changes to one module may affect others

The generated graph can also be exported as a standalone payload such as:

```text
graph.json
```

---

# 🚨 Architectural Smell Detection

Large projects often develop structural problems that aren't immediately obvious.

ONGISA attempts to automatically identify these problems.

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

ONGISA can flag this module based on structural metrics such as:

* File size
* Number of symbols
* Number of responsibilities
* Import count
* Dependency relationships
* Structural complexity

Example:

```text
🔴 God Module Detected

File:
src/services/UserManager.ts

Metrics:
2,800 lines
67 functions
32 imports
18 classes

Recommendation:
Consider separating authentication,
database access, notifications,
and user management.
```

---

## 🔄 Circular Dependencies

ONGISA can detect dependency cycles such as:

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

These relationships can make software harder to maintain, test, and modify.

---

## 🗑️ Disconnected / Orphan Modules

ONGISA can identify modules that appear disconnected from the main application graph.

For example:

```text
Application
│
├── auth.ts
├── users.ts
├── payments.ts
└── database.ts

legacyPayments.ts
```

If `legacyPayments.ts` has no meaningful connections to the application, ONGISA can flag it for investigation.

---

# 🤖 AI Codebase Intelligence

ONGISA uses AI to provide a higher-level understanding of the analyzed project.

Instead of sending an entire codebase blindly to an LLM, ONGISA first analyzes the repository and retrieves the most relevant information.

This allows AI requests to be grounded in:

* Relevant source files
* Symbols
* Imports
* Dependency relationships
* Architectural diagnostics
* Project structure
* Previously indexed code

---

# 🧠 RAG-Powered Codebase Chat

ONGISA can index project code into a local vector store and use **Retrieval-Augmented Generation (RAG)** to answer questions about the codebase.

Developers can ask questions such as:

```text
Why does payments.ts depend on database.ts?

Where is UserService being used?

Which modules depend on authentication?

Why is this module considered a God Module?

What would happen if I changed database.ts?

Where should this functionality be moved?

Are there circular dependencies in the project?
```

Instead of searching through thousands of lines manually, ONGISA retrieves the relevant context and provides it to the AI.

---

# 🔧 AI-Assisted Refactoring

ONGISA can also use the analysis results to create refactoring plans.

For example, you might ask:

```text
Refactor UserManager.ts so that authentication,
database access, and notifications are separated.
```

ONGISA can analyze the existing architecture and propose a structure such as:

```text
Before:

UserManager.ts
├── Authentication
├── Database
├── Notifications
└── User Management


After:

auth/
└── AuthService.ts

users/
├── UserService.ts
└── UserRepository.ts

notifications/
└── EmailService.ts
```

The goal is not simply to generate code.

ONGISA should understand **which existing files are affected and how their dependencies need to change.**

Refactoring operations are designed around a **dry-run workflow**, allowing developers to inspect proposed changes before applying them.

---

# 🖥️ CLI

ONGISA provides a command-line interface for developers who prefer working directly from the terminal.

## Analyze a Project

```bash
forge analyze
```

Analyzes the project and generates structural information and dependency data.

---

## Chat With Your Codebase

```bash
forge chat
```

Starts an AI-powered conversation with the indexed codebase.

Example:

```text
> Which files depend on database.py?

> Why is UserManager.py considered complex?

> Show me potential architectural problems.
```

---

## Refactor a File

```bash
forge refactor
```

Runs an AI-assisted refactoring workflow based on analyzer diagnostics and developer instructions.

---

# 🌐 Web Dashboard

ONGISA also provides a web-based architecture dashboard.

The dashboard is designed to make large codebases easier to understand visually.

### Dashboard capabilities include:

* Interactive dependency graphs
* File filtering
* Language filtering
* Minimum file-size filtering
* Symbol-count filtering
* Custom path filtering
* Architectural smell visualization
* Dependency exploration
* Codebase statistics
* AI-assisted refactoring
* Refactoring previews

Example workflow:

```text
Open Project
     ↓
Analyze Codebase
     ↓
View Architecture
     ↓
Find Problems
     ↓
Inspect Dependencies
     ↓
Ask AI
     ↓
Generate Refactoring Plan
     ↓
Review Changes
```

---

# 🏗️ Project Architecture

ONGISA uses a modular monorepo architecture.

```text
ONGISA/
│
├── packages/
│   │
│   ├── forge-core/
│   │   ├── schemas/
│   │   ├── models/
│   │   └── repository/
│   │
│   ├── forge-analyzer/
│   │   ├── parsers/
│   │   ├── analysis/
│   │   ├── metrics/
│   │   └── graph/
│   │
│   ├── forge-ai/
│   │   ├── embeddings/
│   │   ├── retrieval/
│   │   ├── vector_store/
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
│
├── tests/
│
└── README.md
```

---

# 📦 Core Components

## `forge-core`

Provides shared models and infrastructure used across ONGISA.

Responsibilities include:

* Common schemas
* AST metadata models
* Repository models
* Analysis result structures
* Repository cloning utilities
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

This is the primary source of architectural intelligence in ONGISA.

---

## `forge-ai`

The AI intelligence layer.

Responsibilities include:

* Code indexing
* Embeddings
* Vector storage
* Retrieval
* Context construction
* Gemini integration
* AI codebase chat
* Architecture explanations

---

## `forge-refactor`

The refactoring engine.

Responsibilities include:

* Refactoring job management
* Analyzer diagnostic integration
* AI refactoring prompts
* Transformation planning
* Dry-run changes
* Proposed file modifications

---

## `forge-cli`

The developer-facing terminal interface.

Provides commands such as:

```bash
forge analyze
forge chat
forge refactor
```

The CLI uses terminal-friendly output to make analysis results easy to read.

---

## `forge-web`

The web dashboard.

Built with Next.js, it provides a visual interface for:

* Exploring the project architecture
* Viewing dependency graphs
* Filtering modules
* Inspecting architectural smells
* Interacting with the AI
* Running refactoring workflows

---

# 🔄 Typical Workflow

A typical ONGISA workflow looks like this:

### 1. Point ONGISA at a project

```text
Local Repository
       │
       ▼
     ONGISA
```

### 2. Analyze the project

```text
Source Code
     ↓
Parser
     ↓
AST
     ↓
Symbols + Imports + Metrics
```

### 3. Build the architecture graph

```text
Files
 ↓
Imports
 ↓
Dependencies
 ↓
Graph
```

### 4. Detect problems

```text
Graph + Metrics
       ↓
Architectural Analysis
       ↓
God Modules
Circular Dependencies
Orphan Modules
Other Structural Issues
```

### 5. Ask AI

```text
Developer Question
       ↓
Relevant Code Retrieval
       ↓
Architecture Context
       ↓
Gemini
       ↓
AI Explanation
```

### 6. Refactor

```text
Developer Request
       ↓
Analyzer Diagnostics
       ↓
AI Refactoring Plan
       ↓
Proposed Changes
       ↓
Developer Review
       ↓
Apply Changes
```

---

# 🛠️ Technology Stack

ONGISA is built around a combination of modern developer tooling and AI technologies.

### Backend / Analysis

* Python
* AST / source-code parsing
* Static analysis
* Dependency graph construction
* Code metrics

### AI

* Google Gemini
* Retrieval-Augmented Generation (RAG)
* Embeddings
* Local vector storage
* Context-aware code retrieval

### CLI

* Python
* Typer
* Rich

### Web

* Next.js
* React
* TypeScript
* Modern web visualization technologies

### Architecture

* Monorepo
* Modular packages
* Shared schemas
* CLI + Web interfaces

---

# 🎯 Problem ONGISA Solves

As software projects grow, understanding the architecture becomes increasingly difficult.

A project may contain:

```text
10 files
      ↓
50 files
      ↓
500 files
      ↓
5,000+ files
```

At that point, developers can struggle to answer basic questions:

* What depends on this file?
* Where is this function used?
* Why is this module so large?
* Which files are safe to modify?
* Are there circular dependencies?
* Is this code still being used?
* Where should this functionality live?
* What will break if I change this module?
* How should this part of the system be refactored?

ONGISA aims to answer these questions automatically.

---

# 💡 Why ONGISA?

Traditional code analysis tools are good at identifying individual problems.

AI coding assistants are good at generating and explaining code.

ONGISA combines both approaches.

```text
STATIC ANALYSIS
       +
DEPENDENCY GRAPH
       +
ARCHITECTURE ANALYSIS
       +
RAG
       +
GENERATIVE AI
       =
CODEBASE INTELLIGENCE
```

The analyzer provides **facts about the codebase**.

The AI provides **interpretation and recommendations**.

Together, they provide developers with a higher-level understanding of their software architecture.

---

# 🚧 Project Status

ONGISA is currently under active development.

### Current development focus

* [x] Project structure
* [x] Core schemas
* [x] Repository analysis foundation
* [x] Dependency analysis
* [x] Symbol extraction
* [x] CLI foundation
* [x] AI integration foundation
* [x] RAG architecture
* [x] Web dashboard foundation
* [ ] Expand language support
* [ ] Improve architectural smell detection
* [ ] Improve dependency graph visualization
* [ ] Expand AI codebase reasoning
* [ ] Advanced refactoring transformations
* [ ] Safer automated code modifications
* [ ] Test coverage expansion
* [ ] Production-ready repository ingestion

---

# 🔮 Future Roadmap

ONGISA is intended to evolve into a complete codebase intelligence platform.

### Phase 1 — Static Analysis

* Multi-language parsing
* Improved AST analysis
* Better symbol extraction
* Advanced dependency tracking
* More code metrics

### Phase 2 — Architecture Intelligence

* More architectural smell detectors
* Dependency risk scoring
* Module coupling analysis
* Change-impact analysis
* Architecture health scoring

### Phase 3 — AI Intelligence

* Improved RAG retrieval
* Architecture-aware AI prompts
* Codebase reasoning
* Natural-language architecture exploration
* Better refactoring recommendations

### Phase 4 — Automated Refactoring

* Multi-file refactoring
* Dependency-aware transformations
* Refactoring previews
* Patch generation
* Safe rollback
* Automated tests after refactoring

### Phase 5 — Developer Platform

* GitHub repository integration
* Repository history analysis
* Pull request architecture analysis
* CI/CD integration
* Team dashboards
* Architecture health monitoring

---

# 🔐 Design Philosophy

ONGISA is built around a few important principles.

### 1. Understand Before Changing

AI should understand the architecture before suggesting modifications.

### 2. Analysis Before Generation

The system should gather structural information before asking an LLM to reason about the project.

### 3. Explainable Recommendations

Developers should understand **why** a change is being recommended.

### 4. Safe Refactoring

Refactoring should favor previews, dry runs, and developer approval rather than blindly modifying production code.

### 5. Developer Control

ONGISA is intended to assist developers, not replace their judgment.

---

# 🚀 Getting Started

Clone the repository:

```bash
git clone <repository-url>
cd ONGISA
```

Install dependencies according to the package configuration.

Then run the CLI:

```bash
forge analyze
```

Start an AI codebase session:

```bash
forge chat
```

Run the refactoring workflow:

```bash
forge refactor
```

> Setup instructions will be expanded as the project reaches a stable release.

---

# 📁 Supported Repository Sources

ONGISA is designed to work with software repositories rather than being limited to a single hosting provider.

Potential repository sources include:

```text
Local Project
     │
     ├── Git Repository
     │
     ├── GitHub Repository
     │
     └── Uploaded Project
            │
            ▼
          ONGISA
```

GitHub integration is planned as part of the platform roadmap.

---

# 🤝 Contributing

Contributions are welcome.

If you want to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Add or update tests where appropriate.
5. Run the project checks.
6. Open a pull request.

Example:

```bash
git checkout -b feature/my-feature
```

---

# 📄 License

This project is currently under development.

License information will be added before the first public release.

---

# 👨‍💻 Vision

ONGISA aims to make large software systems easier to understand.

The long-term vision is simple:

> **Give every developer an architectural map of their codebase and an intelligent assistant that understands how the pieces fit together.**

Instead of spending hours manually tracing files, imports, dependencies, and architectural problems, developers should be able to ask:

```text
"What is wrong with my architecture?"

"Why is this module so complicated?"

"What depends on this file?"

"What can I safely change?"

"How should I refactor this?"

"What will be affected if I change this?"

```

And ONGISA should be able to answer using **actual structural knowledge of the codebase**, not just guesses from raw source code.

---

## ⭐ ONGISA

**Analyze. Understand. Visualize. Refactor.**

> **Your codebase has an architecture. ONGISA makes it visible.**
