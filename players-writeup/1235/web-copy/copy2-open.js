// ==UserScript==
// @name         Make the shadow root mode open
// @namespace    http://tampermonkey.net/
// @version      2024-10-14
// @description  try to take over the world!
// @author       You
// @match        https://prob05.geekgame.pku.edu.cn/page2
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    Element.prototype._attachShadow = Element.prototype.attachShadow
    Element.prototype.attachShadow = function () {
        return this._attachShadow({mode:'open'})
    }
})();
