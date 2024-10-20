import subprocess
import pathlib

for K in range(1, 50):
    subprocess.run(["python3", "dinic_datamaker.py"], env={"K_VAL": str(K)})
    proc = subprocess.run(["./dinic"],input=pathlib.Path("./dinic.in").read_bytes(), capture_output=True, shell=True)
    print(f"K={K}, {proc.stderr.decode()}")