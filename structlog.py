import logging
from structlog.stdlib import LoggerFactory
import sys
import structlog

# Импортируем необходимые модули для логирования, работы с Flask и работы со структурированными логами

from flask import Flask, request, g

# Настраиваем стандартное логирование с выводом в stdout и уровнем логирования INFO
logging.basicConfig(format="%(message)s",
                    stream=sys.stdout,
                    level=logging.INFO) # логируем уровень login info

app = Flask(__name__)  # Создаем экземпляр Flask приложения
structuured_log = structlog.get_logger()  # Получаем экземпляр логгера structlog

import datetime


def timesstamer(_, __, eventdict):
    # Добавляем в каждый лог-событие текущую метку времени в ISO формате
    eventdict['time'] = datetime.datetime.now().isoformat()
    return eventdict

# Настраиваем structlog с использованием процессоров и фабрики логгеров
structlog.configure(
    processors=[timesstamer, structlog.processors.JSONRenderer()],
    logger_factory=LoggerFactory()
)


@app.before_request
def before_request():
    # Функция, выполняемая перед каждым запросом
    # Извлекаем метод запроса и user agent, и связываем их с логом
    method = request.user_agent
    user_agent = request.user_agent
    log = structuured_log.bind(method=method, user_agent=user_agent)
    g.log = log  # Сохраняем связанный логгер в глобальном объекте g


@app.route('/one')
def one():
    # Обработчик для маршрута '/one'
    g.log.msg('route one')  # Логируем сообщение 'route one'
    return 'one', 200  # Возвращаем ответ 'one' и статус-код 200

@app.route('/second')
def second():
    # Обработчик для маршрута '/second'
    g.log.msg('route second')  # Логируем сообщение 'route second'
    return 'second', 200  # Возвращаем ответ 'second' и статус-код 200

if __name__ == '__main__':
    # Запускаем приложение Flask, если скрипт выполняется как основная программа
    app.run()
