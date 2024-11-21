#!/bin/bash

# 进入 usd 目录
cd ~/usd || exit

# 创建虚拟环境
python3 -m venv usd_venv

# 激活虚拟环境
source usd_venv/bin/activate

# 安装 requirements.txt 中的库
pip install -r ~/usd/requirements.txt
pip install --upgrade pip

# 检查是否已存在对应的 crontab 任务
(crontab -l | grep -q '~/usd/usd.py') || (crontab -l; echo "15 14 * * * /bin/bash ~/usd/usd.sh") | crontab -

echo "设置完成！"

# 打开 .env 文件以便输入
nano ~/usd/.env
