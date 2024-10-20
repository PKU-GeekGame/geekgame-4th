// ==UserScript==
// @name         Force open Shadow DOM
// @namespace    github.com/panxuc
// @version      1.0
// @description  Force all shadowRoot to be open mode
// @author       Xuc Pan
// @match        https://prob05.geekgame.pku.edu.cn/*
// ==/UserScript==

(function () {
    'use strict';
    const originalAttachShadow = Element.prototype.attachShadow;
    Element.prototype.attachShadow = function (init) {
        if (init && init.mode) {
            init.mode = 'open';
        }
        return originalAttachShadow.call(this, init);
    };
})();
