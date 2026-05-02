# Requirements Document

## Introduction

JupyterLab上でLean4の定理証明支援言語を実行できるpodman compose環境を構築する。ユーザーはnotebookインターフェースからLean4コードを記述・実行でき、オプションとして数式の可視化機能も提供する。

## Glossary

- **JupyterLab**: ブラウザベースのインタラクティブ開発環境。notebookインターフェースを提供する
- **Lean4**: 依存型理論に基づく定理証明支援言語および関数型プログラミング言語
- **Lean4 Kernel**: JupyterのカーネルプロトコルをLean4向けに実装したコンポーネント（lean4-jupyter等）
- **podman compose**: Podmanコンテナエンジン上でDocker Compose互換の複数コンテナ環境を管理するツール
- **Notebook**: JupyterLabで使用するインタラクティブなドキュメント形式（.ipynb）
- **MathJax/KaTeX**: ブラウザ上でLaTeX数式をレンダリングするライブラリ
- **可視化サービス**: notebookセッションの変数や数式をレンダリング・表示するサービス

## Requirements

### Requirement 1

**User Story:** 開発者として、podman composeコマンド一つで環境を起動し、JupyterLabにアクセスできるようにしたい。そうすることで、環境構築の手間なくLean4の学習・開発を始められる。

#### Acceptance Criteria

1. THE podman compose environment SHALL start all required services with a single `podman compose up` command.
2. WHEN the environment starts, THE JupyterLab service SHALL be accessible via a web browser on a configurable port (default: 8888).
3. WHEN the environment starts, THE JupyterLab service SHALL be ready to accept connections within 120 seconds.
4. IF the JupyterLab service fails to start, THEN THE podman compose environment SHALL output an error message to the container logs.

### Requirement 2

**User Story:** 開発者として、JupyterLabのnotebookからLean4コードを記述・実行したい。そうすることで、インタラクティブにLean4の定理証明や関数型プログラミングを試せる。

#### Acceptance Criteria

1. WHEN a user creates a new notebook, THE JupyterLab interface SHALL offer a Lean4 kernel as a selectable option.
2. WHEN a user executes a Lean4 code cell, THE Lean4 Kernel SHALL evaluate the code and return the result or error message to the notebook cell output.
3. WHEN a Lean4 code cell contains a syntax error, THE Lean4 Kernel SHALL return a descriptive error message in the cell output.
4. THE JupyterLab container SHALL include a pre-installed Lean4 toolchain (elan, lean, lake) accessible to the Lean4 Kernel.

### Requirement 3

**User Story:** 開発者として、notebookに含まれるサンプルコードを通じてLean4の基本的な使い方を確認したい。そうすることで、環境が正しく動作していることをすぐに検証できる。

#### Acceptance Criteria

1. THE JupyterLab container SHALL include at least one sample notebook demonstrating basic Lean4 code execution.
2. WHEN a user opens the sample notebook and runs all cells, THE Lean4 Kernel SHALL produce expected outputs without errors.

### Requirement 4

**User Story:** 開発者として、notebookセッション内の変数や数式をLaTeX形式で可視化したい。そうすることで、数学的な概念や証明の構造を視覚的に確認できる。

#### Acceptance Criteria

1. WHERE the visualization feature is enabled, THE system SHALL render Lean4 expressions and type signatures as LaTeX-formatted mathematical notation in notebook cell outputs.
2. WHEN a user calls a visualization function in a Lean4 cell, THE system SHALL display the corresponding mathematical formula rendered by MathJax or KaTeX.
3. WHERE the visualization feature is implemented as a separate service, THE JupyterLab container SHALL be able to communicate with the visualization service over the podman compose internal network.
4. IF the visualization service is unavailable, THEN THE system SHALL display the raw text representation of the expression as a fallback.

### Requirement 5

**User Story:** 開発者として、コンテナを再起動してもnotebookファイルや作業内容が失われないようにしたい。そうすることで、安心して作業を中断・再開できる。

#### Acceptance Criteria

1. THE podman compose environment SHALL mount a host directory as a volume into the JupyterLab container for persistent notebook storage.
2. WHEN a user saves a notebook, THE notebook file SHALL be written to the mounted volume and persist after container restart.
