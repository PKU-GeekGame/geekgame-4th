function xorDecrypt(data, key) {
    let decrypted = '';
    const keyLength = key.length;
    for (let i = 0; i < data.length; i++) {
        decrypted += String.fromCharCode(data.charCodeAt(i) ^ Math.round(Math.sqrt(key[i % keyLength] - 114514)));
    }
    return decrypted;
}

const XOR_KEY = [117430, 121739, 127739, 118739, 114955, 117539, 123923, 116818, 127970, 125963, 126614, 114635, 114955, 114530, 114803, 118235, 126395, 122614, 114710, 117650, 121739, 122614, 115090, 120290, 116818, 120755, 128203, 115810, 125963, 114955, 127739, 114683, 118739, 116450, 121910, 117995, 120139, 117323, 114523, 121910, 114514, 116035, 114914, 114875, 127283, 123923, 114770];

function embedCentralNoise() {
    const noiseContent1 = document.getElementById('centralNoiseContent1');

    const encrypted_noise = atob(noiseContent1.textContent);
    noiseContent1.textContent = '';
    noiseContent1.style.opacity = 'initial';

    const noise = xorDecrypt(encrypted_noise, XOR_KEY);
    const lines = noise.match(/.{1,40}/g) || [];
    lines.forEach(line => {
        if(line.trim() === '') return;

        const div1 = document.createElement('div');
        div1.classList.add('noiseLine');
        div1.textContent = line;
        noiseContent1.appendChild(div1);
    });
}

document.addEventListener('copy', function(e) {
    e.preventDefault();
});

document.addEventListener('selectstart', function(e) {
    e.preventDefault();
});

document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
});

document.addEventListener('keydown', function(e) {
    // F12
    if (e.key === 'F12') {
        e.preventDefault();
    }

    if (e.ctrlKey || e.altKey || e.metaKey) {
        e.preventDefault();
    }
});

setInterval(function() {
    console.clear();
}, 10);

const floatingConfig = {
    charCount: 30, 
    blockCount: 20, 
    animationDuration: [5, 10], 
    animationDelay: [0, 5], 
    characters: 'Il|1O0o@#$%&*()[]{}",./<>?'
};

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateFloatingElements() {
    const container = document.getElementById('floatingElementsContainer');

    for (let i = 0; i < floatingConfig.charCount; i++) {
        const char = document.createElement('div');
        char.classList.add('floating-char');
        char.textContent = floatingConfig.characters.charAt(Math.floor(Math.random() * floatingConfig.characters.length));
        
        char.style.left = `${Math.random() * 100}%`;
        char.style.top = `${Math.random() * 100}%`;
        
        const duration = getRandomInt(floatingConfig.animationDuration[0], floatingConfig.animationDuration[1]);
        const delay = Math.random() * floatingConfig.animationDelay[1];
        char.style.animationDuration = `${duration}s`;
        char.style.animationDelay = `${delay}s`;
        
        container.appendChild(char);
    }

    for (let i = 0; i < floatingConfig.blockCount; i++) {
        const block = document.createElement('div');
        block.classList.add('floating-block');
        
        block.style.left = `${Math.random() * 100}%`;
        block.style.top = `${Math.random() * 100}%`;
        
        const duration = getRandomInt(floatingConfig.animationDuration[0], floatingConfig.animationDuration[1]);
        const delay = Math.random() * floatingConfig.animationDelay[1];
        block.style.animationDuration = `${duration}s`;
        block.style.animationDelay = `${delay}s`;
        
        container.appendChild(block);
    }
}

setInterval(generateFloatingElements, 8000);

window.onload = function() {
    generateFloatingElements(); generateFloatingElements(); generateFloatingElements();
    embedCentralNoise();
};