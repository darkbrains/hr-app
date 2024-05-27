const translations = {
    'en': {
        'title': 'Registration Successful',
        'verified': 'Your account has been verified!',
        'redirect': 'You\'ll be redirected to the Questions page shortly.'
    },
    'ru': {
        'title': 'Регистрация Успешна',
        'verified': 'Ваш аккаунт был проверен!',
        'redirect': 'Вы будете перенаправлены на страницу с вопросами в ближайшее время.'
    },
    'hy': {
        'title': 'Գրանցումը Հաջողվեց',
        'verified': 'Ձեր հաշիվը հաստատված է!',
        'redirect': 'Շուտով կուղղորդվեք հարցերի էջ:'
    }
};


document.addEventListener('DOMContentLoaded', function() {
    const languageSelector = document.getElementById('language-selector');
    const title = document.getElementById('title');
    const verified = document.getElementById('verified');
    const redirect = document.getElementById('redirect');

    function updateLanguage(lang) {
        const langTranslations = translations[lang];
        title.textContent = langTranslations.title;
        verified.textContent = langTranslations.verified;
        redirect.textContent = langTranslations.redirect;
    }

    const serverLang = document.querySelector('input[name="lang"]').value;

    languageSelector.value = serverLang;
    updateLanguage(serverLang);

    languageSelector.addEventListener('change', function() {
        const newLang = this.value;
        localStorage.setItem('selectedLanguage', newLang);
        updateLanguage(newLang);
    });
});
