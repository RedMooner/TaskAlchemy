


# Cmdlet Manager

Cmdlet Manager — это командная оболочка для управления и выполнения командлетов (скриптов) на Python и PowerShell. Она позволяет пользователям создавать, запускать, удалять и получать информацию о командлетах.

## Установка

1. Убедитесь, что у вас установлен Python (версия 3.6 и выше) и PowerShell.
2. Склонируйте репозиторий или скачайте скрипт.
3. Установите необходимые зависимости, если они есть.

## Использование

Запустите скрипт командой:

```bash
python cmdlet_manager.py
```

После запуска вы увидите приглашение командной строки:

```
> 
```

### Доступные команды

- `help` - вывести справку по доступным командам.
- `list` - вывести список доступных командлетов.
- `run <cmdlet_name> [args]` - запустить командлет с аргументами.
- `create <cmdlet_name>` - создать новый командлет.
- `delete <cmdlet_name>` - удалить командлет.
- `man <cmdlet_name>` - вывести информацию о командлете.

### Примеры

#### Список командлетов

Чтобы вывести список доступных командлетов, введите:

```
> list
```

#### Запуск командлета

Чтобы запустить командлет с именем `greet` и передать аргумент, выполните:

```
> run greet -name "Иван"
```

#### Создание нового командлета

Чтобы создать новый командлет с именем `hello.py`, выполните:

```
> create hello.py
```

#### Удаление командлета

Чтобы удалить командлет с именем `greet`, выполните:

```
> delete greet
```

#### Получение информации о командлете

Чтобы получить информацию о командлете `greet`, выполните:

```
> man greet
```

## Логирование

Все действия и ошибки записываются в файл `command_shell.log`. Вы можете просмотреть этот файл для диагностики проблем или анализа использования.

## Примечания

- Командлеты должны иметь расширение `.py` для Python или `.ps1` для PowerShell.
- Убедитесь, что у вас есть необходимые права для выполнения PowerShell скриптов.

## Лицензия

Этот проект лицензирован под MIT License. Пожалуйста, смотрите файл LICENSE для получения дополнительной информации.

## Контрибьюция

Если вы хотите внести свой вклад в проект, пожалуйста, создайте форк репозитория и отправьте пулл-реквест с вашими изменениями.

```

Эта документация охватывает основные аспекты использования вашего скрипта и может быть дополнена в зависимости от ваших потребностей.
