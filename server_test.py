from sys import int_info
import Pyro5.nameserver as ns
import Pyro5.api as pra
from utils.const import *
import typer

prog = typer.Typer()

@pra.expose
class User:
    def __init__(self, name) -> None:
        self.name = name
        self.list = []

    def see_name(self):
        return self.name

    def see_list(self):
        return self.list

    def add_list(self, id):
        self.list.append(id)

@prog.command()
def start_ns():
    uri, deamon, _ = ns.start_ns(host=host__, port=port__)
    print(f"NS running on {uri.location}")
    print(f"URI => {uri.protocol}:{uri.object}@{uri.location}")
    deamon.requestLoop()

@prog.command()
def serve(name: str):
    daemon = pra.Daemon()  # make a Pyro daemon 
    ns = pra.locate_ns()  # find the name server
    uri = daemon.register(User(name), f"user.{name}")
    ns.register(f"user.{name}", uri, metadata=["user"])

    print("Ready.")
    daemon.requestLoop()

@prog.command()
def name(name: str):
    greeting_maker = pra.Proxy(
        f"PYRONAME:user.{name}"
    )  # use name server object lookup uri shortcut

    print(greeting_maker.see_name())


@prog.command()
def add_list(name, id):
    greeting_maker = pra.Proxy(
        f"PYRONAME:user.{name}"
    )  # use name server object lookup uri shortcut

    greeting_maker.add_list(id)


@prog.command()
def list(name):
    print('entre')
    greeting_maker = pra.Proxy(
        f"PYRONAME:user.{name}"
    )  # use name server object lookup uri shortcut

    print(greeting_maker.see_list())

if __name__ == '__main__':
    prog()
