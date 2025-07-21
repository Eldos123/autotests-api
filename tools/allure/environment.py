from config import settings
import platform
import sys


def create_allure_environment_file():

    # Получаем информацию об операционной системе
    os_info = f"{platform.system()}, {platform.release()}"

    # Получаем информацию о версии Python
    python_version = sys.version

    # Создаем список из элементов в формате {key}={value}
    items = [
        f'os_info={os_info}',
        f'python_version={python_version}',
        *[f'{key}={value}' for key, value in settings.model_dump().items()]
    ]

    # Собираем все элементы в единую строку с переносами
    properties = '\n'.join(items)

    # Открываем файл ./allure-results/environment.properties на чтение
    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w+') as file:
        file.write(properties)  # Записываем переменные в файл