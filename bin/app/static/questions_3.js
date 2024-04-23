document.addEventListener('DOMContentLoaded', function() {
    const languageSelector = document.getElementById('language-selector');
    const userGreeting = document.getElementById('user-greeting');
    const translations = {
        'en': `Welcome, ${userName} ${userSurname}! Have a nice day! 😊`,
        'ru': `Добро пожаловать, ${userName} ${userSurname}! Желаем хорошего дня! 😊`,
        'hy': `Բարի գալուստ, ${userName} ${userSurname}! Մաղթում ենք Ձեզ հաճելի օր: 😊`
    };

    function updateLanguage(lang) {
        userGreeting.innerHTML = translations[lang] || translations['hy'];
    }
    languageSelector.addEventListener('change', function() {
        updateLanguage(this.value);
    });
    updateLanguage(languageSelector.value || 'hy');
});
