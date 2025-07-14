import os
import asyncio
import google.generativeai as gen
from dotenv import load_dotenv

from core.crisis import CRISES
from core.advisor import Council

load_dotenv()
gen.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = gen.GenerativeModel("gemini-2.5-flash-preview-05-20")

class GameState:
    def __init__(self):
        self.treasury = 70
        self.stability = 70
        self.popularity = 60
        self.army = 65
        self.turn = 0

    def to_dict(self):
        return {
            "treasury": self.treasury,
            "stability": self.stability,
            "popularity": self.popularity,
            "army": self.army,
            "turn": self.turn
        }
    
async def test_council():
    state = GameState()
    council = Council()
    crisis, options = CRISES[0]
    thread = []
    advice = await council.consult(model, crisis, options, state.to_dict(), thread, [])
    for name, response in advice:
        print(f"{name}: {response}")

#---------------------------------------------------------------------

from rich import print as rprint
from rich.prompt import Prompt
from rich.panel import Panel
from rich.console import Console
import random

from core.stats import apply_policy, print_stats, generate_sample_policy_deltas

def print_player_commands():
    console = Console()
    console.print(Panel.fit(
        "[bold yellow]Player Commands[/bold yellow]\n\n"
        "[cyan]ask [advisor name] [message][/cyan]  - Ask a single advisor something\n"
        "[cyan]all [message][/cyan]               - Broadcast a message to all advisors\n"
        "[cyan]!choose [alloc_A] [alloc_B] [alloc_C][cyan/] - Lock in policy allocations (e.g., !choose 50 30 20)\n"
        "[cyan]log[/cyan]                         - Show the conversation history\n"
        "[cyan]quit[/cyan]                        - End the game immediately\n\n"
        "[dim italic]Example: !choose 60 20 20 (allocates 60% to A, 20% to B, 20% to C)[/dim italic]",
        title="How to Play",
        border_style="bright_blue"
    ))

async def game_loop():
    state = GameState()
    council = Council()
    console = Console()

    model = gen.GenerativeModel("gemini-2.5-flash-preview-05-20")
    gen.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    rprint(Panel("Welcome, ruler. Your reign begins now.", title="Counsel"))
    rprint("You have the following kingdom stats:")
    print_stats(state)
    rprint("Type \"Help\" for a list of commands. \n")

    thread = []

    while state.turn < 6:
        crisis_text, options = random.choice(CRISES)
        # = CRISES[state.turn % len(CRISES)] <- determine crisis selection
        state.turn += 1
        num_options = len(options)

        current_turn_policy_base_effects = [generate_sample_policy_deltas() for _ in options]
        
        rprint(f"\n[bold yellow]Crisis {state.turn}:[/] {crisis_text}")
        rprint("You have the following policy options:")
        for i, option in enumerate(options, start=65):
            rprint(f"  [bold]{chr(i)}[/]: {option}")