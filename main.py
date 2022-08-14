import json
with open("items.json","r",encoding="utf-8") as f:
    data = json.load(f)
print(len(data))