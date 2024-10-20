// Firefox win~
// ref: https://blog.ankursundara.com/shadow-dom/
window.find('兄弟你好香');
const spanContainer = window.getSelection().anchorNode.parentNode.parentNode;
const shadowRoot = spanContainer.parentNode.parentNode.parentNode;

let res = '';
for (const span of spanContainer.children) {
    const template1 = window.getComputedStyle(span, '::before').getPropertyValue('content');
    for (const frag of template1.matchAll(/data-[^)]+/g))
        res += span.getAttribute(frag[0]);
    const template2 = window.getComputedStyle(span, '::after').getPropertyValue('content');
    for (const frag of template2.matchAll(/data-[^)]+/g))
        res += span.getAttribute(frag[0]);
}

document.querySelector('#noiseInput').value = res;
