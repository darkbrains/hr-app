$(document).ready(function() {
    const languageSelector = $('#language-selector');
    const questionsContainer = $('#questions-container');
    let currentQuestionIndex = 0;
    let totalQuestions = translations[languageSelector.val()].questions.length;


    function loadQuestions(lang) {
        const questions = translations[lang].questions;
        const errorMessage = translations[lang].errors.answerRequired;
        questionsContainer.empty();
        questions.forEach((q, index) => {
            const questionDiv = $('<div>', { class: 'question', id: `question${index + 1}`, style: 'display: none;' });
            const questionText = $('<p>').text(`${index + 1}. ${q.text}`);
                const errorDiv = $('<div>', {
                    class: 'error',
                    text: errorMessage,
                    style: 'display: none; color: red;'
                });
            questionDiv.append(questionText);
            q.options.forEach(option => {
                const label = $('<label>');
                const input = $('<input>', { type: 'radio', name: `q${index + 1}`, value: option.value, required: true });
                label.append(input, option.text);
                questionDiv.append(label);
            });
            questionDiv.append(errorDiv);
            questionsContainer.append(questionDiv);
        });
        totalQuestions = questions.length;
        currentQuestionIndex = 1;
        showQuestion(currentQuestionIndex);
        initializeProgress();
    }


    function showQuestion(number) {
        $('.question').hide();
        $(`#question${number}`).show();
        updateProgress(number);
        updateNavigationButtons(number);
    }


    function updateNavigationButtons(number) {
        $('#prevButton').toggle(number > 1);
        $('#nextButton').toggle(number < totalQuestions);
        $('#submit-btn').toggle(number === totalQuestions);
    }


    function initializeProgress() {
        const progressContainer = $('#progress');
        progressContainer.empty();
        for (let i = 1; i <= totalQuestions; i++) {
            const circle = $('<span>').addClass('circle');
            progressContainer.append(circle);
        }
        updateProgress(1);
    }


    function updateProgress(index) {
        $('.circle').slice(0, index).addClass('answered');
    }


    function validateQuestion() {
        const inputs = $(`#question${currentQuestionIndex} input[type="radio"]`);
        const errorDiv = $(`#question${currentQuestionIndex} .error`);
        const errorMessage = translations[languageSelector.val()].errors.answerRequired;
        if (inputs.is(':checked')) {
            errorDiv.hide();
            return true;
        } else {
            console.error(`Error: Question ${currentQuestionIndex} requires an answer!`);
            errorDiv.text(errorMessage).show();
            return false;
        }
    }


    function submitForm() {
        if (validateQuestion()) {
            $('#interviewForm').submit();
        }
    }


    $('#nextButton').click(function() {
        if (validateQuestion()) {
            currentQuestionIndex++;
            showQuestion(currentQuestionIndex);
        }
    });
    $('#prevButton').click(function() {
        if (currentQuestionIndex > 1) {
            currentQuestionIndex--;
            showQuestion(currentQuestionIndex);
        }
    });
    $('#submit-btn').click(function(event) {
        event.preventDefault();
        submitForm();
    });
    languageSelector.change(function() {
        loadQuestions(this.value);
        currentQuestionIndex = 1;
    });

    loadQuestions(languageSelector.val());
    });
