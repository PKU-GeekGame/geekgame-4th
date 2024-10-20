import binascii
import struct
import json

cur_frame_index = 0
cur_frame_done = True
cur_frame_last_len = None
def load_pkt(p):
    global cur_frame_index, cur_frame_done, cur_frame_last_len
    
    hextxt = p['_source']['layers']['rtp']['rtp.payload'].replace(':', '')
    b = binascii.unhexlify(hextxt)
    
    # https://github.com/moonlight-stream/moonlight-common-c/blob/3acba578b19c14a23f58a5f2488c23e5c19ac637/src/Video.h#L25
    pkt_header_fmt = '<IIBBBBI'
    pkt_header_size = struct.calcsize(pkt_header_fmt)
    assert len(b)>pkt_header_size
    
    (
        streamPacketIndex, frameIndex,
        flags, reserved, multiFecFlags, multiFecBlocks,
        fecInfo,
    ) = struct.unpack(pkt_header_fmt, b[:pkt_header_size])
    
    assert multiFecBlocks==0 # multifec not yet implemented
    assert reserved==0
    assert streamPacketIndex&0xff==0
    
    payload = b[pkt_header_size:]
    
    if frameIndex==cur_frame_index+1: # begin of a new frame
        print(f'begin frame {frameIndex}')
    
        cur_frame_index = frameIndex
        cur_frame_done = False
        
        # https://github.com/LizardByte/Sunshine/blob/190ea41b2ea04ff1ddfbe44ea4459424a87c7d39/src/stream.cpp#L81
        frame_header_fmt = '<BHBHxx'
        frame_header_size = struct.calcsize(frame_header_fmt)
        assert len(payload)>frame_header_size
        
        (
            headerType, frame_processing_latency,
            frameType, lastPayloadLen,
        ) = struct.unpack(frame_header_fmt, payload[:frame_header_size])
        
        assert headerType==1
        assert frameType in [1, 2, 4, 5]
        
        cur_frame_last_len = lastPayloadLen
        payload = payload[frame_header_size:]
        
        assert payload[:4]==b'\x00\x00\x00\x01' # h264 header
        return True, payload
    
    elif frameIndex==cur_frame_index: # continuing current frame
    
        if cur_frame_done: # ignore fec data
            return False, None

        if flags==0x03: # FLAG_EOF | FLAG_CONTAINS_PIC_DATA, i.e., last frame
            print(cur_frame_last_len)
            
            cur_frame_done = True
            for padbyte in payload[cur_frame_last_len:]:
                assert padbyte==0
            
            payload = payload[:cur_frame_last_len]
            
        else: # not last frame
            #assert flags<0x08
            #assert len(payload)==1376
            print(len(payload), end=', ')
        
        return False, payload
        
    else:
        raise ValueError(f'frame index {frameIndex} should be {cur_frame_index}')

with open('data/decoded.h264', 'wb') as fw:
    # udp.srcport == 47998 and rtp
    with open('data/rtp-47998.json', encoding='utf-8') as f:
        for p in json.load(f):
            new, pp = load_pkt(p)
            if pp:
                fw.write(pp)
                
print('done')

# then, ffplay -i decoded.h264