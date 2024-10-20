// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      2024-10-12
// @description  try to take over the world!
// @author       You
// @match        https://prob05.geekgame.pku.edu.cn/page2
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        none
// ==/UserScript==

function go() {
    var shadow = event.srcElement.shadowRoot;
    var chunks = shadow.querySelectorAll(".chunk");
    alert(chunks.length)
    var s = ""
    for (var chunk of chunks) {
        s += getComputedStyle(chunk, ":before").getPropertyValue('content').slice(1,-1)
        s += getComputedStyle(chunk, ":after").getPropertyValue('content').slice(1,-1)
    }
    document.getElementById("noiseInput").value=s
}

(function() {
	alert("运行脚本");
    document.onclick=go;
})();