const errorTranslations = {
    en: {
        title: 'Oops! Something went wrong.',
        message: '{{ error }}',
        homeLink: 'Go back'
    },
    ru: {
        title: 'Упс! Что-то пошло не так.',
        message: '{{ error }}',
        homeLink: 'Вернуться на главную'
    },
    hy: {
        title: 'Վայ! Ինչ-որ բան սխալ է արվել։',
        message: '{{ error }}',
        homeLink: 'Վերադառնալ'
    }
};



document.addEventListener('DOMContentLoaded', function() {
    const languageSelector = document.getElementById('language-selector');
    const title = document.getElementById('title');
    const description = document.getElementById('error-message');
    const submitButton = document.getElementById('signupBtn');

    function updateLanguage(lang) {
        const langTranslations = errorTranslations[lang];
        title.textContent = langTranslations.title;
        // description.textContent = langTranslations.description;
        submitButton.textContent = langTranslations.homeLink;
    }

    const serverLang = document.querySelector('input[name="lang"]').value;

    languageSelector.value = serverLang;
    updateLanguage(serverLang);

    languageSelector.addEventListener('change', function() {
        const newLang = this.value;
        localStorage.setItem('selectedLanguage', newLang);
        updateLanguage(newLang);
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
