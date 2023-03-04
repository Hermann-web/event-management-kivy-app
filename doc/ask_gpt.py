import os 

out = "look at my kivy project \n"
list_files = ["main.py", "login_screen.py", "login_screen.kv", "list_screen.py", "list_screen.kv"]
for file in list_files:
	with open(file) as f:
		out += f"\n##{file}\n"
		out+= "'''\n" + f.read() + "\n'''\n"


with open("ask-gpt.txt","w") as f:
    f.write(out)
    
os.startfile("ask-gpt.txt")