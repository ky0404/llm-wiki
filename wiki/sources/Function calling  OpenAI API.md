---
title: Function calling OpenAI API
type: source
tags: [prompt, rag, model context]
sources: [Function calling OpenAI API.md]
created: 2026-04-30
updated: 2026-04-30
---

# Function calling OpenAI API

**Function calling** (also known as **tool calling**) provides a powerful and flexible way for OpenAI models to interface with external systems and access data outside their training data.

## How it works

Tool calling is a multi-step conversation between your application and a model via the OpenAI API:

1. Define functions/tools
2. Model identifies intent to call tool
3. Execute function and return result
4. Model generates final response

## Key Concepts

- **Tools**: Functionality we give the model
- **Tool calls**: Requests from the model to use tools
- **Tool call outputs**: Output we generate for the model

## Best Practices

- Clear function descriptions
- Proper parameter validation
- Error handling
- Async support for long-running calls

## References

- [[wiki/concepts/function-calling]]
- [[wiki/entities/openai]]
- [[wiki/concepts/prompt-engineering]]