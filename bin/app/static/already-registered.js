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
        text: "Դուք հաջողակապես ավարտել եք թեստը։ Մենք կհաղորդակցվենք ձեզ հետ էլ․ փոստով, SMS-ով կամ հեռախոսով։",
        button: 'Վերադառնալ'
    }
};


const languageSelector = document.getElementById('language-selector');
const titleElement = document.getElementById('warning-title');
const textElement = document.getElementById('main-text');
const buttonElement = document.getElementById('finish-btn');


function updateLanguage(lang) {
    titleElement.textContent = translations[lang].title;
    textElement.textContent = translations[lang].text;
    buttonElement.textContent = translations[lang].button;
}

const currentLang = localStorage.getItem('selectedLanguage') || 'hy';
languageSelector.value = currentLang;
updateLanguage(currentLang);
languageSelector.addEventListener('change', function() {
    localStorage.setItem('selectedLanguage', this.value);
    updateLanguage(this.value);
});


function goBack() {
    window.history.back();
}
