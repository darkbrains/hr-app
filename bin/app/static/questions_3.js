document.addEventListener('DOMContentLoaded', function() {
    const languageSelector = document.getElementById('language-selector');
    const userGreeting = document.getElementById('user-greeting');
    const translations = {
        'en': 'Welcome, {{ user_data.name }} {{ user_data.surname }}! Have a nice day! 😊',
        'ru': 'Добро пожаловать, {{ user_data.name }} {{ user_data.surname }}! Желаем хорошего дня! 😊',
        'hy': 'Բարի գալուստ, {{ user_data.name }} {{ user_data.surname }}! Հաճելի օր ունեցեք! 😊'
    };


    function updateLanguage(lang) {
        userGreeting.textContent = translations[lang];
    }
    languageSelector.addEventListener('change', function() {
        updateLanguage(this.value);
    });
    updateLanguage(languageSelector.value);
});
