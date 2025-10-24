import subprocess
import os
import sys

os.chdir('/workspace')

print("=== Git Status ===")
result = subprocess.run(['git', 'status'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

print("\n=== Git Remote ===")
result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

print("\n=== Adding file ===")
result = subprocess.run(['git', 'add', 'sistema-camaras-flask/templates/login.html'], capture_output=True, text=True)
print("Add result:", result.returncode)
if result.stderr:
    print("STDERR:", result.stderr)

print("\n=== Committing ===")
result = subprocess.run(['git', 'commit', '-m', 'Actualizar diseño login: fondo degradado celeste'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print("Commit result:", result.returncode)

print("\n=== Pushing ===")
result = subprocess.run(['git', 'push', 'origin', 'master'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print("Push result:", result.returncode)
