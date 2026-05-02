# Implementation Plan

- [x] 1. Dockerfileの作成





  - Ubuntu 24.04ベースでelan（Lean4バージョンマネージャ）をインストールするDockerfileを作成する
  - elan経由でlean4とlakeをインストールする手順を記述する
  - JupyterLab、lean4-jupyter、sympy、matplotlib、ipywidgetsをpipでインストールする
  - lean4-jupyterカーネルを `python -m lean4_jupyter.install` で登録する手順を追加する
  - _Requirements: 2.4, 2.1_

- [ ] 2. podman-compose.ymlの作成


  - [ ] 2.1 compose設定ファイルを作成する
    - `./docker/Dockerfile` をビルドするjupyterlabサービスを定義する
    - ポート8888をホストに公開する設定を追加する
    - `./notebooks` を `/home/jovyan/work` にバインドマウントする設定を追加する
    - `JUPYTER_TOKEN` 環境変数とJupyterLab起動コマンドを設定する
    - _Requirements: 1.1, 1.2, 5.1_
  - [ ] 2.2 .envファイルのサンプルを作成する
    - `JUPYTER_TOKEN` のデフォルト値を含む `.env.example` を作成する
    - _Requirements: 1.2_

- [ ] 3. 可視化ヘルパーモジュールの実装
  - `notebooks/lean4_viz.py` を作成する
  - `show_latex(latex_str)` 関数を実装する（`IPython.display.Math` を使用）
  - `show_expr(lean_expr_str)` 関数を実装する（テキストをLaTeX風にフォーマットして表示）
  - 不正な入力に対してtry/exceptでフォールバックテキスト表示を実装する
  - _Requirements: 4.1, 4.2, 4.4_

- [ ] 4. サンプルnotebookの作成
  - `notebooks/lean4_intro.ipynb` を作成する
  - `#eval 1 + 1` など基本的なLean4コード実行セルを追加する
  - `#check Nat.add_zero` など型チェックのセルを追加する
  - 簡単な定理証明のセルを追加する
  - `lean4_viz` を使った数式可視化のデモセルを追加する
  - _Requirements: 3.1, 3.2, 4.2_

- [ ] 5. プロジェクト構成ファイルの整備
  - `README.md` に起動手順（`podman compose up --build`）とアクセス方法を記述する
  - `.gitignore` にコンテナビルドキャッシュや一時ファイルを追加する
  - _Requirements: 1.1, 1.2_
