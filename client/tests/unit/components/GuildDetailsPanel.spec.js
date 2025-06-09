import { mount } from '@vue/test-utils'
import GuildDetailsPanel from '@/components/GuildDetailsPanel.vue'

describe('GuildDetailsPanel.vue', () => {
  let wrapper;

  const mockGuild = {
    name: 'Test Guild',
    tag: 'TEST',
    race: 'Human',
    master: 'Test Master',
    members: 10,
    totalPoints: 1000,
    avgPoints: 100,
    description: 'A test description.',
    lieutenants: ['Lieu 1', 'Lieu 2'],
    guildMembers: ['Mem 1', 'Mem 2'],
    bannerDisplayTemplate: '<div>Banner</div>'
  }

  beforeEach(() => {
    wrapper = mount(GuildDetailsPanel, {
      props: {
        selectedGuild: mockGuild
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

  it('emits close-details-panel event when close button is clicked', async () => {
    const closeButton = wrapper.find('button.delete')
    await closeButton.trigger('click')

    expect(wrapper.emitted('close-details-panel')).toHaveLength(1)
  })
}) 