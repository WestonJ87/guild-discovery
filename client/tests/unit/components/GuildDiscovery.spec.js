import { mount } from '@vue/test-utils'
import GuildDiscovery from '@/components/GuildDiscovery.vue'
import GuildFilterPanel from '@/components/GuildFilterPanel.vue'
import axios from 'axios'

// Mock axios globally for all tests in this file
jest.mock('axios')

describe('GuildDiscovery.vue', () => {
  let wrapper;

  beforeEach(() => {
    // Provide a default mock implementation for axios.get before each test
    axios.get.mockResolvedValue({ data: { AllGuilds: [] } });

    wrapper = mount(GuildDiscovery, {
      global: {
        mocks: {
          $log: {
            info: jest.fn(),
            error: jest.fn(),
          },
        },
        stubs: {
          GuildsTable: true,
        }
      },
    })
  })

  it('renders and mounts', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('updates race filter when filter-by-race event is received', async () => {
    // SETUP COMPONENT
    const filterPanel = wrapper.findComponent(GuildFilterPanel)

    // EMIT EVENT
    await filterPanel.vm.$emit('filter-by-race', 'Human')

    // ASSERTIONS
    expect(wrapper.vm.raceFilterObject).toEqual({
      filterType: "text",
      type: "Equals",
      filter: "Human",
    })
    expect(wrapper.vm.raceImageIndex).toBe("02")
  })

  it('updates members filter when filter-by-participants event is received', async () => {
    const filterPanel = wrapper.findComponent(GuildFilterPanel)

    // TEST 1: MINIMUM VALUE
    await filterPanel.vm.$emit('filter-by-participants', { type: 'min', value: 10 })

    expect(wrapper.vm.membersFilterObject).toEqual({
      filterType: 'number',
      type: 'greaterThan',
      filter: 10,
    })

    // 2. Test setting a MAXIMUM value after the minimum is already set
    await filterPanel.vm.$emit('filter-by-participants', { type: 'max', value: 50 })
    
    expect(wrapper.vm.membersFilterObject).toEqual({
      filterType: 'number',
      type: 'inRange',
      filter: 10,
      filterTo: 50,
    })
  })

  it('fetches and loads guild data when hitServer is called', async () => {
    const mockGuilds = [{ guildID: 1, name: 'Test Guild 1' }, { guildID: 2, name: 'Test Guild 2' }]
    const response = { data: { AllGuilds: mockGuilds } }
    
    // SETUP MOCK
    axios.get.mockResolvedValue(response)

    // CALL METHOD
    await wrapper.vm.hitServer('all-guilds')

    // ASSERTIONS
    expect(axios.get).toHaveBeenCalledWith(expect.stringContaining('/api/all-guilds'))
    expect(wrapper.vm.allGuildsData).toEqual(mockGuilds)
  })
}) 