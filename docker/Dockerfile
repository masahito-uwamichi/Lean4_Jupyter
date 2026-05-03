FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/.elan/bin:${PATH}"

# システム依存パッケージのインストール
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# elan（Lean4バージョンマネージャ）のインストール
RUN curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
    | sh -s -- -y --default-toolchain leanprover/lean4:stable

# lean4とlakeが利用可能であることを確認
RUN lean --version && lake --version

# lean4-jupyter が必要とする Lean4 REPL のビルド
# repl はプロジェクトディレクトリごと残す必要がある（lake環境が必要なため）
RUN git clone https://github.com/leanprover-community/repl.git /opt/repl \
    && cd /opt/repl \
    && lake build

# repl をラッパースクリプト経由でPATHに追加
# lake env repl は lakefile.lean があるディレクトリで実行する必要がある
RUN printf '#!/bin/sh\ncd /opt/repl && exec .lake/build/bin/repl "$@"\n' > /usr/local/bin/repl \
    && chmod +x /usr/local/bin/repl

# Python パッケージのインストール
RUN pip3 install --no-cache-dir --break-system-packages \
    jupyterlab \
    lean4-jupyter \
    sympy \
    matplotlib \
    ipywidgets

# lean4-jupyterカーネルの登録
RUN python3 -m lean4_jupyter.install

# lean4_jupyter が lake env repl を /opt/repl で実行するようにパッチ
RUN sed -i 's|pexpect.spawn("lake env repl"|pexpect.spawn("lake env repl", cwd="/opt/repl"|' \
    /usr/local/lib/python3.12/dist-packages/lean4_jupyter/repl.py

# 作業ディレクトリの作成
RUN mkdir -p /home/jovyan/work
WORKDIR /home/jovyan/work

EXPOSE 8888
