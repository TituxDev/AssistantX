# AssistantX

A multi-purpose assistant system powered by AI agents. AssistantX aims to provide a generic environment in which agents can be composed to solve a wide range of tasks. As the user interacts with the system, an internal memory is generated and continuously updated, inferring a model of the user's profile from multiple perspectives so the system's behavior adapts better to the user's workflow over time.

> **Status:** Early-stage / active development. The current codebase implements the foundational `Agent` class that manages communication with AI models. Higher-level features (multi-agent orchestration, memory inference, adaptive workflows) are part of the roadmap and not yet implemented.

## Overview

AssistantX is designed around the idea that no single AI model or fixed workflow fits every task. Instead, the system will orchestrate multiple agents — potentially backed by different AI providers — each contributing to solving user issues. Over time, the system should build an internal, evolving profile of the user (preferences, workflow patterns, context) to better tailor its responses and behavior.

Core goals:
- **Generic environment**: not tied to a single use case; agents can be added to tackle different kinds of problems.
- **Multi-provider**: able to work with AI models from different providers, not locked into one.
- **Adaptive memory**: infer and update a user profile from interactions, from multiple angles, to improve fit with the user's workflow.

## Current State

At this stage, the project consists of a single module containing the `Agent` class, which is responsible for:

- Managing communication with AI models (across different providers).
- Keeping a history of messages sent by the user and responses returned by the model.

Using the `Agent` class, from the main code you can currently:
- Run **single calls** to a model as one-off routines.
- Start an **interactive chat** session, since the `Agent` keeps track of conversation history internally.

## Tech Stack

- **Language**: Python
- **AI Models**: multiple providers (model-agnostic by design)
- Dependencies are listed in `requirements.txt`

## Getting Started

### Prerequisites

- Python 3.x
- API credentials for whichever AI provider(s) you intend to use (set up as environment variables — see note below)

### Installation

```bash
git clone https://github.com/TituxDev/AssitantX.git
cd AssistantX
pip install -r requirements.txt
```

### Usage

> This section will be expanded as the interface stabilizes. For now, the `Agent` class is used directly from the main script — example usage to be added once the entry point is finalized.

```python
from agent import Agent

# Example: single call
agent = Agent("Model name")
response = agent.call("Your prompt here")

# Example: interactive chat
agent.chat()
```

*(Update the snippet above to match the actual constructor/method signatures.)*

## Roadmap

- [ ] Expand beyond a single `Agent` into a multi-agent architecture (agents + skills working together)
- [ ] Support mixing models for different purposes, rather than one model for everything
- [ ] Build the internal memory/user-profile inference system
- [ ] Define a generic interface/environment for plugging in new agents to solve new kinds of issues
- [ ] Add configuration for managing multiple provider credentials
- [ ] Add tests and usage examples

## Project Structure

```
AssistantX/
├── system
|   └── core
|       ├── agent.py          # Agent class: model communication + message history
|       └── requirements.txt
├── requirements.txt  # Python dependencies
└── README.md
```