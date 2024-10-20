def extract(input_file, output_file):
    input_size = 1408
    extract_sizes = range(input_size - 48, input_size)
    for extract_size in extract_sizes:
        with open(input_file, 'rb') as infile, open(output_file+f"_{extract_size}.bin", 'wb') as outfile:
            while True:
                data = infile.read(input_size)
                if len(data) < input_size:
                    break
                last = data[-extract_size:]
                outfile.write(last)


input_file_path = 'udp16.bin'
output_file_path = 'udp16'

extract(input_file_path, output_file_path)
