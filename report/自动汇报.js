// ==UserScript==
// @name         自动汇报
// @namespace    http://tampermonkey.net/
// @version      0.2
// @description  try to take over the world!
// @author       You
// @match        http://*/*
// @match        https://*/*
// @updateURL    https://raw.githubusercontent.com/2412322029/seeme/master/report/%E8%87%AA%E5%8A%A8%E6%B1%87%E6%8A%A5.js
// @downloadURL  https://raw.githubusercontent.com/2412322029/seeme/master/report/%E8%87%AA%E5%8A%A8%E6%B1%87%E6%8A%A5.js
// @grant        GM_xmlhttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_registerMenuCommand
// @icon         https://www.google.com/s2/favicons?sz=64&domain=github.com
// ==/UserScript==

(function() {
    'use strict';
    // 尝试从存储中获取 API_URL 和 SECRET
    const API_URL = GM_getValue('API_URL', '');
    const SECRET = GM_getValue('SECRET', '');
    //console.log(API_URL,SECRET)
    // 注册菜单
    GM_registerMenuCommand('显示/重置 API_URL 和 SECRET', function() {
        // 显示当前值
        const message = `API_URL: ${API_URL}\nSECRET: ${SECRET}\n\n是否要重置这些值？`;
        if (confirm(message)) {
            GM_setValue('API_URL', '');
            GM_setValue('SECRET', '');
            alert('API_URL 和 SECRET 已重置');
        }
    });
    // 检查是否已经保存了 API_URL 和 SECRET
    if (!API_URL | !SECRET) {

        // 如果没有保存，提示用户输入
        const api_url = prompt('请输入 API URL:', '');
        const secret = prompt('请输入 SECRET:', '');

        // 保存用户输入的值
        GM_setValue('API_URL', api_url);
        GM_setValue('SECRET', secret);

        // 重新获取保存的值
        const API_URL = GM_getValue('API_URL');
        const SECRET = GM_getValue('SECRET');
    }


    let lastReport = GM_getValue('lastReport', { url: '', title: '', timestamp: 0 });

    function sendRequest(title,url) {
        var now = new Date();
        var report_time = now.toLocaleString(); // 将日期转换为本地字符串格式
        var currentTimestamp = now.getTime();

        // 检查是否是相同的 URL 和标题，以及是否超过一分钟
        //if (url === lastReport.url && title === lastReport.title && currentTimestamp - lastReport.timestamp < 60000) {
        //   showAlert('相同的 URL 和标题，且未超过一分钟，不发送请求');
        //  return;
        //  }
        const postData = {
            "type": 'browser',
            "title": title,
            "url" : url,
            "report_time": report_time
        };
        const formData = Object.keys(postData).map(key => {
            return encodeURIComponent(key) + '=' + encodeURIComponent(postData[key]);
        }).join('&');
        GM_xmlhttpRequest({
            method: 'POST',
            url: API_URL+"/set_info",
            data: formData,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'API-KEY': SECRET
            },
            onload: (response) => {
                if (response.status === 200) {
                    showAlert(`API 请求成功: ${url}`);
                } else {
                    showAlert(`API 请求失败: ${response.status} ${response.statusText} ${response.response}`);
                }
            },
            onerror: (error) => {
                showAlert(`API 请求出错: ${error}`);
            }
        });

        // 更新 lastReport 信息
        lastReport = { url, title, timestamp: currentTimestamp };
        GM_setValue('lastReport', lastReport);
    }


    function showAlert(message) {
        const alertBox = document.createElement('div');
        alertBox.style.position = 'fixed';
        alertBox.style.top = '50%';
        alertBox.style.left = '50%';
        alertBox.style.transform = 'translate(-50%, -50%)';
        alertBox.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
        alertBox.style.color = 'white';
        alertBox.style.padding = '10px';
        alertBox.style.borderRadius = '5px';
        alertBox.style.zIndex = '10001';
        alertBox.textContent = message;

        document.body.appendChild(alertBox);

        // 3秒后自动消失
        setTimeout(() => {
            alertBox.remove();
        }, 3000);
        console.log(message)
    }

    function createModal() {
        const modal = document.createElement('div');
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.width = '100%';
        modal.style.height = '100%';
        modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        modal.style.zIndex = '10002';
        modal.style.display = 'none';

        const modalContent = document.createElement('div');
        modalContent.style.position = 'absolute';
        modalContent.style.top = '50%';
        modalContent.style.left = '50%';
        modalContent.style.transform = 'translate(-50%, -50%)';
        modalContent.style.backgroundColor = 'white';
        modalContent.style.padding = '20px';
        modalContent.style.borderRadius = '5px';
        modalContent.style.width = '500px';



        const titleLabel = document.createElement('label');
        titleLabel.textContent = '标题:';
        const titleInput = document.createElement('input');
        titleInput.value = document.title;
        const br = document.createElement('br');

        const urlLabel = document.createElement('label');
        urlLabel.textContent = 'URL:';
        const urlInput = document.createElement('input');
        urlInput.value = window.location.href.split('?')[0];

        const confirmButton = document.createElement('button');
        confirmButton.textContent = '确认上传';
        confirmButton.addEventListener('click', () => {
            sendRequest(titleInput.value, urlInput.value);
            modal.style.display = 'none';
        });
        const closeButton = document.createElement('button');
        closeButton.textContent = '关闭';
        closeButton.style.position = 'absolute';
        closeButton.style.right = '10px';
        closeButton.addEventListener('click', () => {
            modal.style.display = 'none';
        });
        titleInput.style.width = '80%';
        titleInput.style.padding = '10px';
        titleInput.style.margin = '6px';
        titleInput.style.border = '2px solid #ccc';
        titleInput.style.borderRadius = '4px';
        titleInput.style.fontSize = '16px';

        urlInput.style.width = '80%';
        urlInput.style.padding = '10px';
        urlInput.style.margin = '6px';
        urlInput.style.border = '2px solid #ccc';
        urlInput.style.borderRadius = '4px';
        urlInput.style.fontSize = '16px';

        modalContent.appendChild(titleLabel);
        modalContent.appendChild(titleInput);
        modalContent.appendChild(br);
        modalContent.appendChild(urlLabel);
        modalContent.appendChild(urlInput);
        modalContent.appendChild(confirmButton);
        modalContent.appendChild(closeButton);

        modal.appendChild(modalContent);
        document.body.appendChild(modal);

        return modal;
    }

    const button = document.createElement('button');
    button.textContent = '↑';
    button.id = 'custom-upload-button';
    button.style.position = 'fixed';
    button.style.top = '10px';
    button.style.right = '10px';
    button.style.width = '60px';
    button.style.height = '30px';
    button.style.fontSize = '12px';
    button.style.zIndex = '10000';
    button.style.backgroundColor = '#007bff';
    button.style.color = 'white';
    button.style.border = 'none';
    button.style.borderRadius = '5px';
    button.style.cursor = 'pointer';
    button.style.outline = 'none';
    button.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.2)';

    button.addEventListener('click', () => {
        const modal = createModal();
        modal.style.display = 'block';
    });
    button.addEventListener('contextmenu', (event) => {
        event.preventDefault();
        button.style.display = 'none';
    })
    document.body.appendChild(button);
})();