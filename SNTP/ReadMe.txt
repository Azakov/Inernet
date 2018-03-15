последние 4 элемента от vars(a) - последний тут всегда говорит правду, остальные нет
Origin Timestamp - время когда клиент отправил серверу запрос
Receive Timestamp - время когда сервер получил запрос
Transmit Timestamp - время когда сервер отправляет запрос
dest_timestamp - время когда ntp отправил серверу запрос

запуск клиента в cmd:
>>> import ntplib
>>> c = ntplib.NTPClient()
>>> a = c.request("127.0.0.1") или a = c.request("127.0.0.1", port = 6000)
>>> vars(a) 

запуск сервера:
py server.py -s 100 - например врет на 100 секунд