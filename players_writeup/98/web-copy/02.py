import os
import re

os.chdir(os.path.dirname(__file__))

with open("02.html", "r", -1, "utf8") as reader:
  text = reader.read()

STYLE_PATTERN = re.compile(r"#(chunk-.+?)::(before|after)\s*\{\s*content:\s*(.+?)\s*\}")
ATTR_PATTERN = re.compile(r"attr\((data-.+?)\)")
SPAN_PATTERN = re.compile(r'<span class="chunk" id="(chunk-.+?)" (.+?)>兄弟你好香</span>', re.DOTALL)
DATA_PATTERN = re.compile(r'(data-.+?)="(.+?)"')

content_dict = {}

for id, position, content in STYLE_PATTERN.findall(text):
  content_dict[id] = content_dict.get(id, {})
  content_dict[id][position] = ATTR_PATTERN.findall(content)

for id, data in SPAN_PATTERN.findall(text):
  content = content_dict[id]
  data_dict = dict(DATA_PATTERN.findall(data))
  for position in ["before", "after"]:
    if position not in content:
      continue

    for attr in content_dict[id][position]:
      print(data_dict.get(attr, ""), end="")

print()
