Это простое приложение чата, использующее Tornado, Redis и WebSocket для двусторонней связи. Сообщения от пользователей отображаются в общем чате , а список подключенных клиентов обновляется в реальном времени.
---
## Функционал
- **Чат в реальном времени:** Сообщения отправляются и принимаются через WebSocket.
- **Список онлайн-клиентов:** Виджет, показывающий текущих пользователей.
- **Использование Redis:** Хранение сообщений и управление Pub/Sub.
---
## Требования
1. Python 3.8+ установлен на вашем компьютере.
2. Установленный и запущенный Redis:
3. Установленные зависимости Python:
   - Tornado
   - Redis
---
## Установка и запуск
### 1. Склонируйте репозиторий или загрузите проект.
Убедитесь, что вы находитесь в рабочей директории проекта.
### 2. Установите зависимости
Выполните следующую команду для установки всех необходимых библиотек:
```pip install tornado redis```

### 3. Убедитесь, что Redis запущен
Для запуска Redis выполните следующую команду:
```redis-server```

### 4. Запустите сервер
Запустите сервер, выполнив:
```python server.py```

После успешного запуска вы увидите сообщение в терминале:

Server started at http://localhost:8888


