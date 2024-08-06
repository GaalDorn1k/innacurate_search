## INNACCURATE SEARCH DEMO
Демка неточного поиска\
Использует OpenOffice для парсинга документов и визуализации поиска\
OpenOffice очень сложно заставить работать с невстроенным в него питоном на винде, поэтому прилагается bash-скрипт с установкой всего необходимого и настройкой зависимостей для WSL:
1. устанавливает Xserver
2. устанавливает LibreOffice
3. прокидывает путь до библиотек OpenOffice в конфиг сервиса

## Перед запуском
1. Для установки LibreOffice и настройки зависимостей выполнить
```
chmod +x setup
./setup
```
2. Установить библиотеки питона
```
pip install -r requirements.txt
```
!!! Не должно работать в виртуальных средах Conda, хотя иногда работает. Лучше не пытаться

## Запуск
```
python run.py
```

## API
Для открытия документа:
```
POST -F file=@FILE_PATH http://localhost:5000/api/open
```
Для поиска по документу:
```
GET http://localhost:5000/api/search?query=QUERY
```
Можно использовать постман, коллекция запросов с примерами в `query_examples.postman_collection.json`\
Когда сервис развернут в WSL, адрес все равно будет localhost