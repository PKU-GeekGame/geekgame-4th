var thumbnail = document.querySelector('#thumbnail');

window.addEventListener("message", function(e) {
    thumbnail.src = e.data.img;
    thumbnail.style.display = 'initial';
});

window.parent.postMessage({
    type: "request",
    data: "Hello from child"
}, '*');