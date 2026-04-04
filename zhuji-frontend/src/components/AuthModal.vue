<template>
  <div class="fixed inset-0 z-[100] flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-on-surface/40 backdrop-blur-sm" @click="$emit('close')"></div>
    
    <!-- Scroll Container -->
    <div 
      class="relative w-full max-w-md bg-[#fdfcf8] overflow-hidden shadow-2xl transition-all duration-700 ease-out"
      :class="[isOpen ? 'max-h-[600px] opacity-100' : 'max-h-0 opacity-0']"
    >
      <!-- Scroll Top Handle -->
      <div class="h-8 bg-secondary/10 flex items-center justify-center border-b border-outline-variant/10">
        <div class="w-12 h-1 bg-secondary/20 rounded-full"></div>
      </div>

      <!-- Content -->
      <div class="p-12 text-center">
        <h2 class="font-serif text-4xl text-primary mb-2">筑迹</h2>
        <p class="text-secondary/60 text-sm mb-12 tracking-widest">Digital Inkscroll Community</p>
        
        <div class="space-y-6">
          <div class="space-y-2 text-left">
            <label class="text-xs font-bold text-secondary/40 uppercase tracking-tighter">账号 / 手机号</label>
            <input 
              type="text" 
              class="w-full border-b border-outline-variant py-2 focus:outline-none focus:border-primary transition-colors bg-transparent"
              placeholder="请输入您的账号"
            />
          </div>
          
          <div class="space-y-2 text-left">
            <label class="text-xs font-bold text-secondary/40 uppercase tracking-tighter">密码</label>
            <input 
              type="password" 
              class="w-full border-b border-outline-variant py-2 focus:outline-none focus:border-primary transition-colors bg-transparent"
              placeholder="请输入您的密码"
            />
          </div>
        </div>

        <button 
          class="w-full mt-12 py-4 bg-primary text-white font-bold rounded-lg shadow-lg shadow-primary/20 hover:bg-primary-container transition-all"
          @click="handleLogin"
        >
          开启筑迹之旅
        </button>
        
        <div class="mt-8 flex items-center justify-between text-xs text-secondary/60">
          <a href="#" class="hover:text-primary transition-colors">忘记密码？</a>
          <a href="#" class="hover:text-primary transition-colors">立即注册</a>
        </div>
      </div>

      <!-- Scroll Bottom Handle -->
      <div class="h-8 bg-secondary/10 flex items-center justify-center border-t border-outline-variant/10">
        <div class="w-12 h-1 bg-secondary/20 rounded-full"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

defineEmits(['close']);

const isOpen = ref(false);

onMounted(() => {
  // 模拟卷轴展开动效
  setTimeout(() => {
    isOpen.value = true;
  }, 50);
});

const handleLogin = () => {
  console.log('Login triggered');
  // TODO: 实现真实登录逻辑
};
</script>

<style scoped>
/* 卷轴展开动效 */
.max-h-0 {
  max-height: 0;
}
.max-h-\[600px\] {
  max-height: 600px;
}
</style>
