# eBay Monitor Pro & Skylots Monitor - Веб-версия для iPhone

## Быстрый старт (локально)

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Запуск eBay Monitor
```bash
python ebay_app.py
```

### 3. Запуск Skylots Monitor
```bash
python app.py
```

### 4. Открыть на iPhone в одной сети
- Найди IP адрес ПК: `ipconfig` (ищи IPv4 Address)
- На iPhone в Safari: `http://[IP]:5000`
- Например: `http://192.168.1.100:5000`

---

## Развертывание на Render (работает везде)

### Шаг 1: Подготовка
1. Создай папку проекта с файлами:
   - `ebay_app.py` (или `app.py` для Skylots)
   - `requirements.txt`
   - `templates/ebay.html` (или `templates/index.html`)

### Шаг 2: GitHub
1. Создай аккаунт на https://github.com
2. Создай новый репозиторий (например, `ebay-monitor`)
3. Загрузи файлы:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/[твой_username]/ebay-monitor.git
   git push -u origin main
   ```

### Шаг 3: Render
1. Перейди на https://render.com
2. Нажми "New +" → "Web Service"
3. Выбери "Connect a repository" → выбери свой репозиторий
4. Заполни:
   - **Name**: `ebay-monitor` (или `skylots-monitor`)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python ebay_app.py` (или `python app.py`)
5. Нажми "Create Web Service"
6. Жди 2-3 минуты
7. Получишь ссылку типа: `https://ebay-monitor.onrender.com`

### Шаг 4: На iPhone
1. Открой Safari
2. Введи полученную ссылку
3. Нажми Share → "Add to Home Screen"
4. Готово! Работает как приложение

---

## Структура проекта

```
project/
├── ebay_app.py          # Flask приложение для eBay
├── app.py               # Flask приложение для Skylots
├── requirements.txt     # Зависимости
└── templates/
    ├── ebay.html        # Интерфейс eBay Monitor
    └── index.html       # Интерфейс Skylots Monitor
```

---

## Важно!

⚠️ **API ключи eBay:**
- Получи на https://developer.ebay.com
- Используй Sandbox ключи для тестирования
- Переключись на Production ключи для реальных аукционов

⚠️ **Безопасность:**
- Не делись ссылкой с API ключами
- Используй HTTPS (Render автоматически)
- Ключи хранятся только в браузере (не отправляются на сервер)

---

## Решение проблем

### Ошибка "Connection refused"
- Проверь что приложение запущено
- Проверь IP адрес (должен быть в одной сети)

### Ошибка "API Key invalid"
- Проверь что ключи скопированы правильно
- Используй Sandbox ключи для тестирования

### Медленная загрузка на Render
- Первый запрос может быть медленным (холодный старт)
- Последующие запросы будут быстрее

---

## Контакты

Если есть вопросы - пиши! 🚀
