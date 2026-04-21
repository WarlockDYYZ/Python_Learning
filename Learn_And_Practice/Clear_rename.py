import os
import shutil

# ================= 配置区域 =================
# 目标文件夹路径
TARGET_FOLDER = r"C:\Users\Administrator\Desktop\Daily_Report"

# 原始文件名 (包含后缀)
OLD_FILENAME = "M1以上及以下员工CPD统计(5).xlsx"

# 新文件名 (包含后缀)
NEW_FILENAME = "CPD.xlsx"


# ===========================================

def main():
    # 拼接完整路径
    old_path = os.path.join(TARGET_FOLDER, OLD_FILENAME)
    new_path = os.path.join(TARGET_FOLDER, NEW_FILENAME)

    print(f"🔍 正在检查文件: {old_path}")

    # 1. 检查原文件是否存在
    if not os.path.exists(old_path):
        print(f"❌ 错误：找不到文件 '{OLD_FILENAME}'")
        print(f"   请确认文件是否真的在文件夹：{TARGET_FOLDER} 中")
        print(f"   注意：文件名必须完全匹配，包括括号和空格。")

        # 辅助功能：列出文件夹内所有 xlsx 文件，方便用户核对文件名
        if os.path.exists(TARGET_FOLDER):
            print("\n💡 该文件夹下现有的 .xlsx 文件有：")
            for f in os.listdir(TARGET_FOLDER):
                if f.lower().endswith('.xlsx'):
                    print(f"   - {f}")
        return

    # 2. 检查新文件名是否已被占用
    if os.path.exists(new_path):
        print(f"⚠️  警告：目标文件 '{NEW_FILENAME}' 已存在！")
        choice = input("   是否覆盖现有文件？(输入 'y' 确认，其他键取消): ")
        if choice.lower() != 'y':
            print("❌ 操作已取消。")
            return
        else:
            print("   即将覆盖原文件...")

    # 3. 执行重命名
    try:
        os.rename(old_path, new_path)
        print("-" * 60)
        print("✅ 重命名成功！")
        print(f"   原文件名：{OLD_FILENAME}")
        print(f"   新文件名：{NEW_FILENAME}")
        print(f"   位置：{TARGET_FOLDER}")
        print("-" * 60)
    except PermissionError:
        print("❌ 失败：权限被拒绝。")
        print("   可能原因：文件正在被 Excel 或其他程序打开。")
        print("   解决方法：请先关闭所有打开的 Excel 文件，然后再运行此脚本。")
    except Exception as e:
        print(f"❌ 发生未知错误：{e}")


if __name__ == "__main__":
    main()
    input("\n按回车键退出...")
