<template>
  <div>
    <h1 class="sr-only">Homescreen</h1>
    <div class="mx-auto h-full max-w-4xl sm:px-5">
      <div class="pt-8 pb-6">
        <button
          @click="showCommandPalette"
          class="w-full rounded-md focus:outline-none focus:ring-1"
        >
          <Input
            :placeholder="searchPlaceholder"
            icon-left="search"
            class="cursor-pointer"
            :disabled="true"
          />
        </button>
      </div>
      <section class="space-y-2">
        <h2 class="text-2xl font-semibold text-gray-900">Recently visited</h2>
        <div class="grid grid-cols-3 gap-2">
          <router-link
            class="group block rounded-lg border px-3 py-2 hover:bg-gray-100"
            :to="{
              name: 'Project',
              params: { projectId: d.project, teamId: d.team },
            }"
            v-for="d in $resources.recentProjects.data"
            :key="d.project"
          >
            <div class="flex items-center justify-between">
              <span
                class="text-sm font-semibold uppercase tracking-wide text-gray-600/90"
              >
                {{ d.team_title }}
              </span>
              <Button
                class="opacity-0 transition-opacity group-hover:opacity-100"
                appearance="minimal"
              >
                <Pin class="-mx-2 h-4 w-4" />
              </Button>
            </div>
            <div class="mt-2 flex items-center gap-2">
              <span class="text-xl">{{ d.icon }}</span>
              <span class="text-lg font-medium text-gray-900">
                {{ d.title }}
              </span>
            </div>
          </router-link>
        </div>
      </section>
    </div>
  </div>
</template>
<script>
import Pin from '@/components/icons/Pin.vue'
import { getPlatform } from '@/utils'
import { showCommandPalette } from '@/components/CommandPalette.vue'

export default {
  name: 'Homescreen',
  components: {
    Pin,
  },
  resources: {
    recentProjects: {
      url: 'gameplan.api.recent_projects',
      auto: true,
    },
  },
  setup() {
    return {
      showCommandPalette,
    }
  },
  computed: {
    searchPlaceholder() {
      let platform = getPlatform()
      if (platform == 'mac') {
        return 'Jump to project or team (⌘+K)'
      }
      return 'Jump to project or team (Ctrl+K)'
    },
  },
}
</script>
