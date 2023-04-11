def menu_start():
    app_running = True
    while app_running:
        choice = welcome_menu()
        if choice == "V":
            print("view something")
        elif choice == "N":
            print("add something")
        elif choice == "A":
            print("analyze something")
        elif choice == "B":
            print("backup now!")
        elif choice == "Q":
            print("peace out!")
            quit()


def welcome_menu():
    while True:
        print("""
        \n==================================
        \n======== Store Inventory =========
        \n==================================
        \n- View Single Product Details: (V)
        \n- Add a New Product: (N)
        \n- View an Analysis: (A)
        \n- Backup Entire Database: (B)
        \n- Quit: (Q)
        """)
        choice = input("\nWhat would you like to do? ").upper()
        if choice in ["V", "N", "A", "B", "Q"]:
            return choice
        else:
            input("""
            \n>>>>>>>>>>>>>
            \n>>> ERROR >>>
            \n>>>>>>>>>>>>>
            \nPlease choose one of the following options...
            \nV, N, A, B or Q.
            \nPress Enter to try again.
            """)
