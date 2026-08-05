import zipfile,os,sys
src=sys.argv[1]; out=sys.argv[2]
names=[]
for root,dirs,files in os.walk(src):
    for f in files:
        p=os.path.join(root,f)
        names.append(os.path.relpath(p,src).replace(os.sep,'/'))
names.sort(key=lambda n:(n!='[Content_Types].xml',n))
if os.path.exists(out): os.remove(out)
z=zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)
for n in names:
    z.write(os.path.join(src,n),n)
z.close()
print(out,'entries',len(names),'first',names[0])
