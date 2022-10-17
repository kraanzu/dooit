# NOTE: See rich style documentation for details
#################################
#             UTILS             #
#################################
def colored(text: str, color: str):
    return f"[{color}]{text}[/{color}]"


#################################
#            NAVBAR             #
#################################
# Vars:
# desc: desc of the workspace/topic
# icon: icon to show for workspace

navbar = {
    "fmt": {
        "highlight": " [b white]{desc}[/b white]",
        "dim": " [d grey50]{desc}[/d grey50]",
        "edit": " [b cyan]{desc}[/b cyan]",
    },
}

#################################
#            TODOS              #
#################################
# Vars:
# name: name of the workspace/topic
# icon: icon to show for workspace and topic
todos = {
    "icon": {
        "status": {
            "done": "",
            "pending": "",
            "overdue": "",
        },
        "urgency": {
            1: "🅓",
            2: "🅒",
            3: "🅑",
            4: "🅐",
        },
    },
    "fmt": {
        "highlight": "",
        "dim": "",
        "edit": "",
    },
}

#################################
#          STATUS BAR           #
#################################
# TOP

# BOTTOM

#################################
#          KEYBINDING           #
#################################
