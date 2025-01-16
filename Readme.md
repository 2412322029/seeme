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
如:`python(w) report.py run -u 服务器地址 -k 'your key'`


添加命令别名和使用环境变量更加方便powershell打开个人配置文件`notepad $PROFILE`添加以下内容
```powershell
$env:REPORT_KEY="your key"
$env:REPORT_URL="服务器地址"

function get-report {
    python path\to\report.py @Args
}
function get-reportw {
    pythonw path\to\report.py @Args
}
Set-Alias -Name report -Value get-report
Set-Alias -Name reportw -Value get-reportw
```
### 浏览器端

使用油猴脚本(安装油猴扩展,谷歌扩展商店下载)
复制`自动汇报.js`内容到自定义新脚本

安装后首次弹窗输入key,api,油猴菜单查看/重置信息

启用后右上角会有上传按钮,编辑确认好(当心url中的敏感信息,?参数默认全部去除)上传,在油猴中管理排除的网站

### ~~安卓端~~

使用MacroDroid,导入`自动汇报.macro`到软件,修改 动作>http请求>配置>查询参数中的key的值为your key

![QQ截图20250108211239](https://github.com/user-attachments/assets/6ca9ef7c-8011-40be-a367-cab4908fe97c)
