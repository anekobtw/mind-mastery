import os
import shutil

shutil.rmtree("database/__pycache__")
shutil.rmtree("handlers/__pycache__")
shutil.rmtree("keyboards/__pycache__")
shutil.rmtree("misc/__pycache__")
shutil.rmtree("__pycache__")

# for database in os.listdir("databases"):
#     os.remove(f"databases/{database}")

os.remove("log.txt")

os.system("black . -l 150")
os.system("isort .")
os.system("cls")
