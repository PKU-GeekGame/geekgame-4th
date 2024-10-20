// ==UserScript==
// @name         Display DOM Info
// @namespace    github.com/panxuc
// @version      1.0
// @description  Display DOM structure, including open-mode Shadow DOM content
// @author       Xuc Pan
// @match        https://prob05.geekgame.pku.edu.cn/*
// ==/UserScript==

(function () {
    'use strict';

    let domInfoContainer = document.createElement('div');
    domInfoContainer.style.position = 'fixed';
    domInfoContainer.style.top = '10px';
    domInfoContainer.style.right = '10px';
    domInfoContainer.style.width = '400px';
    domInfoContainer.style.height = '500px';
    domInfoContainer.style.overflowY = 'scroll';
    domInfoContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    domInfoContainer.style.color = 'white';
    domInfoContainer.style.padding = '10px';
    domInfoContainer.style.zIndex = '9999';
    domInfoContainer.style.fontSize = '12px';
    domInfoContainer.style.border = '1px solid #ccc';
    domInfoContainer.style.borderRadius = '5px';

    document.body.appendChild(domInfoContainer);

    let updateButton = document.createElement('button');
    updateButton.textContent = 'Update DOM Info';
    updateButton.style.position = 'fixed';
    updateButton.style.bottom = '10px';
    updateButton.style.right = '10px';
    updateButton.style.padding = '10px';
    updateButton.style.backgroundColor = '#007bff';
    updateButton.style.color = 'white';
    updateButton.style.border = 'none';
    updateButton.style.borderRadius = '5px';
    updateButton.style.cursor = 'pointer';
    updateButton.style.zIndex = '10000';

    document.body.appendChild(updateButton);

    function generateDOMTreeHTML(element, indent = 0) {
        if (element === domInfoContainer || element === updateButton) {
            return '';
        }

        let html = '';
        let indentSpace = '&nbsp;'.repeat(indent * 4);
        html += indentSpace + '&lt;' + element.tagName.toLowerCase();

        if (element.attributes) {
            for (let attr of element.attributes) {
                html += ' ' + attr.name + '="' + attr.value + '"';
            }
        }

        html += '&gt;<br>';

        if (element.children.length === 0 && element.textContent.trim()) {
            let textContent = element.textContent.trim();
            html += indentSpace + '&nbsp;&nbsp;&nbsp;&nbsp;<strong>Text:</strong> ' + textContent + '<br>';
        }

        if (element.shadowRoot && element.shadowRoot.mode === 'open') {
            html += indentSpace + '&nbsp;&nbsp;&nbsp;&nbsp;<strong>Shadow DOM (open mode):</strong><br>';
            for (let shadowChild of element.shadowRoot.children) {
                html += generateDOMTreeHTML(shadowChild, indent + 1);
            }
        }

        for (let child of element.children) {
            html += generateDOMTreeHTML(child, indent + 1);
        }

        html += indentSpace + '&lt;/' + element.tagName.toLowerCase() + '&gt;<br>';
        return html;
    }

    function updateDOMInfo() {
        let html = generateDOMTreeHTML(document.body);
        domInfoContainer.innerHTML = html;
    }

    updateButton.addEventListener('click', updateDOMInfo);
})();
