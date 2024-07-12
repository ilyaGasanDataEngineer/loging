from flask import Flask
from loguru import logger

app = Flask(__name__)

logger.add( # куда логировать
    "logs/log.log",
    rotation='1 week', # следующий через неделю
    compression='zip', # сжатие
    level='INFO',
    format="{time} {level} {message}",
    backtrace=True, # в случае ошибок будем смотреть от куда пришла
    diagnose=True
)

@app.route('/one')
def one():
    logger.info('one route')
    return 'one', 200

@app.route('/second')
def second():
    # Обработчик для маршрута '/second'
    logger.info('route second')  # Логируем сообщение 'route second'
    return 'second', 200  # Возвращаем ответ 'second' и статус-код 200


@app.route('/decorator_error')
@logger.catch # если маршутизации на ectorator_error будет ошибка loguru подхватит
def decorator_error():
    null_var = 0
    a = 1 / null_var
    return 'decorator_error'

if __name__ == '__main__':
    app.run()