import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import store from '@/store'
import routerGuards from '@/utils/router-guards';

Vue.use(Router)

export default new Router({
	mode: 'history',
	base: process.env.BASE_URL,
	routes: [
		{
			path: '/',
			name: 'home',
			component: Home
		},
		{
			path: '/login',
			name: 'login',
			component: () => import('./views/Login.vue')
		},
		{
			path: '/register',
			name: 'register',
			component: () => import('./views/Register.vue')
		},
		{
			path: '/logout',
			name: 'logout',
			component: () => import('./views/Logout.vue')
		},
		{
			path: '/users/me',
			name: 'usersPage',
			component: () => import('./views/UsersPage.vue'),
			beforeEnter: (to, from, next) => { routerGuards.isLoggedInGuard(to, from, next) }
		},
		{
			path: '/datasets/create',
			name: 'createDataset',
			component: () => import('./views/CreateDataset.vue'),
			beforeEnter: (to, from, next) => { routerGuards.isLoggedInGuard(to, from, next) }
		},
		{
			path: '/datasets/:id',
			name: 'dataset',
			component: () => import('./views/Dataset.vue')
		},
		{
			path: '/datasets/:id/admin-edit-request',
			name: 'editRequestForm',
			component: () => import('./views/EditRequestForm.vue'),
			beforeEnter: (to, from, next) => { routerGuards.isAdminGuard(to, from, next) }
		},
		{
			path: '/datasets/:id/edit',
			name: 'editDataset',
			component: () => import('./views/EditDataset.vue'),
		},
		{
			path: '/datasets/:id/edit/messages',
			name: 'editDatasetMessages',
			component: () => import('./views/EditDatasetMessages.vue'),
		},
		{
			path: '/admin/confirm-datasets',
			name: 'adminConfirmDatasets',
			component: () => import('./views/admin/ConfirmDatasets.vue'),
			beforeEnter: (to, from, next) => { routerGuards.isAdminGuard(to, from, next) }
		},
		{
			path: '/admin/open-edit-requests',
			name: 'adminOpenEditRequests',
			component: () => import('./views/admin/OpenEditRequests.vue'),
			beforeEnter: (to, from, next) => { routerGuards.isAdminGuard(to, from, next) }
		},

	]
})
