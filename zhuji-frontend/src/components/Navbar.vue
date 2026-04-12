<template>
  <nav class="glass-nav fixed top-0 left-0 right-0 z-50 h-20 flex items-center border-b border-outline-variant/10">
    <div class="container mx-auto px-4 flex items-center justify-between">
      <!-- Logo -->
      <div class="flex items-center space-x-2 cursor-pointer" @click="goHome">
        <span class="font-serif text-3xl font-bold text-primary">筑迹</span>
      </div>

      <!-- Links -->
      <div class="hidden md:flex items-center space-x-12 text-secondary font-medium">
        <router-link to="/" class="hover:text-primary transition-colors" active-class="text-primary">首页</router-link>
        <router-link to="/forum" class="hover:text-primary transition-colors" active-class="text-primary">筑匠论坛</router-link>
        <router-link to="/stamps" class="hover:text-primary transition-colors" active-class="text-primary">集章印记</router-link>
        <router-link to="/co-creation" class="hover:text-primary transition-colors" active-class="text-primary">筑品共创</router-link>
      </div>

      <!-- Actions -->
      <div class="flex items-center space-x-6">
        <div class="relative hidden sm:block">
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="搜索古建、帖子、筑品..." 
            class="bg-surface-container-low border border-outline-variant/20 rounded-full py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-primary/40 w-64 transition-all"
            @keyup.enter="doSearch"
          />
          <SearchIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-secondary/40 cursor-pointer" @click="doSearch" />
        </div>
        
        <button
          @click="handleUserClick"
          class="w-10 h-10 rounded-full bg-secondary/10 flex items-center justify-center hover:bg-secondary/20 transition-all relative group"
        >
          <UserIcon class="w-5 h-5 text-secondary group-hover:text-primary transition-colors" />
          <!-- Notification Red Dot -->
          <div class="absolute top-0 right-0 w-2.5 h-2.5 bg-primary rounded-full border-2 border-white"></div>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, inject } from 'vue';
import { useRouter } from 'vue-router';
import { Search as SearchIcon, User as UserIcon } from 'lucide-vue-next';

const router = useRouter();
const toggleAuth = inject<(val: boolean) => void>('toggleAuth');
const searchQuery = ref('');

const doSearch = () => {
  const q = searchQuery.value.trim();
  if (!q) return;
  router.push({ path: '/search', query: { q } });
  searchQuery.value = '';
};

const goHome = () => {
  router.push('/');
};

const navigate = (path: string) => {
  console.log(`Navigating to ${path}`);
  // TODO: 跳转至详情页
  // router.push(`/${path}`);
};

const openAuth = () => {
  if (toggleAuth) toggleAuth(true);
};

const handleUserClick = () => {
  if (localStorage.getItem('access_token')) {
    router.push('/profile');
  } else {
    openAuth();
  }
};
</script>
