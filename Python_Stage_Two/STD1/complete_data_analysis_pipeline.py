import click
import pandas as pd
import matplotlib.pyplot as plt
import subprocess


# 创建工具箱
@click.group()
def data_pipeline():
    """Complete data analysis pipeline"""
    pass


@data_pipeline.command()
# nargs=-1 可以传入 任意数量 的文件（0 个、1 个、5 个、10 个都行）
# 例：python tool.py process 1.csv 2.csv 3.csv 4.csv -o output
@click.argument('input_files', nargs=-1, type=click.Path(exists=True))
@click.option('-o', '--output-dir', type=click.Path(), help='Output directory')
def process(input_files, output_dir):
    """Process multiple data files"""

    for file in input_files:
        # 执行数据清洗
        # 在 Python 代码里，调用并执行另一个 Python 脚本
        subprocess.run([
            'python', 'scripts/clean_data.py',
            file,
            f'--output={output_dir}/cleaned_{file}'
        ])

        # 执行数据分析
        subprocess.run([
            'python', 'scripts/analyze_data.py',
            f'{output_dir}/cleaned_{file}',
            f'--output={output_dir}/analysis_{file}'
        ])

        # 生成可视化
        subprocess.run([
            'python', 'scripts/visualize.py',
            f'{output_dir}/analysis_{file}',
            f'--output={output_dir}/plot_{file}.png'
        ])


@data_pipeline.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', type=click.Path(), help='Final report output')
@click.option('--value-column', default='value', help='Value column name')
def report(input_file, output, value_column):
    """Generate comprehensive analysis report"""

    # 读取分析结果
    analysis_data = pd.read_csv(input_file)

    # 生成报告内容
    report_text = "Data Analysis Reportn"
    report_text += "=" * 50 + "n"
    # 输出数据行数
    report_text += f"Number of records: {len(analysis_data)}n"
    # 输出平均值、中位数、标准差(保留两位小数)
    report_text += f"Mean value: {analysis_data[value_column].mean():.2f}n"
    report_text += f"Median value: {analysis_data[value_column].median():.2f}n"
    report_text += f"Standard deviation: {analysis_data[value_column].std():.2f}n"

    # 保存报告，到指定文件
    with open(output, 'w') as f:
        f.write(report_text)

    click.echo(f"Report generated: {output}")


if __name__ == '__main__':
    data_pipeline()
