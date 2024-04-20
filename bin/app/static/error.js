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


const languageSelector = document.getElementById('language-selector');
const errorTitle = document.getElementById('error-title');
const errorMessage = document.getElementById('error-message');
const homeLink = document.getElementById('home-link');
languageSelector.addEventListener('change', function() {
    const lang = this.value;
    errorTitle.textContent = errorTranslations[lang].title;
    errorMessage.textContent = errorTranslations[lang].message;
    homeLink.textContent = errorTranslations[lang].homeLink;
});
const currentLang = '{{ lang }}';
if (errorTranslations[currentLang]) {
    errorTitle.textContent = errorTranslations[currentLang].title;
    errorMessage.textContent = errorTranslations[currentLang].message;
    homeLink.textContent = errorTranslations[currentLang].homeLink;
}
