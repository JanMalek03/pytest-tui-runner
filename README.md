# pytest-tui-runner

> Interactive Textual User Interface (TUI) for running pytest tests easily from your terminal.


## Introdution

Kdyz jsem spoustel testy pomoci pytestu, tak mel problem s tim, ze jsem neumel lehce spoustet jen ty testy, ktere jsem chtel pomoci pytest prikazu. Proto jsem zacal pracovat na knihovne, ktera mi toto usnadni.


## Features

`pytest-tui-runner` umoznuje vytvoreni vlastniho TUI, ktere obsahuje presne ty testy ktere potrebuje a nasledne je muze spustit.
Obsahuje terminal, ve kterem si muzete projit vypisy od pytestu, ale pro zjednoduseni se spustene testy zabarvi podle vysledku (zelene == test prosel, cervena == test selhal, modra == test probiha)
Plugin take umoznuje parametrizaci testu. Pri configuraci muzu testy uvest jako ze maji argumenty a potom v terminalu zadat jedlotlive hodnoty ktere chci testovat.


## Usage

V hlavni slozce vaseho projektu (tam kde mate slozku tests) je potreba vytvorit slozku s nazvem pytest_tui_runner, coz bude slozka obsahujici vse spolecne s pluginem (logy, config, ulozene stavy widgetu). Po vytvoreni konfiguracniho souboru (vysletlene v casti Configuration) staci v terminalu zadat pytest-tui run a otevre se uzivatelske prostredi.
Jedlotlive testy se daji zaskrtnou a nebo u testu s argumenty se vyplni vsechna pole pro jednotlive argumenty (ty se musi presne schodovat s temi kterema konkretni odkazovany test).



## Configuration

V slozce pytest_tui_runner vytvorte default.yaml soubor, coz bude konfiguracni soubor. 
Struktura souboru je nasledovna:

Testy radime do kategorii (categories), kde kazda ma label.
Kazda kategorie obsahuje podkategorie (subcategories), ktere maji take label.
V podkategorii uz muzu uvest jednotlive testy (tests).

Kazdy test ma label a odkaz na realny test. To bud muze byt test_name, ktere se presne musi schodovat s realnym nazvem testu a nebo pomoci markers, coz je seznam markeru, podle kterych se test bude vyhledavat (pro markery ["setup", "login"] se spusti vsechny testy, ktere maji prave markery setup a login).

Pote co test v configuracnim souboru odkazuje na skutecny test, tak muzeme take zadat ze test ma argumenty (parametrizaci). To udelame pridanim arguments.

Kazdy argument ma arg_name, ktery se presne musi schodovat s argumentem testu. Dale pak arg_type, coz muze byt bud "text_input" a nebo "select".
"test_input" argument

Tady je priklad konfiguracniho souboru:

categories:
  - label: "Category label"
    subcategories:
      - label: "Subcategory label"
        tests:
          - label: "First test name"
            markers: ["test1"]
          - label: "Second test name"
            test_name: "test_2"
      - label: "Second subcategory label"
          - label: "Test with arguments"
            test_name: "test_with_arguments"
            arguments:
              - arg_name: "x"
                arg_type: "text_input"
                placeholder: "Enter x"
              - arg_name: "action"
                arg_type: "select"
                options: ["add", "subtract", "multiply", "divide"]













**Textual-based terminal UI for running pytest tests**

`pytest-tui-runner` is a plugin and standalone tool that provides an interactive **Textual User Interface (TUI)** for configuring and running Python tests using [pytest](https://pytest.org/).  
It allows developers to easily filter, parametrize, and execute tests directly from the terminal in a clear, interactive environment.

---

## Installation

You can install the package from PyPI:

```bash
pip install pytest-tui-runner
```

---


## Usage
```bash
pytest-tui run
```

Or you can run it with specific path to tests
```bash
pytest-tui run /path/to/your/tests
```

---

## Configuration

`pytest-tui-runner` is configured in the pytest_tui_runner folder, which you have to create in the whole project at the ROOT level.
In that folder, create a default_test.ya file and define your required test structure according to the template.

---

## License

This project is licensed under the **[MIT License]** - see the `LICENSE' file for more details..
