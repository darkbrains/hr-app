document.addEventListener('DOMContentLoaded', function() {
    window.translations = {
        'en': {
            'welcome': 'Welcome',
            'signup': 'Sign up to People Connect.',
            'phone': 'Phone number. Example +1234567890',
            'email': 'Email',
            'name': 'Name',
            'surname': 'Surname',
            'password': 'Password',
            'signupBtn': 'Sign up',
            'loginBtn': 'Login',
            'errors': {
                'phoneRequired': 'Phone number is required.',
                'validPhone': 'Please enter a valid phone number with country code.',
                'emailRequired': 'Email is required.',
                'validEmail': 'Please enter a valid email address.',
                'nameRequired': 'Name is required.',
                'surnameRequired': 'Surname is required.',
                'passwordRequired': 'Password is required.'
            }
        },
        'ru': {
            'welcome': 'Добро пожаловать',
            'signup': 'Зарегистрироваться в People Connect.',
            'phone': 'Номер телефона. Пример +1234567890',
            'email': 'Эл. адрес',
            'name': 'Имя',
            'surname': 'Фамилия',
            'password': 'Пароль',
            'signupBtn': 'Регистрация',
            'loginBtn': 'Вход',
            'errors': {
                'phoneRequired': 'Укажите номер телефона.',
                'validPhone': 'Пожалуйста, введите действительный номер телефона с кодом страны.',
                'emailRequired': 'Укажите адрес электронной почты.',
                'validEmail': 'Пожалуйста, введите действительный адрес электронной почты.',
                'nameRequired': 'Укажите имя.',
                'surnameRequired': 'Укажите фамилию.',
                'passwordRequired': 'Укажите пароль.'
            }
        },
        'hy': {
            'welcome': 'Բարի գալուստ',
            'signup': 'Գրանցվել People Connect-ում։',
            'phone': 'Հեռախոսահամար: Օրինակ՝ +1234567890',
            'email': 'Էլ․ հասցե',
            'name': 'Անուն',
            'surname': 'Ազգանուն',
            'password': 'Գաղտնաբառ',
            'signupBtn': 'Գրանցվել',
            'loginBtn': 'Մուտք',
            'errors': {
                'phoneRequired': 'Հեռախոսահամարը պարտադիր է:',
                'validPhone': 'Խնդրում ենք մուտքագրել վավեր հեռախոսահամար՝ երկրի կոդով:',
                'emailRequired': 'Էլ․ հասցեն պարտադիր է:',
                'validEmail': 'Խնդրում ենք մուտքագրել վավեր Էլ․ փոստի հասցե:',
                'nameRequired': 'Անունը պարտադիր է:',
                'surnameRequired': 'Ազգանունը պարտադիր է:',
                'passwordRequired': 'Գաղտնաբառը պարտադիր է:'
            }
        }
    };


    const form = document.querySelector('form');
    const languageSelector = document.getElementById('language-selector');
    const inputs = {
        phone: document.getElementById('phone'),
        email: document.getElementById('email'),
        password: document.getElementById('password'),
        name: document.getElementById('name'),
        surname: document.getElementById('surname')
    };
    const errorElements = {
        phone: document.getElementById('phone-error'),
        email: document.getElementById('email-error'),
        password: document.getElementById('password-error'),
        name: document.getElementById('name-error'),
        surname: document.getElementById('surname-error')
    };
    const submitButton = document.querySelector('button[type="submit"]');
    const defaultLang = 'hy';
    changeLanguage(defaultLang);
    languageSelector.value = defaultLang;
    languageSelector.addEventListener('change', function() {
        changeLanguage(this.value);
    });

    function changeLanguage(lang) {
        const texts = window.translations[lang];
        document.querySelector('.login-form h1').textContent = texts.welcome;
        document.querySelector('.w-text p').textContent = texts.signup;
        Object.keys(inputs).forEach(function(key) {
            inputs[key].placeholder = texts[key];
            errorElements[key].textContent = '';
        });
        submitButton.textContent = texts.loginBtn;
    }

    function showOrHideError(input, message, show) {
        const errorElement = errorElements[input.id];
        errorElement.textContent = message;
        errorElement.style.display = show ? 'block' : 'none';
    }

    function validateInput(input) {
        const lang = languageSelector.value;
        const translations = window.translations[lang].errors;
        let valid = true;
        let message = '';

        if (input.style.display === 'none') {
            showOrHideError(input, '', false);
            return true;
        }

        const value = input.value.trim();
        if (!value) {
            message = translations[input.id + 'Required'];
            valid = false;
        } else if (input.id === 'email' && !/\S+@\S+\.\S+/.test(value)) {
            message = translations.validEmail;
            valid = false;
        } else if (input.id === 'phone' && !/^\+[0-9]{10,14}$/.test(value)) {
            message = translations.validPhone;
            valid = false;
        }

        showOrHideError(input, message, !valid);
        return valid;
    }

    function validateForm() {
        let isFormValid = true;
        Object.values(inputs).forEach(function(input) {
            isFormValid = validateInput(input) && isFormValid;
        });
        return isFormValid;
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const isFormValid = validateForm();
        if (isFormValid) {
            this.submit();
        }
    });

    Object.values(inputs).forEach(function(input) {
        input.addEventListener('input', function() {
            validateInput(input);
        });
    });

    async function checkUser() {
        const phone = inputs.phone.value.trim();
        const email = inputs.email.value.trim();
        if (!phone || !email) {
            inputs.name.style.display = 'none';
            inputs.surname.style.display = 'none';
            submitButton.textContent = window.translations[languageSelector.value].signupBtn;
            return;
        }
        try {
            const response = await fetch('/api/v1/check-user', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `email=${encodeURIComponent(email)}&phone=${encodeURIComponent(phone)}`
            });
            const data = await response.json();
            if (!data.exists) {
                inputs.name.style.display = '';
                inputs.surname.style.display = '';
                submitButton.textContent = window.translations[languageSelector.value].signupBtn;
            } else {
                inputs.name.style.display = 'none';
                inputs.surname.style.display = 'none';
                submitButton.textContent = window.translations[languageSelector.value].loginBtn;
            }
        } catch (error) {
            console.error('Error checking user:', error);
            submitButton.textContent = window.translations[languageSelector.value].signupBtn;
        }
    }

    inputs.email.addEventListener('blur', checkUser);
    inputs.phone.addEventListener('blur', checkUser);
    inputs.name.style.display = 'none';
    inputs.surname.style.display = 'none';
});
