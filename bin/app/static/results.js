const translations = {
    'en': {
        'title': 'Interview Result',
        'completionMsg': 'You\'ve successfully completed the test! We\'ll be in touch via email, SMS, or a phone call.',
        'thanksMsg': 'Thanks and enjoy your day! 😊🌟',
        'finishBtn': 'Finish the Test'
    },
    'ru': {
        'title': 'Результат собеседования',
        'completionMsg': 'Вы успешно прошли тест! Мы свяжемся с вами по электронной почте, SMS или по телефону.',
        'thanksMsg': 'Спасибо и хорошего дня! 😊🌟',
        'finishBtn': 'Завершить тест'
    },
    'hy': {
        'title': 'Հարցազրույցի Արդյունքը',
        'completionMsg': 'Դուք հաջողակ ավարտել եք թեստը: Մենք կկապվենք ձեզ հետ էլփոստով, SMS-ով կամ հեռախոսով։',
        'thanksMsg': 'Շնորհակալ եմ, եւ վայելեք օրընտրակեանքը! 😊🌟',
        'finishBtn': 'Ավարտել թեստը'
    }
};


    document.addEventListener('DOMContentLoaded', function() {
    const languageSelector = document.getElementById('language-selector');
    const title = document.getElementById('title');
    const completionMsg = document.getElementById('completion-msg');
    const thanksMsg = document.getElementById('thanks-msg');
    const finishBtn = document.getElementById('finish-btn');


    function updateLanguage(lang) {
        const langTranslations = translations[lang];
        title.textContent = langTranslations.title;
        completionMsg.textContent = langTranslations.completionMsg;
        thanksMsg.textContent = langTranslations.thanksMsg;
        finishBtn.textContent = langTranslations.finishBtn;
    }


    const currentLang = localStorage.getItem('selectedLanguage') || 'hy';
    languageSelector.value = currentLang;
    updateLanguage(currentLang);
    languageSelector.addEventListener('change', function() {
        const newLang = this.value;
        localStorage.setItem('selectedLanguage', newLang);
        updateLanguage(newLang);
    });
});
