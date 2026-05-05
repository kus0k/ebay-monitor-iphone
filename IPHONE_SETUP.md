# 📱 eBay Monitor для iPhone - Полная инструкция

## ✅ Что нужно сделать

### 1️⃣ GitHub (5 минут)
### 2️⃣ Render (5 минут)
### 3️⃣ iPhone (2 минуты)

---

## 📝 Шаг 1: Создай GitHub аккаунт

1. Перейди на https://github.com/signup
2. Заполни:
   - Email
   - Password
   - Username (запомни!)
3. Нажми "Create account"
4. Подтверди email

---

## 📤 Шаг 2: Загрузи файлы на GitHub

### 2.1 Создай репозиторий

1. На GitHub нажми "+" (вверху справа)
2. Выбери "New repository"
3. Заполни:
   - **Repository name:** `ebay-monitor-iphone`
   - **Description:** eBay Monitor for iPhone
   - **Public** (выбери)
4. Нажми "Create repository"

### 2.2 Загрузи файлы

Открой PowerShell и выполни:

```powershell
cd C:\script

git config --global user.email "твой_email@gmail.com"
git config --global user.name "твой_username"

git init
git add ebay_app.py templates/ebay.html requirements.txt README.md
git commit -m "eBay Monitor for iPhone"
git branch -M main
git remote add origin https://github.com/твой_username/ebay-monitor-iphone.git
git push -u origin main
```

**Замени:**
- `твой_email@gmail.com` → твой email
- `твой_username` → твой GitHub username

---

## 🚀 Шаг 3: Развернись на Render

### 3.1 Создай аккаунт на Render

1. Перейди на https://render.com
2. Нажми "Sign up"
3. Выбери "Continue with GitHub"
4. Авторизуйся

### 3.2 Создай Web Service

1. Нажми "New +" (вверху)
2. Выбери "Web Service"
3. Нажми "Connect a repository"
4. Выбери репозиторий `ebay-monitor-iphone`
5. Нажми "Connect"

### 3.3 Заполни настройки

| Поле | Значение |
|------|----------|
| **Name** | `ebay-monitor` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn ebay_app:app` |
| **Instance Type** | `Free` |

6. Нажми "Create Web Service"
7. **Жди 2-3 минуты** (будет деплоиться)

### 3.4 Получи ссылку

Когда деплой завершится, ты увидишь:
```
https://ebay-monitor.onrender.com
```

Скопируй эту ссылку!

---

## 📱 Шаг 4: На iPhone

### 4.1 Открой в Safari

1. На iPhone открой **Safari**
2. В адресной строке введи:
   ```
   https://ebay-monitor.onrender.com
   ```
3. Нажми "Go"

### 4.2 Добавь на Home Screen

1. Нажми кнопку **Share** (внизу)
2. Выбери **"Add to Home Screen"**
3. Нажми **"Add"**

### 4.3 Готово! 🎉

Теперь у тебя есть приложение на Home Screen!

---

## 🔑 Как использовать

1. **Открой приложение** на iPhone
2. **Введи API ключи eBay:**
   - App ID
   - Dev ID
   - Cert ID
3. **Установи параметры:**
   - Ключевые слова (или оставь пусто)
   - Цена (мин/макс)
   - Минимум ставок
4. **Нажми СТАРТ**
5. **Смотри результаты в реальном времени!**

---

## ⚠️ Важные моменты

### API ключи eBay
- Получи на https://developer.ebay.com
- Используй **Sandbox** ключи для тестирования
- Переключись на **Production** для реальных аукционов

### Первый запуск
- Первый запрос может быть медленным (холодный старт)
- Последующие запросы будут быстрее

### Если не работает
1. Проверь что ссылка правильная
2. Обнови страницу (потяни вниз)
3. Проверь интернет соединение
4. Попробуй в другом браузере

---

## 🆘 Решение проблем

### "Ошибка подключения"
- Проверь интернет
- Проверь что ссылка правильная
- Подожди 5 минут (Render может быть в режиме сна)

### "API Key invalid"
- Проверь что ключи скопированы без пробелов
- Используй Sandbox ключи для тестирования

### "Приложение медленное"
- Это нормально на бесплатном плане Render
- Первый запрос может быть 30 сек
- Потом будет быстрее

---

## 💡 Советы

✅ **Добавь на Home Screen** - будет работать как приложение
✅ **Используй Sandbox ключи** - для тестирования
✅ **Проверь интернет** - нужно хорошее соединение
✅ **Обновляй страницу** - если что-то не работает

---

## 🎉 Готово!

Теперь у тебя есть полнофункциональный eBay Monitor на iPhone!

Работает везде, с любой сети, как настоящее приложение! 🚀
