git clone https://github.com/penggan00/usd.git
chmod +x ~/usd/usd.sh  
chmod +x ~/usd/setup.sh  
~/usd/setup.sh

sudo apt install python3.8-venv
python3 -m venv usd_venv
# 激活虚拟环境
source usd_venv/bin/activate

# 退出虚拟环境
deactivate


crontab -e