#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "opus.h"
#include "debug.h"
#include "opus_types.h"
#include "opus_private.h"
#include "opus_multistream.h"

int main(int argc, char *argv[])
{
    int err;
    char *inFile = "decoded.opus_raw", *outFile = "decoded.pcm";
    FILE *fin = fopen(inFile, "rb");
    FILE *fout = fopen(outFile, "wb");
    const unsigned char mapping[] = {0, 1};
    
    if(!fin) {
        printf("!! fin\n");
        return 0;
    }
    if(!fout) {
        printf("!! fout\n");
        return 0;
    }
    
    err = 0;
    OpusMSDecoder *dec = opus_multistream_decoder_create(
        48000, 2, 1, 1, mapping, &err
    );
    if(err) {
        printf("!! opus_multistream_decoder_create %d\n", err);
        return 0;
    }
    
    const int FRAME_SIZE = 120, BUF_SAMPLES=24000;
    unsigned char framebuf[FRAME_SIZE*20];
    opus_int16 pcmbuf[2*BUF_SAMPLES];
    
    while(1) {
        int nread = fread(framebuf, FRAME_SIZE, 1, fin);
        printf("!! fread %d\n", nread);
        if(nread<=0)
            break;
        
        int nsamples = opus_multistream_decode(
            dec, framebuf, FRAME_SIZE, pcmbuf, BUF_SAMPLES, 0
        );
        printf("!! opus_multistream_decode %d\n", nsamples);
        if(nsamples<=0) {
            return 0;
        }
        
        fwrite(pcmbuf, sizeof(opus_int16), 2*nsamples, fout);
    }
    
    fclose(fout);
    return 0;
}
