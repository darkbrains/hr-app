const languageSelector = document.getElementById('language-selector');
const questionsContainer = document.getElementById('questions-container');
const formLangInput = document.getElementById('form-lang');
const translations = {
    en: {
        questions: [
        {
            text: "Describe your working style:",
            options: [
                { text: "Independently", value: "4" },
                { text: "As part of a team", value: "3" },
                { text: "In a leadership role", value: "2" },
                { text: "Flexible/Adaptable to any style", value: "1" }
            ]
        },
        {
            text: "How do you handle stress and pressure?",
            options: [
                { text: "Through physical activity or meditation", value: "3" },
                { text: "Ignoring it until the stressful period is over", value: "1" },
                { text: "By planning and prioritizing tasks", value: "4" }
            ]
        },
        {
            text: "Which outcome most enhances your motivation at work?",
            options: [
                { text: "Achieving specific goals", value: "4" },
                { text: "Supporting and aiding colleagues", value: "3" },
                { text: "Receiving recognition and tangible rewards", value: "1" },
                { text: "Pursuing personal growth and skills development", value: "2" }
            ]
        },
        {
            text: "Describe your approach to problem-solving:",
            options: [
                { text: "Creative and intuitive", value: "3" },
                { text: "Analytical and methodical", value: "4" },
                { text: "I ask for help when needed", value: "1" },
                { text: "Practical and straightforward", value: "2" }
            ]
        },
        {
            text: "How do you prioritize your work?",
            options: [
                { text: "I struggle with prioritization", value: "1" },
                { text: "By task importance", value: "3" },
                { text: "Based on supervisor direction", value: "2" },
                { text: "By deadline", value: "4" }
            ]
        },
        {
            text: "How do you handle criticism?",
            options: [
                { text: "I use it as motivation", value: "1" },
                { text: "I take it constructively to improve", value: "4" },
                { text: "I find it difficult to accept", value: "2" },
                { text: "It depends on who it comes from", value: "3" }
            ]
        },
        {
            text: "What is your greatest strength?",
            options: [
                { text: "Communication skills", value: "4" },
                { text: "Problem-solving skills", value: "2" },
                { text: "Leadership abilities", value: "3" },
                { text: "Ability to learn quickly", value: "1" }
            ]
        },
        {
            text: "What is your greatest weakness?",
            options: [
                { text: "Hesitation to delegate", value: "3" },
                { text: "Taking on too much work", value: "2" },
                { text: "Impatience", value: "4" },
                { text: "Being too detail-oriented", value: "1" }
            ]
        },
        {
            text: "How do you manage conflicts in a team?",
            options: [
                { text: "By consulting with a supervisor", value: "1" },
                { text: "By avoiding conflict situations", value: "2" },
                { text: "By addressing issues directly", value: "4" },
                { text: "By mediating between parties", value: "3" }
            ]
        },
        {
            text: "Choose one example that best describes a time when you faced a failure.",
            options: [
                { text: "I have never failed in my role.", value: "1" },
                { text: "I failed to meet a project deadline due to poor time management, which led me to enhance my ability to prioritize tasks effectively.", value: "2" },
                { text: "A miscommunication with a team member resulted in a project setback, prompting me to focus on sharpening my communication skills.", value: "3" },
                { text: "The failure was due to a lack of skill, and I pursued additional training.", value: "4" }
            ]
        },
        {
            text: "Why do you want to work here?",
            options: [
                { text: "Other reasons not listed here", value: "1" },
                { text: "The company's culture appeals to me", value: "4" },
                { text: "I am interested in the company's products or services", value: "2" },
                { text: "There are good opportunities for career advancement", value: "3" }
            ]
        },
        {
            text: "What are your career goals?",
            options: [
                { text: "To move into a leadership position", value: "4" },
                { text: "To specialize in my current field", value: "3" },
                { text: "I'm not sure yet", value: "1" },
                { text: "To transition to a different industry", value: "2" }
            ]
        },
        {
            text: "How do you keep up-to-date with industry trends?",
            options: [
                { text: "I find it difficult to keep up", value: "1" },
                { text: "Attending workshops and conferences", value: "3" },
                { text: "Reading professional journals", value: "4" },
                { text: "Networking with industry professionals", value: "2" }
            ]
        },
        {
            text: "How do you evaluate success?",
            options: [
                { text: "By receiving feedback from peers and supervisors", value: "2" },
                { text: "By the impact of my work on the company's success", value: "1" },
                { text: "By achieving personal goals", value: "4" },
                { text: "By achieving team/department goals", value: "3" }
            ]
        },
        {
            text: "What result did you get in your last project?",
            options: [
                { text: "Successfully completed, but over budget", value: "3" },
                { text: "Failed to complete", value: "2" },
                { text: "Successfully completed on time", value: "4" },
                { text: "Led to an unexpected positive outcome", value: "1" }
            ]
        },
        {
            text: "How do you handle a situation where you don't know the answer?",
            options: [
                { text: "Research until I find the answer", value: "4" },
                { text: "Avoid the situation", value: "1" },
                { text: "Ask a colleague or supervisor for guidance", value: "3" },
                { text: "Use my best judgment and proceed", value: "2" }
            ]
        },
        {
            text: "How do you approach learning a new skill or technology?",
            options: [
                { text: "Cautiously but willing to try", value: "3" },
                { text: "Reluctantly, only if necessary", value: "2" },
                { text: "I prefer to stick with what I know", value: "1" },
                { text: "With enthusiasm and determination", value: "4" }
            ]
        },
        {
            text: "Describe how you would work under tight deadlines.",
            options: [
                { text: "Delegating tasks to others", value: "2" },
                { text: "Prioritize tasks and get work done efficiently", value: "4" },
                { text: "Work long hours to meet deadlines", value: "3" },
                { text: "Skip deadline", value: "1" }
            ]
        },
        {
            text: "How do you contribute to a positive work environment?",
            options: [
                { text: "By contributing to team goals", value: "2" },
                { text: "Other reasons not listed here", value: "1" },
                { text: "By being supportive of colleagues", value: "4" },
                { text: "By maintaining a positive attitude", value: "3" }
            ]
        },
        {
            text: "What motivates you at work?",
            options: [
                { text: "Competitive challenges", value: "4" },
                { text: "Collaborative teamwork", value: "3" },
                { text: "Working independently", value: "1" },
                { text: "Flexible work arrangements", value: "2" }
            ]
        },
        ],
        errors: {
            answerRequired: 'An answer is required.'
        },
        buttonNext: 'Next',
        buttonPrev: 'Previous',
        buttonSubmit: 'Finish'
    },

    ru: {
        questions: [
        {
            text: "Опишите свой стиль работы",
            options: [
                { text: "Независимо", value: "4" },
                { text: "В составе команды", value: "3" },
                { text: "На руководящей должности", value: "2" },
                { text: "Гибкость/адаптируемость к любому стилю", value: "1" }
            ]
        },
        {
            text: "Как вы справляетесь со стрессом и давлением?",
            options: [
                { text: "Через физическую активность или медитацию", value: "3" },
                { text: "Игнорирование этого до тех пор, пока стрессовый период не закончится", value: "1" },
                { text: "Планируя и расставляя приоритеты задач", value: "4" }
            ]
        },
        {
            text: "Какой результат больше всего повышает вашу мотивацию на работе?",
            options: [
                { text: "Достижение конкретных целей", value: "4" },
                { text: "Поддержка и помощь коллегам", value: "3" },
                { text: "Получение признания и материального вознаграждения", value: "1" },
                { text: "Стремление к личностному росту и развитию навыков", value: "2" }
            ]
        },
        {
            text: "Опишите свой подход к решению проблем",
            options: [
                { text: "Креативный и интуитивно понятный", value: "3" },
                { text: "Аналитический и методический", value: "4" },
                { text: "Я прошу помощи, когда это необходимо", value: "1" },
                { text: "Практичный и простой", value: "2" }
            ]
        },
        {
            text: "Как вы расставляете приоритеты в своей работе?",
            options: [
                { text: "Я борюсь с расстановкой приоритетов", value: "1" },
                { text: "По важности задачи", value: "3" },
                { text: "По указанию руководителя", value: "2" },
                { text: "К сроку", value: "4" }
            ]
        },
        {
            text: "Как вы относитесь к критике?",
            options: [
                { text: "Я использую это как мотивацию", value: "1" },
                { text: "Я воспринимаю это конструктивно, чтобы улучшить", value: "4" },
                { text: "Мне трудно принять", value: "2" },
                { text: "Это зависит от того, от кого оно исходит", value: "3" }
            ]
        },
        {
            text: "Какая ваша самая сильная сторона?",
            options: [
                { text: "Навыки коммуникации", value: "4" },
                { text: "Навыки решения проблем", value: "2" },
                { text: "Лидерские способности", value: "3" },
                { text: "Способность быстро учиться", value: "1" }
            ]
        },
        {
            text: "Какая ваша самая большая слабость?",
            options: [
                { text: "Нерешительность делегировать", value: "3" },
                { text: "Беру на себя слишком много работы", value: "2" },
                { text: "Нетерпение", value: "4" },
                { text: "Слишком ориентирован на детали", value: "1" }
            ]
        },
        {
            text: "Как управлять конфликтами в команде?",
            options: [
                { text: "Посоветовавшись с руководителем", value: "1" },
                { text: "Избегая конфликтных ситуаций", value: "2" },
                { text: "Решая проблемы напрямую", value: "4" },
                { text: "Посредничество между сторонами", value: "3" }
            ]
        },
        {
            text: "Выберите один пример, который лучше всего описывает момент, когда вы столкнулись с неудачей.",
            options: [
                { text: "Я ни разу не провалился в своей роли.", value: "1" },
                { text: "Мне не удалось уложиться в сроки проекта из-за плохого управления временем, что позволило мне улучшить свою способность эффективно расставлять приоритеты в задачах.", value: "2" },
                { text: "Недопонимание с членом команды привело к провалу проекта, что побудило меня сосредоточиться на совершенствовании своих коммуникативных навыков.", value: "3" },
                { text: "Неудача произошла из-за отсутствия навыков, и я продолжил дополнительное обучение.", value: "4" }
            ]
        },
        {
            text: "Почему вы хотите работать здесь?",
            options: [
                { text: "Другие причины, не перечисленные здесь", value: "1" },
                { text: "Культура компании мне импонирует", value: "4" },
                { text: "Меня интересуют продукты или услуги компании", value: "2" },
                { text: "Возможности карьерного роста", value: "3" }
            ]
        },
        {
            text: "Каковы ваши карьерные цели?",
            options: [
                { text: "Чтобы занять руководящую должность", value: "4" },
                { text: "Специализироваться в моей текущей области", value: "3" },
                { text: "Я еще не уверен", value: "1" },
                { text: "Переход в другую отрасль", value: "2" }
            ]
        },
        {
            text: "Как вы следите за тенденциями отрасли?",
            options: [
                { text: "Мне трудно идти в ногу со временем", value: "1" },
                { text: "Посещение семинаров и конференций", value: "3" },
                { text: "Чтение профессиональных журналов", value: "4" },
                { text: "Общение с профессионалами отрасли", value: "2" }
            ]
        },
        {
            text: "Как вы оцениваете успех?",
            options: [
                { text: "Получая обратную связь от коллег и руководителей", value: "2" },
                { text: "По влиянию моей работы на успех компании", value: "1" },
                { text: "Достигая личных целей", value: "4" },
                { text: "Путем достижения целей команды/отдела", value: "3" }
            ]
        },
        {
            text: "Какого результата вы добились в своем последнем проекте?",
            options: [
                { text: "Успешно завершено, но превышает бюджет", value: "3" },
                { text: "Не удалось завершить", value: "2" },
                { text: "Успешно завершено в срок", value: "4" },
                { text: "Привел к неожиданному положительному результату", value: "1" }
            ]
        },
        {
            text: "Как поступить в ситуации, когда не знаешь ответа?",
            options: [
                { text: "Исследуйте, пока не найду ответ", value: "4" },
                { text: "Избегайте ситуации", value: "1" },
                { text: "Попросите совета у коллеги или руководителя", value: "3" },
                { text: "Используйте мое лучшее суждение и продолжайте", value: "2" }
            ]
        },
        {
            text: "Как вы подходите к изучению нового навыка или технологии?",
            options: [
                { text: "Осторожно, но готов попробовать", value: "3" },
                { text: "Неохотно, только при необходимости", value: "2" },
                { text: "Я предпочитаю придерживаться того, что знаю", value: "1" },
                { text: "С энтузиазмом и решимостью", value: "4" }
            ]
        },
        {
            text: "Опишите, как вы будете работать в сжатые сроки.",
            options: [
                { text: "Делегирование задач другим", value: "2" },
                { text: "Расставляйте приоритеты задач и выполняйте работу эффективно», значение", value: "4" },
                { text: "Работать сверхурочно, чтобы уложиться в сроки», значение", value: "3" },
                { text: "Пропустить срок", value: "1" }
            ]
        },
        {
            text: "Как вы способствуете созданию позитивной рабочей атмосферы?",
            options: [
                { text: "Внося свой вклад в достижение командных целей", value: "2" },
                { text: "Другие причины, не перечисленные здесь", value: "1" },
                { text: "Поддерживая коллег", value: "4" },
                { text: "Поддерживая позитивный настрой", value: "3" }
            ]
        },
        {
            text: "Что мотивирует вас в работе?",
            options: [
                { text: "Конкурентные задачи", value: "4" },
                { text: "Совместная работа в команде", value: "3" },
                { text: "Работаем независимо", value: "1" },
                { text: "Гибкий график работы", value: "2" }
            ]
        }
        ],
        errors: {
            answerRequired: 'Требуется ответ.'
        },
        buttonNext: 'Далее',
        buttonPrev: 'Назад',
        buttonSubmit: 'Заканчивать'
    },


    hy: {
        questions: [
        {
            text: "Նկարագրեք ձեր գործելաոճը.",
            options: [
                { text: "Ինքնուրույն", value: "4" },
                { text: "Որպես թիմի մաս", value: "3" },
                { text: "Առաջնորդի դերում", value: "2" },
                { text: "Ճկուն/հարմարվող ցանկացած ոճին", value: "1" }
            ]
        },
        {
            text: "Ինչպե՞ս եք վարվում սթրեսի և ճնշման հետ:",
            options: [
                { text: "Ֆիզիկական ակտիվության կամ մեդիտացիայի միջոցով", value: "3" },
                { text: "Անտեսելով այն, քանի դեռ չի անցել սթրեսային շրջանը", value: "1" },
                { text: "Առաջադրանքների պլանավորման և առաջնահերթությունների միջոցով", value: "4" }
            ]
        },
        {
            text: "Ո՞ր արդյունքն է առավել մեծացնում ձեր մոտիվացիան աշխատանքի մեջ:",
            options: [
                { text: "Հատուկ նպատակների իրականացում", value: "4" },
                { text: "Գործընկերների աջակցություն", value: "3" },
                { text: "Ստանալ ճանաչում և շոշափելի պարգևներ", value: "1" },
                { text: "Հետամուտ լինել անձնական աճին և հմտությունների զարգացմանը", value: "2" }
            ]
        },
        {
            text: "Նկարագրեք խնդրի լուծման ձեր մոտեցումը.",
            options: [
                { text: "Ստեղծագործական և ինտուիտիվ", value: "3" },
                { text: "Վերլուծական և մեթոդական", value: "4" },
                { text: "Անհրաժեշտության դեպքում օգնություն եմ խնդրում", value: "1" },
                { text: "Գործնական և պարզ", value: "2" }
            ]
        },
        {
            text: "Ինչպե՞ս եք առաջնահերթություն տալիս ձեր աշխատանքին:",
            options: [
                { text: "Ես դժվարանում եմ առաջնահերթություն տալ առաջադրանքներին", value: "1" },
                { text: "Ըստ առաջադրանքի կարևորության", value: "3" },
                { text: "Ղեկավարի ցուցումով", value: "2" },
                { text: "Ըստ վերջնաժամկետի", value: "4" }
            ]
        },
        {
            text: "Ինչպե՞ս եք վերաբերվում քննադատությանը:",
            options: [
                { text: "Ես դա օգտագործում եմ որպես մոտիվացիա", value: "1" },
                { text: "Ես դա կառուցողական եմ ընկալում, որպեսզի բարելավվեմ", value: "4" },
                { text: "Ես դժվարանում եմ ընդունել", value: "2" },
                { text: "Քննադատության հանդեպ իմ արձագանքը տարբեր է՝ կախված քննադատից", value: "3" }
            ]
        },
        {
            text: "Ո՞րն է ձեր ամենամեծ ուժը:",
            options: [
                { text: "Հաղորդակցման հմտություններ", value: "4" },
                { text: "Խնդիրներ լուծելու հմտություններ", value: "2" },
                { text: "Առաջնորդության ունակություններ", value: "3" },
                { text: "Արագ սովորելու ունակություն", value: "1" }
            ]
        },
        {
            text: "Ո՞րն է ձեր ամենամեծ թուլությունը:",
            options: [
                { text: "Չեմ համարձակվում պատվիրակել", value: "3" },
                { text: "Չափից շատ աշխատանք ստանձնելը", value: "2" },
                { text: "Անհամբերությունը", value: "4" },
                { text: "Չափազանց մանրամասն կողմնորոշված լինելը", value: "1" }
            ]
        },
        {
            text: "Ինչպե՞ս եք կառավարում կոնֆլիկտները թիմում:",
            options: [
                { text: "Խորհրդակցելով ղեկավարի հետ", value: "1" },
                { text: "Խուսափելով կոնֆլիկտային իրավիճակներից", value: "2" },
                { text: "Խնդիրներին ուղղակիորեն անդրադառնալով", value: "4" },
                { text: "Կողմերի միջև միջնորդությամբ", value: "3" }
            ]
        },
        {
            text: "Ընտրեք մեկ օրինակ, որը լավագույնս նկարագրում է այն պահը, երբ դուք բախվում եք ձախողման:",
            options: [
                { text: "Ես երբեք չեմ ձախողվել իմ դերում.", value: "1" },
                { text: "Ժամանակի վատ կառավարման արդյունքում, չեմ կարողացել առաջադրանը ավարտել դրա կատարման համար հատկացված ժամանակահատվածում, ինչը ինձ օգնեց հետագայում կատարելագործել առաջադրանքներում գործողությունները առավել արդյունավետ դասակարգելու իմ կարողությունը:", value: "2" },
                { text: "Թիմի անդամների հետ սխալ շփվելը հանգեցրեց նախագծի ձախողմանը, ինչը ստիպեց ինձ կենտրոնանալ իմ հաղորդակցման հմտությունների կատարելագործման վրա:", value: "3" },
                { text: "Անհաջողությունը հմտության պակասի պատճառով էր, և ես հետամուտ էի լրացուցիչ վերապատրաստման։", value: "4" }
            ]
        },
        {
            text: "Ինչո՞ւ եք ուզում այստեղ աշխատել:",
            options: [
                { text: "Այլ պատճառներ, որոնք նշված չեն այստեղ", value: "1" },
                { text: "Ընկերության մշակույթը գրավում է ինձ", value: "4" },
                { text: "Ես հետաքրքրված եմ ընկերության ապրանքներով կամ ծառայություններով", value: "2" },
                { text: "Լավ հնարավորություններ կան կարիերայի առաջխաղացման համար", value: "3" }
            ]
        },
        {
            text: "Որո՞նք են ձեր կարիերայի նպատակները:",
            options: [
                { text: "Ղեկավար  պաշտոնի զբաղեցնելը", value: "4" },
                { text: "Մասնագիտանալ իմ ներկայիս ոլորտում", value: "3" },
                { text: "Ես դեռ վստահ չեմ", value: "1" },
                { text: "Անցում դեպի այլ արդյունաբերություն", value: "2" }
            ]
        },
        {
            text: "Ինչպե՞ս եք հետևում ինչ որ ոլորտի թրենդներին:",
            options: [
                { text: "ես դժվարանում եմ հետևել թրենդներին", value: "1" },
                { text: "Աշխատաժողովների և կոնֆերանսների մասնակցություն", value: "3" },
                { text: "Մասնագիտական ամսագրերի ընթերցում", value: "4" },
                { text: "Կոմունիկացիայի պահպանում ոլորտի մասնագետների հետ", value: "2" }
            ]
        },
        {
            text: "Ինչպե՞ս եք գնահատում հաջողությունը:",
            options: [
                { text: "Գործընկերների և ղեկավարների կողմից արձագանքներ ստանալու միջոցով", value: "2" },
                { text: "Ընկերության հաջողության վրա իմ աշխատանքի ազդեցությամբ", value: "1" },
                { text: "Անձնական նպատակներին հասնելով", value: "4" },
                { text: "Թիմի/բաժանմունքի նպատակներին հասնելով", value: "3" }
            ]
        },
        {
            text: "Ի՞նչ արդյունք եք ունեցել ձեր վերջին նախագծում:",
            options: [
                { text: "Հաջողությամբ ավարտվեց, բայց ծախսերը գերազանցել են նախագծին նախատեսված բյուջեն", value: "3" },
                { text: "Չհաջողվեց ավարտել", value: "2" },
                { text: "Հաջողությամբ ավարտվեց ժամանակին", value: "4" },
                { text: "Հանգեցրեց անսպասելի դրական արդյունքի", value: "1" }
            ]
        },
        {
            text: "Ինչպե՞ս եք վերաբերվում իրավիճակին, երբ չգիտեք հարցի պատասխանը:",
            options: [
                { text: "Ուսումնասիրել, մինչև ես գտնեմ պատասխանը", value: "4" },
                { text: "Խուսափել իրավիճակից", value: "1" },
                { text: "Հարցնել գործընկերոջը կամ ղեկավարին առաջնորդության համար", value: "3" },
                { text: "Օգտագործել իմ լավագույն դատողությունը և շարունակել", value: "2" }
            ]
        },
        {
            text: "Ինչպե՞ս եք մոտենում նոր հմտություն կամ տեխնոլոգիա սովորելուն:",
            options: [
                { text: "Փորձելու պատրաստակամությամբ", value: "3" },
                { text: "Դժկամությամբ, միայն անհրաժեշտության դեպքում", value: "2" },
                { text: "Ես նախընտրում եմ ունենալ այն, ինչ գիտեմ", value: "1" },
                { text: "Խանդավառությամբ և վճռականությամբ", value: "4" }
            ]
        },
        {
            text: "Նկարագրեք, թե ինչպես կաշխատեք սեղմ ժամկետներում:",
            options: [
                { text: "Հանձնարարելով առաջադրանքներ ուրիշներին", value: "2" },
                { text: "Առաջնահերթություն տալ առաջադրանքներին  և կատարել արդյունավետ աշխատանք", value: "4" },
                { text: "Աշխատել երկար ժամեր՝ վերջնաժամկետները պահպանելու համար", value: "3" },
                { text: "Բաց թողնել վերջնաժամկետը", value: "1" }
            ]
        },
        {
            text: "Ինչպե՞ս եք նպաստում դրական աշխատանքային միջավայրի ստեղծմանը:",
            options: [
                { text: "Նպաստելով թիմային նպատակներին", value: "2" },
                { text: "Այլ պատճառներ, որոնք նշված չեն այստեղ", value: "1" },
                { text: "Աջակցելով գործընկերներին", value: "4" },
                { text: "Պահպանելով դրական վերաբերմունք", value: "3" }
            ]
        },
        {
            text: "Ի՞նչն է ձեզ մոտիվացնում աշխատանքի մեջ:",
            options: [
                { text: "Մրցակցային մարտահրավերները", value: "4" },
                { text: "Համագործակցային թիմային աշխատանքը", value: "3" },
                { text: "Անկախ աշխատելը", value: "1" },
                { text: "Աշխատանքի ճկուն գրաֆիկը", value: "2" }
            ]
        }
        ],
        errors: {
            answerRequired: 'Պատասխանը պարտադիր է։'
        },
        buttonNext: 'Հաջորդը',
        buttonPrev: 'Նախորդը',
        buttonSubmit: 'Ավարտել'
    },
};


function updateLanguage(lang) {
    formLangInput.value = lang;
    const data = translations[lang];
    questionsContainer.innerHTML = '';

    data.questions.forEach((q, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question';
        questionDiv.id = `question${index + 1}`;
        questionDiv.innerHTML = `<p>${index + 1}. ${q.text}</p>`;
        q.options.forEach(option => {
            const label = document.createElement('label');
            const input = document.createElement('input');
            input.type = 'radio';
            input.name = `q${index + 1}`;
            input.value = option.value;
            input.required = true;
            label.appendChild(input);
            label.append(option.text);
            questionDiv.appendChild(label);
        });

        questionsContainer.appendChild(questionDiv);
    });
    $('#nextButton').text(data.buttonNext);
    $('#prevButton').text(data.buttonPrev);
    $('#submit-btn').text(data.buttonSubmit);
}


languageSelector.value = formLangInput.value;
    updateLanguage(formLangInput.value);
languageSelector.addEventListener('change', function() {
    updateLanguage(this.value);
});
