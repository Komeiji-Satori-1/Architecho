<template>
  <div class="pt-20">
    <!-- Hero Section / Carousel Placeholder -->
    <section class="relative h-[80vh] overflow-hidden bg-on-surface">
      <div class="absolute inset-0">
        <img 
          :src="hero.cover_image || 'https://picsum.photos/seed/architecture/1920/1080'" 
          class="w-full h-full object-cover opacity-60 scale-105"
          referrerpolicy="no-referrer"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-on-surface via-transparent to-transparent"></div>
      </div>
      
      <div class="container mx-auto px-4 h-full relative z-10 flex flex-col justify-center items-center text-center">
        <div class="inline-block px-4 py-1 bg-tertiary text-white text-[10px] font-bold uppercase tracking-widest mb-6">
          本月推荐
        </div>
        <h1 class="font-serif text-6xl md:text-8xl text-white mb-8 tracking-tight leading-tight">
          {{ hero.name || '大唐遗风：五台山佛光寺' }}
        </h1>
        <p class="text-white/80 text-lg max-w-2xl mb-12 leading-relaxed font-light">
          {{ hero.desc || '穿越千年的斗拱结构，触摸中华木构建筑的巰峰。加入本月共创计划，重塑经典文创，延续匠心之美。' }}
        </p>
        <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-6">
          <button @click="router.push('/stamps')" class="px-10 py-4 bg-primary text-white font-bold rounded-lg hover:bg-primary-container transition-all flex items-center">
            开始探索 <ArrowRightIcon class="ml-2 w-4 h-4" />
          </button>
          <button @click="router.push('/stamps')" class="px-10 py-4 bg-white/10 backdrop-blur-md text-white font-bold rounded-lg hover:bg-white/20 transition-all border border-white/20">
            了解集章
          </button>
        </div>
      </div>

      <!-- Carousel Indicators -->
      <div class="absolute bottom-12 left-1/2 -translate-x-1/2 flex space-x-3">
        <div v-for="i in 3" :key="i" class="w-12 h-1 rounded-full transition-all" :class="i === 1 ? 'bg-white' : 'bg-white/30'"></div>
      </div>
    </section>

    <!-- Main Content -->
    <section class="py-24 bg-surface">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
          
          <!-- Left: Stamp Progress -->
          <div class="lg:col-span-4">
            <StampLayer 
              :title="stampProgress.title"
              :progress="stampProgress.progress"
              :collected="stampProgress.collected"
              :total="stampProgress.total"
              :description="stampProgress.description"
              @click="handleStampClick"
            />
          </div>

          <!-- Center: Forum Hot Topics -->
          <div class="lg:col-span-5">
            <div class="flex items-center justify-between mb-10">
              <h2 class="font-serif text-3xl flex items-center">
                <MessageSquareIcon class="w-6 h-6 mr-3 text-primary" /> 筑匠论坛热门
              </h2>
              <a href="#" class="text-xs font-bold text-primary hover:underline" @click.prevent="router.push('/forum')">查看全部</a>
            </div>
            
            <!-- 加载骨架 -->
            <div v-if="hotTopicsLoading" class="space-y-8">
              <div v-for="i in 4" :key="i" class="flex items-start">
                <div class="w-12 h-10 bg-secondary/5 rounded mr-6 animate-pulse"></div>
                <div class="flex-1 space-y-2">
                  <div class="h-4 bg-secondary/5 rounded animate-pulse"></div>
                  <div class="h-3 w-1/2 bg-secondary/5 rounded animate-pulse"></div>
                </div>
              </div>
            </div>

            <div v-else class="space-y-8">
              <div 
                v-for="(topic, index) in hotTopics" :key="topic.id" 
                class="flex items-start group cursor-pointer"
                @click="router.push(`/forum/${topic.id}`)"
              >
                <span class="font-serif text-4xl text-secondary/10 mr-6 group-hover:text-primary/20 transition-colors">0{{ index + 1 }}</span>
                <div>
                  <h3 class="font-serif text-lg mb-2 group-hover:text-primary transition-colors">{{ topic.title }}</h3>
                  <div class="flex items-center space-x-4 text-[10px] text-secondary/40 font-bold uppercase tracking-widest">
                    <span>作者：{{ topic.author }}</span>
                    <span>{{ topic.reads }} 阅读</span>
                  </div>
                </div>
              </div>
              <p v-if="!hotTopicsLoading && hotTopics.length === 0" class="text-secondary/40 text-sm">暂无热门话题</p>
            </div>
          </div>

          <!-- Right: Co-creation Status -->
          <div class="lg:col-span-3">
            <div class="bg-primary p-8 rounded-2xl text-white h-full relative overflow-hidden">
              <div class="relative z-10">
                <h2 class="font-serif text-2xl mb-8">共创动态</h2>
                
                <!-- 加载骨架 -->
                <div v-if="coNewsLoading" class="space-y-8">
                  <div v-for="i in 2" :key="i" class="p-4 bg-white/10 rounded-xl border border-white/10 space-y-2">
                    <div class="h-3 w-1/3 bg-white/20 rounded animate-pulse"></div>
                    <div class="h-3 bg-white/10 rounded animate-pulse"></div>
                    <div class="h-3 w-3/4 bg-white/10 rounded animate-pulse"></div>
                  </div>
                </div>

                <div v-else class="space-y-8">
                  <div v-for="item in coNews" :key="item.id" class="p-4 bg-white/10 rounded-xl border border-white/10">
                    <div class="flex items-center text-[10px] font-bold uppercase tracking-widest mb-2">
                      <CheckCircleIcon class="w-3 h-3 mr-2" /> {{ item.label }}
                    </div>
                    <p class="text-xs text-white/80 leading-relaxed">{{ item.content }}</p>
                  </div>
                  <div v-if="!coNewsLoading && coNews.length === 0" class="p-4 bg-white/10 rounded-xl border border-white/10">
                    <div class="flex items-center text-[10px] font-bold uppercase tracking-widest mb-2">
                      <MegaphoneIcon class="w-3 h-3 mr-2" /> 敬请期待
                    </div>
                    <p class="text-xs text-white/80 leading-relaxed">更多共创动态即将开启。</p>
                  </div>
                </div>

                <button @click="router.push('/co-creation')" class="w-full mt-12 py-4 bg-white text-primary font-bold rounded-lg hover:bg-surface transition-all flex items-center justify-center">
                  <PenToolIcon class="w-4 h-4 mr-2" /> 我也要贡献灵感
                </button>
              </div>
              
              <!-- Decorative Pattern -->
              <div class="absolute -bottom-10 -right-10 w-40 h-40 border-8 border-white/5 rounded-full"></div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- Editorial Section -->
    <section class="py-32 bg-white overflow-hidden">
      <div class="container mx-auto px-4">
        <div class="flex flex-col lg:flex-row items-center gap-20">
          <div class="lg:w-1/2 relative">
            <div class="aspect-[3/4] rounded-3xl overflow-hidden shadow-2xl">
              <img 
                :src="hero.cover_image || 'https://picsum.photos/seed/roof/800/1200'" 
                class="w-full h-full object-cover"
                referrerpolicy="no-referrer"
              />
            </div>
            <div class="absolute -bottom-10 -right-10 bg-surface p-8 rounded-2xl shadow-xl max-w-xs border border-outline-variant/10">
              <div class="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                <CompassIcon class="w-5 h-5 text-primary" />
              </div>
              <h4 class="font-serif text-lg mb-2">营造技艺解析</h4>
              <p class="text-xs text-secondary/60 leading-relaxed">
                深入了解中国传统木结构的灵魂——斗拱。不仅是结构支撑，更是流动的艺术韵律。
              </p>
            </div>
          </div>
          
          <div class="lg:w-1/2">
            <div class="w-16 h-1 bg-primary mb-12"></div>
            <h2 class="font-serif text-5xl md:text-7xl mb-12 leading-tight">
              不仅仅是保存<br/>
              更是<span class="text-primary italic">新生</span>
            </h2>
            <p class="text-secondary/80 text-lg mb-12 leading-relaxed font-light">
              “筑迹”致力于连接古建爱好者与现代设计师。我们通过数字化的印记采集与大众参与的共创模式，让沉寂在历史深处的木构建筑，在数字时代焕发出全新的生命力。
            </p>
            
            <div class="grid grid-cols-2 gap-12">
              <div>
                <p class="text-4xl font-serif text-on-surface mb-2">450+</p>
                <p class="text-xs text-secondary/40 font-bold uppercase tracking-widest">已录入古建</p>
              </div>
              <div>
                <p class="text-4xl font-serif text-on-surface mb-2">12k</p>
                <p class="text-xs text-secondary/40 font-bold uppercase tracking-widest">社区筑匠</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { 
  ArrowRight as ArrowRightIcon, 
  MessageSquare as MessageSquareIcon,
  CheckCircle as CheckCircleIcon,
  Megaphone as MegaphoneIcon,
  PenTool as PenToolIcon,
  Compass as CompassIcon
} from 'lucide-vue-next';
import StampLayer from '@/components/StampLayer.vue';

const router = useRouter();

// ─── 响应式数据 ─────────────────────────────────────────────────────const stampProgress = ref({
  title: '应县木塔',
  progress: 0,
  collected: 0,
  total: 10,
  description: '登录后查看你的个人集章进度。',
});
const hero = ref<{
  id?: number;
  name?: string;
  desc?: string;
  cover_image?: string;
  era?: string;
  location?: string;
}>({});

const hotTopics = ref<{ id: number; title: string; author: string; reads: number }[]>([]);
const hotTopicsLoading = ref(true);

const coNews = ref<{ id: number; label: string; content: string }[]>([]);
const coNewsLoading = ref(true);

// ─── 数据拉取 ─────────────────────────────────────────────────────
onMounted(async () => {
  await Promise.allSettled([
    fetchHero(),
    fetchHotTopics(),
    fetchCoNews(),
    fetchStampProgress(),
  ]);
});

async function fetchStampProgress() {
  const token = localStorage.getItem('access_token');
  if (!token) return;
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/stamps/my-progress/', {
      headers: { Authorization: `Bearer ${token}` },
    });
    stampProgress.value = res.data;
  } catch {
    // 未收集印章或 token 过期时保持默认占位
  }
}

async function fetchHero() {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/monuments/featured/');
    hero.value = res.data;
  } catch {
    // 保持默认占位文案
  }
}

async function fetchHotTopics() {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/forum/hot-topics/');
    hotTopics.value = res.data;
  } catch {
    hotTopics.value = [];
  } finally {
    hotTopicsLoading.value = false;
  }
}

async function fetchCoNews() {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/cocreation/recent-news/');
    coNews.value = res.data;
  } catch {
    coNews.value = [];
  } finally {
    coNewsLoading.value = false;
  }
}

// ─── 交互 ──────────────────────────────────────────────────────
const handleStampClick = () => {
  router.push('/stamps');
};
</script>
