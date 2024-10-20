#include <cstdio>
#include <pulse/pulseaudio.h>

int main() {
    // pa_sw_volume_to_dB
    printf("%u\n", PA_VOLUME_NORM);
    double db1 = pa_sw_volume_to_dB((pa_volume_t) (1.00 * PA_VOLUME_NORM));
    double db2 = pa_sw_volume_to_dB((pa_volume_t) (0.75 * PA_VOLUME_NORM));
    double db3 = pa_sw_volume_to_dB((pa_volume_t) (0.25 * PA_VOLUME_NORM));
    printf("100%%: %f dB\n", db1);
    double d = db2 - db3;
    printf("difference: %f dB\n", d);
    return 0;
}