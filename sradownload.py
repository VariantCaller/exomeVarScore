import os

text = 'SRR11304597'
for text in text.split():
    print("Default \033[92mLight green")
    print("Default \033[44mBlue")
    first = "_1.fastq"
    second = "_2.fastq"
    os.system(f"fasterq-dump {text} -p -e 12")
    os.system(f"gzip {text}{first}")
    os.system(f"gzip {text}{second}")
    # os.system(f"parallel-fastq-dump --sra-id {text} --threads 16 --outdir /media/jake/Linux.HDD/Endo/ --split-files --gzip")
print("Default \033[39mDefault")
print("Default \033[49mDefault")

