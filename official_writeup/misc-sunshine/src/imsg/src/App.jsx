import {useState, useEffect} from 'react';
import {SendOutlined, EyeInvisibleOutlined, EyeOutlined} from '@ant-design/icons';

import './automation';

import './App.css';
import sticker_recv from './you-sticker.png';
import sticker_send from './sakiko-sticker.jpg';
import alert from './alert.png';

window.hook_send = ()=>{};

function SendBar({onSend}) {
    let [encrypted, setEncrypted] = useState(false);
    let [msg, setMsg] = useState('');

    function send() {
        onSend(encrypted ? <i>你发送了一条加密信息</i> : msg);
        setMsg('');
        setEncrypted(false);
        window.hook_send();
    }

    return (
        <div className="send-bar">
            <div className="container">
                <div className="send-btn" onClick={()=>setEncrypted(!encrypted)}>
                    {encrypted ? <EyeInvisibleOutlined /> : <EyeOutlined />}
                </div>
                <input
                    autoFocus type={encrypted ? 'password' : 'text'}
                    placeholder={encrypted ? '加密 !Message 信息' : '!Message 信息'}
                    value={msg} onChange={(e)=>setMsg(e.target.value)}
                    onKeyDown={(e)=>{if(e.key==='Enter') send()}}
                />
                <div className="send-btn" onClick={send}><SendOutlined /></div>
            </div>
        </div>
    )
}

function MsgHistory({history}) {
    return (
        <div className="msg-history">
            <div className="container">
                {history.map(([is_send, txt], idx)=>(
                <div key={idx} className={'msg msg-'+(is_send ? 'send' : 'recv')}>
                    {!is_send && <img src={sticker_recv} className="sticker" />}
                    <div className="msg-box">{txt}</div>
                    {is_send && <img src={sticker_send} className="sticker" />}
                </div>
                ))}
            </div>
        </div>
    );
}

function Popup() {
    let [show, setShow] = useState(false);

    window.show_popup = ()=>setShow(true);

    return (
        <div className={'popup'+(show ? '' : ' popup-hide')} onClick={()=>setShow(false)}>
            <img src={alert} />
        </div>
    );
}

export function App() {
    let [history, setHistory] = useState([]);

    window.hook_recv = (msg)=>{
        setHistory([...history, [false, msg]]);
    };
    window.hook_clear = ()=>{
        setHistory([]);
    };

    useEffect(() => {
        scrollTo(0, document.body.scrollHeight);
    }, [history]);

    useEffect(() => {
        window.hook_init();
    }, []);

    return (
        <div>
            <Popup />
            <div className="header">!Message</div>
            <MsgHistory history={history} />
            <SendBar onSend={(m)=>setHistory([...history, [true, m]])} />
        </div>
    );
}