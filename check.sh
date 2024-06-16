ruff check . &&
ruff format --check . &&
mypy . --strict &&
pytest &&
printf "\033[1mAll is good!\033[0m 🚀\n"
