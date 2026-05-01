import click
import pandas as pd


@click.group()
# 创建一个名为cli的工具箱，可以放多个子命令（summary、plot...）
def cli():
    """Data analysis command line tool"""
    pass


@cli.command()
# 把函数变成终端命令，summary
@click.argument('input_file', type=click.Path(exists=True))
# 必须传的参数：输入 CSV 文件exists=True → 文件必须存在，否则报错
@click.option('-o', '--output', type=click.Path(), help='Output file path')
# 可选参数 -o 简写 --output 全写 用来指定输出文件
def summary(input_file, output):
    """Generate data summary"""
    df = pd.read_csv(input_file)
    summary_text = df.describe().to_string()
    if output:
        with open(output, 'w') as f:
            f.write(summary_text)
    else:
        click.echo(summary_text)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), help='Output image path')
@click.option('--x', help='X-axis column')
@click.option('--y', help='Y-axis column')
def plot(input_file, output, x, y):
    """Generate plot"""
    df = pd.read_csv(input_file)
    if not x or not y:
        click.echo("Error: Both --x and --y are required")
        return
    import matplotlib.pyplot as plt
    plt.plot(df[x], df[y])
    plt.savefig(output)
    click.echo(f"Plot saved to {output}")


# 运行文件 → 启动命令行工具
if __name__ == '__main__':
    cli()
