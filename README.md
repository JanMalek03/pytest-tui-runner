# pytest-tui-runner

> Interactive Textual User Interface (TUI) for running pytest tests easily from your terminal.


## Introdution

When I was running tests with `pytest`, I often struggled to easily select and execute only the tests I needed.  
Typing long and complex command-line arguments was error-prone and not very convenient.  
That inspired me to create **`pytest-tui-runner`**, a plugin that makes working with tests much simpler and more interactive — right inside your terminal.


## Features
`pytest-tui-runner` allows you to create your own **text-based interface** that lists and organizes your tests exactly the way you want.  
You can select tests, provide parameters, and run them. All from a user-friendly terminal interface.

Main features:
- **Interactive test selection** – check or uncheck which tests to run
- **Color-coded test results** – 
  - 🟢 Green → test passed  
  - 🔴 Red → test failed  
  - 🔵 Blue → test running
- **Test parametrization** – easily provide test arguments via text inputs or dropdown menus  
- **Integrated terminal output** – see real pytest logs while tests run  
- **Persistent interface state** – the layout and widget values are saved in local files, so you can easily share or restore your test setup later.


## Instalation

Install from PyPI using:

```bash
pip install pytest-tui-runner
```



## Usage

In the **root folder** of your project (where you have the `tests/` directory), create a folder named `pytest_tui_runner`.  
This folder will store everything related to the plugin — logs, configuration files, and widget states.

Once your configuration file is ready (see the *Configuration* section below), simply run:

```bash
pytest-tui run
```

The terminal interface will open.  
You can then:
- Check or uncheck individual tests to include or exclude them  
- Fill in argument fields for parametrized tests  
- Add additional parameter sets using the green **+** button (each click creates a new row of arguments)  
- Start the execution directly from the TUI  
- Switch to the **terminal view** – you can copy text from it by holding **Shift** and dragging the mouse to select the desired output 


## Configuration

Inside the `pytest_tui_runner` folder, create a file named **`default.yaml`**.  
This is the main configuration file defining how your tests are grouped and displayed.

### Structure overview

Tests are organized into **categories**, each with a `label`.  
Each category can contain one or more **subcategories**, which also have their own `label`.  
Inside each subcategory, you define individual **tests**.

Every test can be referenced in two ways:
- Using `test_name` → must exactly match the real test function name.  
  This means that **one checkbox in the TUI corresponds to one specific test function**.
- Using `markers` → a list of pytest markers (e.g. `["setup", "login"]`) that will be used to find all matching tests.  
  In this case, **a single checkbox can represent multiple tests** — all tests that contain the specified markers will be executed together.


You can also define **arguments** for parametrized tests.  
Each argument must be described precisely using the following fields:

- `arg_name` → must exactly match the argument name used in the referenced test function  
- `arg_type` → specifies how the value will be entered in the TUI and must be one of:
  - `"text_input"` – user can type a custom text value manually  
  - `"select"` – user can choose from predefined options
- Additional fields depending on the type:
  - for `"text_input"` → include a `placeholder` field to show a hint in the input box  
  - for `"select"` → include an `options` field, which is a list of selectable values  

These definitions allow the TUI to dynamically generate interactive input fields that correspond to real test parameters.

---

### Example configuration file

```yaml
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
        tests:
          - label: "Test with arguments"
            test_name: "test_with_arguments"
            arguments:
              - arg_name: "x"
                arg_type: "text_input"
                placeholder: "Enter x"
              - arg_name: "action"
                arg_type: "select"
                options: ["add", "subtract", "multiply", "divide"]
```


## Example Project Structure

```
my_project/
├── pytest_tui_runner/
│   └── default.yaml
├── tests/
│   ├── test_math.py
│   └── test_login.py
└── src/
    └── my_app/
```



## 🖼️ Screenshots

Here’s how the TUI looks in action:

![pytest-tui-runner main view](https://raw.githubusercontent.com/JanMalek03/pytest-tui-runner/default_tui/docs/MainScreen.png)


## 🤝 Contributing

If you have ideas, feedback, or suggestions for improvements, I’d love to hear from you!  
You can reach out directly via **email** or message me on **LinkedIn**:

- Email: your.email@example.com  
- LinkedIn: [Your Name](https://www.linkedin.com/in/janmalek436159283)  

If you prefer, you can also open a discussion or issue on the [GitHub Issues](https://github.com/JanMalek03/pytest-tui-runner/issues) page.


## License

This project is licensed under the **[MIT License]** - see the `LICENSE' file for more details..
