#!/usr/bin/env python3

import subprocess
from bin2fm2 import bin_to_fm2
import os
import signal

# xmcp: kill previous processes

PID_FILE = '/tmp/judge.pid'

if os.path.isfile(PID_FILE):
  with open(PID_FILE) as f:
    pid = int(f.read().strip())
    try:
      os.killpg(pid, signal.SIGKILL)
    except Exception:
      pass

with open(PID_FILE, 'w') as f:
  f.write(str(os.getpgrp()))

'''
Path to FCEUX binary.

On macOS: build/src/fceux.app/Contents/MacOS/fceux
'''
FCEUX_PATH = '/root/fceux/build/src/fceux'


FLAG_ARGS = {
  #     Lua file         flag file   timeout (seconds)
  '1': ('/root/judger/flag1.lua', '/flag1', 10 * 60),
  '2': ('/root/judger/flag2.lua', '/flag2', 90),
  '3': ('/root/judger/flag3.lua', '/flag3', 5 * 60),
}

MOVIE_FILE = '/root/judger/movie.fm2'
MEMORY_DUMP_FILE = '/root/judger/mem.bin'
LAST_FRAME = '/root/judger/last-frame.png'


def read_and_check_input(input_file: str, timeout: int) -> bytes | None:
  '''
  Reads the given input file and returns the contents.
  Raises an exception if the input may exceeds the timeout.
  '''
  with open(input_file, 'rb') as f:
    input = f.read()
  if len(input) > timeout * 60:
    return None
  return input


def run_fceux(lua_file: str, timeout: int | None = None) -> int:
  '''
  Runs FCEUX with the given Lua script.
  Returns the exit code.
  '''
  try:
    if timeout is not None:
      timeout += 5
    return subprocess.run([FCEUX_PATH, '--no-config', '1', '--noframe', '1',
                           '--fullscreen', '1', '--loadlua', lua_file],
                          capture_output=True, timeout=timeout).returncode
  except:
    return -1


def show_image_text(img_file: str, text: str | None = None) -> None:
  '''
  Shows the given image and text.
  '''
  import tkinter as tk
  from PIL import Image, ImageTk

  label_attr = {
    'fg': 'white',
    'font': ('monospace', 16),
    'wraplength': 500,
  }

  window = tk.Tk()
  window.geometry('512x448')
  window.overrideredirect(True)
  window.configure(bg='black')

  if os.path.exists(img_file):
    img = Image.open(img_file)
    img = img.resize((512, 448), Image.NEAREST)
    if text is not None:
      overlay = Image.new('RGBA', img.size, (0, 0, 0, int(255 * 0.7)))
      img = Image.alpha_composite(img.convert('RGBA'), overlay)
    img_tk = ImageTk.PhotoImage(img)
    if text is None:
      label = tk.Label(window, image=img_tk)
    else:
      label = tk.Label(window, image=img_tk, text=text,
                       compound='center', **label_attr)
    label.pack()
  else:
    assert text is not None
    label = tk.Label(window, text=text, bg='black', **label_attr)
    label.pack(expand=True)

  window.mainloop()


def judge_flag1_flag2(input_file: str,
                      lua_file: str, flag_file: str, timeout: int) -> str:
  '''
  Judges for flag 1 or flag 2.
  Returns the flag if successful, or an error message otherwise.
  '''
  input = read_and_check_input(input_file, timeout)
  if input is None:
    return 'Time limit exceeded.'
  with open(MOVIE_FILE, 'w') as f:
    f.write(bin_to_fm2(input))
  if run_fceux(lua_file, timeout) != 0:
    return 'You lose.'
  with open(flag_file) as f:
    return f.read()


def judge_flag3(input_file: str, mem_dump_file: str,
                lua_file: str, flag_file: str, timeout: int) -> str | None:
  '''
  Judges for flag 3.
  Returns `None` if successful, or an error message otherwise.
  '''
  input = read_and_check_input(input_file, timeout)
  if input is None:
    return 'Time limit exceeded.'
  with open(flag_file) as f:
    flag = f.read().encode()
    assert len(flag) < 64
  with open(MOVIE_FILE, 'w') as f:
    f.write(bin_to_fm2(input + flag + b'\x00' * 10))

  if os.path.isfile(mem_dump_file):
    subprocess.run(['cp', mem_dump_file, MEMORY_DUMP_FILE])
  else:
    with open(MEMORY_DUMP_FILE, 'wb') as f:
      f.write(b'\x00'*2048)
  assert run_fceux(lua_file, timeout) == 0


if __name__ == '__main__':
  import sys
  judge_mode = sys.argv[1]
  args = FLAG_ARGS[judge_mode]
  try:
    if judge_mode in ('1', '2'):
      input_file = sys.argv[2]
      result = judge_flag1_flag2(input_file, *args)
    else:
      input_file, mem_dump_file = sys.argv[2], sys.argv[3]
      result = judge_flag3(input_file, mem_dump_file, *args)
  except:
    result = 'Something went wrong,\ntry again?'
  show_image_text(LAST_FRAME, result)
