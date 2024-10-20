from flask import *
import os
import re
import subprocess
import hashlib
import base64

import logger

import traceback
def get_traceback(e):
    lines = traceback.format_exception(type(e), e, e.__traceback__)
    return ''.join(lines)

with open('/flag1') as f:
    FLAG1 = f.read().strip()
with open('/flag2') as f:
    FLAG2 = f.read().strip()

app = Flask("complexity")
app.secret_key = "redbud@tsinghua.complexity-yasar"

descriptions = {
    "SPFA": "最短路径快速算法 (Shortest Path Faster Algorithm, SPFA)，一般也被称为带有队列优化的 Bellman-Ford 算法。\n相较于 Bellman-Ford 算法，SPFA 的最坏复杂度和其一致为O(|V||E|)\n但是在实际使用中，在很多情况下，SPFA 的速度远优于其最坏复杂度。\n请尝试让 SPFA 达到其理论最坏复杂度 (使代码中的计数器超过 2e6)。",
    "Dinic": "Dinic 算法是在网络流计算最大流的强多项式复杂度的算法。\n类似于复杂度为 O(|V||E|^2)的 Edmonds–Karp 算法，Dinic 算法的复杂度为 O(|V|^2|E|)\n但是在大多数网络建模下，Dinic 的速度远优于其最坏复杂度。\n请尝试让 Dinic 达到其理论最坏复杂度 (使代码中的计数器超过 1e6)。",
}

SRC = {}
with open('spfa.cpp') as f:
    SRC['SPFA'] = f.read().strip()
with open('dinic.cpp') as f:
    SRC['Dinic'] = f.read().strip()

SIZE_LIMIT = 200*1000

def render(title, input_data=None, output_data=None, flag=None):
    return render_template(
        "problem.html",
        title=title,
        code=SRC[title],
        description=descriptions[title],
        input_data=input_data.decode() if input_data else None,
        output_data=output_data.decode() if output_data else None,
        flag=open(flag).read() if flag else None,
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/spfa", methods=["GET", "POST"])
def spfa():
    if request.method == "POST":
        try:
            if "input_file" not in request.files:
                flash('找不到输入文件', 'danger')
                return render("SPFA")
            input_data = request.files["input_file"].read()
            if len(input_data)>SIZE_LIMIT:
                flash('输入文件太大', 'danger')
                return render("SPFA")
            if not re.match(r"^[\d\s]*$", input_data.decode()):
                flash('输入文件格式错误', 'danger')
                return render("SPFA")
            
            p = subprocess.Popen(
                ["./spfa"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            p.stdin.write(input_data)
            p.stdin.flush()
            try:
                code = p.wait(5)
            except subprocess.TimeoutExpired:
                p.terminate()
                flash('Time Limit Exceeded', 'danger')
                return render("SPFA")
            
            logger.write(None, ["submit_1", hashlib.md5(input_data).hexdigest(), code])
            
            if code != 0:
                flash('Runtime Error', 'danger')
                return render("SPFA")
            output_data = p.stdout.read()
            err_data = p.stderr.read()

            ops = int(err_data.decode().strip())
            flash(f'ops = {ops}', 'info')
            
            if ops > 2e6:  # TODO: decide the limit
                logger.write(
                    None,
                    [
                        "get_flag1",
                        hashlib.md5(input_data).hexdigest(),
                        ops,
                        input_data.decode(),
                    ],
                )
                flash("Accepted! " + FLAG1, 'success')

            input_data = (
                input_data[:100] + b"..." if len(input_data) > 100 else input_data
            )
            output_data = (
                output_data[:100] + b"..." if len(output_data) > 100 else output_data
            )
            return render("SPFA", input_data, output_data)
        except Exception as e:
            tb = get_traceback(e)
            logger.write(None, ['exception', str(type(e)), str(e), tb])
            
            flash('Internal System Error', 'danger')
            return render("SPFA")
    return render("SPFA")


@app.route("/dinic", methods=["GET", "POST"])
def dinic():
    if request.method == "POST":
        try:
            if "input_file" not in request.files:
                flash('找不到输入文件', 'danger')
                return render("Dinic")
            input_data = request.files["input_file"].read()
            if len(input_data)>SIZE_LIMIT:
                flash('输入文件太大', 'danger')
                return render("Dinic")
            if not re.match(r"^[\d\s]*$", input_data.decode()):
                flash('输入文件格式错误', 'danger')
                return render("Dinic")
            
            p = subprocess.Popen(
                ["./dinic"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            p.stdin.write(input_data)
            p.stdin.flush()
            try:
                code = p.wait(5)
            except subprocess.TimeoutExpired:
                p.terminate()
                flash('Time Limit Exceeded', 'danger')
                return render("Dinic")
            
            logger.write(None, ["submit_2", hashlib.md5(input_data).hexdigest(), code])
            
            if code != 0:
                flash('Runtime Error', 'danger')
                return render("Dinic")
            output_data = p.stdout.read()
            err_data = p.stderr.read()

            ops = int(err_data.decode().strip())
            flash(f'ops = {ops}', 'info')
            
            if ops > 1e6:  # TODO: decide the limit
                logger.write(
                    None,
                    [
                        "get_flag2",
                        hashlib.md5(input_data).hexdigest(),
                        ops,
                        input_data.decode(),
                    ],
                )
                flash("Accepted! " + FLAG2, 'success')

            input_data = (
                input_data[:100] + b"..." if len(input_data) > 100 else input_data
            )
            output_data = (
                output_data[:100] + b"..." if len(output_data) > 100 else output_data
            )
            return render("Dinic", input_data, output_data)
        except Exception as e:
            tb = get_traceback(e)
            logger.write(None, ['exception', str(type(e)), str(e), tb])
            
            flash('Internal System Error', 'danger')
            return render("Dinic")
    return render("Dinic")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
