from textual.widget import Widget

TestWidget = Widget | list[Widget]

Category = str

WidgetsDict = dict[str, dict[str, dict[str, TestWidget]]]


# widgets state type
TestValue = list[bool] | list[dict[str, str]]
SavedSubcat = dict[str, TestValue]
SavedCat = dict[str, SavedSubcat]

# main type
SavedState = dict[str, SavedCat]
