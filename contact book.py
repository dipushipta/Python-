def add():
    name = input("Enter Name: ")
    phone = input("Enter Phone: ")
    email = input("Enter Email: ")
    address = input("Enter Address: ")
    open("contacts.txt","a").write(f"{name},{phone},{email},{address}\n")
    print(" Saved!\n")

def view():
    try:
        for c in open("contacts.txt"):
            name,phone,email,address = c.strip().split(",")
            print(f"Name:{name},Phone:{phone},Email:{email},Address:{address}")
    except:
        print("No Contacts!\n")

def search():
    s = input("Search Name:").lower()
    try:
        for c in open("contacts.txt"):
            if s in c.lower():
             print("Found:",c.strip())
             break
        else:
         print("Not found!\n")
    except:
        print("No File\n")

while True:
    d = input("\n 1.Add 2.View 3.Search 4.Exit:  ")
    if d == "1": add()
    elif d == "2": view()
    elif d == "3": search()
    elif d == "4": exit()
    else: print("Invalid")
