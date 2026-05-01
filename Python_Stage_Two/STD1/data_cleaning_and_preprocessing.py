import pandas as pd
import numpy as np
import click


# 创建工具箱 工具名：data_cleaner
@click.group()
def data_cleaner():
    """Data cleaning and preprocessing tool"""
    pass


@data_cleaner.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), help='Cleaned output file')
# --dropna 例：--dropna name --dropna age → 删除这些列里有空值的行
@click.option('--dropna', multiple=True, help='Columns to drop NA values')
# --fillna age 0→ 把 指定 列的空值填成 0
@click.option('--fillna', nargs=2, multiple=True, help='Column and value to fill NA')
# --convert-date date → 把 date 列转成标准日期格式
@click.option('--convert-date', multiple=True, help='Columns to convert to date')
def clean(input_file, output, dropna, fillna, convert_date):
    """Clean data by handling missing values and converting data types"""
    df = pd.read_csv(input_file)

    # 处理缺失值
    if dropna:
        # 只要指定的列里有空，整行删掉！
        df = df.dropna(subset=list(dropna))
    # 填充空值
    if fillna:
        # 根据传入参数填充空值，如(age, 0)
        for col, value in fillna:
            df[col] = df[col].fillna(value)
    # 转换日期格式，转换成 pandas 能识别的时间类型
    if convert_date:
        for col in convert_date:
            df[col] = pd.to_datetime(df[col])

    # 输出结果
    if output:
        df.to_csv(output, index=False)
        click.echo(f"Cleaned data saved to {output}")
    else:
        click.echo("Cleaned data preview:")
        click.echo(df.head())


@data_cleaner.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--column', help='Column to analyze')
@click.option('--threshold', type=float, default=3.0, help='Z-score threshold for outliers')
def detect_outliers(input_file, column, threshold):
    """Detect outliers using Z-score method"""
    df = pd.read_csv(input_file)

    if column not in df.columns:
        click.echo(f"Error: Column '{column}' not found")
        return

    from scipy.stats import zscore

    z_scores = zscore(df[column])
    # 筛选所有异常值
    outliers = df[np.abs(z_scores) > threshold]
    # 输出异常值数量
    click.echo(f"Detected {len(outliers)} outliers:")
    # 显示异常值
    click.echo(outliers[[column]])
    # 输出示例
    # Detected 1 outliers:
    #   price
    # 3 1000


if __name__ == '__main__':
    data_cleaner()
