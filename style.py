from colorama import Fore, Back, Style


class StyleConfig:
    AliveColor = Fore.CYAN
    BorderColor = Fore.BLUE
    BackgroundColor = Back.RESET

    FontStyle = Style.BRIGHT

    ResetForeColor = Fore.RESET
    ResetBackgroundColor = Back.RESET
    ResetStyle = Style.RESET_ALL
    ResetAll = ResetForeColor + ResetBackgroundColor + ResetStyle