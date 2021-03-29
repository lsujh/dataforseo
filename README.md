# dataforseo

Используя сервис SERP API (v3) (кроме live SERP) получаем данные, сохранем их в базу, результаты отображаются в браузере.

     Пользователь:
    - выбирает поисковую систему
    - выбирает регион поиска 
    - вводит ключевое слово
    - отправляет запрос

    Отображение статуса поставленных задач и результатов по ним.
    
## Cloning & Run:

git clone https://github.com/lsujh/dataforseo.git

cd dataforseo

pip install -r requirements.txt

python3 manage.py runserver

python3 manage.py migrate

python3 manage.py createsuperuser
