// ==UserScript==
// @name         Fill in the input box
// @namespace    http://tampermonkey.net/
// @version      2024-10-14
// @description  try to take over the world!
// @author       You
// @match        https://prob05.geekgame.pku.edu.cn/page2
// @grant        none
// @run-at       document-idle
// ==/UserScript==

(function() {
    'use strict';

    var captchaText = '';
    var centralNoiseContainer = document.getElementById('root').shadowRoot.querySelector('#centralNoiseContainer');
    var chunkSpans = centralNoiseContainer.querySelectorAll('span.chunk');
    chunkSpans.forEach(function(span) {
        var spanId = span.id;
        var styleContent = centralNoiseContainer.querySelector('style').textContent;

        var regex = new RegExp('#' + spanId + '::before\\{content:attr\\((data-[a-z0-9]+)\\)\\s*attr\\((data-[a-z0-9]+)\\)\\s*attr\\((data-[a-z0-9]+)\\)\\s*attr\\((data-[a-z0-9]+)\\)\\}', 'g');
        var match = regex.exec(styleContent);
        var dataAttrs = match.slice(1, 5);
        var content = dataAttrs.map(function(dataAttr) {
            return span.getAttribute(dataAttr);
        }).join('');
        captchaText += content;

        regex = new RegExp('#' + spanId + '::after\\{content:attr\\((data-[a-z0-9]+)\\)\\s*attr\\((data-[a-z0-9]+)\\)\\s*attr\\((data-[a-z0-9]+)\\)\\s*attr\\((data-[a-z0-9]+)\\)\\}', 'g');
        match = regex.exec(styleContent);
        dataAttrs = match.slice(1, 5);
        content = dataAttrs.map(function(dataAttr) {
            return span.getAttribute(dataAttr);
        }).join('');
        captchaText += content;
    });

    var input = document.getElementById('noiseInput');
    for (var i = 0; i < captchaText.length; i++) {
        input.value += captchaText[i];
    }

    debugger;
})();
