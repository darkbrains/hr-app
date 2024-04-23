const translations = {
    'en': {
        'title': 'Verify Your Phone',
        'description': 'The confirmation code has been sent to your phone number. Please check your messages.',
        'signupBtn': 'Verify',
        'errorMessage': 'The field is required.'
    },
    'ru': {
        'title': 'Подтвердите свой телефон',
        'description': 'Код подтверждения был отправлен на ваш номер телефона. Пожалуйста, проверьте свои сообщения.',
        'signupBtn': 'Проверять',
        'errorMessage': 'Это поле обязательно.'
    },
    'hy': {
        'title': 'Հաստատեք ձեր հեռախոսը',
        'description': 'Հաստատման կոդը ուղարկել է Ձեր հեռախոսահամարին: ',
        'signupBtn': 'Հաստատել',
        'errorMessage': 'Դաշտը պարտադիր է։'
    }
};


document.addEventListener('DOMContentLoaded', function() {
    const languageSelector = document.getElementById('language-selector');
    const title = document.getElementById('title');
    const description = document.getElementById('description');
    const submitButton = document.getElementById('signupBtn');
    const form = document.getElementById('verifyForm');
    const codeInput = document.querySelector('.code-input');
    const errorMessage = document.querySelector('.error-message');


    function updateLanguage(lang) {
        const langTranslations = translations[lang];
        title.textContent = langTranslations.title;
        description.textContent = langTranslations.description;
        submitButton.textContent = langTranslations.signupBtn;
        errorMessage.textContent = langTranslations.errorMessage;
    }


    const currentLang = localStorage.getItem('selectedLanguage') || 'hy';
    languageSelector.value = currentLang;
    updateLanguage(currentLang);
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
