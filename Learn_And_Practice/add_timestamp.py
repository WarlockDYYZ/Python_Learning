from datetime import datetime
import os
import re


folder_path = r"C:\Users\Administrator\Desktop\Temp"

def clean_filename(filename):
    # 1. 分离文件名和扩展名，防止把 .xlsx 等后缀也误删了
    name, ext = os.path.splitext(filename)

    timestamp = datetime.now().timestamp()
    dt_object = datetime.fromtimestamp(timestamp)
    formatted_time = dt_object.strftime("%Y-%m-%d-%H-%M-%S-")

    new_name = formatted_time + name

    return new_name + ext


def batch_rename(directory):
    if not os.path.exists(directory):
        print(f"❌ 错误：文件夹路径不存在，请检查！ -> {directory}")
        return

    renamed_count = 0
    # 遍历文件夹下的所有文件
    for filename in os.listdir(directory):

        if filename == "add_timestamp.py":
            continue

        file_path = os.path.join(directory, filename)

        # 只处理文件，跳过子文件夹
        if os.path.isfile(file_path):
            new_filename = clean_filename(filename)
            new_file_path = os.path.join(directory, new_filename)

            # 如果新旧文件名不一样，才执行重命名
            if filename != new_filename:
                # 防止因为去后缀导致文件名完全相同而报错（例如 a(1).xlsx 和 a.xlsx 同时存在）
                if os.path.exists(new_file_path):
                    print(f"⚠️ 跳过：目标文件已存在，无法重命名 -> {filename}")
                    continue

                try:
                    os.rename(file_path, new_file_path)
                    print(f"✅ 已重命名：{filename}  ->  {new_filename}")
                    renamed_count += 1
                except Exception as e:
                    print(f"❌ 失败：{filename}，错误信息：{e}")

    print(f"\n🎉 处理完成！共成功清理了 {renamed_count} 个文件。")


if __name__ == '__main__':
    batch_rename(folder_path)