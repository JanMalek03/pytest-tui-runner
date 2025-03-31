import subprocess
import sys

def main():
    try:
        subprocess.run(["uv", "run", "-m", "src.ui.tui.app"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Chyba při spuštění aplikace: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
