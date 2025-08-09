from textual.widget import Widget

TestArguments = list[Widget]

TestWidgets = list[Widget] | list[TestArguments]

WidgetsDict = dict[str, dict[str, dict[str, TestWidgets]]]
