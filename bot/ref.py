import os
import shutil

shutil.rmtree("handlers/__pycache__")
shutil.rmtree("misc/__pycache__")
shutil.rmtree("__pycache__")

# for database in os.listdir("databases"):
#     os.remove(f"databases/{database}")

os.system("black . -l 9999")
os.system("isort .")
os.system("cls")
