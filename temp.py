import time
import sys
from colorama import init, Fore, Style

# Initialize colorama for Windows compatibility
init()

# Colors for the loading bar
colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

def colorful_loading_bar(total=300, delay=0.1):
    """
    Displays a colorful animated loading bar.
    
    Args:
        total (int): The length of the loading bar.
        delay (float): Delay between each step in seconds.
    """
    for i in range(1, total + 1):
        color = colors[i % len(colors)]  # Cycle through colors
        bar = "█" * i + "-" * (total - i)  # Create the bar
        sys.stdout.write(f"\r{color}[{bar}]{Style.RESET_ALL} {int(i/total * 100)}%")
        sys.stdout.flush()
        time.sleep(delay)

    print("\nDone! ✅")

# Run the loading bar
colorful_loading_bar()
