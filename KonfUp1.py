import os
import platform
import shlex

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

    while True:
        # формируем приглашение
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

        # разбор аргументов с учётом кавычек
        try:
            tokens = shlex.split(line)
        except ValueError as e:
            print(f"Parse error: {e}")
            continue

        comm, *args = tokens

        # подстановка переменных окружения вида $VAR
        expanded_args = []
        for arg in args:
            if arg.startswith("$"):
                val = os.getenv(arg[1:])
                if val is None:
                    print(f"Variable {arg} not found")
                    val = ""
                expanded_args.append(val)
            else:
                expanded_args.append(arg)

        # обработка команд
        if comm not in commands:
            print(f"Unknown command: {comm}")
            continue

        if comm == "exit":
            print("Bye!")
            break
        else:
            commands[comm](expanded_args)

if __name__ == "__main__":
    main()
