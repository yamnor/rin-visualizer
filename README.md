# RIN Visualizer for HIV Protease

- HIV プロテアーゼ（A 鎖: 99 残基, B 鎖：99 残基）に、基質として 10 残基のアミノ酸ペプチドが結合した複合体について、アミノ酸残基相互作用（RIN）の解析結果を Web アプリ（`streamlit`アプリ）を用いて可視化する。

## 準備

- ローカル環境で解析するには、予め、`streamlit`を自分のパソコンにインストールしておく。
- このアプリは、MD 計算で得られた構造データを RIN 解析した結果を可視化するためのツールなので、RIN 解析そのものはおこなわない。

## 手順１：タンパク質の立体構造を可視化する

- タンパク質の立体構造（PDB 座標）を読み取って、各アミノ酸残基の Cα 炭素の３次元 xyz 座標データを [t-SNE](https://w.wiki/6CXt) を用いて２次元データに圧縮する。

### 手順１−１：アプリを起動する

#### クラウド環境で解析する場合

- https://vis-pdb.streamlit.app

#### ローカル環境で解析する場合

      streamlit run vis-pdb.py

### 手順１−２：アプリで解析する

- `Read a PDB file` で PDBファイルを読み込む。
  - あらかじめ、水やイオンを取り除いておく。
- `Perplexity` を調節する。
  - `Perplexity`は、**最近接探索の程度**を決めるパラメータ。
  - タンパク質の立体構造を適切に表現しているっぽいものを試行錯誤して見付ける。
  - 最大値は、データの個数。
  - HIV プロテアーゼの場合、これまでの経験的には、`100` 前後が良さそう。
- `Rotate` を調節する。
  - 表示されたものを適切に回転して、良い感じにする。
- `Download a node file` で、`node.txt` をダウンロードする。

### 補足事項

- HIV プロテアーゼにペプチドが結合した複合体に対する PDB ファイルを `example/protease.pdb` に置いている。
- クラウド環境（https://vis-pdb.streamlit.app）だと、t-SNE のプロセスに数分かかる。
  - １回だけだったら良いけれど、`Perplexity` や `Rotate` などのパラメータを変えながら何度も試行錯誤するのはつらい。
- この系について、あらかじめこのアプリで得られたデータを`example/node.txt`に置いている。
  - この手順１はスキップして、手順２では `example/node.txt` を利用してもよい。

## 手順２：RIN 解析の結果を可視化する

- RIN 解析で出力された `rin.fraction` を可視化する。

### 手順２−１：アプリを起動する

#### クラウド環境で解析する場合

- https://vis-rin.streamlit.app

#### ローカル環境で解析する場合

      streamlit run vis-rin.py

### 手順２−２：アプリで解析する

- `Read a node file` で、`node.txt`ファイルを読み込む。
- `Read a RIN fraction file`で、`rin.fraction`ファイルを読み込む。
  - `ring` ツールで出力されたもの。
- ２つの RIN 解析結果を比較するときには、`Read an another RIN fraction file`で、別の`rin.fraction`ファイルを読み込む。

### 補足事項

- この手順では、RIN の結果をグラフ化しているだけなので、クラウド環境でもまったく問題ない。

## 参考

- [sklearn.manifold.TSNE — scikit-learn 1.2.0 documentation](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html)
- [t-SNEを理解して可視化力を高める - Qiita](https://qiita.com/g-k/items/120f1cf85ff2ceae4aba)
