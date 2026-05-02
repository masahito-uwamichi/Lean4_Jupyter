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

# Python パッケージのインストール
RUN pip3 install --no-cache-dir --break-system-packages \
    jupyterlab \
    lean4-jupyter \
    sympy \
    matplotlib \
    ipywidgets

# lean4-jupyterカーネルの登録
RUN python3 -m lean4_jupyter.install

# 作業ディレクトリの作成
RUN mkdir -p /home/jovyan/work
WORKDIR /home/jovyan/work

EXPOSE 8888
