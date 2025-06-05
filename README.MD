[![PyPI version](https://img.shields.io/pypi/v/deepseek_chat_sdk.svg)](https://pypi.org/project/deepseek_chat_sdk/)
[![Downloads](https://static.pepy.tech/badge/deepseek_chat_sdk)](https://pepy.tech/project/deepseek_chat_sdk)

# 🛰️ deepseek-chat-sdk

**A thin, battle-tested Python wrapper around the DeepSeek `/chat/completions` API**  
with *built-in conversation-tree persistence*.

- **Drop-in call style** – mirrors `openai-python` (`messages=[…]`)  
- **Two storage back-ends**    
  *MongoDB* (default) **or** ultra-light *JSON file* – same API, switch in one flag  
- **Tree-structured memory** – each reply is a **node**; fork, branch & query whole tree  
- **Token-budget guard** – automatic context trimming (or raise)  
- **100 % sync code** – keep dependencies minimal, trivially pluggable into any code-base  

```text
pip install deepseek_chat          # from PyPI (or pip install -e .)
export DEEPSEEK_API_KEY=sk-...
````

---

## ⭐ Quick Start

```python
from deepseek_chat import create_session, continue_chat, get_tree

# --- root turn --------------------------------------------------------
answer, sess_id, root_id = create_session(
    system_prompt="你好，我是助手。",
    question="帮我推荐一部电影。",
    api_key="sk-...",                     # or rely on $DEEPSEEK_API_KEY
)
print(answer)

# --- branch off the same parent --------------------------------------
continue_chat(session_id=sess_id, parent_node_id=root_id,
              question="有没有同类型但评分更高的？")

# --- show the whole tree --------------------------------------------
print(get_tree(sess_id))
```

### Switch to local file storage (no Mongo)

```python
answer, sid, nid = create_session(
    system_prompt="你好！",
    question="今天杭州天气如何？",
    api_key="sk-...",
    store_backend="file",              # ← key flag
    json_path="./history.json",        # optional; default ~/.deepseek_chat/history.json
)
```

### Custom Mongo URI (user/pass, replica set …)

```python
import os
os.environ["DEEPSEEK_API_KEY"] = "sk-..."
answer, sid, nid = create_session(
    system_prompt="You are helpful.",
    question="Tell me a joke.",
    mongo_uri="mongodb://dbUser:dbPwd@mongo-1:27017,mongo-2:27017/?replicaSet=rs0",
)
```

---

## 🔧 Installation

```bash
# bare minimum
pip install deepseek_chat

# dev / tests / ruff
pip install "deepseek_chat"
pytest -q
```

| Dependency | Used for       | Optional?                             |
| ---------- | -------------- | ------------------------------------- |
| `requests` | REST calls     | ❌                                     |
| `pymongo`  | Mongo back-end | ✅ (not imported if you choose `file`) |
| `tiktoken` | token counting | ✅ (falls back to word count)          |

---

## 🗺️ API Surface

### Functional helpers (one-liners)

| function                                                 | returns                         | must pass                                  |
| -------------------------------------------------------- | ------------------------------- | ------------------------------------------ |
| `create_session(system_prompt, question, …)`             | `(answer, session_id, node_id)` | `system_prompt`, `question`                |
| `continue_chat(session_id, parent_node_id, question, …)` | `(answer, new_node_id)`         | `session_id`, `parent_node_id`, `question` |
| `get_tree(session_id, …)`                                | nested `dict`                   | `session_id`                               |

All take the same optional kwargs:

```text
api_key        DeepSeek API key (fallback $DEEPSEEK_API_KEY)
base_url       custom gateway (fallback $DEEPSEEK_BASE_URL)
model          deepseek-chat / deepseek-coder / …
store_backend  "mongo" | "file"   (default "mongo")
mongo_uri      mongodb connection string
json_path      path for file store
```

### Class-level control

Need multiple clients or stores side-by-side? Use the OOP facade:

```python
from deepseek_chat import ChatService, DeepSeekClient, FileStore

svc = ChatService(
    client=DeepSeekClient(api_key="sk-..."),
    store=FileStore("/tmp/ds_history.json"),
)

ans, sid, nid = svc.create_session(
    system_prompt="You are GPT-5",
    question="What's new in 2025?",
)
```

---

## ⚙️ Configuration matrix

| config source               | DeepSeek                                                                              | Mongo                  | File         |
| --------------------------- | ------------------------------------------------------------------------------------- | ---------------------- | ------------ |
| ENV var (default singleton) | `DEEPSEEK_API_KEY` `DEEPSEEK_BASE_URL`                                                | `MONGO_URI` `MONGO_DB` | —            |
| per-call kwargs             | `api_key=` `base_url=`                                                                | `mongo_uri=`           | `json_path=` |
| programmatic                | build your own `DeepSeekClient` + `ChatStore`/`FileStore` and pass into `ChatService` |                        |              |

---

## 📚 Advanced features

### JSON Output & Function Calling

Simply forward the native OpenAI-style params:

```python
client = DeepSeekClient(api_key="sk-...")

resp = client.chat(
    messages=[...],
    response_format={"type": "json_object"},
)

resp_tool = client.chat(
    messages=[...],
    tools=[{ "type": "function", "function": {...} }],
)
```

The higher-level helpers (`create_session`/`continue_chat`) accept **any extra
kwargs** and pass them straight to `DeepSeekClient.chat()`.

### Token-budget enforcement

`ensure_token_budget()` truncates eldest user/assistant pairs once total tokens
exceed the limit (default 32 k). Raise `TokenLimitExceeded` if **only** the
system prompt already exceeds the model context.

Set a custom limit:

```bash
export TOKEN_LIMIT=16000
```

---

## 🛠️ Project layout

```
deepseek_chat/
├── client.py        # DeepSeek REST wrapper
├── service.py       # high-level orchestration
├── store.py         # Mongo persistence
├── filestore.py     # JSON persistence
├── utils.py         # token helpers
└── __init__.py      # facade + functional helpers
```

Unit tests live under `tests/`, demo scripts under `examples/`.

---

## 🪄 Roadmap

* async variant (`httpx.AsyncClient`, `motor`)
* automatic summarisation for ultra-long histories
* plug-in hooks (on\_new\_message, on\_error)

Contributions welcome – just open an issue or PR.

---


