// You can declare a mixin as the same style as components.
<script lang="ts">
import { AccessType, Account, SessionStorageKeys } from '@/util/constants'
import { AccountSettings } from '@/models/account-settings'
import Component from 'vue-class-component'
import ConfigHelper from '@/util/config-helper'
import { Organization } from '@/models/Organization'
import Vue from 'vue'
import { mapState } from 'pinia'
import { useOrgStore } from '@/stores/org'
import { useUserStore } from '@/stores/user'
@Component({
  name: 'AccountMixin',
  computed: {
    ...mapState(useUserStore, [
      'currentUser'
    ]),
    ...mapState(useOrgStore, [
      'currentOrganization',
      'currentMembership'
    ])
  }
})
// TODO in the mounted ; do load all the properties if its not loaded already
export default class AccountMixin extends Vue {
  protected readonly currentOrganization!: Organization

  getAccountFromSession (): AccountSettings {
    return JSON.parse(ConfigHelper.getFromSession(SessionStorageKeys.CurrentAccount || '{}'))
  }
  get isPremiumAccount (): boolean {
    return this.currentOrganization?.orgType === Account.PREMIUM
  }
  get isRegularAccount (): boolean {
    return this.currentOrganization?.accessType === AccessType.REGULAR
  }

  get anonAccount (): boolean {
    return this.currentOrganization?.accessType === AccessType.ANONYMOUS
  }

  get isGovmAccount (): boolean {
    return this.currentOrganization?.accessType === AccessType.GOVM
  }

  get isGovnAccount (): boolean {
    return this.currentOrganization?.accessType === AccessType.GOVN
  }

  get isStaffAccount (): boolean {
    return this.currentOrganization?.orgType === Account.STAFF
  }

  get isSbcStaffAccount (): boolean {
    return this.currentOrganization?.orgType === Account.SBC_STAFF
  }

  get isExternalStaffAccount (): boolean {
    return [Account.CONTACT_CENTRE_STAFF, Account.MAXIMUS_STAFF].includes(this.currentOrganization?.orgType)
  }
}
</script>
