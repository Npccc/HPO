import shlex
import subprocess

def main():
    
    shell_cmd = "python classifier.py"
    cmd = shlex.split(shell_cmd)
    p = subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    intermediate_seg = 'Intermediate valid accuracy:'
    final_seg = 'Final valid accuracy:'
    with open("record.txt",'a') as f:
        while p.poll() is None:
            line = p.stdout.readline().decode('utf8')
            if intermediate_seg in line:
                data = line.strip().split(intermediate_seg)[1]
                f.write("Intermediate valid accuracy is " + data + '.\n')
            elif final_seg in line:
                data = line.strip().split(final_seg)[1]
                f.write("Final valid accuracy is " + data + '.\n')

        if p.returncode == 0:
            f.write("Success.\n")  
        else:
            f.write("Failed.\n") 

if __name__ == "__main__":
    main()
