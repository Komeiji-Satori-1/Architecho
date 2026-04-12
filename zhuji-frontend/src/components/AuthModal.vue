<template>
  <div class="fixed inset-0 z-[100] flex items-center justify-center p-4">
    <div class="absolute inset-0 bg-on-surface/40 backdrop-blur-sm" @click="$emit('close')"></div>
    
    <div 
      class="relative w-full max-w-md bg-[#fdfcf8] overflow-hidden shadow-2xl transition-all duration-700 ease-out"
      :class="[isOpen ? 'max-h-[700px] opacity-100' : 'max-h-0 opacity-0']"
    >
      <div class="h-8 bg-secondary/10 flex items-center justify-center border-b border-outline-variant/10">
        <div class="w-12 h-1 bg-secondary/20 rounded-full"></div>
      </div>

      <div class="p-12 text-center">
        <h2 class="font-serif text-4xl text-primary mb-2">筑迹</h2>
        <p class="text-secondary/60 text-sm mb-12 tracking-widest">Digital Inkscroll Community</p>
        
        <div class="space-y-6">
          <div class="space-y-2 text-left">
            <label class="text-xs font-bold text-secondary/40 uppercase tracking-tighter">账号</label>
            <input 
              type="text" v-model="username"
              class="w-full border-b border-outline-variant py-2 focus:outline-none focus:border-primary transition-colors bg-transparent"
              placeholder="请输入您的账号"
            />
          </div>
          <div class="space-y-2 text-left">
            <label class="text-xs font-bold text-secondary/40 uppercase tracking-tighter">密码</label>
            <input 
              type="password" v-model="password"
              class="w-full border-b border-outline-variant py-2 focus:outline-none focus:border-primary transition-colors bg-transparent"
              placeholder="请输入您的密码"
            />
          </div>
          <!-- 注册时才显示确认密码 -->
          <div v-if="mode === 'register'" class="space-y-2 text-left">
            <label class="text-xs font-bold text-secondary/40 uppercase tracking-tighter">确认密码</label>
            <input 
              type="password" v-model="passwordConfirm"
              class="w-full border-b border-outline-variant py-2 focus:outline-none focus:border-primary transition-colors bg-transparent"
              placeholder="请再次输入密码"
            />
          </div>
        </div>

        <p v-if="errorMsg" class="mt-4 text-xs text-red-500">{{ errorMsg }}</p>

        <button 
          class="w-full mt-12 py-4 bg-primary text-white font-bold rounded-lg shadow-lg shadow-primary/20 hover:bg-primary-container transition-all"
          @click="mode === 'login' ? handleLogin() : handleRegister()"
        >
          {{ mode === 'login' ? '开启筑迹之旅' : '加入筑迹' }}
        </button>
        
        <div class="mt-8 flex items-center justify-between text-xs text-secondary/60">
          <a href="#" class="hover:text-primary transition-colors" @click.prevent>忘记密码？</a>
          <a href="#" class="hover:text-primary transition-colors" @click.prevent="toggleMode">
            {{ mode === 'login' ? '立即注册' : '已有账号？去登录' }}
          </a>
        </div>
      </div>

      <div class="h-8 bg-secondary/10 flex items-center justify-center border-t border-outline-variant/10">
        <div class="w-12 h-1 bg-secondary/20 rounded-full"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import service from '@/api/request';

const emit = defineEmits(['close']);

const isOpen = ref(false);
const mode = ref<'login' | 'register'>('login');
const username = ref('');
const password = ref('');
const passwordConfirm = ref('');
const errorMsg = ref('');
onMounted(() => {
  setTimeout(() => {
    isOpen.value = true;
  }, 50);
});
const toggleMode = () => {
  mode.value = mode.value === 'login' ? 'register' : 'login';
  errorMsg.value = '';
  password.value = '';
  passwordConfirm.value = '';
};
const handleLogin = async () => {
  try {
    const response = await service.post('/users/login/', {
      username: username.value,
      password: password.value,
    });
    localStorage.setItem('access_token', response.access);
    localStorage.setItem('refresh_token', response.refresh);
    localStorage.setItem('user_role', response.user?.role || 'user');
    emit('close');
    window.location.reload();
  } catch {
    alert('账号或密码错误，请重新输入');
  }
};
const handleRegister = async () => {
  errorMsg.value = '';
  try {
    const res = await service.post('/users/register/', {
      username: username.value,
      password: password.value,
      password_confirm: passwordConfirm.value,
    });
    localStorage.setItem('access_token', res.access);
    localStorage.setItem('refresh_token', res.refresh);
    localStorage.setItem('user_role', res.user?.role || 'user');
    emit('close');
    window.location.reload();
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || '注册失败，请稍后重试';
  }
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

