# Star do Vale

An indie farming simulation role-playing game.

## How to Run

After installing (follow the **Getting Started** section), just run:

```shell
python -m src.main
```

## Getting Started

Follow the steps below to ensure you have the necessary tools installed before starting development.

### 1. Install poetry

```shell
sudo apt install poetry
```

### 2. Check poetry version

```shell
poetry --version
```

Your poetry version should not be be below 1.2. Ideally, it should be above 1.5. Update your poetry version if needed. Try:

```shell
poetry self update 1.8.3
```

### 2. Check python version

```shell
python --version
```

Your python version should be above 3.12. If it's not, try updating it:

```shell
sudo apt install python3.12-tk
```

### 3. Install dependencies

After you are done with poetry and python isntallation, install all other project dependencies using poetry:

```shell
poetry install
```
