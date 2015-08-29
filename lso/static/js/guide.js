(function() {
    // All non-ASCII IAST graphemes, listed here in HK. This is used in a
    // widget that allows the user to click on the special character they wish
    // to insert.
    var iastSpecialChars = ['A', 'I', 'U', 'R', 'RR', 'N', 'J', 'T', 'D', 'z', 'S'];

    // Template for the overall quiz.
    var quizTemplate = _.template(
        '<% q = data; %>' +
        '<div class="wrapper">' +
        '<h2><%= q.name %></h2>' +
        '<div class="progress"><div class="progress-bar" /></div>' +
        '<p><%= q.description %></p>' +
        '<div class="quiz-question" />' +
        '<p class="quiz-answer-preview">Answer: </p>' +
        '<div class="simple-form">' +
        '  <input type="text"></input><button class="right submit">Check</button>' +
        '  <p class="quiz-status" />' +
        '  <p>Click for special characters:</p>' +
        '  <ul class="special-chars">' +
        '    <% _.each(specialChars, function(c) { %>' +
        '      <li data-value="<%= c %>"><%= sa2(c) %> <kbd><%= c %></kbd></li>' +
        '    <% }); %>' +
        '  </ul>' +
        '</div>' +
        '</div>'
    );

    // Template for the question.
    var questionTemplate = _.template(
        '<% if (data.language === "sa") { %>' +
        '  <%= exemplify(data.curQuestion.question, true) %>' +
        '<% } else if (data.language === "devanagari") { %>' +
        '  <%= exemplify(data.curQuestion.question, false) %>' +
        '<% } else { %>' +
        '  <%= data.curQuestion.question %>' +
        '<% } %>'
    );

    // Template for the answer preview
    var answerPreviewTemplate = _.template(
        'Answer: <%= sa2(str) %>'
    );

    // Template for the quiz status (example, n remaining, done)
    var statusTemplate = _.template(
        '<% if (!data.usedExample) { %>' +
        '  This is an example question. The answer is <%= sa2(data.curQuestion.answer) %>.' +
        '<% } else if (!data.done) { %>' +
        '  Answer <%= model.getNumRemaining() %> more question(s) to finish the quiz.' +
        '<% } else { %>' +
        "  You've finished the quiz. " +
        "  If you like, you can continue to answer questions for practice." +
        '<% } %>'
    );


    // Print `s` in Devanagari. If `useBoth`, use IAST too.
    function exemplify(s, useBoth) {
        var result = '<p class="sa1">' +
            Sanscript.t(s, 'hk', 'devanagari') +
            '</p>';
        if (useBoth) {
            result += '<p class="sa2" lang="sa">' +
                Sanscript.t(s, 'hk', 'iast') +
                '</p>';
        }
        result = result.replace(/\[/g, '<mark>').replace(/]/g, '</mark>');
        return result;
    }

    // Print `s` as an sa2 span in IAST.
    function sa2(s) {
        var text = Sanscript.t(s, 'hk', 'iast');
        return '<span class="sa2" lang="sa">' + text + '</span>';
    }


    // Manages the entire quiz state, including the current question and the
    // number of questions remaining.
    var Quiz = Backbone.Model.extend({
        initialize: function() {
            this.set('numCorrect', 0);
            this.set('curQuestion', null);
            // True iff the user has correctly answered the example.
            this.set('usedExample', false);
            // True iff the user has "finished" the quiz.
            this.set('done', false);
        },

        // Return the quiz progress, on a [0, 1] scale.
        getFractionDone: function() {
            return (this.get('numCorrect') + 0.0) / this.get('numRequired');
        },

        // Return the number of questions left before the quiz is done.
        getNumRemaining: function() {
            return this.get('numRequired') - this.get('numCorrect');
        },

        // Process a (correct or incorrect) answer by updating the model's
        // internal state.
        processAnswer: function(answer) {
            hasCorrectAnswer = (answer === this.get('curQuestion').answer);
            if (this.get('done')) {
                return;
            }
            if (!this.get('usedExample')) {
                this.set('usedExample', hasCorrectAnswer);
                return;
            }

            if (hasCorrectAnswer) {
                this.set('numCorrect', this.get('numCorrect') + 1);
            } else {
                this.set('numCorrect', Math.max(this.get('numCorrect') - 1, 0));
            }

            if (this.get('numCorrect') == this.get('numRequired')) {
                this.set('done', true);
            }
        },

        // Update `curQuestion`.
        getNextQuestion: function() {
            if (this.get('example') && !this.get('usedExample')) {
                this.set('curQuestion', this.get('example'));
            } else {
                var nextQuestion = this.get('curQuestion');
                // TODO: better dup checking (history?)
                while (_.isEqual(nextQuestion, this.get('curQuestion'))) {
                    var index = _.random(0, this.get('items').length - 1);
                    nextQuestion = this.get('items')[index];
                }
                this.set('curQuestion', nextQuestion);
            }
        }
    });

    // Defines an interactive quiz. The user sees a question, types in an
    // answer, and gets immediate feedback.
    var QuizView = Backbone.View.extend({
        initialize: function() {
            this.$el.html(quizTemplate({ 'data': this.model.attributes,
                                         'exemplify': exemplify,
                                         'specialChars': iastSpecialChars,
                                         'sa2': sa2 }));

            this.$question = $('.quiz-question', this.el);
            this.$status = $('p.quiz-status', this.el);
            this.$answerPreview = $('.quiz-answer-preview', this.el);

            this.model.on('change:curQuestion', this.render, this);
            this.model.on('change:done', this.markAsDone, this);

            this.model.getNextQuestion();
        },

        events: {
            'click button': 'checkAnswer',
            'input input': 'showAnswerPreview',
            'keyup input': 'catchEnterKeypress',
            'click ul.special-chars li': 'addSpecialCharacter'
        },

        render: function() {
            this.$question.html(
                questionTemplate({ 'data': this.model.attributes,
                                   'exemplify': exemplify }));

            var percentComplete = 100.0 * this.model.getFractionDone();
            $('.progress-bar', this.el).width(percentComplete + '%');

            this.$status.html(
                statusTemplate({
                    'data': this.model.attributes,
                    'model': this.model,
                    'sa2': sa2
                }));
        },

        // Inform the user that the quiz is done.
        markAsDone: function() {
            this.$el.addClass('done');
        },

        // Insert a special (i.e. non-ASCII) character into the input field.
        addSpecialCharacter: function(e) {
            var newToken = $(e.currentTarget).data('value'),
               $input = this.$('input'),
                dom_input = $input.get()[0],
                cursorPos = dom_input.selectionStart;
            if (cursorPos) {
                var val = $input.val();
                $input.val(val.slice(0, cursorPos) + newToken + val.slice(cursorPos));
                // Force cursor to appear after newToken. Without this, the
                // cursor goes to the end of the input.
                dom_input.setSelectionRange(cursorPos + newToken.length,
                                            cursorPos + newToken.length);
            } else {
                $input.val($input.val() + newToken);
            }
            $input.focus();
            this.showAnswerPreview();
        },

        // checkAnswer() if the user pressed Enter.
        catchEnterKeypress: function(e) {
            if (e.which == 13) {
                this.checkAnswer();
            }
        },

        // Show the Devanagari and IAST versions of the user's input.
        showAnswerPreview: function() {
            var val = this.$('input').val();
            this.$answerPreview.html(answerPreviewTemplate({
                'str': val, 'sa2': sa2
            }));
        },

        // Check the user's answer then show a new question.
        checkAnswer: function() {
            var actual = this.$('input').val();
            this.model.processAnswer(this.$('input').val());
            this.$('input').val('');
            this.showAnswerPreview();
            this.model.getNextQuestion()
        }
    });

    $(function() {
        $.getJSON(document.URL + ':exercises', function(data) {
            new QuizView({
                // TODO: support multiple quizzes
                model: new Quiz(data[0]),
                el: $('section.exercises'),
            });
        });
    });
}());
