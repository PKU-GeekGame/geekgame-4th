// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      2024-10-12
// @description  try to take over the world!
// @author       You
// @match        https://prob05.geekgame.pku.edu.cn/page2
// @icon         https://www.google.com/s2/favicons?sz=64&domain=pku.edu.cn
// @grant        none
// ==/UserScript==

const shadow_dom_style = `
 #centralBox {
        position: fixed;
        top: 0%;
        left: 0%;
        width: 500px;
        height: 1000px;
        background-color: rgba(0, 0, 0, 0.8);
        border: 2px solid #0F0;
        border-radius: 10px;
        padding: 20px;
        box-sizing: border-box;
        z-index: 1;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
    }

    #centralNoiseContainer {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: 1;
    }

    .centralNoiseContent {
        position: absolute;
        width: 100%;
        height: 100%;
        overflow: auto;
        color: rgba(0, 255, 0, 0.6);
        font-size: 20px;
        font-weight: bold;
        text-shadow: 0 0 3px rgba(0, 255, 0, 0.5);
        line-break: anywhere;
        word-wrap: break-word;
    }

    #centralBoxContent {
        position: relative;
        z-index: 1;
        color: #0F0;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 0 0 5px #0F0;
        white-space: pre-wrap;
        text-align: center;
        line-height: 1.5;
        animation: centralFlicker 5s infinite;
    }

    @keyframes centralFlicker {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    * {
        -webkit-user-drag: none !important;
        -webkit-touch-callout: none !important;
        user-select: none !important;
    }

    #noiseContainer,
    #floatingBoxesContainer,
    #floatingTextContainer,
    #additionalFloatingCharsContainer {
        display: none;
    }

    #floatingElementsContainer {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 4;
        overflow: hidden;
    }

    .floating-char {
        position: absolute;
        color: rgba(0, 255, 0, 0.8);
        font-size: 18px;
        font-weight: bold;
        text-shadow: 0 0 2px rgba(0, 255, 0, 0.5);
        user-select: none;
        animation: floatUp linear infinite;
    }

    .floating-block {
        position: absolute;
        width: 20px;
        height: 20px;
        background-color: rgba(0, 255, 0, 0.5);
        border: 1px solid rgba(0, 255, 0, 0.8);
        border-radius: 4px;
        opacity: 0.7;
        animation: floatUp linear infinite;
    }

    @keyframes floatUp {
        0% {
            transform: translateY(100%) translateX(0);
            opacity: 1;
        }
        100% {
            transform: translateY(-100%) translateX(50px);
            opacity: 0;
        }
    }
`

function _0xe7c12d(_0x5411b3, _0x388f1b) {
    return a0_0x32746c(_0x388f1b, _0x5411b3 - -0x141);
}

function _0x4bbdbc(_0x1a1e15, _0x19ed69) {
		return a0_0x2e32a9(_0x1a1e15, _0x19ed69 - 0x233);
	}

function _0x358a2f(_0x1aadd0, _0x497d2c) {
		return a0_0x32746c(_0x497d2c, _0x1aadd0 - 0x24c);
	}


function _0x4c2965(_0x3ed4be, _0x3fd5cb) {
		return a0_0x58c8(_0x3fd5cb - 0x30a, _0x3ed4be);
	}

	function _0x490522(_0x5819b9, _0x14eeb0) {
		return a0_0x58c8(_0x5819b9 - 0x111, _0x14eeb0);
	}

function log(message) {
	const body = document.getElementsByTagName("body")[0];
	const new_div = document.createElement("div");
	new_div.innerText = message;
	body.appendChild(new_div);
	// Set position to top-left
	new_div.style.position = "fixed";
	new_div.style.top = "0";
	new_div.style.left = "0";
	// auto wrap
	new_div.style.whiteSpace = "pre-wrap";
	// max width
	new_div.style.width = "100%";
	// max height
	new_div.style.height = "100%";
	// overflow
	new_div.style.overflow = "scroll";
}

function fuck(orig_text) {
    // log(document.head.innerHTML);
    let root = document.getElementById("root");
    // log(root.style.height);
    // log(_0x4bbdbc(0xe36, 0xdb8));
    // log(_0x490522(0xf68, 0x940));
    let new_div = document.createElement("div");
    let shadow_dom = new_div.attachShadow({'mode': 'open'});
    shadow_dom.innerHTML = `  <div id="centralBox">
        <div id="centralNoiseContainer">
            <div class="centralNoiseContent" id="centralNoiseContent1"></div>
        </div>
        <div id="centralBoxContent">
        </div>
        <div id="floatingElementsContainer"></div>
    </div>`;
    const style_node = document.createElement('style');
	style_node.textContent = shadow_dom_style, shadow_dom.appendChild(style_node);
    let noise_elem = shadow_dom.getElementById('centralNoiseContent1');
    try {
        a0_0x102d1b(noise_elem, orig_text);
        // log(noise_elem.innerHTML)
        document.body.appendChild(new_div);
    } catch (e) {
        log(e)
    }
}
(function() {
    'use strict';
    let root = document.getElementById("root");
    let orig_text = root.innerText;

    // Your code here...
    setTimeout(() => fuck(orig_text), 500);
})();