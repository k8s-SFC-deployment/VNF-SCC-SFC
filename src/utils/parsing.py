import re
import json

# ! must consider it only work when key and value exist in a same line
def load_json_one_depth(json_str):
  pattern = re.compile('''["']([a-zA-Z0-9]+)["']\s*:\s*(["']?)([a-zA-Z0-9.]+|\[.*\]|\{.*\})([!"']?)''', flags=re.M)
  json_dict = {}  
  for groups in re.findall(pattern, json_str):
    key = groups[0]
    value = groups[2]
    if groups[1] != "" and groups[1] == groups[3]:
      _type = str
    elif '.' in groups[2]:
      _type = float
    elif groups[2] == "null":
       value = None
    else:
      _type = int
    json_dict[key] = _type(value)
  return json_dict


# ! it work well, but somewhat not efficient
def load_json_one_depth_v2(json_str, except_keys):
    json_dict = json.loads(json_str)
    for ek in except_keys:
        if ek in json_dict.keys() and json_dict[ek] is not None:
            json_dict[ek] = json.dumps(json_dict[ek])
    return json_dict


example1 = """{
  "ABC": "1234",
  'abc': '{"asd": "assa"}',
  "def": 'dasad',
  'kbs": 1213
}"""

example2 = """{
    "processingLoad": '{"cpu_core": 1,  "percentage": 70, "mem_mb": 512, "duration_sec": 5.5}',
    "transmittingLoad": null,
    "next": '{"target_url":"http://localhost:7000/load","message": {"processingLoad": {"cpu_core": 1, "percentage": 70, "mem_mb": 512, "duration_sec": 10 }, "transmittingLoad": null,  "next": null}}'
}
"""

if __name__ == "__main__":
  print("EXAMPLE 1: ")
  print(load_json_one_depth(example1))
  print("\n\nEXAMPLE2")
  for key, value in load_json_one_depth(example2).items():
    print(f"{key}: {value}")
