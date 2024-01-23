FROM python:3.10.13-bullseye

# /appで作業を実施します。
WORKDIR /app
# ローカルのrequirements.txtをDockerコンテナ内部にコピー。
COPY ./docker/python/requirements.txt /app/requirements/requirements.txt
# Linuxで使うライブラリを取得
RUN apt-get update && apt-get install -y \
    tzdata \
&&  ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/*

# 上のライブラリ周りと合わせて、timezoneをAsia/Tokyoに
ENV TZ=Asia/Tokyo

#jupyter labなどの絶対に使用するライブラリをインストール
RUN python3 -m pip install --upgrade pip \
&&  pip install --no-cache-dir \
    black \
    jupyterlab \
    jupyterlab_code_formatter \
    jupyterlab-git \
    lckr-jupyterlab-variableinspector \
    jupyterlab_widgets \
    ipywidgets \
    import-ipynb

# pipでrequirements.txtのライブラリダウンロード
RUN python3 -m pip install --upgrade pip \
&&  pip install -r /app/requirements/requirements.txt
