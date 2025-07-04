from dataclasses import dataclass
from sys import argv, exit
from Code import Code

class Command:
    pass

@dataclass
class A(Command):
    value: str

@dataclass
class L(Command):
    value: str

@dataclass
class C(Command):
    value: str


class Parser:
    def __init__(self, path):
        with open(path, "r") as f:
            contents = f.read()
            if not contents.strip():
                print("Empty file")
                exit(1)
            self.commands = contents.strip().split("\n")
            self.instruction = -1
            self.current = None
            self.advance()

    def has_more_commands(self) -> bool:
        return self.instruction + 1 < len(self.commands)

    def advance(self):
        if not self.has_more_commands():
            return
        self.instruction += 1
        command = self.command_type(self.commands[self.instruction].strip())
        # skip empty lines & comments
        if not command.value or command.value.startswith("//"):
            self.advance()
        else:
            self.current = command

    @staticmethod
    def command_type(command: str) -> Command:
        command = command.split("//")[0]
        if command.startswith("@"):
            return A(command[1:].strip())
        if command.startswith("(") and command.endswith(")"):
            return L(command[1:-1].strip())
        return C(command.strip())

    def symbol(self) -> str:
        if isinstance(self.current, (A, L)):
            return self.current.value

    def comp(self) -> str:
        if isinstance(self.current, C):
            code = self.current.value
            if "=" in code:
                code = code.split("=")[1].split(";")[0].strip()
            elif ";" in code:
                code = code.split(";")[0].strip()
            else:
                print(f"Invalid C-instruction syntax at line: {self.instruction + 1}")
                exit(1)
            exists = Code.comp(code)
            if not exists:
                print(f"{self.instruction + 1}: {code} UNDEFINED") 
                exit(1)
            return exists

    def jump(self) -> str:
        if isinstance(self.current, C):
            value = self.current.value
            if ";" in value:
                code = value.split(";")[1].strip()
                exists = Code.jump(code)
                if not exists:
                    print(f"{self.instruction + 1}: {code} UNDEFINED") 
                    exit(1)
                return exists
        return "000"

    def dest(self) -> str:
        if isinstance(self.current, C):
            value = self.current.value
            if "=" in value:
                code = value.split("=")[0].strip()
                exists = Code.dest(code)
                if not exists:
                    print(f"{self.instruction + 1}: {code} UNDEFINED") 
                    exit(1)
                return exists
        return "000"

def main():
    if len(argv) != 2:
        print("Invalid argument length.")
        exit(1)

    path = argv[1]
    if not path.endswith(".asm"):
        print("Invalid file extension. Only .asm files are allowed.")
        exit(1)

    parsed = Parser(path)
    out = path.split(".")[0]

    try:
        with open(f"{out}.hack", "w") as output:
            while True:
                command = parsed.current
                if isinstance(command, A):
                    address = int(parsed.symbol())
                    output.write(f"{address:016b}\n")
                elif isinstance(command, C):
                    output.write(f"111{parsed.comp()}{parsed.dest()}{parsed.jump()}\n")

                if not parsed.has_more_commands():
                    break
                parsed.advance()
    except Exception as e:
        print(f"Could not compile: {path}\nError: {e}")
        exit(1)

if __name__ == "__main__":
    main()
