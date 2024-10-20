
//import { createPinia } from 'pinia'

//const pinia = createPinia();

import { createApp } from 'vue'
import './main.css'
import Hello from './views/Hello.vue'

const app = createApp(Hello)

app.mount('#app')

function logger(e) {
    return function() {
        fetch('/log/'+e, {credentials: 'include'});
    };
}

function on_paste(e) {
    let upload = {};
    e.clipboardData.types.forEach((t)=>{
        let data = e.clipboardData.getData(t);
        upload[t] = data.slice(0, 2048);
    });
    fetch('/log/paste', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(upload),
    });
}

window.addEventListener('focus', logger('focus'));
window.addEventListener('blur', logger('blur'));
window.addEventListener('paste', on_paste);