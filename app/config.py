from pathlib import Path

from envparse import env

root_dir = Path(__file__).parent.parent
res_dir = root_dir / "res"

env.read_envfile(root_dir / ".env")

TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN")
SQLITE_URI = f"sqlite://{root_dir}/db.sqlite"
print(SQLITE_URI)
