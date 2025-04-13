import subprocess

def print_file(file_path):
    subprocess.run(['lp', file_path])

# Example
print_file('/Users/ahmedzaiou/Documents/ProjetsApps/TrackPharmic/README.md')
