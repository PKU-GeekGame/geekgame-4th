// ==UserScript==
// @name         Copy Noise Content to Input
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Copy content of div elements with class containing "noise" to an input element with id "noiseInput"
// @author       You
// @match        *://*/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    function init() {
        Element.prototype._attachShadow = Element.prototype.attachShadow;
        Element.prototype.attachShadow = function () {
            return this._attachShadow({ mode: "open" });
        };
    }

    function parse_(centralDiv, styleBlock) {
        const spans = centralDiv.querySelectorAll('.chunk');
        let chunkArray = [];
        let chunkMap = {};
        let chunkText = {};

        let attrCounter = 0;

        spans.forEach(span => {
            const chuckId = span.id;
            let chunkInfo = {};
            // iterate all attributes of the span
            for (let i = 0; i < span.attributes.length; i++) {
                const attr = span.attributes[i];
                if (attr.name.startsWith('data-')) {
                    chunkInfo[attr.name] = attr.value;
                    attrCounter++;
                }
            }
            chunkArray.push(chuckId);
            chunkMap[chuckId] = chunkInfo;
        });

        // parse css in style block
        // split by "#"
        const cssText = styleBlock.textContent;
        const cssArray = cssText.split('#');
        cssArray.forEach(css => {
            if(!css.startsWith('chunk')) {
                return;
            }
            const splitText = css.split(':');
            if (splitText.length != 4) {
                return 'splitText.length != 4';
            }
            const chunkId = splitText[0];
            const rawAttrs = splitText[3];
            // rawAttrs like: "attr(data1) attr(data2) attr(data3) ..."
            // now use regex to extract all the datas
            const regex = /attr\(([^)]+)\)/g;
            let match;
            let text = '';
            while (match = regex.exec(rawAttrs)) {
                const dataName = match[1];
                const dataValue = chunkMap[chunkId][dataName];
                text += dataValue;
            }

            chunkText[chunkId] = text;
        });

        let result = '';
        chunkArray.forEach(chunkId => {
            const c = chunkText[chunkId];
            result += c;
        });
        return result;
    }

    function parse(centerDiv, styleBlock) {
        const spans = centerDiv.querySelectorAll('.chunk');
        let result = "";
        let dataMap = {};
        let chunkIds = [];
        let allDataArray = [];
        const parseAttrs = txt => {
            const regex = /attr\(([^)]+)\)/g;
            let match;
            while (match = regex.exec(txt)) {
                allDataArray.push(match[1]);
            }
        };
        spans.forEach(span => {
            chunkIds.push(span.id);
            for (let i = 0; i < span.attributes.length; i++) {
                const attr = span.attributes[i];
                if (attr.name.startsWith('data-')) {
                    dataMap[attr.name] = attr.value;
                }
            }
            const beforeText = window.getComputedStyle(span, '::before').getPropertyValue('content');
            if (beforeText != 'none') {
                parseAttrs(beforeText);
            }
            const afterText = window.getComputedStyle(span, '::after').getPropertyValue('content');
            if (afterText) {
                parseAttrs(afterText);
            }
        });
        allDataArray.forEach(data => {
            result += dataMap[data];
        });
        return result;
    }

    function setNoiseDivsContentToInput() {
        // const body = document.querySelector('body');
        const root = document.getElementById('root');
        const noiseInput = document.getElementById('noiseInput');

        // set the page scrollable
        document.body.style.overflow = 'auto';

        // access the existed shadow root
        const shadowRoot = root.shadowRoot;
        if (shadowRoot) {
            // get the centralNoiseContent div and the style after the centralNoiseContent div
            const centralNoiseContents = shadowRoot.querySelectorAll('.centralNoiseContent');
            if (centralNoiseContents.length != 1) {
                noiseInput.value = 'Element with class "centralNoiseContent" number = ' + centralNoiseContents.length;
                return;
            }
            const centralNoiseContent = centralNoiseContents[0];
            const styleBlock = centralNoiseContent.nextElementSibling;
            noiseInput.value = parse(centralNoiseContent, styleBlock);
        } else {
            noiseInput.value = 'Shadow root not found';
        }
    }

    // 在页面加载完成后执行函数
    window.addEventListener('load', function() {
        init();
        setTimeout(setNoiseDivsContentToInput, 3000);
    });
})();
