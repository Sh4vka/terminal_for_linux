import os
import sys
import subprocess
import signal
import time

current_process = None

def main():
    print ("This is terminal emulator!\n Input <help> for see comands!")

    while True:
        command = input("Matthew-linux>>> ").strip()
        if not command:
            continue
        tokens = command.split()

        if tokens[0] == "exit":
            break
        elif tokens[0] == "help":
            com_help()
        elif tokens[0] == "ls" and len(tokens) > 1:
            com_ls_path(tokens[1])
        elif tokens[0] == "ls":
            com_ls()
        elif tokens[0] == "cat" and len(tokens) > 1:
            com_cat(tokens[1])
        elif tokens[0] == "nice" and len(tokens) > 3:
            com_nice(tokens[2], tokens[3])
        elif tokens[0] == "killall" and len(tokens) > 1:
            com_killall(tokens[1])
        else:
            try:
                com_prog(tokens[0])
            except:
                print("Error! Input <help>")

    print("See you next time!")

def log_action(action):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("/home/matthew/lessons/OS/terminal_for_linux/log.log", "a") as log_file:
        log_file.write(f"[{timestamp}] {action}\n")

def handle_sigint(signal_num, frame):
    global current_process
    if current_process:
        log_action("Ctrl+C pressed. Terminating the process...")
        print("\nCtrl+C pressed. Terminating the process...")
        try:
            current_process.terminate()
            current_process.wait(timeout=1)
        except:
            current_process.kill()
        finally:
            current_process = None
    else:
        log_action("Ctrl+C pressed. No running process to terminate.")
        print("\nNo running process to terminate.")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)

def com_help():
    print("  ls                        - List directory contents")
    print("  cat <file>                - Display file contents")
    print("  nice <priority> <command> - Run command with adjusted priority")
    print("  killall <process>         - Kill all processes by name")
    print("  programm <name>           - Open browser by name")
    print("  exit                      - Exit the terminal")

def com_ls():
    try:
        directory = os.listdir(".")
        for file in directory:
            print (file)
    except:
        print ("Error!!!")

def com_ls_path(path):
    try:
        directory = os.listdir(path)
        for file in directory:
            print (file)
    except:
        print ("Error!!! Directory is not exist")

def com_cat(path):
    try:
        with open(path, 'r') as text:
            for line in text:
                print(line, " ")
    except:
        print("Error! File for read is not exist")

def com_nice(priority, prog):
    global current_process
    try:
        log_action(f"Started program: {prog}")
        current_process = subprocess.Popen(["nice", "-n", priority, prog])
        current_process.wait()
    except:
        log_action(f"Error running program {prog}: {str(e)}")
        print("Error!")

def com_killall(prog):
    try:
        subprocess.run(["killall", prog])
    except:
        print("Program is not start")
        
def com_prog(prog):
    global current_process
    if current_process is not None:
        print("Another instance is already running. Please close it first.")
        return
    try:
        log_action(f"Started program: {prog}")
        current_process = subprocess.Popen(['/usr/bin/' + prog])
        current_process.wait() 
        current_process = None 
    except:
        log_action(f"Error running program {prog}: {str(e)}")
        print("Error!!!")

main()