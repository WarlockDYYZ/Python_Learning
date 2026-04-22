import pandas as pd


def calculate_matched_consumption():
    # 1. 读取两个 Excel 文件
    # 假设数据都在第一个 Sheet 中，如果有特定 Sheet 名，可以添加 sheet_name='Sheet1'
    try:
        df_charge = pd.read_excel(r'C:\Users\Administrator\Desktop\4月快手充值.xlsx')
        df_source = pd.read_excel(r'C:\Users\Administrator\Desktop\11.xlsx')
        print("✅ 文件读取成功")
    except FileNotFoundError:
        print("❌ 错误：找不到文件，请确认 '充值表.xlsx' 和 '11.xlsx' 在当前目录下")
        return

    match_key = "营业执照"
    column_name1 = "真新客累计消耗现金金额"
    column_name2 = "假新客累计消耗现金金额"

    # 2. 数据预处理（可选，但推荐）
    # 为了防止因为空格导致匹配失败（例如 "A1001" 和 "A1001 "），建议去除首尾空格
    # 假设 C列 和 A列 都是字符串类型，如果是数字类型则不需要 astype(str)
    # 这里为了保险起见，统一转为字符串并去空格
    df_charge[match_key] = df_charge.iloc[:, 2].astype(str).str.strip()  # 获取C列（索引为2）
    df_source[match_key] = df_source.iloc[:, 0].astype(str).str.strip()  # 获取A列（索引为0）

    # 3. 跨表匹配 (Merge)
    # on='匹配键': 使用刚才创建的临时列进行匹配
    # how='left': 左连接，保留充值表的所有行。如果11.xlsx中没有对应的值，消耗列会显示为 NaN
    merged_df = pd.merge(
        df_charge[[match_key]],
        df_source[[match_key, column_name1, column_name2]],
        on=match_key,
        how='left',
        suffixes=('', '_source')  # 防止列名冲突
    )

    # 4. 计算总和
    # 检查列是否存在，防止报错
    if column_name1 not in merged_df.columns or column_name2 not in merged_df.columns:
        print("❌ 错误：在 '11.xlsx' 中找不到 '真新客消耗' 或 '假新客消耗' 列，请检查表头。")
        return

    # 填充 NaN 为 0，防止计算出错（即匹配不到的行消耗视为0）
    merged_df[column_name1] = merged_df[column_name1].fillna(0)
    merged_df[column_name2] = merged_df[column_name2].fillna(0)

    # 1. 从合并后的大表中，只选出我们需要的三列
    result_df = merged_df[[column_name1, column_name2]]

    # 2. 计算并添加“消耗总和”列
    result_df['消耗总和'] = result_df[column_name1] + result_df[column_name2]

    # 3. 最后，将“营业执照”列设置为索引
    result_df.index = merged_df[match_key]
    result_df.index.name = match_key  # 为索引列命名

    # 5. 保存结果
    output_file = r'C:\Users\Administrator\Desktop\消耗情况.xlsx'
    result_df.to_excel(output_file, index=True)
    print(f"✅ 处理完成！仅包含消耗值的文件已保存为：{output_file}")

    # (可选) 打印总和供快速查看
    print(f"📊 统计：真新客总消耗={result_df[column_name1].sum()}, 假新客总消耗={result_df[column_name2].sum()}")


if __name__ == "__main__":
    calculate_matched_consumption()
