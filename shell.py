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


class Shell:
    def __init__(self):
        pass

    def command_dictionary(self):
        command_dict = {
            "scheduler": lambda: ShellSchedulerCommand(self),
        }
        return command_dict

    def command_execute(self, args):
        if not args in self.command_dictionary():
            raise ValueError("명령어가 정확하지 않습니다.")
        ShellCommand: Command = self.command_dictionary()[args]()
        ShellCommand.execute()

    def main(self):
        while True:
            command = input("Shell>")
            if command == 'exit': break
            self.command_execute(command)


if __name__ == "__main__":
    Shell().main()
