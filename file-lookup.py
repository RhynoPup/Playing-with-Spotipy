import os,glob,pprint,json

output = []
files = glob.glob('data/*.json')
for file in files: 
    output.append('..\\'+file)

with open('datafiles.json','w') as f:
    f.write(json.dumps(output,indent=4))
f.close()
