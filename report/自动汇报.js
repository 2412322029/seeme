// ==UserScript==
// @name         自动汇报
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        http://*/*
// @match        https://*/*
// @grant        GM_xmlhttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// @icon         https://www.google.com/s2/favicons?sz=64&domain=github.com
// ==/UserScript==

(function() {
    'use strict';
    const API_URL = ''
    const SECRET = ''


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

        const apiUrl = `${API_URL}?key=${encodeURIComponent(SECRET)}&title=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}&type=browser&report_time=${encodeURIComponent(report_time)}`;

        GM_xmlhttpRequest({
            method: 'GET',
            url: apiUrl,
            onload: (response) => {
                if (response.status === 200) {
                    showAlert(`API 请求成功: ${url}`);
                } else {
                    showAlert(`API 请求失败: ${response.status} ${response.statusText}`);
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

        // 2秒后自动消失
        setTimeout(() => {
            alertBox.remove();
        }, 2000);
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