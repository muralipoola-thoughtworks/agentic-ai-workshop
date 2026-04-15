# Glossary

**What is `Node JS` ?**

> Node.js is an open-source, asynchronous, event-driven JavaScript runtime environment built on Chrome's V8 engine. It allows developers to run JavaScript code outside of a web browser, enabling backend server-side development. Node.js is designed for building scalable, high-performance network applications using non-blocking I/O. Can be installed using command: `brew install node`

**What is `npm` ?**

> npm (Node Package Manager) is the default package manager for Node.js, used to install, share, and manage dependencies (libraries/packages) in JavaScript projects. It consists of a command-line tool for managing local/global dependencies and a massive online registry containing over 2.1 million open-source packages. 

**What is `npx` ?**

> npx (Node Package Execute) is a powerful CLI tool bundled with npm (v5.2.0+) that allows you to execute JavaScript packages directly from the npm registry without installing them permanently. It solves global namespace pollution and versioning issues by downloading and running tools temporarily. 
DEV Community

**What is `uv` tool ?**

> uv is an extremely fast, Rust-based Python package and project manager designed to replace and unify tools like pip, pip-tools, pipx, poetry, pyenv, and virtualenv

**What is MCP ?**

> The `Model Context Protocol` (MCP) is an open-source standard introduced by Anthropic in 2024 that allows AI models to seamlessly connect with external data, tools, and software systems.

**What is MCP Inspector ?**

> The MCP Inspector is an interactive, browser-based developer tool designed to test and debug Model Context Protocol (MCP) servers locally. Often described as "Postman for MCP," it allows developers to connect to servers, inspect resources/tools, and validate JSON-RPC messages without needing a full AI client.  You can run MCP inspector using command :`npx @modelcontextprotocol/inspector@latest`

**What is `FastMCP` ?**

> `FastMCP` is a high-level Python framework designed to simplify building Model Context Protocol (MCP) servers and clients. It allows developers to quickly connect Large Language Models (LLMs) to local tools, data, and APIs using simple Python decorators, automatically managing schema generation, transport, and validation. It is considered the standard, developer-friendly way to build MCP applications. 

**What is `FastAPI` ?**

> `FastAPI` is a modern, high-performance web framework for building APIs with Python 3.8+ based on standard Python type hints. It is designed to be fast to code, easy to learn, and production-ready.


**What is `Uvicorn` ?**

> `Uvicorn` is a lightning-fast, lightweight ASGI (Asynchronous Server Gateway Interface) web server for Python, designed to run asynchronous frameworks like FastAPI and Starlette. It acts as a high-performance bridge between Python web applications and the HTTP client, enabling high concurrency.