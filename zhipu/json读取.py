import json
import os

def read_json_content_by_index(folder_path, index):
    try:
        # 获取文件夹中的所有文件
        files = os.listdir(folder_path)

        # 筛选出JSON文件
        json_files = [file for file in files if file.endswith('.json')]

        # 检查索引是否有效
        if index < 0 or index >= len(json_files):
            print(f"索引 {index} 超出范围")
            return

        # 获取指定索引的文件名
        file_name = json_files[index]
        file_path = os.path.join(folder_path, file_name)

        # 打开文件并读取JSON数据
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 提取content字段
        contents = [item['content'] for item in data if 'content' in item]

        return contents
    except FileNotFoundError:
        print(f"文件夹 {folder_path} 未找到")
    except json.JSONDecodeError:
        print(f"文件 {file_path} 不是有效的JSON格式")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")


# 指定文件夹路径和文件索引
folder_path = 'save_json'
index = 0  # 例如，读取第一个JSON文件

# 调用函数并打印结果
contents = read_json_content_by_index(folder_path, index)
if contents:
    for content in contents:
        print(content)