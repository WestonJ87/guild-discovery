import { mount } from '@vue/test-utils'
import QuestionaireElement from '@/components/QuestionaireElement.vue'

describe('QuestionaireElement.vue', () => {
  let wrapper;

  const mockQuestion = {
    type: 'text',
    label: 'Test Label',
    placeholder: 'Test Placeholder',
    isHorizontalField: false,
  }

  beforeEach(() => {
    wrapper = mount(QuestionaireElement, {
      props: {
        currentQuestion: mockQuestion
      },
      global: {
        mocks: {
          $log: {
            info: jest.fn(),
            error: jest.fn(),
          },
        },
      },
    })
  })

  it('renders and mounts', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('emits question-page-completed with user input for text type', async () => {
    // SETUP COMPONENT
    const input = wrapper.find('input[type="text"]')

    // EMIT EVENT
    await input.setValue('Hello World')

    // TRIGGER EVENT
    await input.trigger('blur')

    // ASSERTIONS
    const emittedEvent = wrapper.emitted('question-page-completed')
    expect(emittedEvent).toHaveLength(1)
    expect(emittedEvent[0][0]).toEqual({ type: 'text', results: 'Hello World' })
  })

  it('emits question-page-completed with user selection for select type', async () => {
    // SETUP COMPONENT
    const selectQuestion = {
      type: 'select',
      label: 'Select Label',
      options: [
        { value: 'opt1', description: 'Option 1' },
        { value: 'opt2', description: 'Option 2' },
      ],
    }
    await wrapper.setProps({ currentQuestion: selectQuestion })

    // SETUP COMPONENT
    const select = wrapper.find('select')

    // EMIT EVENT
    await select.setValue('opt2')

    // TRIGGER EVENT
    await select.trigger('blur')

    // ASSERTIONS
    const emittedEvent = wrapper.emitted('question-page-completed')
    expect(emittedEvent).toHaveLength(1)
    expect(emittedEvent[0][0]).toEqual({ type: 'select', results: 'opt2' })
  })

  it('builds a survey map and emits on completion for surveystyle', async () => {
    const surveyQuestion = {
      type: 'surveystyle',
      headers: ['H1', 'H2'],
      survey: [ ['Q1'], ['Q2'] ],
      categoryMap: ['C1']
    }
    await wrapper.setProps({ currentQuestion: surveyQuestion })

    // SETUP
    const rows = wrapper.findAll('tbody tr:not(.category-header)')

    // EMIT EVENT
    await rows[0].findAll('input[type="radio"]')[0].trigger('click')

    // ASSERTIONS
    expect(wrapper.vm.surveyMap).toHaveLength(1)
    expect(wrapper.vm.surveyMap[0]).toEqual({ question: 'Q1', weight: 0 })
    expect(wrapper.emitted('question-page-completed')).toBeUndefined()

    // EMIT ANOTHER EVENT
    await rows[1].findAll('input[type="radio"]')[1].trigger('click')
    
    // ASSERTIONS
    const emittedEvent = wrapper.emitted('question-page-completed')
    expect(emittedEvent).toHaveLength(1)
    expect(emittedEvent[0][0]).toEqual({
      type: 'survey',
      results: [
        { question: 'Q1', weight: 0 },
        { question: 'Q2', weight: 0 }
      ]
    })
  })

  it('emits question-page-completed with user input for textarea type', async () => {
    // SETUP COMPONENT
    const textareaQuestion = {
      type: 'textarea',
      label: 'Textarea Label',
      placeholder: 'Textarea Placeholder',
      threshold: 100, // for the :class bindings
    }
    await wrapper.setProps({ currentQuestion: textareaQuestion })

    // SETUP COMPONENT
    const textarea = wrapper.find('textarea')

    // EMIT EVENT
    await textarea.setValue('This is a longer text entry.')

    // TRIGGER EVENT
    await textarea.trigger('blur')

    // ASSERTIONS
    const emittedEvent = wrapper.emitted('question-page-completed')
    expect(emittedEvent).toHaveLength(1)
    expect(emittedEvent[0][0]).toEqual({ type: 'text', results: 'This is a longer text entry.' })
  })

  it('emits question-page-completed with user selections for multi-select type', async () => {
    // SETUP COMPONENT
    const multiSelectQuestion = {
      type: 'select',
      isMultiple: true,
      options: [
        { value: 'opt1', description: 'Option 1' },
        { value: 'opt2', description: 'Option 2' },
        { value: 'opt3', description: 'Option 3' },
      ],
    }
    await wrapper.setProps({ currentQuestion: multiSelectQuestion })
    
    // SETUP COMPONENT
    const select = wrapper.find('select')

    // EMIT EVENT
    await select.setValue(['opt1', 'opt3'])

    // TRIGGER EVENT
    await select.trigger('blur')

    // ASSERTIONS
    const emittedEvent = wrapper.emitted('question-page-completed')
    expect(emittedEvent).toHaveLength(1)
    expect(emittedEvent[0][0]).toEqual({ type: 'select', results: ['opt1', 'opt3'] })
  })
}) 