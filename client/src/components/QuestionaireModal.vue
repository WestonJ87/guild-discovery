<template>
<div :class="{ 'is-active': showUserCorrelationForm }" class="modal">
    <div class="modal-background"></div>
    <div class="modal-content">
        <section class="section">
        <div class="container">
            <div id="user-correlation-form" class="card">
            <h3 class="title">Describe your ideal playstyle...</h3>
            <h5 class="subtitle has-text-centered">
                <i>we'll find you that most perfect guild partnership for future pillaging... or farming.. your perogative.</i>
            </h5>
            <QuestionaireForm
                @complete-survey="userQuestionaireCompleted" 
                :resetStep="resetStep">
            </QuestionaireForm>
            </div>
        </div>
        </section>
    </div>
    <button @click="closeUserCorrelationForm" class="modal-close is-large" aria-label="close"></button>
    </div>    
</template>

<script>
import QuestionaireForm from './QuestionaireForm'

export default {
    name: 'QuestionaireModal',
    data () {
        return {
        name: 'QuestionaireModal',
        resetStep: false
        }
    },
    props: [ 'showUserCorrelationForm' ],
    components: {
        QuestionaireForm
    },
    mounted: function () {
        this.$log.info("CONTEXT : ", this.name + " : MOUNTED");
    },
    methods: {
        userQuestionaireCompleted: function (results) {
            this.$emit('user-correlation-survey-complete', results);
            this.closeUserCorrelationForm();
        },
        closeUserCorrelationForm: function() {
            this.resetStep = true;
            this.$emit('close-correlation-form');
      }
    }
}
</script>

<style lang="scss" scoped>
.subtitle {
  margin-top: 30px !important;
}

#user-correlation-form {
  padding: 50px;
  height: 70vh;
  width: 80vw;
}

.modal-content {
  width: auto;
  min-width: 0;
}
</style>