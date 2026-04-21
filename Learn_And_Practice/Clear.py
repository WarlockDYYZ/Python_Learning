import os
import re
import sys

# ================= 配置区域 =================
# 这里直接写死了你提供的路径
TARGET_FOLDER = r"C:\Users\Administrator\Desktop\Daily_Report"


# ===========================================

def clean_filename(filename):
    """
    去除文件名末尾的 '年月(1)(1)...' 后缀
    逻辑：保留扩展名，去除 扩展名前的 数字+括号组合
    """
    # 分离文件名和扩展名
    name, ext = os.path.splitext(filename)

    if not ext:
        return filename

    # 正则解释:
    # \d{4,8}   : 匹配 4到8位数字 (如 2026, 202603, 20260326)
    # (\(\d+\))*: 匹配紧随其后的任意数量的括号数字，如 (1), (1)(1)
    # $         : 确保匹配到字符串末尾
    pattern = r'\d{4,8}(\(\d+\))*$'

    new_name = re.sub(pattern, '', name)

    if new_name != name:
        return new_name + ext
    else:
        return filename


def main():
    # 检查路径是否存在
    if not os.path.exists(TARGET_FOLDER):
        print(f"❌ 错误：找不到文件夹路径 -> {TARGET_FOLDER}")
        print("请检查路径是否正确，或者文件夹是否被移动/删除。")
        return

    if not os.path.isdir(TARGET_FOLDER):
        print(f"❌ 错误：{TARGET_FOLDER} 不是一个有效的文件夹。")
        return

    print(f"📂 正在处理目录: {TARGET_FOLDER}")
    print("-" * 60)

    count = 0
    skip_count = 0
    # 支持的文件类型
    supported_extensions = ('.xlsx', '.xls', '.csv', '.docx', '.doc', '.pdf', '.txt')

    try:
        files = os.listdir(TARGET_FOLDER)
    except PermissionError:
        print("❌ 权限错误：无法访问该文件夹，请以管理员身份运行或检查文件夹权限。")
        return

    for filename in files:
        # 只处理特定格式的文件
        if filename.lower().endswith(supported_extensions):
            new_filename = clean_filename(filename)

            if filename != new_filename:
                old_path = os.path.join(TARGET_FOLDER, filename)
                new_path = os.path.join(TARGET_FOLDER, new_filename)

                # 防止覆盖已有文件
                if os.path.exists(new_path):
                    print(f"⚠️  跳过: {filename}")
                    print(f"   原因: 目标文件 '{new_filename}' 已存在，避免覆盖！")
                    skip_count += 1
                else:
                    try:
                        os.rename(old_path, new_path)
                        print(f"✅ 重命名成功:")
                        print(f"   原: {filename}")
                        print(f"   新: {new_filename}")
                        count += 1
                    except Exception as e:
                        print(f"❌ 失败: {filename} - 错误信息: {e}")

    print("-" * 60)
    print(f"🎉 处理完成！")
    print(f"   成功重命名: {count} 个文件")
    if skip_count > 0:
        print(f"   因冲突跳过: {skip_count} 个文件")


if __name__ == "__main__":
    print("⚠️  即将处理文件夹：C:\\Users\\Administrator\\Desktop\\Daily_Report")
    print("此操作将直接修改文件名，建议先确认重要文件已备份。")
    user_input = input("按回车键开始执行，输入 'q' 退出: ")

    if user_input.lower() != 'q':
        main()
    else:
        print("操作已取消。")

    # 防止窗口一闪而过 (如果是双击运行的话)
    if sys.stdin.isatty():
        input("\n按回车键关闭窗口...")
