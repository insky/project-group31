import rich
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import re
import ast
from address_book import Record, AddressBook


def welcome(welcome_phrase:str):

    line = f'[underline yellow]{welcome_phrase}[/]'
    rich.print(Panel.fit(line))
    
def error_output(error_messege:str):

    rich.print(f'[bold red]{error_messege}[/]')

def incorrect_message(message:str):

    rich.print(f'[bold orange]{message}[/]')

def simple_messege(messege:str):

    rich.print(f'[bold white]{messege}[/]')

def Table_message(info:str):
    splited_info = re.split(r'[\n]', info)
    for line in splited_info:
        splited_line = re.split(r'[;]', line)
        list_b = []
        for i in splited_line:
            re.sub(r' ', '', i)
            list_a = re.split(r'[:]', i)
            for a in list_a:
                list_b.append(a)
        list_c = []
        tabl = Table()
        count_b = 0
        count_c = 1
        for i in range(len(list_b)//2):
            tabl.add_column(list_b[count_b])
            count_b+=2
        for i in range(len(list_b)//2):
            list_c.append(list_b[count_c])
            count_c+=1
        tabl.add_row(*list_c)
        console = Console()
        console.print(tabl)
    
def asking(text:str):

    theme = Prompt.ask(f'[bold white]{text}[/]')
    return theme
    






