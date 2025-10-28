import os

# Create all directories
dirs = [
    'tools',
    'src/core',
    'src/app_web',
    'tests',
    'data/inbox',
    'data/processed'
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"Created: {d}")

print("\nAll directories created successfully!")
