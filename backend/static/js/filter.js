document.addEventListener("DOMContentLoaded", function() {


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
    document.querySelector('.prev-button').addEventListener('click', scrollLeft);
    document.querySelector('.next-button').addEventListener('click', scrollRight);
});