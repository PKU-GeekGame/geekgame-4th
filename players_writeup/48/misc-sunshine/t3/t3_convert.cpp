#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <unistd.h>

#include <opus/opus.h>
#include <ogg/ogg.h>

#define DYNAMIC_PAYLOAD_TYPE_MIN 96

/* state struct for passing around our handles */
typedef struct {
  ogg_stream_state *stream;
  FILE *out;
  int seq;
  ogg_int64_t granulepos;
  int linktype;
  int dst_port;
  int payload_type;
} state;

/* helper, write a little-endian 32 bit int to memory */
void le32(unsigned char *p, int v)
{
  p[0] = v & 0xff;
  p[1] = (v >> 8) & 0xff;
  p[2] = (v >> 16) & 0xff;
  p[3] = (v >> 24) & 0xff;
}

/* helper, write a little-endian 16 bit int to memory */
void le16(unsigned char *p, int v)
{
  p[0] = v & 0xff;
  p[1] = (v >> 8) & 0xff;
}

/* helper, write a big-endian 32 bit int to memory */
void be32(unsigned char *p, int v)
{
  p[0] = (v >> 24) & 0xff;
  p[1] = (v >> 16) & 0xff;
  p[2] = (v >> 8) & 0xff;
  p[3] = v & 0xff;
}

/* helper, write a big-endian 16 bit int to memory */
void be16(unsigned char *p, int v)
{
  p[0] = (v >> 8) & 0xff;
  p[1] = v & 0xff;
}

/* manufacture a generic OpusHead packet */
ogg_packet *op_opushead(int samplerate, int channels)
{
  int size = 19;
  unsigned char *data = (unsigned char *) malloc(size);
  ogg_packet *op = (ogg_packet *) malloc(sizeof(*op));

  if (!data) {
    fprintf(stderr, "Couldn't allocate data buffer.\n");
    free(op);
    return NULL;
  }
  if (!op) {
    fprintf(stderr, "Couldn't allocate Ogg packet.\n");
    free(data);
    return NULL;
  }

  memcpy(data, "OpusHead", 8);  /* identifier */
  data[8] = 1;                  /* version */
  data[9] = channels;           /* channels */
  le16(data+10, 0);             /* pre-skip */
  le32(data + 12, samplerate);  /* original sample rate */
  le16(data + 16, 0);           /* gain */
  data[18] = 0;                 /* channel mapping family */

  op->packet = data;
  op->bytes = size;
  op->b_o_s = 1;
  op->e_o_s = 0;
  op->granulepos = 0;
  op->packetno = 0;

  return op;
}


/* manufacture a generic OpusTags packet */
ogg_packet *op_opustags(void)
{
  char *identifier = "OpusTags";
  char *vendor = "opus rtp packet dump";
  int size = strlen(identifier) + 4 + strlen(vendor) + 4;
  unsigned char *data = (unsigned char *) malloc(size);
  ogg_packet *op = (ogg_packet *)malloc(sizeof(*op));

  if (!data) {
    fprintf(stderr, "Couldn't allocate data buffer.\n");
    free(op);
    return NULL;
  }
  if (!op) {
    fprintf(stderr, "Couldn't allocate Ogg packet.\n");
    free(data);
    return NULL;
  }

  memcpy(data, identifier, 8);
  le32(data + 8, strlen(vendor));
  memcpy(data + 12, vendor, strlen(vendor));
  le32(data + 12 + strlen(vendor), 0);

  op->packet = data;
  op->bytes = size;
  op->b_o_s = 0;
  op->e_o_s = 0;
  op->granulepos = 0;
  op->packetno = 1;

  return op;
}

/* free a packet and its contents */
void op_free(ogg_packet *op)
{
  if (op) {
    if (op->packet) {
      free(op->packet);
    }
    free(op);
  }
}

ogg_packet *op_from_pkt(const unsigned char *pkt, int len)
{
  ogg_packet *op = (ogg_packet*)malloc(sizeof(*op));
  if (!op) {
    fprintf(stderr, "Couldn't allocate Ogg packet.\n");
    return NULL;
  }

  op->packet = (unsigned char *)pkt;
  op->bytes = len;
  op->b_o_s = 0;
  op->e_o_s = 0;

  return op;
}

/* helper, write out available ogg pages */
int ogg_write(state *params)
{
  ogg_page page;
  size_t written;

  if (!params || !params->stream || !params->out) {
    return -1;
  }

  while (ogg_stream_pageout(params->stream, &page)) {
    written = fwrite(page.header, 1, page.header_len, params->out);
    if (written != (size_t)page.header_len) {
      fprintf(stderr, "Error writing Ogg page header\n");
      return -2;
    }
    written = fwrite(page.body, 1, page.body_len, params->out);
    if (written != (size_t)page.body_len) {
      fprintf(stderr, "Error writing Ogg page body\n");
      return -3;
    }
  }

  return 0;
}

/* helper, flush remaining ogg data */
int ogg_flush(state *params)
{
  ogg_page page;
  size_t written;

  if (!params || !params->stream || !params->out) {
    return -1;
  }

  while (ogg_stream_flush(params->stream, &page)) {
    written = fwrite(page.header, 1, page.header_len, params->out);
    if (written != (size_t)page.header_len) {
      fprintf(stderr, "Error writing Ogg page header\n");
      return -2;
    }
    written = fwrite(page.body, 1, page.body_len, params->out);
    if (written != (size_t)page.body_len) {
      fprintf(stderr, "Error writing Ogg page body\n");
      return -3;
    }
  }

  return 0;
}


void write_packet(u_char *args, const u_char *packet, uint64_t seq, int size)
{
  int samples;
  state *params = (state *)(void *)args;
  ogg_packet *op;
  op = op_from_pkt(packet, size);
  op->packetno = seq;
  samples = opus_packet_get_nb_samples(packet, size, 48000);
  if (samples > 0) params->granulepos += samples;
  op->granulepos = params->granulepos;
  ogg_stream_packetin(params->stream, op);
  free(op);
  ogg_write(params);
}

/* use libpcap to capture packets and write them to a file */
int sniff(const char *input_file, const char *device, const char *output_file,
        int dst_port, int payload_type, int samplerate, int channels)
{
  state *params;
  ogg_packet *op;

  params = (state*)malloc(sizeof(state));
  params->stream = (ogg_stream_state*)malloc(sizeof(ogg_stream_state));
  if (ogg_stream_init(params->stream, rand()) < 0) {
    fprintf(stderr, "Couldn't initialize Ogg stream state.\n");
    free(params->stream);
    free(params);
    return 1;
  }
  params->out = NULL;
  params->seq = 0;
  params->granulepos = 0;
  params->dst_port = dst_port;
  params->payload_type = payload_type;

  if (output_file) {
    if (strcmp(output_file, "-") == 0) {
      params->out = stdout;
    } else {
      params->out = fopen(output_file, "wb");
    }
    if (!params->out) {
      fprintf(stderr, "Couldn't open output file.\n");
      free(params->stream);
      free(params);
      return 1;
    }
    /* write stream headers */
    op = op_opushead(samplerate, channels);
    ogg_stream_packetin(params->stream, op);
    op_free(op);
    op = op_opustags();
    ogg_stream_packetin(params->stream, op);
    op_free(op);
    ogg_flush(params);
  }

  /* start capture loop */
  for (uint64_t seq = 0; ; seq++) {
    char fname[256];
    snprintf(fname, sizeof(fname), "%s-%d.in", input_file, seq);
    FILE *f = fopen(fname, "rb");
    if (!f) {
      break;
    }
    char packet[1500];
    int size = fread(packet, 1, sizeof(packet), f);
    fclose(f);
    write_packet((u_char *)params, (const u_char*)packet, seq, size);
  }

  /* write outstanding data */
  if (params->out) {
    ogg_flush(params);
    if (params->out == stdout) {
      fflush(stdout);
    } else {
      fclose(params->out);
    }
    params->out = NULL;
  }

  /* clean up */
  ogg_stream_destroy(params->stream);
  free(params);
  return 0;
}

int main() {
  sniff("t3src", "device", "t3.opus", 0, 0, 48000, 2);
  return 0;
}