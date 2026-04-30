import argparse
import pandas as pd


def main():
    # 复习的时候记得，把这个命令行工具，整合进你之前的 DataPreprocessor 类 ####################################################
    parser = argparse.ArgumentParser(description='Data analysis tool')
    # 位置参数：输入文件
    parser.add_argument('input_file', help='Input CSV file')
    # 可选参数：输出文件
    parser.add_argument('-o', '--output', help='Output file path')
    # 可选参数：分析类型
    parser.add_argument('--analysis-type', choices=['summary', 'plot', 'stats'],
                        default='summary', help='Type of analysis to perform')
    # 可选参数：日期列
    parser.add_argument('--date-column', help='Name of date column')
    args = parser.parse_args()

    # 读取数据
    df = pd.read_csv(args.input_file)
    # 根据分析类型执行相应操作
    if args.analysis_type == 'summary':
        print("Data summary:")
        # 输出数据的统计概要（均值、最大最小、数量等）
        print(df.describe())
    elif args.analysis_type == 'plot':
        import matplotlib.pyplot as plt
        # 用日期列画折线图，保存成图片
        plt.plot(df[args.date_column], df['value'])
        plt.savefig(args.output)
    elif args.analysis_type == 'stats':
        print("Statistical analysis:")
        print(f"Mean: {df['value'].mean()}")
        print(f"Median: {df['value'].median()}")
        print(f"Standard deviation: {df['value'].std()}")


if __name__ == '__main__':
    main()
