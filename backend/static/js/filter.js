// Обработчик события для кнопки прокрутки влево
document.querySelector('.prev-button').addEventListener('click', scrollLeft);

// Функция для прокрутки колонок влево
function scrollLeft() {
    var container = document.querySelector('.event-grid');
    container.scrollLeft -= 100; // Измените это значение на количество пикселей, на которое вы хотите прокрутить контейнер влево
}

// Функция для прокрутки колонок вправо
function scrollRight() {
    var container = document.querySelector('.event-grid');
    container.scrollLeft += 100; // Измените это значение на количество пикселей, на которое вы хотите прокрутить контейнер вправо
}