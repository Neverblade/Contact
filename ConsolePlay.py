from Contact import Contact

contact = Contact()


def process_input(line):
    tokens = line.split()
    if tokens[0] == "add":
        if len(tokens) == 2:
            contact.add_player(tokens[1])
            return
    elif tokens[0] == "remove":
        if len(tokens) == 2:
            contact.remove_player(tokens[1])
            return
    elif tokens[0] == "submit":
        if len(tokens) == 3:
            contact.submit_word(tokens[1], tokens[2])
            return
    print("Not a valid command.")

process_input("add p1")
process_input("add p2")
process_input("add p3")
contact.print_state()
while True:
    process_input(input())
    while contact.has_messages():
        print(contact.read_message())
    contact.print_state()