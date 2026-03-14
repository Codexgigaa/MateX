# test_db.py

from database.db import save_messages, get_history

save_messages("user", "Hello", "2026-03-15")
save_messages("bot", "Hi there", "2026-03-15")

history = get_history()

print(history)