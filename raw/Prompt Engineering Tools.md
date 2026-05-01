---
title: "Prompt Engineering Tools"
source: "https://learnprompting.org/docs/tooling/tools"
author:
  - "[[\"Sander Schulhoff\"]]"
published:
created: 2026-04-30
description: "Learn Prompting is the largest and most comprehensive course in prompt engineering available on the internet, with over 60 content modules, translated into 9 languages, and a thriving community."
tags:
  - "clippings"
---
This section contains a list of non-IDE tools that are useful for prompting.

## Prompt Development, Testing, and Chaining

### LangChain

> Large Language Models (LLMs) are emerging as a transformative technology, enabling developers to build applications that they previously could not. But using these LLMs in isolation is often not enough to create a truly powerful app - the real power comes when you can combine them with other sources of computation or knowledge.
> 
> This library is aimed at assisting in the development of those types of applications.

### PromptAppGPT

> PromptAppGPT is a low-code prompt-based rapid app development framework. PromptAppGPT contains features such as low-code prompt-based development, GPT text generation, [DALLE](https://learnprompting.org/docs/tooling/IDEs/DALLE) image generation, online prompt editer+compiler+runer, automatic user interface generation, support for plug-in extensions, etc. PromptAppGPT aims to enable natural language app development based on GPT.
> 
> PromptAppGPT provides multi-task conditional triggering, result verification, and failure retry capabilities, allowing manual generation tasks that would otherwise require multiple steps to be automated. At the same time, users no longer need to memorise and enter the tedious prompt mantra themselves, and can easily complete tasks by entering only the core necessary information for the task.
> 
> PromptAppGPT significantly lowers the barrier to GPT application development, allowing anyone to develop AutoGPT-like applications with a few lines of low code.

### Prompt-generator-for-ChatGPT

> The "Prompt generator for ChatGPT" application is a desktop tool designed to help users generate character-specific prompts for ChatGPT, a chatbot model developed by OpenAI.

### Dust.tt

> The [Dust](https://learnprompting.org/docs/tooling/IDEs/dust) platform helps build Large Language Model applications as a series of prompted calls to external models. It provides an easy to use graphical UI to build chains of prompts, as well as a set of standard blocks and a custom programming language to parse and process language model outputs.
> 
> It provides a series of features to make development of applications faster, easier and more robust:

- running multiple completions in parallel
- inspecting execution outputs
- versioning prompt chains
- custom programming language to process data and text
- [API](https://learnprompting.org/vocabulary/api) integration for various models and external services

### OpenPrompt

> Prompt-learning is the latest paradigm to adapt pre-trained language models (PLMs) to downstream NLP tasks, which modifies the input text with a textual template and directly uses PLMs to conduct pre-trained tasks. [OpenPrompt](https://learnprompting.org/docs/tooling/IDEs/openprompt) is a library built upon PyTorch and provides a standard, flexible and extensible framework to deploy the prompt-learning pipeline. OpenPrompt supports loading PLMs directly from huggingface transformers. In the future, we will also support PLMs implemented by other libraries.

### BetterPrompt

> ⚡ Test suite for [LLM](https://learnprompting.org/vocabulary/LLM) prompts before pushing them to PROD ⚡

### Prompt Engine

> NPM utility library for creating and maintaining prompts for Large Language Models (LLMs).

### Promptify

> Relying solely on LLMs is often insufficient to build applications & tools. To unlock their full potential, it's necessary to integrate LLMs with other sources of computation or knowledge and get the pipeline ready for production.
> 
> This library is aimed at assisting in developing a pipeline for using LLMs APIs in production, solving NLP Tasks such as NER, Classification, Question, Answering, Summarization, Text2Graph etc. and providing powerful agents for building chat agents for different tasks.

### PromptFlow

> PromptFlow is a free, open-source, low-code tool that allows users to integrate LLMs, prompts, Python functions, and conditional logic to create flowcharts. It includes nodes for:
> 
> OpenAI API Calls (any model, including Whisper speech-to-text)
> 
> Anthropic [Claude](https://learnprompting.org/docs/models/claude) Calls, Arbitrary Python Code blocks, and Long + Short term history management
> 
> Database Queries, PostgresML integration, and Text Embeddings
> 
> HTTP Requests, SerpAPI Google Searches, and ElevenLabs Speech Synthesis Documentation can be found [here](https://www.promptflow.org/en/latest/index.html)

### TextBox

> TextBox 2.0 is an up-to-date text generation library based on Python and PyTorch focusing on building a unified and standardized pipeline for applying pre-trained language models to text generation:

### ThoughtSource

> "ThoughtSource is a central, open resource and community centered on data and tools for Chain-of-Thought reasoning in Large Language Models (Wei 2022). Our long-term goal is to enable trustworthy and robust reasoning in advanced AI systems for driving scientific research and medical practice."

## Misc.

### GPT Index

> GPT Index is a project consisting of a set of data structures designed to make it easier to use large external knowledge bases with LLMs

### Deforum

> AI animated videos

### Visual Prompt Builder

> Build prompts, visually

### Interactive Composition Explorer

> ICE is a Python library and trace visualizer for language model programs.

### PTPT - Prompt To Plain Text

> PTPT is an command-line tool that allows you to easily convert plain text files using pre-defined prompts with the help of ChatGPT. With PTPT, you can effortlessly create and share prompt formats, making collaboration and customization a breeze. Plus, by subscribing, you gain access to even more prompts to enhance your experience. If you're interested in [prompt engineering](https://learnprompting.org/vocabulary/prompt_engineering), you can use PTPT to develop and share your prompts.

### Orquesta AI Prompts

> Low-code collaboration platform for AI Prompts

- Full prompt lifecycle management (from ideation to feedback collection)
- Enterprise-grade features and security
- Support for public, private, and custom LLMs
- Prompts based on custom context and business rules. Evaluations on the Edge
- Real-time logging and collection of performance and prompt economics

### LMQL

> LMQL is a specialized query language designed for working with language models like OpenAI's GPT series. LMQL enables users to perform complex queries and retrieve specific information from language models efficiently. It allows users to perform structured queries, similar to SQL, and utilize condintional logic within the queries to refine and control output.

### LLMStack

> LLMStack is LMStack is an open-source, no-code platform for building [generative AI applications](https://learnprompting.org/docs/basics/generative_ai_applications), chatbots, agents and interfacing them with your data and business processes.

- combines the power of AI with information retreival
- enables users to create and access their applications with interface of choice
- supports multimodal features within applications
- provides viewer and collaborator roles to allow multiple users to modify and build the app together

### Other

[https://gpttools.com](https://gpttools.com/)

## Footnotes

### Sander Schulhoff

Sander Schulhoff is the CEO of HackAPrompt and Learn Prompting. He created the first Prompt Engineering guide on the internet, two months before ChatGPT was released, which has taught 3 million people how to prompt ChatGPT. He also partnered with OpenAI to run the first AI Red Teaming competition, HackAPrompt, which was 2x larger than the White House's subsequent AI Red Teaming competition. Today, HackAPrompt partners with the Frontier AI labs to produce research that makes their models more secure. Sander's background is in Natural Language Processing and deep reinforcement learning. He recently led the team behind The Prompt Report, the most comprehensive study of prompt engineering ever done. This 76-page survey, co-authored with OpenAI, Microsoft, Google, Princeton, Stanford, and other leading institutions, analyzed 1,500+ academic papers and covered 200+ prompting techniques.