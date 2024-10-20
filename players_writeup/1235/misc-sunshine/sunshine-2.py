with open("sunshine-video.raw", "rb") as f:
    gather: dict[int, list[bytes]] = {}
    # read 1392 bytes each time, until the end of the file
    for chunk in iter(lambda: f.read(1392), b""):
        # take bytes f[4:8] to get an int
        frameid = int.from_bytes(chunk[4:8], byteorder='little')
        # take byte f[10] to get an int
        fecflag = int(chunk[10])
        if fecflag != 0x10:
            continue
        if frameid not in gather:
            gather[frameid] = []
        gather[frameid].append(chunk[16:])
    for frameid in sorted(gather):
        lastlen = int.from_bytes(gather[frameid][0][4:6], byteorder='little')
        gather[frameid][0] = gather[frameid][0][8:]
        gather[frameid][len(gather[frameid]) - 1] = gather[frameid][len(gather[frameid]) - 1][:lastlen]
    # write all gathers to a file
    with open("sunshine-video.h264", "wb") as out:
        for frameid in sorted(gather):
            for chunk in gather[frameid]:
                out.write(chunk)
# ffmpeg -i sunshine-video.h264 -c copy sunshine-video.mp4
# flag{BigBrotherIsWatchingYou!!}