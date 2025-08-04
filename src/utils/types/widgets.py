from textual.widget import Widget

TestWidget = Widget | list[Widget]

Category = str

WidgetsDict = dict[str, dict[str, dict[str, TestWidget]]]
