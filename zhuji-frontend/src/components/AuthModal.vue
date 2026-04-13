<template>
  <div class="fixed inset-0 z-[100] flex items-center justify-center p-4">
    <div class="absolute inset-0 bg-on-surface/40 backdrop-blur-sm" @click="$emit('close')"></div>
    
    <div 
      class="relative w-full max-w-md bg-[#fdfcf8] overflow-hidden shadow-2xl transition-all duration-700 ease-out"
      :class="[isOpen ? 'max-h-[800px] opacity-100' : 'max-h-0 opacity-0']"
    >
      <div class="h-8 bg-secondary/10 flex items-center justify-center border-b border-outline-variant/10">
        <div class="w-12 h-1 bg-secondary/20 rounded-full"></div>
      </div>

      <div class="p-12 text-center">
        <h2 class="font-serif text-4xl text-primary mb-2">筑迹</h2>
        <p class="text-secondary/60 text-sm mb-12 tracking-widest">Digital Inkscroll Community</p>
        
        <!-- Login / Register Form -->
        <template v-if="mode === 'login' || mode === 'register'">
          <div class="space-y-6">
            <div class="space-y-2 text-left">
              <label class="text-xs font-bold text-secondary/40 uppercase tracking-tighter">账号</label>
              <input 
                type="text" v-model="username"
                class="w-full border-b border-outline-variant py-2 focus:outline-none focus:border-primary transition-colors bg-transparent"
                placeholder="请输入您的账号"
              />
            </div>
            <div v-if="mode === 'register'" class="space-y-2 text-left">
              <label class="text-xs font-bold text-secondary/40 uppercase tracking-tighter">邮箱（用于找回密码）</label>
              <input 
                type="email" v-model="email"
                class="w-full border-b border-outline-variant py-2 focus:outline-none focus:border-primary transition-colors bg-transparent"
                placeholder="请输入您的邮箱"
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
          <p v-if="successMsg" class="mt-4 text-xs text-green-600">{{ successMsg }}</p>

          <button 
            class="w-full mt-12 py-4 bg-primary text-white font-bold rounded-lg shadow-lg shadow-primary/20 hover:bg-primary-container transition-all disabled:opacity-60"
            :disabled="loading"
            @click="mode === 'login' ? handleLogin() : handleRegister()"
          >
            {{ loading ? '处理中...' : (mode === 'login' ? '开启筑迹之旅' : '加入筑迹') }}
          </button>
          
          <div class="mt-8 flex items-center justify-between text-xs text-secondary/60">
            <a href="#" class="hover:text-primary transition-colors" @click.prevent="mode = 'forgot-email'">忘记密码？</a>
            <a href="#" class="hover:text-primary transition-colors" @click.prevent="toggleMode">
              {{ mode === 'login' ? '立即注册' : '已有账号？去登录' }}
            </a>
          </div>
        </template>

        <!-- Forgot Password Step 1: Enter Email -->
        <template v-if="mode === 'forgot-email'">
          <div class="space-y-6">
            <p class="text-sm text-secondary/60 mb-4">请输入您注册时使用的邮箱，我们将发送验证码。</p>
            <div class="space-y-2 text-left">
              <label class="text-xs font-bold text-secondary/40 uppercase tracking-tighter">邮箱</label>
              <input 
                type="email" v-model="forgotEmail"
                class="w-full border-b border-outline-variant py-2 focus:outline-none focus:border-primary transition-colors bg-transparent"
                placeholder="请输入注册邮箱"
              />
            </div>
          </div>

          <p v-if="errorMsg" class="mt-4 text-xs text-red-500">{{ errorMsg }}</p>
          <p v-if="successMsg" class="mt-4 text-xs text-green-600">{{ successMsg }}</p>

          <button 
            class="w-full mt-12 py-4 bg-primary text-white font-bold rounded-lg shadow-lg shadow-primary/20 hover:bg-primary-container transition-all disabled:opacity-60"
            :disabled="loading || cooldown > 0"
            @click="handleRequestCode"
          >
            {{ loading ? '发送中...' : (cooldown > 0 ? `${cooldown}s 后可重发` : '获取验证码') }}
          </button>
          
          <div class="mt-8 text-xs text-secondary/60">
            <a href="#" class="hover:text-primary transition-colors" @click.prevent="backToLogin">← 返回登录</a>
          </div>
        </template>

        <!-- Forgot Password Step 2: Enter Code + New Password -->
        <template v-if="mode === 'forgot-reset'">
          <div class="space-y-6">
            <p class="text-sm text-secondary/60 mb-4">验证码已发送至 <span class="text-primary font-bold">{{ forgotEmail }}</span></p>
            <div class="space-y-2 text-left">
              <label class="text-xs font-bold text-secondary/40 uppercase tracking-tighter">验证码</label>
              <input 
                type="text" v-model="verifyCode" maxlength="6"
                class="w-full border-b border-outline-variant py-2 focus:outline-none focus:border-primary transition-colors bg-transparent text-center text-2xl tracking-[0.5em] font-mono"
                placeholder="000000"
              />
            </div>
            <div class="space-y-2 text-left">
              <label class="text-xs font-bold text-secondary/40 uppercase tracking-tighter">新密码</label>
              <input 
                type="password" v-model="newPassword"
                class="w-full border-b border-outline-variant py-2 focus:outline-none focus:border-primary transition-colors bg-transparent"
                placeholder="请输入新密码（至少6位）"
              />
            </div>
            <div class="space-y-2 text-left">
              <label class="text-xs font-bold text-secondary/40 uppercase tracking-tighter">确认新密码</label>
              <input 
                type="password" v-model="newPasswordConfirm"
                class="w-full border-b border-outline-variant py-2 focus:outline-none focus:border-primary transition-colors bg-transparent"
                placeholder="请再次输入新密码"
              />
            </div>
          </div>

          <p v-if="errorMsg" class="mt-4 text-xs text-red-500">{{ errorMsg }}</p>
          <p v-if="successMsg" class="mt-4 text-xs text-green-600">{{ successMsg }}</p>

          <button 
            class="w-full mt-12 py-4 bg-primary text-white font-bold rounded-lg shadow-lg shadow-primary/20 hover:bg-primary-container transition-all disabled:opacity-60"
            :disabled="loading"
            @click="handleResetPassword"
          >
            {{ loading ? '提交中...' : '重置密码' }}
          </button>
          
          <div class="mt-8 flex items-center justify-between text-xs text-secondary/60">
            <a href="#" class="hover:text-primary transition-colors" @click.prevent="mode = 'forgot-email'">← 重新获取</a>
            <a href="#" class="hover:text-primary transition-colors" @click.prevent="backToLogin">返回登录</a>
          </div>
        </template>
      </div>

      <div class="h-8 bg-secondary/10 flex items-center justify-center border-t border-outline-variant/10">
        <div class="w-12 h-1 bg-secondary/20 rounded-full"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import service from '@/api/request';

const emit = defineEmits(['close']);

const isOpen = ref(false);
const mode = ref<'login' | 'register' | 'forgot-email' | 'forgot-reset'>('login');
const username = ref('');
const email = ref('');
const password = ref('');
const passwordConfirm = ref('');
const errorMsg = ref('');
const successMsg = ref('');
const loading = ref(false);

// Forgot password state
const forgotEmail = ref('');
const verifyCode = ref('');
const newPassword = ref('');
const newPasswordConfirm = ref('');
const cooldown = ref(0);
let cooldownTimer: ReturnType<typeof setInterval> | null = null;

onMounted(() => {
  setTimeout(() => { isOpen.value = true; }, 50);
});

onUnmounted(() => {
  if (cooldownTimer) clearInterval(cooldownTimer);
});

/** SHA-256 哈希：浏览器原生 Web Crypto API */
async function sha256(message: string): Promise<string> {
  const data = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

const clearMessages = () => { errorMsg.value = ''; successMsg.value = ''; };

const toggleMode = () => {
  mode.value = mode.value === 'login' ? 'register' : 'login';
  clearMessages();
  password.value = '';
  passwordConfirm.value = '';
};

const backToLogin = () => {
  mode.value = 'login';
  clearMessages();
  forgotEmail.value = '';
  verifyCode.value = '';
  newPassword.value = '';
  newPasswordConfirm.value = '';
};

const handleLogin = async () => {
  clearMessages();
  if (!username.value || !password.value) {
    errorMsg.value = '请填写账号和密码';
    return;
  }
  loading.value = true;
  try {
    const hashedPwd = await sha256(password.value);
    const response: any = await service.post('/users/login/', {
      username: username.value,
      password: hashedPwd,
    });
    localStorage.setItem('access_token', response.access);
    localStorage.setItem('refresh_token', response.refresh);
    localStorage.setItem('user_role', response.user?.role || 'user');
    emit('close');
    window.location.reload();
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || '账号或密码错误，请重新输入';
  } finally {
    loading.value = false;
  }
};

const handleRegister = async () => {
  clearMessages();
  if (!username.value || !password.value) {
    errorMsg.value = '请填写账号和密码';
    return;
  }
  if (password.value !== passwordConfirm.value) {
    errorMsg.value = '两次密码输入不一致';
    return;
  }
  if (password.value.length < 6) {
    errorMsg.value = '密码长度不能少于6位';
    return;
  }
  loading.value = true;
  try {
    const hashedPwd = await sha256(password.value);
    const res: any = await service.post('/users/register/', {
      username: username.value,
      email: email.value,
      password: hashedPwd,
      password_confirm: hashedPwd,
    });
    localStorage.setItem('access_token', res.access);
    localStorage.setItem('refresh_token', res.refresh);
    localStorage.setItem('user_role', res.user?.role || 'user');
    emit('close');
    window.location.reload();
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || '注册失败，请稍后重试';
  } finally {
    loading.value = false;
  }
};

const startCooldown = () => {
  cooldown.value = 60;
  cooldownTimer = setInterval(() => {
    cooldown.value--;
    if (cooldown.value <= 0 && cooldownTimer) {
      clearInterval(cooldownTimer);
      cooldownTimer = null;
    }
  }, 1000);
};

const handleRequestCode = async () => {
  clearMessages();
  if (!forgotEmail.value) {
    errorMsg.value = '请填写邮箱地址';
    return;
  }
  loading.value = true;
  try {
    const res: any = await service.post('/users/forgot-password/request/', {
      email: forgotEmail.value,
    });
    successMsg.value = res.detail || '验证码已发送至您的邮箱';
    startCooldown();
    mode.value = 'forgot-reset';
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || '发送失败，请检查邮箱是否正确';
  } finally {
    loading.value = false;
  }
};

const handleResetPassword = async () => {
  clearMessages();
  if (!verifyCode.value || !newPassword.value) {
    errorMsg.value = '请填写验证码和新密码';
    return;
  }
  if (newPassword.value !== newPasswordConfirm.value) {
    errorMsg.value = '两次密码输入不一致';
    return;
  }
  if (newPassword.value.length < 6) {
    errorMsg.value = '密码长度不能少于6位';
    return;
  }
  loading.value = true;
  try {
    const hashedPwd = await sha256(newPassword.value);
    const res: any = await service.post('/users/forgot-password/reset/', {
      email: forgotEmail.value,
      code: verifyCode.value,
      new_password: hashedPwd,
    });
    successMsg.value = res.detail || '密码重置成功！';
    setTimeout(() => { backToLogin(); }, 1500);
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || '重置失败，请检查验证码';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.max-h-0 {
  max-height: 0;
}
.max-h-\[800px\] {
  max-height: 800px;
}
</style>

