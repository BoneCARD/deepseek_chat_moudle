"""
run_branching_demo_file.py
--------------------------
• 会话数据保存在本地 JSON 文件（~/.deepseek_chat/history.json）
• 不依赖 MongoDB
"""

from deepseek_chat import create_session, continue_chat, get_tree

API_KEY = "sk-44ccb84c5b8a49aa8a75f2320d79d1e9"                       # 建议改成 env 变量
BASE    = "https://api.deepseek.com"

# ------- ① 创建根节点 ------------------------------------------------
answer, sess_id, root_id = create_session(
    system_prompt="你好，我是助手。",
    question="帮我推荐一部电影。",
    api_key=API_KEY,
    base_url=BASE,
    store_backend="file",                # ★ 关键切换
    json_path="./my_history.json",  # 可自定义文件位置
)
print("[root]", answer, "\n")

# ------- ② 线性追问 --------------------------------------------------
answer_a, node_a = continue_chat(
    session_id=sess_id,
    parent_node_id=root_id,
    question="能不能再详细介绍一下剧情？",
    api_key=API_KEY, base_url=BASE,
    store_backend="file",
    json_path="./my_history.json",  # 可自定义文件位置
)
print("[child_A]", answer_a, "\n")

# ------- ③ root 再分支 ----------------------------------------------
answer_b, node_b = continue_chat(
    session_id=sess_id,
    parent_node_id=root_id,
    question="有没有同类型、但评分更高的电影？",
    api_key=API_KEY, base_url=BASE,
    store_backend="file",
    json_path="./my_history.json",  # 可自定义文件位置
)
print("[child_B]", answer_b, "\n")

# ------- ④ child_A 再分支 -------------------------------------------
answer_c, node_c = continue_chat(
    session_id=sess_id,
    parent_node_id=node_a,
    question="这部电影的导演还拍过哪些代表作？",
    api_key=API_KEY, base_url=BASE,
    store_backend="file",
    json_path="./my_history.json",  # 可自定义文件位置
)
print("[grandchild_C]", answer_c, "\n")

# ------- ⑤ 打印整棵树 -----------------------------------------------
def print_tree(node: dict, indent: int = 0):
    pad = "    " * indent
    print(f"{pad}- node_id={node['id']}  user→ {node['user_question']}")
    print(f"{pad}  ↳ assistant: {node['assistant_answer'][:60]}…\n")
    for ch in node.get("children", []):
        print_tree(ch, indent + 1)

print("\n========  FULL TREE (file)  ========\n")
tree = get_tree("e8ed38b8-839c-4dbf-9f90-229632578bff", api_key=API_KEY, base_url=BASE, store_backend="file", json_path="./my_history.json")
print_tree(tree)
