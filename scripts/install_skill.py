from pathlib import Path
import argparse,shutil
p=argparse.ArgumentParser(description="Install the complete, self-contained skill without overwriting an existing installation.")
p.add_argument('--destination',required=True,help='Your Codex skills directory');args=p.parse_args()
source=Path(__file__).resolve().parents[1]/'skills/photo-book-studio';target=Path(args.destination).expanduser().resolve()/'photo-book-studio'
if target.exists():p.error(f'{target} already exists; inspect or back it up before replacing it.')
shutil.copytree(source,target);print(f'Installed {target}. Start a new conversation to discover it.')
