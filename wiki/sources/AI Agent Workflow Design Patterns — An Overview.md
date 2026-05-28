---
title: "AI Agent Workflow Design Patterns — An Overview"
type: source
tags: ["agent", "prompt", "llm", "rag", "langchain", "service", "langgraph", "pdf"]
sources: ["AI Agent Workflow Design Patterns \u2014 An Overview.md"]
created: 2026-04-30
updated: 2026-04-30
---


In our previous post, we introduced [AI Agent Design Patterns](https://medium.com/binome/designing-llm-based-agents-key-principles-part-1-7e8c6fe3ddaf). Now, we are in the process of implementing an agent framework based on that design. At the same time, we are actively researching various workflow design patterns. Special thanks to [Lychee Zhong](https://www.linkedin.com/in/yi-z-a7a4602a2/) for compiling these patterns with clear and informative diagrams.

Before diving deeper, let’s revisit the concept of an LLM-based AI agent. As described by the [nvidia blog](https://developer.nvidia.com/blog/introduction-to-llm-agents/), LLM-powered agents are systems that utilize a large language model (LLM) to reason through problems, create actionable plans, and execute those plans using a set of tools. Simply put, these agents combine advanced reasoning capabilities, memory, and task execution.

The evolution of LLM-based AI agent workflow design patterns began in late 2022 and continues to evolve and innovate.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*08KTKf0vmwm-pTdvhOcoSg.png)

This paper introduced ReAct Pattern, which published in October 2022. This pattern enhancing the strength of Agents by integrating the use of tools.

This is one of the earliest papers on LLM Agents. Although it may seem basic by today’s standards, at the time, ChatGPT hadn’t been released yet, and the idea of teaching LLMs to use tools was groundbreaking.

In the following section, we summarize the patterns we’ve learned and believe will be applicable to real-world business needs.

## Introduction

Currently, there are numerous workflow designs. To summarize them based on their focus, we’ve categorized the workflow design patterns we’ve learnt so far into two groups: **Reflection-focused** and **Planning-focused**.

### Reflection-focused

**Reflection** allows agents to learn from experience, improving adaptability and resilience. These agents emphasize introspection and learning from past experiences. They analyze previous actions and outcomes to refine future behaviour. By evaluating their performance, they identify mistakes and successes, allowing for continuous improvement. This reflective process enables the agent to adapt its strategies over time, leading to more effective problem-solving. \[[LangChain Blog](https://blog.langchain.dev/reflection-agents/)\]

- [**Basic Reflection**: Reflecting and learning from the steps.](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/reflection/reflection.ipynb)
- [**Reflexion**: Enhancing the next steps of the Agent through reinforcement learning.](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/reflexion/reflexion.ipynb)
- [**Tree search**: TOT + reinforcement learning-based reflection.](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/lats/lats.ipynb)
- [**Self-Discover**: Reasoning within the task.](https://arxiv.org/abs/2402.03620)

### Planning-focused

**Planning** enables agents to approach tasks methodically, increasing efficiency and effectiveness. These agents prioritize the development of structured plans before taking action. They decompose complex tasks into manageable sub-tasks and sequence them logically to achieve specific goals. By formulating detailed plans, these agents can anticipate potential challenges and allocate resources efficiently, resulting in more organized and goal-directed behaviour. \[[https://arxiv.org/pdf/2402.02716](https://arxiv.org/pdf/2402.02716)\]

- [**Plan & Solve**: Plan → Task list → RePlan.](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/plan-and-execute/plan-and-execute.ipynb)
- [**LLM compiler**: Plan → Action in parallel → Joint execution.](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/llm-compiler/LLMCompiler.ipynb)
- [**REWOO**: Plan (including dependencies) → Action (depends on the previous step).](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/rewoo/rewoo.ipynb)
- [**Storm**: Search for outline → Search each topic in the outline → Summarize into a long text.](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/storm/storm.ipynb)

When reviewing these design patterns, we see the workflow as an orchestrator. Each node can represent an LLM task, a function call, and other tasks like Retrieval-Augmented Generation (RAG) task, which we typically treat as another type of function call. This concept is one of the main drivers behind developing our own agent. We’ve designed the workflow as a flexible task orchestrator, allowing developers to create various workflows to tackle different problems.

In this post, we will explore two specific workflow design patterns: the *ReAct pattern* and the *Plan-Solve pattern*. For the remaining patterns, we’ll provide a brief summary to explain their motivation and use cases.

## ReAct Pattern

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*08KTKf0vmwm-pTdvhOcoSg.png)

The ReAct principle is straightforward and reflects a core aspect of human intelligence: “actions guided by verbal reasoning.” After each action, there’s an internal “Observation” or self-reflection: “What did I just do? Have I achieved my goal?” This enables the agent to retain short-term memory. Before ReAct, reasoning and action were treated as separate processes.

For example, imagine you ask someone to find a pen on your desk, and you give step-by-step instructions (similar to the Chain-of-Thought prompting strategy):

1. First, check the pen holder.
2. Then, look in the drawer.
3. Lastly, check behind the computer monitor.

Without ReAct, regardless of where the pen is found, the person would follow all the steps, checking each location (Action).

With ReAct, the process would look like this:

1. Action 1: First, check the pen holder;
2. Observation 1: The pen is not in the pen holder, so move to the next step;
3. Action 2: Then, check the drawer;
4. Observation 2: The pen is in the drawer;
5. Action 3: Take the pen from the drawer.

### ReAct Implementation

After reviewing several open-source codes, let’s focus on [the simplest one](https://github.com/samwit/langchain-tutorials/blob/main/agents/YT_Exploring_ReAct_on_Langchain.ipynb) for analysis. As you explore it, you’ll notice that, at its essence, all Agent design patterns *revolve around translating human thinking and management strategies into structured prompts*. These prompts guide the large model to plan, invoke tools for execution, and continuously refine its approach through iteration.

The code logic is outlined in the diagram below (take a close look):

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*yw_98xQCBzzpuJ0nzLEYDw.jpeg)

- **Generate the prompt**: First, the predefined ReAct prompt template (formatted as Question -> Thought -> Action -> Observation) is merged with the user’s question. The resulting prompt looks like this.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*xTfOitvz3wL5QAGijgONow.jpeg)

- **Call the large model to generate Thought + Action**: Next, send the few-shot prompt to the large model. If sent as is, the model will generate Thought, Action, and Observation responses. However, since the Action isn’t fully defined, we prevent the model from generating the Observation by using Stop.Observation, ensuring it stops after Thought and Action.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Mph9P_JDiASY5nq_ZI_Qbw.jpeg)

- **Calling External Tools**: Once the Action is obtained, the model can call external tools. First, check if the Action is “Finish.” If not, the model converts the Action into an API-compatible format using its function-calling feature. This fine-tunes the model for language-to-API conversion, though not all large models support function calling.
- **Generating Observation**: After the API interface returns the result, it is converted into natural language output to generate the Observation. Then the Observation, along with the previously generated Thought and Action, is input back into the model, repeating steps 2 and 3 until the Action is “Finish.”
- **Final Output**: The final Observation is converted into natural language and output to the user.

From this, we can see that implementing an Agent in a specific scenario requires customizing two key components:

1. The few-shot examples in the prompt template
2. The definition of external tools for function calling

The few-shot examples essentially mirror structured human thinking patterns. Reviewing prompt templates for different design patterns is a great way to understand Agent design. Once you grasp this approach, it can be applied to other design patterns similarly.

## Plan and Solve Pattern

As the name suggests, this design pattern involves planning first and then executing. If ReAct is more suitable for tasks like “getting pen from the the desk” then Plan & Solve is better suited for tasks like “making a cup of flat white.” You need to plan, and the plan might change during the process (for example, if you open the fridge and find no milk, you would add “buy milk” as a new step in the plan).

Regarding the prompt template, the paper’s title makes it clear: [*Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models*.](https://arxiv.org/abs/2305.04091) In short, it’s about improving zero-shot capabilities. The following image shows some PS-Plan and Solve prompts provided in the author’s code.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*5PDTqST0eh-qYCbX-uhzcQ.png)

[Link](https://github.com/AGI-Edgerunners/Plan-and-Solve-Prompting)

Its architecture is composed as follows:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*WQarFPrWeatrSZHeRoHjTQ.png)

- Planner: Responsible for enabling the LLM to generate a multi-step plan to complete a large task. In the code, there are both a Planner and a Replanner. The Planner is responsible for generating the plan initially; the Replanner, on the other hand, comes into play after each individual task is completed, adjusting the plan based on the current progress. Therefore, the Replanner’s prompt includes not only the zero-shot input but also the goal, the original plan, and the status of completed steps.
- Executor: Receives the user’s query and the steps from the plan, then calls one or more tools to accomplish the task.

## Other Workflow Design Patterns

Here we give the brief introduction of other design patterns listed above.

### Reason without Observation (REWOO)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*srID4HdpUFpE-5wlSQHg5g.png)

REWOO (Reason without Observation) is a variation on the observation process seen in ReAct. While ReAct follows the structure: Thought → Action → Observation, REWOO simplifies this by removing the explicit observation step. Instead, it implicitly embeds observation into the next execution unit. In practice, the next executor automatically observes the outcome of the previous step, streamlining the process.

### LLMCompiler

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*_8FP1sYMWwcVZaD8tObjVA.png)

In computer science, a compiler refers to the orchestration of tasks to optimize computational efficiency. The concept behind An LLM Compiler for Parallel Function Calling, as outlined in the original paper, is simple yet effective: it aims to enhance efficiency by enabling parallel function calls. For instance, if a user asks, “What’s the difference between AWS Glue and MWAA?”, the compiler would search for the AWS services definition simultaneously and combine the results, rather than handling each query sequentially.

### Basic Reflection

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*9543fUoJVC5xq9Ot5aLbvw.png)

Basic Reflection can be compared to a feedback loop between a student (the Generator) and a teacher (the Reflector). The student completes an assignment, the teacher provides feedback, and the student revises their work based on this feedback, repeating the cycle until the task is satisfactorily completed.

### Reflexion

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*owP9OsMtoMBNT5BnGYR1GA.png)

Reflexion builds on Basic Reflection, incorporating principles of reinforcement learning. Described in the paper Reflexion: Language Agents with Verbal Reinforcement Learning, this approach goes beyond simple feedback. It evaluates the response using external data and forces the model to address any redundancies or omissions, making the reflective process more robust and the output more refined.

### Language Agent Tree Search (LATS)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*IpwqQIk8i7k-lLf9HRQHSw.png)

LATS is detailed in the paper [*Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models.*](https://arxiv.org/abs/2310.04406) It combines several techniques, including Tree Search, ReAct, and Plan & Solve. LATS uses tree search to assess outcomes (drawing from reinforcement learning), while also integrating reflection to achieve optimal results. In essence, LATS can be represented by the following formula:

*LATS = Tree Search + ReAct + Plan & Solve + Reflection + Reinforcement Learning.*

In terms of prompt design, the difference between LATS and earlier methods such as Reflection, Plan & Solve, and ReAct is minimal. The key addition is the tree search evaluation step and the return of those evaluated results within the task context. Architecturally, LATS involves multiple rounds of Basic Reflection, with several Generators and Reflectors working collaboratively.

### Self-Discovery

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*dIw0pcymwtjUMVmYnwrBqw.png)

The core of Self-Discovery is to allow the large model to reflect at a more granular level. While Plan & Solve focuses on whether a task requires additional steps or adjustments, Self-Discovery goes further, encouraging reflection on the task itself. This involves evaluating each component of the task and the execution of those components.

### Storm

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ixKPpWglH89IdRdoHsFQQA.png)

Storm, outlined in the paper [*Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models*](https://arxiv.org/abs/2402.14207), introduces a workflow for generating comprehensive articles from scratch, similar to a Wikipedia entry. The agent first uses external tools to search for information and generate an outline. Then, it produces content for each section based on the outline, making the process structured and efficient.

## Conclusion

In this post, we explore various AI agent workflow design patterns, we categorize the patterns into Reflection-focused and Planning-focused, showcasing examples like the ReAct and Plan-Solve patterns. For developing purposes, these workflow patterns emphasize that workflows act as orchestrators for tasks within an agent. Each node in the workflow represents actions such as LLM tasks, function calls, or Retrieval-Augmented Generation (RAG). This structure enables the agent to plan, execute tasks, and iterate, simulating human reasoning.

We are currently developing our own agent based on these principles, utilizing workflows as flexible task orchestrators to handle different problems. More details on our agent implementation will be covered in the next post.
