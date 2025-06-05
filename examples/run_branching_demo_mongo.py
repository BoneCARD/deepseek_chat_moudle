"""
run_branching_demo_mongo.py
---------------------------
• 会话数据写入远程 MongoDB
  示例 URI:  mongodb://ds_user:ds_pwd@127.0.0.1:27017
  （若无密码，改成 mongodb://127.0.0.1:27017）
"""

from deepseek_chat import create_session, continue_chat, get_tree

API_KEY   = "sk-44ccb84c5b8a49aa8a75f2320d79d1e9"
BASE      = "https://api.deepseek.com"
# MONGO_URI = "mongodb://ds_user:ds_pwd@127.0.0.1:27017"   # ★ 带账号密码
MONGO_URI = "mongodb://127.0.0.1:27017"   # ★ 带账号密码

# ------- ① 创建根节点 ------------------------------------------------
answer, sess_id, root_id = create_session(
    system_prompt="你好，我是助手。",
    question="帮我推荐一部电影。",
    api_key=API_KEY, base_url=BASE,
    store_backend="mongo",           # 默认也是 mongo，这里显式写
    mongo_uri=MONGO_URI,             # ★ 指向带凭证的 Mongo
)
print("[root]", answer, "\n")

# ------- ② 线性追问 --------------------------------------------------
answer_a, node_a = continue_chat(
    session_id=sess_id,
    parent_node_id=root_id,
    question="能不能再详细介绍一下剧情？",
    api_key=API_KEY, base_url=BASE,
    store_backend="mongo",
    mongo_uri=MONGO_URI,
)
print("[child_A]", answer_a, "\n")

# ------- ③ root 再分支 ----------------------------------------------
answer_b, node_b = continue_chat(
    session_id=sess_id,
    parent_node_id=root_id,
    question="有没有同类型、但评分更高的电影？",
    api_key=API_KEY, base_url=BASE,
    store_backend="mongo",
    mongo_uri=MONGO_URI,
)
print("[child_B]", answer_b, "\n")

# ------- ④ child_A 再分支 -------------------------------------------
answer_c, node_c = continue_chat(
    session_id=sess_id,
    parent_node_id=node_a,
    question="这部电影的导演还拍过哪些代表作？",
    api_key=API_KEY, base_url=BASE,
    store_backend="mongo",
    mongo_uri=MONGO_URI,
)
print("[grandchild_C]", answer_c, "\n")

# ------- ⑤ 打印整棵树 -----------------------------------------------
def print_tree(node: dict, indent: int = 0):
    pad = "    " * indent
    print(f"{pad}- node_id={node['id']}  user→ {node['user_question']}")
    print(f"{pad}  ↳ assistant: {node['assistant_answer'][:60]}…\n")
    for ch in node.get("children", []):
        print_tree(ch, indent + 1)

print("\n========  FULL TREE (mongo)  ========\n")
tree = get_tree(
    sess_id, api_key=API_KEY, base_url=BASE,
    store_backend="mongo", mongo_uri=MONGO_URI,
)
print_tree(tree)
