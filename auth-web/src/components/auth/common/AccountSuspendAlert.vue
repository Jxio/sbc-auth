<template>
  <v-alert
    class="px-8 py-7"
    :icon="false"
    prominent
    type="error"
  >
    <div class="account-alert">
      <div class="account-alert-inner">
        <v-icon
          large
          class="mt-2"
        >
          mdi-alert-circle-outline
        </v-icon>
        <div
          v-if="isSuspendedForNSF"
          class="account-alert__info ml-7"
        >
          <div class="font-weight-bold">
            Account Suspended
          </div>
          <div>
            Account has been suspended for {{ accountSuspendReason }}.
          </div>
          <div class="mt-6 title font-weight-bold">
            BALANCE DUE:  ${{ totalAmountToPay.toFixed(2) }}
          </div>
        </div>
        <div
          v-if="isSuspendedForNSF"
          class="account-alert__date"
        >
          {{ suspendedDate }}
        </div>
        <div
          v-else
          class="d-flex flex-column ml-7"
        >
          <div class="title font-weight-bold">
            Account Suspended ({{ suspendedReason() }})
          </div>
          <div class="d-flex">
            <span>Date Suspended: {{ suspendedDate }}<span class="vertical-line" /> Suspended by: {{ suspendedBy }}</span>
          </div>
        </div>
      </div>
    </div>
  </v-alert>
</template>

<script lang="ts">
import { AccountStatus, SuspensionReasonCode } from '@/util/constants'
import { Action, State } from 'pinia-class'
import { Component, Vue } from 'vue-property-decorator'
import { Code } from '@/models/Code'
import CommonUtils from '@/util/common-util'
import { FailedInvoice } from '@/models/invoice'
import { Organization } from '@/models/Organization'
import { useCodesStore } from '@/stores/codes'
import { useOrgStore } from '@/stores/org'

@Component
export default class AccountSuspendAlert extends Vue {
  @Action(useOrgStore) private calculateFailedInvoices!: () => FailedInvoice
  @State(useOrgStore) private currentOrganization!: Organization
  @State(useCodesStore) private suspensionReasonCodes!: Code[]
  private formatDate = CommonUtils.formatDisplayDate

  totalTransactionAmount = 0
  totalAmountToPay = 0
  totalPaidAmount = 0

  get suspendedDate () {
    return (this.currentOrganization?.suspendedOn)
      ? this.formatDate(new Date(this.currentOrganization.suspendedOn)) : ''
  }

  get isSuspendedForNSF (): boolean {
    return this.currentOrganization?.statusCode === AccountStatus.NSF_SUSPENDED
  }

  get suspendedBy (): string {
    return this.currentOrganization?.decisionMadeBy
  }

  get accountSuspendReason (): string {
    if (this.currentOrganization?.suspensionReasonCode === SuspensionReasonCode.OVERDUE_EFT) {
      return 'overdue EFT payments'
    }
    return 'outstanding balance (NSF)'
  }

  suspendedReason (): string {
    return this.suspensionReasonCodes?.find(suspensionReasonCode =>
      suspensionReasonCode?.code === this.currentOrganization?.suspensionReasonCode)?.desc
  }

  async mounted () {
    if (this.isSuspendedForNSF) {
      const failedInvoices: FailedInvoice = await this.calculateFailedInvoices()
      this.totalTransactionAmount = failedInvoices.totalTransactionAmount || 0
      this.totalAmountToPay = failedInvoices.totalAmountToPay || 0
    }
  }
}
</script>

<style lang="scss" scoped>
  .account-alert-inner {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
  }

  .account-alert__info {
    flex: 1 1 auto;
  }

  .account-alert__date {
    flex: 0 0 auto;
  }

  .vertical-line {
  margin: 0 2em;
  border-left: solid;
  border-width: 0.125em;
  }

</style>
