import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import ForumList from '@/views/ForumList.vue';
import PostDetail from '@/views/PostDetail.vue';
import StampDiscovery from '@/views/StampDiscovery.vue';
import CoCreation from '@/views/CoCreation.vue';
import UserProfile from '@/views/UserProfile.vue';
import AdminDashboard from '@/views/AdminDashboard.vue';
import PublishPost from '@/views/PublishPost.vue';
import MonumentArticle from '@/views/MonumentArticle.vue';
import SearchResults from '@/views/SearchResults.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/forum',
    name: 'ForumList',
    component: ForumList,
  },
  {
    path: '/forum/:id',
    name: 'PostDetail',
    component: PostDetail,
  },
  {
    path: '/stamps',
    name: 'StampDiscovery',
    component: StampDiscovery,
  },
  {
    path: '/stamps/article/:monumentId',
    name: 'MonumentArticle',
    component: MonumentArticle,
  },
  {
    path: '/co-creation',
    name: 'CoCreation',
    component: CoCreation,
  },
  {
    path: '/profile',
    name: 'UserProfile',
    component: UserProfile,
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
  },
  {
    path: '/forum/publish',
    name: 'PublishPost',
    component: PublishPost,
  },
  {
    path: '/search',
    name: 'SearchResults',
    component: SearchResults,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

router.beforeEach((to, _from, next) => {
  if (to.name === 'AdminDashboard') {
    const role = localStorage.getItem('user_role');
    if (role !== 'superadmin' && role !== 'moderator') {
      next('/');
      return;
    }
  }
  if (to.name === 'UserProfile') {
    if (!localStorage.getItem('access_token')) {
      next('/');
      return;
    }
  }
  next();
});

export default router;
