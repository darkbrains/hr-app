
error_messages = {
    'signup': {
        'en': 'A user with that email or phone  already exists.',
        'ru': 'Пользователь с этой электронной почтой или телефоном уже существует.',
        'hy': 'Նման էլ. փոստի հասցե կամ հեռախոս ունեցող օգտատեր արդեն գոյություն ունի:'
    },
    'signup_error': {
        'en': 'Failed to process signup. Please try again later.',
        'ru': 'Не удалось выполнить регистрацию. Пожалуйста, повторите попытку позже.',
        'hy': 'Չհաջողվեց մշակել գրանցումը: Խնդրում եմ փորձեք մի փոքր ուշ:'
    },
    'questions_error': {
        'en': 'Failed to load questions. Please try again later.',
        'ru': 'Не удалось загрузить вопросы. Пожалуйста, повторите попытку позже.',
        'hy': 'Չհաջողվեց բեռնել հարցերը: Խնդրում եմ փորձեք մի փոքր ուշ:'
    },
    'submit_error': {
        'en': 'Failed to submit form. Please try again later.',
        'ru': 'Не удалось отправить форму. Пожалуйста, повторите попытку позже.',
        'hy': 'Չհաջողվեց ուղարկել նմուշը: Խնդրում եմ փորձեք մի փոքր ուշ:'
    },
    'verify_no_code': {
        'en': 'No verification code found. Please try again.',
        'ru': 'Код подтверждения не найден. Пожалуйста, попробуйте  еще раз.',
        'hy': 'Նույնականացման կոդը չի գտնվել: Խնդրում ենք կրկին փորձել:'
    },
    'verify_expired': {
        'en': 'Verification code expired. Please try again.',
        'ru': 'Срок действия кода подтверждения истек. Пожалуйста, попробуйте еще раз.',
        'hy': 'Նույնականացման կոդը ժամկետանց է: Խնդրում ենք կրկին փորձել:'
    },
    'verify_incorrect': {
        'en': 'Incorrect verification code. Please try again.',
        'ru': 'Неправильный код подтверждения. Пожалуйста, попробуйте еще раз.',
        'hy': 'Սխալ նույնականացման կոդը: Խնդրում եմ կրկին փորձեք:'
    },
    'verify_error': {
        'en': 'An internal error occurred.',
        'ru': 'Возникла внутренняя ошибка.',
        'hy': 'Տեղի ունեցավ ներքին սխալ:'
    },
    'incorrect_password': {
        'en': 'Incorrect password. Please try again.',
        'ru': 'Неверный пароль. Пожалуйста, попробуйте еще раз.',
        'hy': 'Սխալ գաղտնաբառ. Խնդրում եմ կրկին փորձեք.'
    }
}



def get_message(key, lang='en'):
    """
    Fetches a message by key and language.
    :param key: Key for the message type (e.g., 'signup')
    :param lang: Language code (default is 'en')
    :return: Message string in the requested language
    """
    return error_messages.get(key, {}).get(lang, "")
