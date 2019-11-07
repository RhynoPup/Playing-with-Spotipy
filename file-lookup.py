import os,glob,pprint,json

output = []
files = glob.glob('static/data/*.json')
print(files)
for file in files: 
    output.append(file)

with open('static/datafiles.json','w') as f:
    f.write(json.dumps(output,indent=4))
f.close()
