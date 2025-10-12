import os
import platform
import shlex
import sys

class Shell:
    def ls(self, args):
        # Заглушка для команды ls
        print(f"ls called with args: {args}")

    def cd(self, args):
        # Заглушка для команды cd
        print(f"cd called with args: {args}")

def main():
    shell = Shell()
    commands = {"ls": shell.ls, "cd": shell.cd, "exit": None}

    vfs_name = "VFS"  # имя виртуальной FS для приглашения
    
    if len(sys.argv) == 3:
        #Режим скрипта
        vfs_path = sys.argv[1]
        script_path = sys.argv[2]
        print(f"[DEBUG] VFS path: {vfs_path}")
        print(f"[DEBUG] Script path: {script_path}")

        try:
            with open(script_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Script not found: {script_path}")
            return

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            print(f"{vfs_name}$ {line}")
            tokens = shlex.split(line)
            comm, *args = tokens
            if comm not in commands:
                print(f"Unknown command: {comm}")
                break
            if comm == "exit":
                print("Bye!")
                break
            else:
                commands[comm](args)

    else:
        # Этап 1
        while True:
            try:
                user = os.getlogin()
            except Exception:
                user = "user"
            host = platform.node()
            prompt = f"{vfs_name}:{user}@{host}$ "

            try:
                line = input(prompt).strip()
            except EOFError:
                print("\nexit")
                break
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
                continue

            if not line:
                continue
            tokens = shlex.split(line)
            comm, *args = tokens
            if comm not in commands:
                print(f"Unknown command: {comm}")
                continue
            if comm == "exit":
                print("Bye!")
                break
            else:
                commands[comm](args)

if __name__ == "__main__":
    main()
