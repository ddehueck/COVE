<template>
  <div class="logout container">
  </div>
</template>

<script>

import DatasetService from '@/services/DatasetService'
import router from '@/router'

export default {
	name: 'logout',

	methods: {
		async logout () {
			return await DatasetService.logoutUser()
		}
	},

	beforeMount(){
		this.logout().then((response) => {
			this.$store.dispatch('logout')
			router.push({ name: 'home' })
		}).catch((err) => {
			this.$store.dispatch('logout')
			router.push({ name: 'home' })
		})
	},
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">
</style>
