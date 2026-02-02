import sys

from praynet import create_app

try:
    app = create_app()
except Exception as e:
    print(f"Failed to create app: {e}", file=sys.stderr)
    raise e

if __name__ == "__main__":
    app.run(debug=True)
