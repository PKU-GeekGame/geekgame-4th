import dtmf from './dtmf.mp3';
import chime from './MacStartupChime.mp3';

let list = [
    // delay_s, text, wait_count, callback
    [0, '什么事？', 0, ()=>{new Audio(chime).play();}],
    [1, '你要哪几个flag', 1, null],
    [1, '两个flag换两个flag', 1, null],
    [1, '行吧，那你拿flag1来换', 1, null],
    [1, '别急我先试试对不对', 1, null],
    [2, '好像是对的，谢谢师傅', 0, ()=>{window.show_popup();}],
    [1, 'flag2是', 0],
    [2, 'flag{BigBrotherIsWatchingYou!!}', 0, null],
    [1, 'flag3是', 0, null],
    [2, '那我混淆一下发给你吧', 2, null],
    [2, <>flag{'{'}<audio src={dtmf} autoPlay controls />{'}'}</>, 0, null],
    [1, '合作愉快', 1, null],
]

window.hook_init = function() {
    let idx = 0;
    function next() {
        if (idx>=list.length) return;
        let [delay_s, text, wait_count, callback] = list[idx];

        let tot_send = 0;
        function check() {
            if(tot_send===wait_count) {
                setTimeout(()=>{
                    window.hook_recv(text);
                    if(callback)
                        callback();
                    idx++;
                    next();
                }, delay_s*1000);
            }
        }
        window.hook_send = ()=>{
            tot_send++;
            check();
        };
        check();
    }
    next();
}