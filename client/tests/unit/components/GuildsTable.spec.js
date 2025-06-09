import { mount } from '@vue/test-utils'
import GuildsTable from '@/components/GuildsTable.vue'
import { nextTick } from 'vue'

describe('GuildsTable.vue', () => {
  let wrapper;
  let mockGridApi;
  let mockFilterInstance;

  beforeEach(() => {
    // Create a detailed mock for the AG Grid API
    mockFilterInstance = {
      setModel: jest.fn(),
    };
    mockGridApi = {
      getFilterInstance: jest.fn(() => mockFilterInstance),
      onFilterChanged: jest.fn(),
      setFilterModel: jest.fn(),
      sizeColumnsToFit: jest.fn(),
      resetRowHeights: jest.fn(),
      refreshCells: jest.fn(),
      getFilterModel: jest.fn(),
    };

    wrapper = mount(GuildsTable, {
      props: {
        isDetailsPanelVisible: false,
        allGuildsData: [],
        userCorrelationMap: null,
        showUserCorrelation: false,
        raceFilterObject: null,
        membersFilterObject: null,
        pointsFilterObject: null,
        descriptionFilterObject: null,
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
    
    // Manually inject the mocked gridOptions after mount
    wrapper.vm.gridOptions.api = mockGridApi;
  })

  it('renders and mounts, and emits hit-server', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.emitted('hit-server')).toHaveLength(1)
    expect(wrapper.emitted('hit-server')[0]).toEqual(['guilds'])
  })

  it('calls the grid API when a filter prop changes', async () => {
    // 1. Simulate a prop change from the parent
    const raceFilter = { filterType: 'text', type: 'equals', filter: 'Human' }
    await wrapper.setProps({ raceFilterObject: raceFilter })
    await nextTick() // Wait for the watcher to fire

    // 2. Assert that our component called the correct grid API methods
    expect(mockGridApi.getFilterInstance).toHaveBeenCalledWith('race')
    expect(mockFilterInstance.setModel).toHaveBeenCalledWith(raceFilter)
    expect(mockGridApi.onFilterChanged).toHaveBeenCalled()
  })

  it('calls setFilterModel with null when clearFilters is called', () => {
    wrapper.vm.clearFilters()
    expect(mockGridApi.setFilterModel).toHaveBeenCalledWith(null)
  })

  it('emits launch-guild-details when a guild-info icon is clicked', async () => {
    // We can't easily simulate a click on the AG-Grid-rendered DOM.
    // Instead, we can call the method directly with a mock event object.
    const mockEvent = {
      target: {
        matches: (selector) => selector === '.guild-info, i',
        parentElement: {
          innerText: '12345'
        }
      }
    }
    wrapper.vm.monitorClicks(mockEvent)

    await nextTick()

    expect(wrapper.emitted('launch-guild-details')).toHaveLength(1)
    expect(wrapper.emitted('launch-guild-details')[0][0]).toBe('12345')
  })
}) 