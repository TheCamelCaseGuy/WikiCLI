import wikipedia
import warnings
from bs4 import GuessedAtParserWarning
from colorama import Fore
import click
import webbrowser
import config
import os
import sys

warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

abspath = os.path.dirname(os.path.abspath(sys.executable))
CONFIG = config.Config(os.path.join(abspath, "config", "config.json"))

wikipedia.set_lang(CONFIG.get("language"))

def searchWiki(query):
    candidates = wikipedia.search(query)
    if not candidates:
        return (None, [])
    
    top = candidates[0]
    return (top, candidates)

def generateWikiLink(title: str):
    base = f"https://{CONFIG.get("language")}.wikipedia.org/wiki/"
    title_ = title.replace(" ", "_")
    return base + title_

def openPage(query, raw):
        try:
            top, candidates = searchWiki(query)
            
            if not top:
                print(f"{Fore.RED}No results for term {query}{Fore.RESET}")
            else:
                if raw:
                    webbrowser.open(generateWikiLink(query))
                else:
                    print(f"Closest Match: {top}")        
                    webbrowser.open(generateWikiLink(top))

        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:10]
            print(f"{Fore.RED}The term {query} is ambiguous. Please refine your query.\n\n{Fore.RESET}Possible Matches: ")
            print("\n".join(f" - {opt}" for opt in options))

        except wikipedia.exceptions.PageError:
            print(f"{Fore.RED}No results for term {query}{Fore.RESET}")

        except wikipedia.exceptions.HTTPTimeoutError:
            print(f"{Fore.RED}Please check your internet connection{Fore.RESET}")

        except Exception as e:
            print(f"An unknown error occured: {e}")

def getInfo(query, length=3, raw=False):
    
    try:
        top, candidates = searchWiki(query)
        
        if not top:
            print(f"{Fore.RED}No results for term {query}{Fore.RESET}")
        else:
            if raw:
                return wikipedia.summary(query, sentences=length, auto_suggest=False)
            else:
                print(f"Closest Match: {top}")        
                return wikipedia.summary(top, sentences=length, auto_suggest=False)

    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:10]
        print(f"{Fore.RED}The term {query} is ambiguous. Please refine your query.\n\n{Fore.RESET}Possible Matches: ")
        print("\n".join(f" - {opt}" for opt in options))

    except wikipedia.exceptions.PageError:
        print(f"{Fore.RED}No results for term {query}{Fore.RESET}")

    except wikipedia.exceptions.HTTPTimeoutError:
        print(f"{Fore.RED}Please check your internet connection{Fore.RESET}")

    except Exception as e:
        print(f"An unknown error occured: {e}")

@click.group()
def cli():
    pass

@cli.command()
@click.argument("query")
@click.option("--raw", is_flag=True, help="Get summary without searching for closest match")
def summarize(query, raw=False):
    print("Summarizing...")
    info = getInfo(query, CONFIG.get("info-length.summary"), raw)
    print(info)

@cli.command()
@click.argument("query")
@click.option("--length", default=CONFIG.get("info-length.definition"), help="Number of sentences in the definition")
@click.option("--raw", is_flag=True, help="Get summary without searching for closest match")
def define(query, length=15, raw=False):
    print("Defining...")
    info = getInfo(query, length, raw)
    print(info)

@cli.command()
@click.argument("query")
def search(query):
    top, candidates = searchWiki(query)
    print("Searching...")
    if top:
        print("\n".join(f" - {candidate}" for candidate in candidates[:10]))
    else:
        print(f"{Fore.RED}No results for term {query}{Fore.RESET}")

@cli.command()
@click.argument("query")
@click.option("--raw", is_flag=True, help="Open Wiki without searching for closest match")
def open(query, raw=False):
    print("Opening...")
    openPage(query, raw)

@cli.command()
@click.option("--open", is_flag=True, help="Open Wiki in the web browser")
def random(open):
    print("Fetching random article...")
    title = wikipedia.random()
    if open:
        openPage(title, True)
    else:
        info = getInfo(title, CONFIG.get("info-length.summary"), True)
        print(info)
    
@cli.command()
def version():
    print(f"{Fore.LIGHTGREEN_EX}WikiCLI v1.0.0{Fore.LIGHTYELLOW_EX}\n -theCamelCaseGuy{Fore.RESET}")

@cli.command()
def help():
    print("""
    WikiCLI - A command line tool to fetch information from Wikipedia.

    Commands:
        summarize [QUERY]      - Get a brief summary of the topic.
        define [QUERY]         - Get a detailed definition of the topic.
        search [QUERY]         - Search for topics related to the query.
        open [QUERY]           - Open the Wikipedia page for the topic in a web browser.
        random                 - Fetch a random Wikipedia article.
        version                - Display the version of WikiCLI.

    Options:
        --raw                  - Fetch information without searching for the closest match.
        --length [NUMBER]      - Specify the number of sentences in the definition (default is 15).
        --open                 - Open the Wikipedia page in a web browser (used with 'random' command).

    Examples:
        wiki summarize "Python programming"
        wiki define "Quantum mechanics" --length 10
        wiki search "Artificial Intelligence"
        wiki open "Machine Learning" --raw
        wiki random --open
        wiki version
    """)

cli()