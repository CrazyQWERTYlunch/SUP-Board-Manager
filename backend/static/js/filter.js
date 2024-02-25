// Функция для прокрутки колонок влево
function scrollLeft() {
    var container = document.querySelector('.event-grid');
    container.scrollLeft -= 100; // Измените это значение на количество пикселей, на которое вы хотите прокрутить контейнер влево
}

function scrollRight() {
    var container = document.querySelector('.event-grid');
    container.scrollLeft += 100; // Измените это значение на количество пикселей, на которое вы хотите прокрутить контейнер вправо
}