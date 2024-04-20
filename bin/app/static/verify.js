const translations = {
    'en': {
        'title': 'Verify Your Account',
        'description': 'We have sent a verification code to your email. Please check your inbox.',
        'signupBtn': 'Verify'
    },
    'ru': {
        'title': 'Проверьте ваш аккаунт',
        'description': 'Мы отправили код подтверждения на вашу электронную почту. Пожалуйста, проверьте ваш почтовый ящик.',
        'signupBtn': 'Проверять'
    },
    'hy': {
        'title': 'Ստուգեք Ձեր հաշիվը',
        'description': 'Մենք ուղարկել ենք վավերացման կոդ Ձեր էլեկտրոնային փոստին։ Խնդրում ենք, ստուգեք Ձեր նամականիշը։',
        'signupBtn': 'Հաստատել'
    }
};


document.addEventListener('DOMContentLoaded', function() {
    const languageSelector = document.getElementById('language-selector');
    const title = document.getElementById('title');
    const description = document.getElementById('description');
    const submitButton = document.getElementById('signupBtn');


    function updateLanguage(lang) {
        const langTranslations = translations[lang];
        title.textContent = langTranslations.title;
        description.textContent = langTranslations.description;
        submitButton.textContent = langTranslations.signupBtn;
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


document.querySelectorAll('.code-input').forEach((input, index, array) => {
    input.addEventListener('keyup', (e) => {
        handleInputFocusChange(e, index, array);
    });

    input.addEventListener('paste', (e) => {
        handlePaste(e, array);
    });
});


function handleInputFocusChange(e, index, array) {
    if (index < array.length - 1 && e.target.value) {
        array[index + 1].focus();
    } else if (index > 0 && !e.target.value) {
        array[index - 1].focus();
    }
    updateFullCode(array);
}


function handlePaste(e, array) {
    e.preventDefault();
    const pasteData = e.clipboardData.getData('text');
    pasteData.split('').forEach((char, index) => {
        if (index < array.length) {
            array[index].value = char;
        }
    });
    updateFullCode(array);
}


function updateFullCode(array) {
    let fullCode = '';
    array.forEach(codeInput => {
        fullCode += codeInput.value;
    });
    document.getElementById('fullCode').value = fullCode;
}
