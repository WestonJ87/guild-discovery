import { mount } from '@vue/test-utils'
import GuildFilterPanel from '@/components/GuildFilterPanel.vue'

// Mock lodash debounce
jest.mock('lodash', () => ({
  ...jest.requireActual('lodash'),
  debounce: (fn) => fn,
}));

describe('GuildFilterPanel.vue', () => {
  let wrapper;

  beforeEach(() => {
    // Mock localStorage
    Object.defineProperty(window, 'localStorage', {
      value: {
        surveyResults: null,
        getItem: jest.fn(),
        setItem: jest.fn(),
        clear: jest.fn()
      },
      writable: true
    });

    wrapper = mount(GuildFilterPanel, {
      props: {
        isDetailsPanelVisible: false,
        showUserCorrelationForm: false
      },
      global: {
        stubs: {
          QuestionaireModal: true,
        },
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

  it('emits filter-by-race event when race is selected', async () => {
    const select = wrapper.find('select')
    await select.setValue('Human')

    const emittedEvent = wrapper.emitted('filter-by-race')
    expect(emittedEvent).toHaveLength(1)
    expect(emittedEvent[0][0]).toBe('Human')
  })

  it('emits filter-by-participants event when minimumMembers is changed', async () => {
    const input = wrapper.find('#member-min')
    await input.setValue('10')

    const emittedEvent = wrapper.emitted('filter-by-participants')
    expect(emittedEvent).toHaveLength(1)
    expect(emittedEvent[0][0]).toEqual({ type: 'min', value: '10' })
  })

  it('resets all data and emits reset-filters event on click', async () => {
    // SETUP
    await wrapper.setData({
      race: 'Demon',
      minimumMembers: '10',
      maximumMembers: '100'
    })

    // EMIT EVENT
    const resetButton = wrapper.find('button.delete')
    await resetButton.trigger('click')

    // ASSERTIONS
    expect(wrapper.emitted('reset-filters')).toHaveLength(1)
    expect(wrapper.vm.race).toBe('')
    expect(wrapper.vm.minimumMembers).toBe('')
    expect(wrapper.vm.maximumMembers).toBe('')
  })

  it('emits filter-by-points event when minimumTotalPoints is changed', async () => {
    const input = wrapper.find('#total-points')
    await input.setValue('1000')

    const emittedEvent = wrapper.emitted('filter-by-points')
    expect(emittedEvent).toHaveLength(1)
    expect(emittedEvent[0][0]).toEqual({ type: 'total', value: '1000' })
  })

  it('emits show-hide-single-member event when checkbox is toggled', async () => {
    const checkbox = wrapper.find('[data-testid="hide-single-member-guilds-checkbox"]')
    await checkbox.setChecked()

    const emittedEvent = wrapper.emitted('show-hide-single-member')
    expect(emittedEvent).toHaveLength(1)
    expect(emittedEvent[0][0]).toBe(true)
  })

  it('emits launch-user-survey and handles completion state', async () => {
    // SETUP
    const surveyButton = wrapper.find('#user-survey-form-btn a')
    await surveyButton.trigger('click')

    // ASSERT
    expect(wrapper.emitted('launch-user-survey')).toHaveLength(1)
    
    // SETUP
    await wrapper.setData({ userCorrelationFormCompleted: true })
    
    // ASSERT
    expect(surveyButton.text()).toContain('Redo guild dating profile')

    // EMIT EVENT
    await surveyButton.trigger('click')

    // ASSERT
    expect(wrapper.vm.userCorrelationFormCompleted).toBe(false)
  })

  it('emits get-user-correlations when the request button is clicked', async () => {
    // SETUP
    await wrapper.setData({ userCorrelationFormCompleted: true })

    // EMIT EVENT
    const requestButton = wrapper.find('#generate-user-correlation-btn a')
    await requestButton.trigger('click')

    // ASSERT
    expect(wrapper.emitted('get-user-correlations')).toHaveLength(1)
  })

  it('emits close-correlation-form when the child modal emits it', async () => {
    const modal = wrapper.findComponent({ name: 'QuestionaireModal' })
    await modal.vm.$emit('close-correlation-form')
    expect(wrapper.emitted('close-correlation-form')).toHaveLength(1)
  })

  it('emits survey-complete and updates state when the child modal emits it', async () => {
    const modal = wrapper.findComponent({ name: 'QuestionaireModal' })
    const mockResults = { some: 'data' }
    await modal.vm.$emit('user-correlation-survey-complete', mockResults)

    // ASSERTIONS
    expect(wrapper.emitted('user-correlation-survey-complete')[0][0]).toEqual(mockResults)
    expect(wrapper.vm.userCorrelationFormCompleted).toBe(true)
  })
})

describe('GuildFilterPanel.vue with localStorage', () => {
  it('sets userCorrelationFormCompleted to true if surveyResults exist in localStorage', () => {
    // SETUP
    Object.defineProperty(window, 'localStorage', {
      value: {
        surveyResults: 'some-results',
      },
      writable: true
    });

    const wrapper = mount(GuildFilterPanel, {
      global: {
        stubs: {
          QuestionaireModal: true,
        },
        mocks: {
          $log: {
            info: jest.fn(),
          },
        },
      },
    })

    // ASSERTIONS
    expect(wrapper.vm.userCorrelationFormCompleted).toBe(true)
  })
}) 