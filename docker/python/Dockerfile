FROM python:3.10.12

# /appで作業を実施します。
WORKDIR /app
# ローカルのrequirements.txtをDockerコンテナ内部にコピーします。
COPY ./docker/python/requirements.txt /app/requirements/requirements.txt
# Linuxで使うライブラリを取得
RUN apt-get update && apt-get install -y \
    tzdata \
&&  ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/*

# 上のライブラリ周りと合わせて、timezoneをAsia/Tokyoに
ENV TZ=Asia/Tokyo

# pipアップグレード＋pipでrequirements.txtのライブラリダウンロード
RUN python3 -m pip install --upgrade pip \
&&  pip install -r /app/requirements/requirements.txt
