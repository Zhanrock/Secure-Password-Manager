from vault.vault import create_vault, open_vault, save_vault

# Create vault
try:
    create_vault("test.vault", "correct horse battery staple")
except FileExistsError:
    print("Vault already exists, opening existing one...")
vault = open_vault("test.vault", "correct horse battery staple")

# Open vault
vault = open_vault("test.vault", "correct horse battery staple")
print("Original:", vault)

# Add entry
vault["entries"]["example.com"] = {
    "username": "user123",
    "password": "p@ssw0rd"
}

# Save updated vault
save_vault(vault, "test.vault", "correct horse battery staple")

# Reopen to confirm
vault2 = open_vault("test.vault", "correct horse battery staple")
print("After update:", vault2)
