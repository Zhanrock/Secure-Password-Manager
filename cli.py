# vault_cli.py
import getpass
from pathlib import Path
from vault.vault import create_vault, open_vault, save_vault

def main():
    vault_path = input("Enter vault path: ").strip()
    password = getpass.getpass("Enter vault password: ")

    path = Path(vault_path)
    if path.exists():
        try:
            vault = open_vault(vault_path, password)
            print("Vault loaded.")
        except Exception as e:
            print("Failed to open vault:", e)
            return
    else:
        create_vault(vault_path, password)
        vault = open_vault(vault_path, password)
        print("New vault created.")

    # CLI loop
    while True:
        cmd = input("> ").strip().lower()
        if cmd == "list":
            entries = vault["entries"]
            if not entries:
                print("No entries")
            else:
                for site, data in entries.items():
                    print(f"{site}: {data['username']} / {data['password']}")
        elif cmd == "add":
            site = input("Site: ").strip()
            username = input("Username: ").strip()
            pwd = getpass.getpass("Password: ")
            vault["entries"][site] = {"username": username, "password": pwd}
            print("Entry added.")
        elif cmd == "edit":
            site = input("Site to edit: ").strip()
            if site not in vault["entries"]:
                print("Entry not found.")
                continue
            username = input(f"Username [{vault['entries'][site]['username']}]: ").strip()
            pwd = getpass.getpass("Password [hidden]: ")
            if username:
                vault["entries"][site]["username"] = username
            if pwd:
                vault["entries"][site]["password"] = pwd
            print("Entry updated.")
        elif cmd == "delete":
            site = input("Site to delete: ").strip()
            if site in vault["entries"]:
                del vault["entries"][site]
                print("Entry deleted.")
            else:
                print("Entry not found.")
        elif cmd == "exit":
            save_vault(vault, vault_path, password)
            print("Vault saved. Goodbye!")
            break
        else:
            print("Commands: list, add, edit, delete, exit")

if __name__ == "__main__":
    main()
