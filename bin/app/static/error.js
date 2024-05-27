const errorTranslations = {
    'en': {
        'title': 'Oops! Something went wrong.',
        'message': '{{ error }}',
        'homeLink': 'Go back'
    },
    'ru': {
        'title': 'Упс! Что-то пошло не так.',
        'message': '{{ error }}',
        'homeLink': 'Вернуться на главную'
    },
    'hy': {
        'title': 'Վայ! Ինչ-որ բան սխալ է արվել։',
        'message': '{{ error }}',
        'homeLink': 'Վերադառնալ'
    }
};



document.addEventListener('DOMContentLoaded', function() {
    const languageSelector = document.getElementById('language-selector');
    const title = document.getElementById('error-title');
    const submitButton = document.getElementById('home-link');;
    const errorMessage = document.getElementById('error-message');
    function updateLanguage(lang) {
        const langTranslations = translations[lang];
        title.textContent = langTranslations.title;
        submitButton.textContent = langTranslations.signupBtn;
        errorMessage.textContent = langTranslations.errorMessage;
    }

    const serverLang = document.querySelector('input[name="lang"]').value;

    languageSelector.value = serverLang;
    updateLanguage(serverLang);

    languageSelector.addEventListener('change', function() {
        const newLang = this.value;
        localStorage.setItem('selectedLanguage', newLang);
        updateLanguage(newLang);
    });

    codeInput.addEventListener('input', function() {
        this.value = this.value.replace(/\D/g, '');
        if (this.value.length > 6) {
            this.value = this.value.substring(0, 6);
        }
    });

    form.addEventListener('submit', function(event) {
        if (!codeInput.value || codeInput.value.length !== 6) {
            event.preventDefault();
            errorMessage.style.display = 'block';
        } else {
            errorMessage.style.display = 'none';
        }
    });
});
