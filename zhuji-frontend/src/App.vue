<template>
  <div class="min-h-screen flex flex-col">
    <Navbar />
    <main class="flex-grow">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <!-- 全局登录弹窗 -->
    <AuthModal v-if="showAuth" @close="showAuth = false" />
    
    <footer class="bg-white py-12 border-t border-outline-variant/10">
      <div class="container mx-auto px-4 text-center">
        <h2 class="font-serif text-2xl mb-4">筑迹</h2>
        <div class="flex justify-center space-x-8 text-secondary text-sm mb-8">
          <a href="#" class="hover:text-primary transition-colors">关于我们</a>
          <a href="#" class="hover:text-primary transition-colors">社区准则</a>
          <a href="#" class="hover:text-primary transition-colors">隐私政策</a>
          <a href="#" class="hover:text-primary transition-colors">联系我们</a>
        </div>
        <p class="text-secondary/60 text-xs">© 2024 筑迹古建筑社区. 传承千年匠心.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, provide } from 'vue';
import Navbar from '@/components/Navbar.vue';
import AuthModal from '@/components/AuthModal.vue';

const showAuth = ref(false);

// 提供给子组件控制登录弹窗
provide('toggleAuth', (val: boolean) => {
  showAuth.value = val;
});
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.container {
  max-width: 1280px;
}
</style>
