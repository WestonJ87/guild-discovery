<template>
    <div id="selected-question">
        <div v-show="currentQuestion.type == 'text'" class="field simple-text-field" 
             :class="{'is-horizontal' : currentQuestion.isHorizontalField }">
            <div class="field-label is-large"> 
                <label class="label">{{ currentQuestion.label }}</label>
            </div>
            <div class="field-body">
                <div class="field" required>
                <input v-model="userInput" v-on:blur="progressQuestionaire" 
                    class="input is-large" type="text" 
                    :placeholder="currentQuestion.placeholder">
                </div>
            </div>
        </div>
        <div v-show="currentQuestion.type == 'select'" class="field simple-select-field"
             :class="{'is-horizontal' : currentQuestion.isHorizontalField }">
            <div class="field-label is-large"> 
                <label class="label">{{ currentQuestion.label }}</label>
            </div>
            <div class="field-body">
                <div class="field" required>
                    <div class="select is-large" :class="{ 'is-multiple' : currentQuestion.isMultiple }">
                        <select v-model="selectResults" 
                            v-on:blur="validateResponse"
                            v-bind:multiple="currentQuestion.isMultiple || false" 
                            class="is-large">
                            <option value="">- Select -</option>
                            <option v-for="option in currentQuestion.options" 
                                    v-bind:key="option.value" :value="option.value">
                                    {{ option.description }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="currentQuestion.type == 'textarea'" class="field text-area-field"
             :class="{'is-horizontal' : currentQuestion.isHorizontalField}">
            <div class="field-label is-large"> 
                <label class="label">{{ currentQuestion.label }}</label>
            </div>
            <div class="field-body">
                <div class="field" required>
                    <div class="control">
                        <textarea v-model="userInput" v-on:blur="validateResponse" class="textarea is-large"
                            :class="{
                                'is-info': inputLength < currentQuestion.threshold * 0.1,
                                'is-danger': inputLength >= currentQuestion.threshold * 0.1 && inputLength < currentQuestion.threshold * 0.3,
                                'is-warning' : inputLength >= currentQuestion.threshold * 0.3 && inputLength < currentQuestion.threshold * 0.7,
                                'is-success' : inputLength >= currentQuestion.threshold *0.7
                            }"
                            :placeholder="currentQuestion.placeholder"
                            :rows="currentQuestion.rows">
                        </textarea>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="currentQuestion.type == 'surveystyle'" class="field surveystyle"
             :class="{'is-horizontal' : currentQuestion.isHorizontalField || currentQuestion.noLabel }">
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <div class="table-container">
                            <table class="table is-bordered is-striped is-hoverable is-fullwidth">
                                <thead>
                                    <tr class="sticky-table-header">
                                        <th class="has-text-right"> Question : </th>
                                        <th v-for="(header, index) in currentQuestion.headers" 
                                            v-bind:key="index"
                                            class="has-text-centered">
                                            {{ header }}
                                        </th>
                                    </tr>
                                </thead>
                                <tbody v-for="(category, index) in currentQuestion.survey" v-bind:key="index">
                                    <tr class="category-header">
                                        <td :colspan="currentQuestion.headers.length + 1"> 
                                            {{ currentQuestion.categoryMap[index] }}
                                        </td>
                                    </tr>
                                    <tr v-for="(question, indexLower) in category" v-bind:key="indexLower" required>
                                        <td class="has-text-right">{{ question }}</td>
                                        <td v-for="header in currentQuestion.headers" 
                                            v-bind:key="header"
                                            class="has-text-centered">
                                            <input class="survey-radio" type="radio" 
                                                @click="logSurveyEntry($event, question, indexLower)">
                                        </td>
                                    </tr>
                                </tbody>
                                <tfoot></tfoot>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'QuestionaireElement',
    props: [ 'currentQuestion' ],
    data () {
        return {
            name: 'QuestionaireElement',
            userInput: '',
            selectResults: [],
            surveyMap: []
        }
    },
    mounted: function (){
        this.$log.info("CONTEXT : ", this.name + " : MOUNTED");
    },
    computed: {
        inputLength: function () {
            return this.userInput.length
        }
    },
    methods: {
        validateResponse: function () {
            // How shall we do this?
            this.progressQuestionaire();
        },
        progressQuestionaire: function () {
            if (this.currentQuestion.type == 'textarea') {
                this.questionPageCompleted('text');
            } else {
                this.questionPageCompleted(this.currentQuestion.type);
            }
            this.userInput = '';
            this.selectResults = [];
            this.surveyMap = [];
        },
        logSurveyEntry: function(e, question, index) {
            // get all radio elements for row
            let allRadioBtns = Array.prototype.map.call(e.target.parentElement.parentElement.children, (node) => node.children[0] );
            allRadioBtns.shift();
            // uncheck any currently checked radios for the row
            allRadioBtns.forEach(radio => radio.checked = false );
            e.target.checked = true;
            //console.log(e, question, index);

            // update map of survey questions
            let found = this.surveyMap.findIndex(row => row.question == question);
            if (found == -1) {
                this.surveyMap.push({ question: question, weight: index });
            } else {
                this.surveyMap[found].weight = index;
            }
            // TODO: revise this in the future incase we want multiple surveyMaps
            // console.log(this.surveyMap, [].concat(...this.currentQuestion.survey).length);
            if (this.surveyMap.length == [].concat(...this.currentQuestion.survey).length) {
                this.questionPageCompleted('survey');
            }
        },
        questionPageCompleted: function (type) {
            switch (type) {
                case 'survey':
                    this.$emit('question-page-completed', { type: type, results: this.surveyMap });
                    break;
                case 'text':
                    this.$emit('question-page-completed', { type: type, results: this.userInput });
                    break;
                case 'select':
                    this.$emit('question-page-completed', { type: type, results: this.selectResults });
                    break;
            }
            
        }
    }
}
</script>

<style scoped lang="scss">
#selected-question {
    margin-top: -100px;
}

.text-area-field, .simple-text-field, .simple-select-field {
    margin: 0 auto;
    padding-right: 150px;
    padding-left: 150px;
}

.simple-select-field > .field-body > .field > .select > select {
    width: 600px;
}

.category-header > td {
    background-color: gainsboro !important;
    box-shadow: 0 5px 2px -4px black !important;
    font-weight: 500;
    font-size: 1.1em;
}

/* doesnt work */
th {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  z-index: 2;
}

.surveystyle {
    max-height: 375px;
    overflow: scroll;
}

.survey-radio {
    transform: scale(1.2);
}
</style>