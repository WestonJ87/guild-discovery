<template>
    <form id="questionaire-workspace">
        <div id="highlighted-question">
            <QuestionionaireElement
                @question-page-completed="progressQuestionaire"
                :currentQuestion="currentQuestion">
            </QuestionionaireElement>
        </div>
        <div id="progress-dots" class="has-text-centered">
            <div class="dotstyle dotstyle-smalldotstroke">
					<ul>
						<li v-for="(item, index) in questionaireQuestions"  v-bind:key=index
                            :class="{'current': item.current }" class="">
                                <a v-if="!item.completed" href="#"></a>
                                <img v-if="item.completed" class="checkmark" src="@/images/check.png"/>
                        </li>
                        <li style="margin-top: -5px;">
                            <button @click="completeSurvey" :disabled="!questionaireSurveyFilled"
                                type="button"
                                :class="{'is-success ' : questionaireSurveyFilled }" 
                                class="button is-small is-rounded">{{ questionaireSurveyFilled ? 'DONE' : "continue" }}
                            </button>
                        </li>
					</ul>
				</div>
        </div>
    </form>
</template>

<script>
import QuestionionaireElement from './QuestionaireElement'

export default {
    name: 'QuestionaireForm',
    props: [ 'resetStep' ],
    data () {
        return {
            name: 'QuestionaireForm',
            questionaireQuestions: [],
            questionaireResults: [],
            questionaireCompleted: false,
            questionaireSurveyFilled: false,
            step: 0,
            currentQuestion: null
        }
    },
    components: {
        QuestionionaireElement
    },
    beforeMount() {
        this.$log.info("CONTEXT : ", this.name + " : MOUNTED");
        this.questionaireQuestions = this.getQuestionaireQuestions();
        this.currentQuestion = this.questionaireQuestions[this.step];
    },
    watch: {
        resetStep: function () {
            this.resetProgessionForm();
        }
    },
    methods: {
        completeSurvey: function() {
            if (this.questionaireSurveyFilled) {
                this.$emit('complete-survey', this.questionaireResults);
            }
        },
        progressQuestionaire: function(payload) {
            // add result of user input to the results array
            this.questionaireResults.push(payload);

            // check for full form completion.  This should match once all have been done
            if (this.questionaireQuestions.length == this.questionaireResults.length) {
                this.questionaireSurveyFilled = true;
            } else {
                // Manage step settings and whether questions have been completed
                this.questionaireQuestions[this.step].current = false;
                this.questionaireQuestions[this.step].completed = true;
                this.step += 1;
                this.currentQuestion = this.questionaireQuestions[this.step]
                this.questionaireQuestions[this.step].current = true;
            }
        },
        resetProgessionForm: function () {
            this.currentQuestion = null;
            this.questionaireQuestions.map( (question) => question.current = false );
            this.questionaireQuestions.map( (question) => question.completed = false );
            this.step = 0;
            this.currentQuestion = this.questionaireQuestions[this.step];
            this.questionaireQuestions[this.step].current = true;
        },
        getQuestionaireQuestions: function () {
            return [
                {
                    type: 'text',
                    label: 'Age',
                    placeholder: 'Age in years.',
                    current: true,
                    completed: false,
                    isHorizontalField: true,
                    noLabel: false
                }, 
                {
                    type: 'text',
                    label: 'Gender',
                    placeholder: 'Gender - Pronouns.',
                    current: false,
                    completed: false,
                    isHorizontalField: true,
                    noLabel: false
                }, 
                {
                    type: 'select',
                    label: 'Race',
                    selected: '',
                    options: [
                        { value: 'D', description: 'Demon' }, 
                        { value: 'B', description: 'Beastman' }, 
                        { value: 'H', description: 'Human' }
                    ],
                    isMultiple: true,
                    current: false,
                    completed: false,
                    isHorizontalField: true,
                    noLabel: false
                }, 
                {
                    type: 'select',
                    label: 'Frequency of Play (Best estimate)',
                    selected: '',
                    options: [
                        { value: 8, description: '6+ hours daily' }, 
                        { value: 7, description: '3+ hours daily' }, 
                        { value: 6, description: '1 hour daily' }, 
                        { value: 5, description: '3-6 times per week - long session' }, 
                        { value: 4, description: '3-6 times per week - short session' }, 
                        { value: 3, description: '1-3 times per week' }, 
                        { value: 2, description: 'weekly' }, 
                        { value: 1, description: 'monthly' }
                    ],
                    isMultiple: false,
                    current: false,
                    completed: false,
                    isHorizontalField: true,
                    noLabel: false
                }, 
                {
                    type: 'textarea',
                    label: 'Describe guild participation style',
                    rows: 8,
                    threshold: 250,
                    current: false,
                    completed: false,
                    isHorizontalField: false,
                    noLabel: false
                },
                {
                    type: 'surveystyle',
                    label: 'Rate yourself on the following metrics',
                    headers: [
                        'Not at all interested', 
                        'occasionally interested', 
                        'indifferent', 
                        'often interested', 
                        'most interested'
                    ],
                    survey: [
                    [
                            'Do you enjoy PvP?',
                            'Do you enjoy farming?',
                            'Do you enjoy crafting?',
                            'Are you a treasure hunter?',
                            'Do you care about getting the best items in game?',
                    ],
                    [
                        'in game sexting?',
                        'virtual harassment and social engineering?',
                        'another question',
                        'another one',
                        'another one - DJ Khalid'
                    ]],
                    categoryMap: ['important', 'not so important'],
                    current: false,
                    completed: false,
                    noLabel: true
                }
            ]
        }
    }
}
</script>

<style lang="scss" scoped>
#questionaire-workspace {
    height: 100%;
    position: relative;
}

#highlighted-question {
  display: flex;
  justify-content: center;
  flex-direction: column;
  height: 500px;
}

.checkmark {
    transform: scale(1.5);
}

#progress-dots {
    position: absolute;
    bottom: 10%;
    height: 50px;
    margin: 0 auto;
    width: 80%;
    left: 0;
    right: 0;
}

.dotstyle ul {
	position: relative;
	display: inline-block;
	margin: 0 auto;
	padding: 0;
	list-style: none;
	cursor: default;
}

.dotstyle li {
	position: relative;
	display: block;
	float: left;
	margin: 0 16px;
	width: 16px;
	height: 16px;
    border-radius: 50%;
	cursor: pointer;
}

.dotstyle li a {
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	outline: none;
	background-color: #333;
	background-color: rgba(71, 70, 70, 0.329);
    border-radius: 50%;
	text-indent: -999em;
	cursor: pointer; /* make the text accessible to screen readers */
	position: absolute;
}

.dotstyle-smalldotstroke li a {
	background-color: rgba(120, 120, 120, 0.7);
	-webkit-transition: background-color 0.3s ease, -webkit-transform 0.3s ease;
	transition: background-color 0.3s ease, transform 0.3s ease;
}

.dotstyle-smalldotstroke li a:hover,
.dotstyle-smalldotstroke li a:focus,
.dotstyle-smalldotstroke li.current a {
	background-color: #777;
}

.dotstyle-smalldotstroke li.current a {
	-webkit-transform: scale(0.4);
	transform: scale(0.4);
}

.dotstyle-smalldotstroke li.current {
	box-shadow: 0 0 0 2px #777;
}

</style>