from abc import ABC, abstractmethod
from scheduler import Scheduler


class Command(ABC):
    def __init__(self, shell):
        self.shell = shell

    @abstractmethod
    def execute(self):
        pass


class ShellSchedulerCommand(Command):
    def __init__(self, shell):
        super().__init__(shell)

    def execute(self):
        scheduler = Scheduler()
        scheduler.execute()

class ShellHelpCommand(Command):
    def __init__(self, shell):
        super().__init__(shell)

    def execute(self):
        print(
            "[Help]",
            "===== Shell 명령어 설명 =====",
            "scheduler : 여러 사람들의 공통된 빈 시간을 알려주는 기능입니다.",
            "help      : 사용 가능한 명령어 목록을 보여줍니다.",
            "exit      : 셸을 종료합니다.",
            sep='\n'
        )
class Shell:
    def __init__(self):
        self._command_dict = {
            "help": lambda: ShellHelpCommand(self),
            "scheduler": lambda: ShellSchedulerCommand(self),
        }

    def command_execute(self, args):
        if args not in self._command_dict:
            print(f"명령어가 정확하지 않습니다.: '{args}'")
            print("사용 가능한 명령어:", ", ".join(self._command_dict.keys()))
            return

        ShellCommand: Command = self._command_dict[args]()
        ShellCommand.execute()
    def main(self):
        while True:
            command = input("Shell>").strip()
            if command == 'exit': break
            self.command_execute(command)


if __name__ == "__main__":
    Shell().main()
