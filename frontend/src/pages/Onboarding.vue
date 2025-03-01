<template>
  <div class="flex h-full flex-col items-center bg-gray-100 pt-10">
    <span
      class="select-none text-3xl font-black uppercase tracking-[0.5em] text-gray-900"
    >
      Gameplan
    </span>
    <div class="min mt-7 min-w-[36rem] rounded-lg bg-white p-9 shadow-md">
      <div
        v-if="$resources.onboarding.loading"
        class="flex items-center justify-center"
      >
        <LoadingIndicator class="h-4 w-4 text-gray-600" />
        <span class="ml-2 text-base text-gray-900">
          Setting up your team and project
        </span>
      </div>
      <div v-if="!$resources.onboarding.loading">
        <div class="flex items-baseline justify-between">
          <h2 class="text-2xl font-bold text-gray-900">
            {{ activeStep.title }}
          </h2>
          <span class="text-sm text-gray-600">
            Step {{ activeStepIndex + 1 }} of {{ steps.length }}
          </span>
        </div>
        <div class="mt-3.5 flex w-full gap-2">
          <div
            class="h-[2px] w-full transition-colors"
            :class="i <= activeStepIndex ? 'bg-blue-500' : 'bg-gray-200'"
            v-for="(step, i) in steps"
          ></div>
        </div>
        <div class="mt-6">
          <component
            v-if="activeStep.component"
            :is="activeStep.component"
            v-model="data"
          />
        </div>
        <ErrorMessage class="mt-2" :message="$resources.onboarding.error" />
        <div class="mt-10 flex items-center justify-between">
          <Button v-show="activeStepIndex > 0" @click="prevStep">
            Previous
          </Button>
          <Button
            class="ml-auto"
            v-show="activeStepIndex < steps.length - 1"
            appearance="primary"
            @click="nextStep"
          >
            Next
          </Button>
          <Button
            v-show="activeStepIndex === steps.length - 1"
            appearance="primary"
            @click="completeSetup"
          >
            Complete Setup
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { Input, LoadingIndicator, ErrorMessage } from 'frappe-ui'
import OnboardingStepTeam from './OnboardingStepTeam.vue'
import OnboardingStepProject from './OnboardingStepProject.vue'
import OnboardingStepInvites from './OnboardingStepInvites.vue'
import { teams } from '@/data/teams'
import { projects } from '@/data/projects'

export default {
  name: 'Onboarding',
  components: { Input, LoadingIndicator, ErrorMessage },
  resources: {
    onboarding: {
      url: 'gameplan.api.onboarding',
      makeParams() {
        return {
          data: this.data,
        }
      },
      validate() {
        if (!this.data.team) {
          return 'Please select a team'
        }
        if (!this.data.project) {
          return 'Please select a project'
        }
        if (this.data.emails.filter(Boolean).length === 0) {
          return 'Please enter at least one email'
        }
      },
      onSuccess(teamId) {
        teams.reload()
        projects.reload()
        this.$router.push({ name: 'Team', params: { teamId } })
      },
    },
  },
  data() {
    return {
      data: {
        team: null,
        project: null,
        emails: ['', '', ''],
      },
      activeStepIndex: 0,
    }
  },
  computed: {
    steps() {
      return [
        {
          name: 'Team',
          title: 'Which team are you a part of?',
          component: OnboardingStepTeam,
          isCompleted: Boolean(this.data.team),
        },
        {
          name: 'Project',
          title: 'Which project are you working on?',
          component: OnboardingStepProject,
          isCompleted: Boolean(this.data.project),
        },
        {
          name: 'Invite',
          title: 'Invite people you work with',
          component: OnboardingStepInvites,
          isCompleted: this.data.emails.filter(Boolean).length > 0,
        },
      ]
    },
    activeStep() {
      return this.steps[this.activeStepIndex]
    },
  },
  methods: {
    nextStep() {
      if (this.activeStep.isCompleted) {
        this.activeStepIndex++
      }
      if (this.activeStepIndex > this.steps.length - 1) {
        this.activeStepIndex = this.steps.length - 1
      }
    },
    prevStep() {
      this.activeStepIndex--
      if (this.activeStepIndex < 0) {
        this.activeStepIndex = 0
      }
    },
    completeSetup() {
      this.$resources.onboarding.submit()
    },
  },
}
</script>
