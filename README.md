# Сервис деления счета в ресторане от Сбера

Сервис предназначен для удобного и быстрого деления счета между посетителями ресторана. Пользователи могут сканировать чек и автоматически разделить сумму, либо ввести съеденные блюда вручную.

---

## Возможности

- **Сканирование чека** с помощью `apple_ocr` (технология Apple Vision)
- **Ручной выбор блюд** для точного подсчета
- **Создание сессий** с приглашением других участников
- **Просмотр активных сессий и профиля пользователя**
- Поддержка аналитики и визуализации через Plotly

---

## Технологии

### Backend:
- Python
- Django

### OCR и обработка изображений:
- `apple_ocr` *(использует Apple Vision)*
- `Pillow`
- `Torch`
- `NumPy`
- `Pandas`
- `Scikit-learn`
- `Plotly`
- `Pyobjc`

### Frontend:
- Django шаблоны
- `django_bootstrap5` (Bootstrap 5 для стилизации)

---

## Важно

> Проект использует `apple_ocr`, в котором применяется технология **Apple Vision**, доступная только на **macOS**. Для запуска проекта требуется сервер с **macOS** (например, Mac Mini, MacBook или облачные решения).

---

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/sber-bill-splitter.git
   ```
2. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Выполните миграции и запустите сервер:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

Пример использования

Создайте новую сессию.
Пригласите участников по ID или через ссылку.
Загрузите фотографию чека или используйте камеру.
Система распознает чек и предложит разделение суммы.
Пользователи могут выбрать блюда вручную или принять авто-деление.
Профиль пользователя

Каждый пользователь имеет:

Уникальный ID
Никнейм
Адрес электронной почты
Список активных и завершённых сессий

Структура проекта:
```cpp
sber-bill-splitter/
├── mysite/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── scan/
│   ├── images/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── static/
├── db.sqlite3
├── requirements.txt
└── README.md
```

---

Обратная связь
Почта капитана y4ne242@gmail.com
