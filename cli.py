# vault_cli.py

from vault.vault import create_vault, open_vault, save_vault
import getpass
import sys

# ---------- helpers ----------

def prompt(msg: str) -> str:
    return input(f"{msg}: ").strip()

def confirm(msg: str) -> bool:
    return input(f"{msg} (y/n): ").lower() == "y"

def header(title: str):
    print("\n" + title)
    print("─" * len(title))

def pretty_entries(entries: dict):
    if not entries:
        print("📭 Vault is empty")
        return

    for site, data in entries.items():
        print(f"🔑 {site}")
        print(f"   Username: {data['username']}")
        print("-" * 30)

# ---------- vault actions ----------

def add_entry(vault: dict):
    header("➕ Add Entry")
    site = prompt("Site")
    username = prompt("Username")
    password = getpass.getpass("Password: ")

    vault["entries"][site] = {
        "username": username,
        "password": password,
    }

    print("✅ Entry added")

def view_entry(vault: dict):
    header("👁 View Entry")
    site = prompt("Site")

    entry = vault["entries"].get(site)
    if not entry:
        print("❌ Entry not found")
        return

    print(f"Site: {site}")
    print(f"Username: {entry['username']}")
    print(f"Password: {entry['password']}")

def search_entries(vault: dict):
    header("🔍 Search Entries")
    keyword = prompt("Search keyword").lower()

    results = {
        site: data
        for site, data in vault["entries"].items()
        if keyword in site.lower()
    }

    pretty_entries(results)

def delete_entry(vault: dict):
    header("🗑 Delete Entry")
    site = prompt("Site")

    if site not in vault["entries"]:
        print("❌ Entry not found")
        return

    if confirm(f"Delete '{site}'?"):
        del vault["entries"][site]
        print("✅ Entry deleted")

# ---------- menus ----------

def vault_menu(path: str, password: str):
    try:
        vault = open_vault(path, password)
    except Exception as e:
        print(f"❌ {e}")
        return

    while True:
        header("📂 Vault Menu")
        print("1. List entries")
        print("2. Add entry")
        print("3. View entry")
        print("4. Search entries")
        print("5. Delete entry")
        print("6. Save & exit")

        choice = prompt("Choose")

        if choice == "1":
            pretty_entries(vault["entries"])
        elif choice == "2":
            add_entry(vault)
        elif choice == "3":
            view_entry(vault)
        elif choice == "4":
            search_entries(vault)
        elif choice == "5":
            delete_entry(vault)
        elif choice == "6":
            save_vault(
                path=path,
                vault_data=vault,
                password=password,
            )
            print("💾 Vault saved. Goodbye!")
            return
        else:
            print("❌ Invalid choice")

def startup_menu():
    header("🔐 Secure Password Vault")
    print("1. Create new vault")
    print("2. Open existing vault")
    print("3. Exit")

    choice = prompt("Choose")

    if choice == "1":
        path = prompt("Vault filename")
        password = getpass.getpass("Master password: ")
        try:
            create_vault(path, password)
            print("✅ Vault created")
        except FileExistsError:
            print("❌ Vault already exists")

    elif choice == "2":
        path = prompt("Vault filename")
        password = getpass.getpass("Master password: ")
        vault_menu(path, password)

    elif choice == "3":
        sys.exit(0)

    else:
        print("❌ Invalid choice")

# ---------- entry point ----------

def main():
    while True:
        startup_menu()

if __name__ == "__main__":
    main()
