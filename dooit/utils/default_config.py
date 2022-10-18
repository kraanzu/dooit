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
# desc: desc of the Todo
# icon: icon to show for status
# tags: show tags, if any( modify tag format in extra_fmt )
# recur: show recurrence, if any ( modify tag format in extra_fmt )

todos = {
    "icon": {
        "status": {
            "done": "X",
            "pending": "o",
            "overdue": "O",
        },
        "urgency": {
            1: "🅓",
            2: "🅒",
            3: "🅑",
            4: "🅐",
        },
    },
    "extra_fmt": {
        "tag": "T {tags}",  # how to show tags
        "recur": "R {recur}",  # how to show recurrence,
    },
    "fmt": {
        "about": {
            "highlight": "[b white]{desc}[/b white]",
            "dim": "[d grey50]{desc}[/d grey50]",
            "edit": "[b cyan]{desc}[/b cyan]",
        },
        "date": {
            "highlight": "[b white]{date}[/b white]",
            "dim": "[d grey50]{date}[/d grey50]",
            "edit": "[b cyan]{date}[/b cyan]",
        },
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
