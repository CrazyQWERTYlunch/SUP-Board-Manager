// Функция для прокрутки колонок влево
function scrollLeft() {
    const container = document.querySelector('.event-grid');
    container.scrollBy({
        left: -100,
        behavior: 'smooth'
    });
}

// Функция для прокрутки колонок вправо
function scrollRight() {
    const container = document.querySelector('.event-grid');
    container.scrollBy({
        left: 100,
        behavior: 'smooth'
    });
}

// Показываем кнопки прокрутки по умолчанию
document.querySelectorAll('.scroll-button').forEach(button => {
    button.style.display = 'block';
});