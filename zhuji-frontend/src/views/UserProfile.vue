<template>
  <div class="pt-24 pb-24 bg-surface min-h-screen">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        <!-- Left Sidebar: Navigation -->
        <div class="lg:col-span-3">
          <div class="bg-white rounded-3xl p-8 border border-outline-variant/10 shadow-sm sticky top-24">
            <div class="mb-12">
              <h2 class="font-serif text-3xl text-on-surface mb-1">匠心馆</h2>
              <p class="text-[10px] text-secondary/40 font-bold uppercase tracking-widest">User Pavilion</p>
            </div>

            <nav class="space-y-2">
              <button 
                v-for="item in menuItems" 
                :key="item.id"
                @click="activeSection = item.id"
                class="w-full flex items-center justify-between px-6 py-4 rounded-2xl transition-all group"
                :class="activeSection === item.id ? 'bg-primary/5 text-primary' : 'text-secondary/60 hover:bg-surface hover:text-secondary'"
              >
                <div class="flex items-center">
                  <component :is="item.icon" class="w-5 h-5 mr-4" />
                  <span class="font-bold text-sm">{{ item.name }}</span>
                </div>
                <div v-if="item.hasBadge" class="w-2 h-2 bg-primary rounded-full"></div>
              </button>
            </nav>

            <div class="mt-12 pt-12 border-t border-outline-variant/10">
              <div class="bg-surface rounded-2xl p-6 text-center">
                <p class="text-[10px] text-secondary/40 font-bold uppercase mb-2">当前等级</p>
                <div class="inline-block px-4 py-1 bg-tertiary text-white text-xs font-bold rounded">{{ levelLabel }}</div>
              </div>
              <div class="mt-4">
              <button 
                @click="handleLogout"
                class="w-full flex items-center justify-center px-6 py-4 rounded-2xl border border-error/20 text-error hover:bg-error/5 transition-all group"
              >
                <LogOutIcon class="w-5 h-5 mr-3 group-hover:-translate-x-1 transition-transform" />
                <span class="font-bold text-sm">退出筑迹之旅</span>
              </button>
            </div>
            </div>
            
          </div>
        </div>

        <!-- Right Content Area -->
        <div class="lg:col-span-9 space-y-8">
          
          <!-- Section: Dashboard -->
          <div v-if="activeSection === 'dashboard'" class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Accuracy Card -->
            <div class="bg-white rounded-3xl p-10 border border-outline-variant/10 shadow-sm flex flex-col items-center text-center">
              <h3 class="font-serif text-xl mb-8">答题正确率</h3>
              <div class="relative w-48 h-48 mb-8">
                <svg viewBox="0 0 100 100" class="w-full h-full transform -rotate-90">
                  <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="8" class="text-secondary/5" />
                  <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="8" :stroke-dasharray="282.7" :stroke-dashoffset="quizAccuracyOffset" class="text-primary" />
                </svg>
                <div class="absolute inset-0 flex flex-col items-center justify-center">
                  <span class="text-4xl font-serif text-on-surface">{{ Math.round(quizAccuracy) }}%</span>
                  <span class="text-[10px] text-secondary/40 font-bold uppercase">Accuracy</span>
                </div>
              </div>
              <p class="text-xs text-secondary/60 leading-relaxed">
                在 {{ quizTotalCount }} 个古建知识点中<br />您已领先 92% 的营造师
              </p>
            </div>

            <!-- Footprint Card -->
            <div class="bg-white rounded-3xl p-10 border border-outline-variant/10 shadow-sm">
              <div class="flex justify-between items-end mb-8">
                <div>
                  <h3 class="font-serif text-xl mb-1">探索足迹</h3>
                  <p class="text-[10px] text-secondary/40 font-bold">各类型古建筑探访分布</p>
                </div>
                <div class="text-right">
                  <span class="text-3xl font-serif text-on-surface">{{ footprintCount }}</span>
                  <span class="text-sm text-secondary/40">/150</span>
                </div>
              </div>
              
              <div class="space-y-6 mb-8">
                <div v-for="stat in footprintStats" :key="stat.label">
                  <div class="flex justify-between text-[10px] font-bold text-secondary/60 uppercase mb-2">
                    <span>{{ stat.label }}</span>
                    <span>{{ stat.percent }}%</span>
                  </div>
                  <div class="w-full h-1.5 bg-secondary/5 rounded-full overflow-hidden">
                    <div class="h-full bg-primary" :style="{ width: stat.percent + '%' }"></div>
                  </div>
                </div>
              </div>

              <div v-if="footprintMonuments.length > 0">
                <p class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest mb-4">已探访古建</p>
                <div class="flex flex-wrap gap-2">
                  <div
                    v-for="m in footprintMonuments"
                    :key="m.id"
                    class="flex items-center gap-2 px-3 py-1.5 bg-surface rounded-xl border border-outline-variant/10"
                  >
                    <img v-if="m.cover" :src="m.cover" class="w-5 h-5 rounded object-cover flex-shrink-0" />
                    <div v-else class="w-5 h-5 rounded bg-secondary/10 flex-shrink-0"></div>
                    <div>
                      <p class="text-[11px] font-bold text-on-surface leading-none">{{ m.name }}</p>
                      <p v-if="m.location" class="text-[9px] text-secondary/40 mt-0.5">{{ m.location }}</p>
                    </div>
                  </div>
                </div>
              </div>
              <p v-else class="text-[10px] text-secondary/30 text-center py-4">暂无足迹，去探访古建或作答题目吧</p>
            </div>
          </div>

          <!-- Section: Stamps -->
          <div v-if="activeSection === 'stamps'" class="bg-white rounded-3xl p-10 border border-outline-variant/10 shadow-sm">
            <div class="flex items-center justify-between mb-12">
              <h3 class="font-serif text-2xl flex items-center">
                <LayoutGridIcon class="w-6 h-6 mr-4 text-primary" /> 虚拟印章册
              </h3>
              <button class="text-xs font-bold text-secondary/40 hover:text-primary transition-colors flex items-center">
                查看完整图册 <ChevronRightIcon class="ml-1 w-4 h-4" />
              </button>
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6">
              <div v-for="stamp in stamps" :key="stamp.id" class="group">
                <div 
                  class="aspect-square rounded-2xl mb-4 flex items-center justify-center transition-all duration-500"
                  :class="stamp.unlocked ? 'bg-surface shadow-inner group-hover:shadow-lg' : 'bg-surface/50 border border-dashed border-outline-variant/20'"
                >
                  <img v-if="stamp.unlocked" :src="stamp.image" class="w-2/3 h-2/3 object-contain grayscale group-hover:grayscale-0 transition-all" referrerpolicy="no-referrer" />
                  <LockIcon v-else class="w-6 h-6 text-secondary/10" />
                </div>
                <p class="text-center text-[10px] font-bold" :class="stamp.unlocked ? 'text-secondary' : 'text-secondary/20'">
                  {{ stamp.unlocked ? stamp.name : '待解锁' }}
                </p>
              </div>
            </div>
          </div>

          <!-- Section: Messages -->
          <div v-if="activeSection === 'messages'" class="bg-white rounded-3xl p-10 border border-outline-variant/10 shadow-sm">
            <h3 class="font-serif text-2xl mb-12 flex items-center">
              <MailIcon class="w-6 h-6 mr-4 text-primary" /> 消息中心
            </h3>

            <div class="space-y-6">
              <div 
                v-for="msg in messages" 
                :key="msg.id"
                class="flex items-start p-6 rounded-2xl transition-colors hover:bg-surface group relative"
              >
                <div v-if="msg.unread" class="absolute top-6 left-2 w-1.5 h-1.5 bg-primary rounded-full"></div>
                <div class="w-12 h-12 rounded-xl flex items-center justify-center mr-6" :class="msg.typeBg">
                  <component :is="msg.icon" class="w-5 h-5" :class="msg.typeColor" />
                </div>
                <div class="flex-grow">
                  <div class="flex justify-between items-start mb-2">
                    <h4 class="font-bold text-sm text-on-surface">{{ msg.title }}</h4>
                    <span class="text-[10px] text-secondary/40">{{ msg.time }}</span>
                  </div>
                  <p class="text-xs text-secondary/60 leading-relaxed">{{ msg.content }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Section: Rewards -->
          <div v-if="activeSection === 'rewards'" class="bg-white rounded-3xl p-10 border border-outline-variant/10 shadow-sm">
            <h3 class="font-serif text-2xl mb-12 flex items-center">
              <GiftIcon class="w-6 h-6 mr-4 text-primary" /> 我的奖励
            </h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div v-for="reward in rewards" :key="reward.id" class="p-6 border border-outline-variant/10 rounded-2xl flex items-center">
                <div class="w-16 h-16 bg-tertiary/10 rounded-xl flex items-center justify-center mr-6">
                  <component :is="reward.icon" class="w-8 h-8 text-tertiary" />
                </div>
                <div>
                  <h4 class="font-bold text-sm mb-1">{{ reward.name }}</h4>
                  <p class="text-[10px] text-secondary/60">{{ reward.desc }}</p>
                  <button class="mt-3 text-[10px] font-bold text-primary uppercase tracking-widest">立即查看</button>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { 
  LayoutDashboard as DashboardIcon,
  LayoutGrid as LayoutGridIcon,
  Gift as GiftIcon,
  Bell as MailIcon,
  Lock as LockIcon,
  ChevronRight as ChevronRightIcon,
  MessageSquare as MessageIcon,
  Star as StarIcon,
  Info as InfoIcon,
  Ticket as TicketIcon,
  Award as AwardIcon,
  LogOut as LogOutIcon,
  ThumbsUp as ThumbsUpIcon,
} from 'lucide-vue-next';
import { useRouter } from 'vue-router';
import request from '../api/request';

const activeSection = ref('dashboard');
const router = useRouter();
const userProfile = ref<any>(null);
const loading = ref(true);
const menuItems = [
  { id: 'dashboard', name: '进度看板', icon: DashboardIcon },
  { id: 'stamps', name: '印章册', icon: LayoutGridIcon },
  { id: 'rewards', name: '我的奖励', icon: GiftIcon },
  { id: 'messages', name: '消息管理', icon: MailIcon, hasBadge: true },
];

// Notification type → icon / style mapping
const notificationStyleMap: Record<string, { icon: any; typeBg: string; typeColor: string }> = {
  reply: { icon: MessageIcon, typeBg: 'bg-primary/5', typeColor: 'text-primary' },
  announcement: { icon: InfoIcon, typeBg: 'bg-tertiary/5', typeColor: 'text-tertiary' },
  badge: { icon: StarIcon, typeBg: 'bg-on-surface/5', typeColor: 'text-on-surface' },
  reward: { icon: GiftIcon, typeBg: 'bg-tertiary/5', typeColor: 'text-tertiary' },
  like: { icon: ThumbsUpIcon, typeBg: 'bg-secondary/5', typeColor: 'text-secondary' },
};

const rewardIconMap: Record<string, any> = {
  coupon: TicketIcon,
  badge: AwardIcon,
  other: GiftIcon,
};

const footprintStats = computed(() => {
  if (!userProfile.value?.footprint_stats) return [];
  return userProfile.value.footprint_stats;
});

const footprintMonuments = computed(() => {
  return userProfile.value?.footprint_monuments || [];
});

const stamps = ref([
  { id: 1, name: '故宫 · 角楼', unlocked: true, image: 'https://picsum.photos/seed/s1/200/200' },
  { id: 2, name: '苏州 · 拙政园', unlocked: true, image: 'https://picsum.photos/seed/s2/200/200' },
  { id: 3, name: '五台山 · 佛光寺', unlocked: true, image: 'https://picsum.photos/seed/s3/200/200' },
  { id: 4, name: '待解锁', unlocked: false },
  { id: 5, name: '待解锁', unlocked: false },
]);

const quizAccuracy = computed(() => {
  if (!userProfile.value) return 0;
  return userProfile.value.quiz_accuracy || 0;
});

const quizAccuracyOffset = computed(() => {
  const circumference = 2 * Math.PI * 45;
  return circumference - (circumference * quizAccuracy.value / 100);
});

const levelLabel = computed(() => {
  if (!userProfile.value) return '—';
  return userProfile.value.level_label;
});

const footprintCount = computed(() => {
  return userProfile.value?.footprint_count || 0;
});

const quizTotalCount = computed(() => {
  return userProfile.value?.quiz_total_count || 0;
});

const messages = computed(() => {
  if (!userProfile.value?.notifications) return [];
  return userProfile.value.notifications.map((n: any) => {
    const style = notificationStyleMap[n.type] || notificationStyleMap.announcement;
    return {
      id: n.id,
      title: n.title,
      content: n.content,
      time: n.time,
      unread: n.unread,
      icon: style.icon,
      typeBg: style.typeBg,
      typeColor: style.typeColor,
    };
  });
});

const rewards = computed(() => {
  if (!userProfile.value?.rewards) return [];
  return userProfile.value.rewards.map((r: any) => ({
    id: r.id,
    name: r.name,
    desc: r.desc,
    icon: rewardIconMap[r.reward_type] || GiftIcon,
  }));
});

const fetchUserProfile = async () => {
  try {
    loading.value = true;
    const data = await request.get('/api/users/me/');
    userProfile.value = data;
  } catch (e) {
    console.error('Failed to fetch user profile:', e);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  if (!localStorage.getItem('access_token')) {
    router.replace('/');
    return;
  }
  fetchUserProfile();
});

const handleLogout = () => {
  if (confirm('确定要暂别“筑迹”，结束本次营造之旅吗？')) {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_role');
    router.replace('/').then(() => {
      window.location.reload();
    });
  }
};
</script>
