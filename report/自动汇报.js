// ==UserScript==
// @name         自动汇报
// @namespace    https://github.com/2412322029/seeme
// @version      0.3
// @description  自动汇报
// @author       2412322029@qq.com
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

    function applyStyles(element, styles) {
        Object.assign(element.style, styles);
    }

    const commonStyles = {
        // 通用样式
        fixedCenter: {
            position: 'fixed',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
        },
        darkBg: {
            backgroundColor: '#1a1a1a',
            color: '#ffffff',
        },
        buttonBase: {
            backgroundColor: '#007bff',
            color: '#ffffff',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
        },
        inputBase: {
            backgroundColor: '#333',
            color: '#ffffff',
            padding: '10px',
            border: '1px solid #555',
            borderRadius: '4px',
            fontSize: '16px',
        }
    };

    function showAlert(message) {
        const alertBox = document.createElement('div');
        applyStyles(alertBox, {
            ...commonStyles.fixedCenter,
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            color: 'white',
            padding: '10px',
            borderRadius: '5px',
            zIndex: '2147483647',
        });
        alertBox.textContent = message;

        document.body.appendChild(alertBox);

        // 3秒后自动消失
        setTimeout(() => {
            alertBox.remove();
        }, 3000);
        console.log(message);
    }

    let modalInstance = null;

    function createModal() {
        if (modalInstance) {
            modalInstance.style.display = 'block';
            return modalInstance;
        }

        const modal = document.createElement('div');
        applyStyles(modal, {
            position: 'fixed',
            top: '0',
            left: '0',
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            zIndex: '2147483647',
            display: 'none',
        });

        const modalContent = document.createElement('div');
        applyStyles(modalContent, {
            ...commonStyles.fixedCenter,
            ...commonStyles.darkBg,
            padding: '20px',
            borderRadius: '8px',
            width: '500px',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.5)',
        });

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
        confirmButton.textContent = '确认上传 [Enter]';

        const handleConfirm = () => {
            sendRequest(titleInput.value, urlInput.value);
            modal.style.display = 'none';
        };

        confirmButton.addEventListener('click', handleConfirm);

        // 添加回车键监听
        modal.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                handleConfirm();
            } else if (event.key === 'Escape') {
                modal.style.display = 'none';
            }
        });

        const closeButton = document.createElement('button');
        closeButton.textContent = '×';
        closeButton.addEventListener('click', () => {
            modal.style.display = 'none';
        });

        // 输入框和标签样式
        const inputStyles = {
            ...commonStyles.inputBase,
            width: '80%',
            margin: '6px',
        };

        const labelStyles = {
            color: '#ffffff',
            marginRight: '10px',
        };

        [titleLabel, urlLabel].forEach(label => {
            applyStyles(label, labelStyles);
        });

        [titleInput, urlInput].forEach(input => {
            applyStyles(input, inputStyles);
        });

        // 按钮样式
        applyStyles(confirmButton, {
            ...commonStyles.buttonBase,
            padding: '8px 16px',
            marginTop: '10px',
            float: 'right',
        });

        applyStyles(closeButton, {
            position: 'absolute',
            right: '10px',
            top: '10px',
            backgroundColor: 'transparent',
            border: 'none',
            color: '#ffffff',
            fontSize: '20px',
            cursor: 'pointer',
            padding: '10px',
        });

        modalContent.appendChild(titleLabel);
        modalContent.appendChild(titleInput);
        modalContent.appendChild(br);
        modalContent.appendChild(urlLabel);
        modalContent.appendChild(urlInput);
        modalContent.appendChild(confirmButton);
        modalContent.appendChild(closeButton);

        modal.appendChild(modalContent);
        document.body.appendChild(modal);

        modalInstance = modal;
        return modal;
    }

    // Alt + 1 打开模态框
    document.addEventListener('keydown', function(event) {
        if (event.altKey && event.key === '1') {
            event.preventDefault();
            if (modalInstance && modalInstance.style.display === 'block') {
                modalInstance.style.display = 'none';
            } else {
                const modal = createModal();
                modal.style.display = 'block';
                // 自动聚焦到标题输入框
                // modal.querySelector('input').focus();
            }
        }
    });

})();