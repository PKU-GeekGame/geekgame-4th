import { fileURLToPath } from 'node:url';
import fastify from 'fastify';
import fs from 'node:fs';
import child_process from 'node:child_process';
import fastifyHttpProxy from '@fastify/http-proxy';
import fastifyStatic from '@fastify/static';
import fastifyMultipart from '@fastify/multipart';

const server = fastify({ logger: true });
server.register(fastifyHttpProxy, {
    prefix: '/websockify',
    websocket: true,
    upstream: 'http://localhost:8080'
});
server.register(fastifyStatic, {
    root: fileURLToPath(new URL('./static', import.meta.url))
});
server.register(fastifyStatic, {
    root: '/usr/share/novnc',
    prefix: '/novnc',
    decorateReply: false
});
server.register(fastifyMultipart);

server.post('/launch', async (req, rep) => {
    let fields = {};
    let buffers = {};
    for await (const part of req.parts()) {
        if(part.type==='file')
            buffers[part.fieldname] = await part.toBuffer();
        else
            fields[part.fieldname] = part.value;
    }
    let lv = parseInt(fields.level);
    if(lv<1 || lv>3)
        return 'bad level';
    if(buffers.movie_file.length>36000)
        return 'bad movie file size';
    fs.writeFileSync('/tmp/movie_file', buffers.movie_file);
    let has_ram = false;
    if(lv===3) {
        if(buffers.init_ram && buffers.init_ram.length>0) {
            if(buffers.init_ram.length!==2048)
                return 'bad ram file size';
            fs.writeFileSync('/tmp/init_ram', buffers.init_ram);
            has_ram = true;
        }
    }
    child_process.spawn(
        'python3',
        ['/root/judger/judge.py', ''+lv, '/tmp/movie_file', ...(has_ram ? ['/tmp/init_ram'] : [''])], 
        {stdio: 'ignore', 'detached': true}
    ).unref();
    return `task ${lv} started, input length ${buffers.movie_file.length}, see the screen below`;
})

server.listen({
    host: '0.0.0.0',
    port: 3030
});
