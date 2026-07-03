<template>
  <v-container class="vendor-connections-container">
<div class="view-header flex-column mb-3">
      <h2
        class="view-header__title"
        data-test="vendor-connections-title"
      >
        {{ $t('thirdPartyConnectionsTitle') }}
      </h2>
      <p class="mt-3 payment-page-sub">
        {{ $t('thirdPartyConnectionsSubtitle') }}
      </p>
    </div>
    <ThirdPartyConnectionsTable />
  </v-container>
</template>

<script lang="ts">
import { defineComponent, onMounted } from '@vue/composition-api'
import { Pages } from '@/util/constants'
import ThirdPartyConnectionsTable from '@/components/auth/account-settings/advance-settings/ThirdPartyConnectionsTable.vue'
import { canViewThirdPartyConnections } from '@/util/third-party-connection-util'
import { useOrgStore } from '@/stores/org'
import { useUserStore } from '@/stores/user'

export default defineComponent({
  name: 'ThirdPartyConnections',
  components: {
    ThirdPartyConnectionsTable
  },
  setup (_, { root }) {
    const orgStore = useOrgStore()
    const userStore = useUserStore()

    onMounted(() => {
      if (!canViewThirdPartyConnections(
        orgStore.currentMembership?.membershipTypeCode,
        userStore.currentUser?.roles
      )) {
        root.$router.push(`/${Pages.MAIN}/${orgStore.currentOrganization?.id}/settings/account-info`)
      }
    })
  }
})
</script>

<style lang="scss" scoped>
.view-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
</style>
