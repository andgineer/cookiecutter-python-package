## Установка

## Установка pipx
[`pipx`](https://pypa.github.io/pipx/) создает изолированные среды, чтобы избежать конфликтов с 
существующими системными пакетами.

=== "MacOS"
    В терминале выполните:
    ```bash
    brew install pipx
    pipx ensurepath
    ```

=== "Linux"
    Сначала убедитесь, что Python установлен.

    Введите в терминал:

    ```bash
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    ```

=== "Windows"
    Сначала установите Python, если он еще не установлен.

    В командной строке введите (если Python был установлен из Microsoft Store, используйте `python3` вместо `python`):
    
    ```bash
    python -m pip install --user pipx
    ```

## Установка `{{ cookiecutter.package_name }}`:
В терминале (командной строке) выполните:

```bash
pipx install {{ cookiecutter.package_name }}
```
