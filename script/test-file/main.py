import shlex
import subprocess
from multiprocessing import Process, Pipe

def test1():
    
    shell_cmd = "python sub-process.py"
    cmd = shlex.split(shell_cmd)
    p = subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    i = 0 
    while p.poll() is None:
        line = p.stdout.readline()
        with open('record.txt','a+b') as f:
            if line != b'':
                f.write(line)
                f.write(b'!!\n')
    
    if p.returncode == 0:
        with open('record.txt','a') as f:
            f.write("Success.\n")
    else:
        with open('record.txt','a') as f:
            f.write("Failed.\n")

def proc(pipe):
    i = 0
    while True:
        content = pipe.recv()
        with open('child-recv.txt','a') as f:
            f.write('child-recv:' + content + '\n')

        pipe.send("child-send:" + str(i))


def test2():
    parentPipe,childPipe = Pipe(duplex=True)
    p = Process(target=proc,args=(childPipe,))
    p.start()
    i = 0 
    while i < 10:
        parentPipe.send('parent sent:' + str(i))
        i += 1
        content =  parentPipe.recv()
        with open('parent-recv.txt','a') as f:
            f.write("parent-recv:" + content + '\n')

def main():
    test1()

if __name__ == "__main__":
    main()
