// ==UserScript==
// @name         Decode Stupid web-copy
// @namespace    github.com/panxuc
// @version      1.0
// @description  Display the data-... attributes of each chunk in shadow DOM when button is clicked
// @author       Xuc Pan
// @match        https://prob05.geekgame.pku.edu.cn/*
// ==/UserScript==

(function () {
    'use strict';

    let chunkDataContainer = document.createElement('div');
    chunkDataContainer.style.position = 'fixed';
    chunkDataContainer.style.top = '10px';
    chunkDataContainer.style.left = '10px';
    chunkDataContainer.style.width = '400px';
    chunkDataContainer.style.height = '500px';
    chunkDataContainer.style.overflowY = 'scroll';
    chunkDataContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    chunkDataContainer.style.color = 'white';
    chunkDataContainer.style.padding = '10px';
    chunkDataContainer.style.zIndex = '9999';
    chunkDataContainer.style.fontSize = '12px';
    chunkDataContainer.style.border = '1px solid #ccc';
    chunkDataContainer.style.borderRadius = '5px';
    chunkDataContainer.style.display = 'none';

    document.body.appendChild(chunkDataContainer);

    let showButton = document.createElement('button');
    showButton.textContent = 'Show Chunk Data';
    showButton.style.position = 'fixed';
    showButton.style.bottom = '10px';
    showButton.style.left = '10px';
    showButton.style.padding = '10px';
    showButton.style.backgroundColor = '#007bff';
    showButton.style.color = 'white';
    showButton.style.border = 'none';
    showButton.style.borderRadius = '5px';
    showButton.style.cursor = 'pointer';
    showButton.style.zIndex = '10000';

    document.body.appendChild(showButton);

    function getChunkDataAttributes() {
        let result = '';

        let root = document.querySelector('div#root');
        if (!root || !root.shadowRoot) return;

        let shadowRoot = root.shadowRoot;

        let style = shadowRoot.querySelector('style');
        let styleContent = style.textContent;
        styleContent = styleContent.replace('.chunk{font-size:0;color:transparent}', '');
        styleContent = styleContent.replace('.chunk::before,.chunk::after{font-size:1rem;color:rgba(0, 255, 0, 0.6)}', '');

        let chunkData = {};
        let chunkDataArray = styleContent.split(')}#');
        for (let chunkDataStr of chunkDataArray) {
            let chunkDataStrArray = [];
            let flag = false;
            if (chunkDataStr.includes('::before{content:attr(')) {
                chunkDataStrArray = chunkDataStr.split('::before{content:attr(');
            }
            else if (chunkDataStr.includes('::after{content:attr(')) {
                chunkDataStrArray = chunkDataStr.split('::after{content:attr(');
                flag = true;
            }
            if (chunkDataStrArray.length < 2) {
                alert(`chunk data attributes not found: ${chunkDataStr}`);
            }
            let chunk = chunkDataStrArray[0];
            if (chunk.startsWith('#')) {
                chunk = chunk.substring(1);
            }
            let dataAttributes = chunkDataStrArray[1].split(') attr(');
            for (let i = 0; i < dataAttributes.length; i++) {
                dataAttributes[i] = dataAttributes[i].replace(')', '');
                dataAttributes[i] = dataAttributes[i].replace('}', '');
            }
            if (flag) {
                chunkData[`#${chunk}`] = dataAttributes;
            }
            else {
                chunkData[chunk] = dataAttributes;
            }
        }

        shadowRoot.querySelectorAll('.chunk').forEach((chunk) => {
            let dataAttributes = [];
            let chunkName = chunk.getAttribute('id');
            if (chunkData[chunkName]) {
                for (let dataAttr of chunkData[chunkName]) {
                    if (chunk.getAttribute(dataAttr) === null) {
                        alert(`chunk ${chunkName} does not have data attribute ${dataAttr}`);
                    }
                    dataAttributes.push(`${chunk.getAttribute(dataAttr)}`);
                }
            }
            if (chunkData[`#${chunkName}`]) {
                for (let dataAttr of chunkData[`#${chunkName}`]) {
                    if (chunk.getAttribute(dataAttr) === null) {
                        alert(`chunk ${chunkName} does not have data attribute ${dataAttr}`);
                    }
                    dataAttributes.push(`${chunk.getAttribute(dataAttr)}`);
                }
            }
            result += `${dataAttributes.join('')}`;
        });

        chunkDataContainer.textContent = result;
    }

    showButton.addEventListener('click', () => {
        if (chunkDataContainer.style.display === 'none') {
            chunkDataContainer.style.display = 'block';
            getChunkDataAttributes();
        } else {
            chunkDataContainer.style.display = 'none';
        }
    });
})();
