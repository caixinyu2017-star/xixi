#!/usr/bin/env python3
"""Assemble a Nature-Communications-style .docx from a markdown source that uses
[[key]] citation placeholders and a python refs module.

Usage: python3 build.py paper1 refs1
"""
import re, sys, subprocess, importlib, os

HERE=os.path.dirname(os.path.abspath(__file__))

def compress(nums):
    """[3,4,5,7,9,10]->'3-5,7,9-10' with en-dash."""
    nums=sorted(set(nums)); out=[]; i=0
    while i<len(nums):
        j=i
        while j+1<len(nums) and nums[j+1]==nums[j]+1: j+=1
        if j-i>=2: out.append(f"{nums[i]}–{nums[j]}")
        else: out.extend(str(nums[k]) for k in range(i,j+1))
        i=j+1
    return ",".join(out)

def main():
    stem=sys.argv[1]; refsmod=sys.argv[2]
    md=open(f"{HERE}/{stem}.md").read()
    refs=importlib.import_module(refsmod).REFS

    order=[]
    def note(key):
        if key not in order: order.append(key)

    md=re.sub(r'\]\]\s*\[\[', ';', md)   # merge consecutive [[a]][[b]] -> [[a;b]]
    token=re.compile(r'\[\[([^\]]+)\]\]')
    for m in token.finditer(md):
        for k in [x.strip() for x in m.group(1).split(';')]:
            note(k)
    missing=[k for k in order if k not in refs]
    if missing: raise SystemExit(f"ERROR missing refs for keys: {missing}")
    num={k:i+1 for i,k in enumerate(order)}

    def repl(m):
        ks=[x.strip() for x in m.group(1).split(';')]
        return f"^{compress([num[k] for k in ks])}^"
    body=token.sub(repl, md)

    reflines=["", "# References", "", '::: {custom-style="RefList"}', ""]
    for i,k in enumerate(order):
        reflines.append(str(i+1)+"\\. "+refs[k])   # escaped dot => literal number, not a list
        reflines.append("")
    reflines.append(":::")
    final=body+"\n"+"\n".join(reflines)+"\n"
    finalmd=f"{HERE}/{stem}_final.md"
    open(finalmd,"w").write(final)

    out=f"{HERE}/{stem}.docx"
    cmd=["pandoc",finalmd,"-o",out,
         "--reference-doc",f"{HERE}/reference.docx",
         "--resource-path",HERE,"-M","lang=en-GB"]
    subprocess.run(cmd,check=True)
    print(f"[{stem}] refs={len(order)}  ->  {out}")

if __name__=="__main__":
    main()
