## 服务端
使用python flask服务器，mc查询使用mcstatus(安装flask,mcstatus)`pip insatll flask,mcstatus`

    templates文件夹，main,mcinfo文件是服务端

创建config.toml 填写SECRET_KEY = "your key" 记住这个key
```bash
python main.py
```
记住服务端地址(ip/域名)

## 报告端
报告端任选，有对应报告端就有对应数据显示(都在report文件夹中)
### pc报告端

使用python脚本(安装pygetwindow)`pip insatll pygetwindow`

report.py是一个报告命令行程序，定期向服务器发送当前正在玩儿什么，-h显示帮助
如:`python(w) report.py run -u http://服务器地址/pcinfo -k 'your key'`

### 浏览器端

使用油猴脚本(安装油猴扩展,谷歌扩展商店下载)
复制`自动汇报.js`内容到自定义新脚本，填写API_URL，SECRET

### 安卓端

使用MacroDroid,修改 动作>http请求>配置>查询参数中的key的值为your key