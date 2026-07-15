from src.etl.loader import load_supporting_files

data = load_supporting_files()

print("Peer Groups Columns:")
print(data["peer_groups"].columns.tolist())

print("\nSectors Columns:")
print(data["sectors"].columns.tolist())
