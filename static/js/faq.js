const faqQuestions = document.querySelectorAll('.faq-question');
faqQuestions.forEach(question => {
    question.addEventListener('click', () => {
        const answer = question.nextElementSibling;
        if (answer.classList.contains('open')) {
            answer.classList.remove('open');
        } else {
            document.querySelectorAll('.faq-answer').forEach(a => a.classList.remove('open'));
            answer.classList.add('open');
        }
    });
});