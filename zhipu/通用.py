import os
from zhipuai import ZhipuAI
import json
from datetime import datetime

""""增加流式传输"""

# 替换为你的API Key
api_key = "c6e0af4cc4dba662ef4cb15023f08f1b.9g4gjNVUOn7y8XlH"

# 初始化客户端
client = ZhipuAI(api_key=api_key)

# 初始化对话历史
conversation_history = []

# 设置系统提示
system_prompt = ["当你回答一个知识点的时候，说明它的原理，并有详细的列子，而且运用类比的方法，帮助我理解",'对代码进行解释，并说说它类似于python的什么代码，以及有什么是python没有的',
                 '你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。']

def save_conversation_to_file(conversation, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(conversation, f, ensure_ascii=False, indent=4)

def get_current_time_filename():
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"conversation_{current_time}.json"

def ensure_directory_exists(directory):
   if not os.path.exists(directory):
       os.makedirs(directory)

def main():
    global conversation_history
    print("欢迎使用智谱清言助手！输入'exit'结束对话。")

    # 确保保存文件的目录存在
    save_directory = "save_json"
    ensure_directory_exists(save_directory)

    while True:
        # 用户输入
        user_input = input("用户：")
        if user_input.lower() == 'exit':
            print("对话结束。")
            break

        # 更新对话历史
        conversation_history.append({"role": "user", "content": user_input})

        # 调用API进行流式传输
        response = client.chat.completions.create(
            model="glm-4-plus",
            messages=[
                {"role": "system", "content": system_prompt[2]},
                *conversation_history
            ],
            stream=True
        )

        # 累积流式传输的结果
        assistant_reply = ""
        for chunk in response:
            content = chunk.choices[0].delta.content if chunk.choices[0].delta.content else ""
            assistant_reply += content
            print(content, end="", flush=True)

        # 更新对话历史
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        print()  # 打印换行符，以便区分不同的回复

    # 保存对话历史到文件
    filename = get_current_time_filename()
    save_path = os.path.join(save_directory, filename)
    save_conversation_to_file(conversation_history, save_path)
    print(f"对话历史已保存到文件：{save_path}")


if __name__ == "__main__":
    main()