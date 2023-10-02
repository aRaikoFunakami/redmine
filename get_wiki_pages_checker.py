import pandas as pd
import argparse
import matplotlib.pyplot as plt

# コマンドライン引数の解析
parser = argparse.ArgumentParser(description='Read a CSV file into a DataFrame.')
parser.add_argument('file_name', type=str, help='Name of the CSV file to read.')
args = parser.parse_args()

# DataFrameの読み込み
try:
    df = pd.read_csv(args.file_name)
except FileNotFoundError:
    print(f"File {args.file_name} not found.")
    exit(1)

# 'journals'列の各要素の文字数を計算
df['journals_length'] = df['journals'].apply(lambda x: len(str(x)) if x is not None else 0)

# グラフの作成
plt.figure(figsize=(10, 6))
plt.bar(df.index, df['journals_length'])
plt.xlabel('Index')
plt.ylabel('Journals Length')
plt.title('Length of Journals by Index')

# グラフをファイルに保存
plt.savefig(f"get_wiki_pages_checker.png")

# グラフを表示（必要に応じて）
# plt.show()
