const translations = {
    en: {
        title: "Warning!",
        text: "You've successfully completed the test! We'll be in touch via email, SMS, or a phone call.",
        button: 'Go back'
    },
    ru: {
        title: "Внимание!",
        text: "Вы успешно завершили тест! Мы свяжемся с вами по электронной почте, SMS или по телефону.",
        button: 'Вернуться'
    },
    hy: {
        title: "Զգուշացում!",
        text: "Դուք հաջողությամբ անցել եք թեստը: Մենք կկապվենք Ձեզ հետ էլեկտրոնային փոստով, SMS հաղորդագրությամբ կամ հեռախոսազանգով:",
        button: 'Վերադառնալ'
    }
};


document.addEventListener('DOMContentLoaded', function() {
    const languageSelector = document.getElementById('language-selector');
    const title = document.getElementById('warning-title');
    const description = document.getElementById('main-text');
    const submitButton = document.getElementById('finish-btn');

    function updateLanguage(lang) {
        const langTranslations = translations[lang];
        title.textContent = langTranslations.title;
        description.textContent = langTranslations.text;
        submitButton.textContent = langTranslations.button;
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

function goBack() {
    window.history.back();
}