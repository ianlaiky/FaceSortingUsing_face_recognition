from pathlib import Path
destdir = Path('img')
files = [p for p in destdir.iterdir() if p.is_file()]
for p in files:
    with p.open() as f:
        print(f.name)