const ss = process.binding('spawn_sync');
const p = '/tmp/get_flag2'
const ret = ss.spawn({
    file: p,
    args: [p],
    detached: false,
    stdio: [
        { type: 'pipe', readable: true, writable: true },
        { type: 'pipe', readable: true, writable: true },
        { type: 'pipe', readable: true, writable: true }
    ]
})
// console.log(ret)
console.log(ret.output[1].toString())
