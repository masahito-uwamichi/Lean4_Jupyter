# JupyterLab + Lean4 (podman compose)

podman compose を使って JupyterLab + Lean4 環境をワンコマンドで起動できるプロジェクトです。

## 必要なもの

- [Podman](https://podman.io/) および [podman-compose](https://github.com/containers/podman-compose)

```bash
# インストール例（Ubuntu/Debian）
sudo apt install podman
pip install podman-compose
```

## セットアップ

### 1. 環境変数の設定

`.env.example` をコピーして `.env` を作成します。

```bash
cp .env.example .env
```

必要に応じて `JUPYTER_TOKEN` を変更してください（デフォルト: `lean4dev`）。

```dotenv
JUPYTER_TOKEN=lean4dev
```

### 2. 起動

```bash
podman compose up --build
```

初回はイメージのビルドに数分かかります（Lean4 ツールチェーンのインストールを含むため）。

2回目以降はキャッシュが使われるため高速に起動します。

```bash
podman compose up
```

### 3. JupyterLab へのアクセス

起動後、ブラウザで以下の URL を開きます。

```
http://localhost:8888
```

トークン認証が求められた場合は、`.env` に設定した `JUPYTER_TOKEN` の値を入力してください。

URL にトークンを含めて直接アクセスすることもできます。

```
http://localhost:8888/?token=lean4dev
```

## 使い方

### Lean4 カーネルの選択

新しい notebook を作成する際に、カーネルとして **Lean 4** を選択してください。

### サンプル notebook

`notebooks/lean4_intro.ipynb` に基本的な使用例が含まれています。

- `#eval 1 + 1` などの式評価
- `#check Nat.add_zero` などの型チェック
- 簡単な定理証明
- `lean4_viz` を使った数式の LaTeX 表示

### 可視化ヘルパー（現状動きません）

`notebooks/lean4_viz.py` を使うと、数式を LaTeX 形式で表示できます。

```python
import lean4_viz
lean4_viz.show_latex(r"\forall x \in \mathbb{N}, x + 0 = x")
lean4_viz.show_expr("Nat.add_zero")
```

## notebook の永続化

`./notebooks` ディレクトリがコンテナ内の `/home/jovyan/work` にマウントされています。
コンテナを停止・再起動しても notebook ファイルは保持されます。

## 停止

```bash
podman compose down
```

## ポートの変更

デフォルトのポート（8888）を変更したい場合は、`docker-compose.yml` の `ports` セクションを編集してください。

```yaml
ports:
  - "9999:8888"  # ホスト側のポートを 9999 に変更
```

## トラブルシューティング

### コンテナログの確認

```bash
podman compose logs jupyterlab
```

### コンテナの再ビルド

依存パッケージを更新した場合などは `--build` オプションで再ビルドします。

```bash
podman compose up --build
```

### キャッシュを無視して完全再ビルド

```bash
podman compose build --no-cache
podman compose up
```
