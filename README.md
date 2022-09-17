Перед использванием нужно переименовать .env.example -> .env и установить свои настройки при необходимости

Url'ы сервисов находятся в target_services.json

LoadBalancer работает на порте 1000
Сервисы-таргеты на портах 1001-1005

Запуск приложения
```
docker compose up -d --force-recreate --build
```

Выключение одного из сервисов-таргетов
```
docker compose stop {container}
```

Включение одного из сервисов-таргетов
```
docker compose start {container}
```

Просмотр логов
```
docker compose logs -f {container}
```