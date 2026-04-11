<template>
  <div class="pt-24 pb-12 bg-surface min-h-screen">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

        <!-- Left Sidebar: Categories -->
        <aside class="lg:col-span-2 space-y-6">
          <div class="bg-white rounded-xl p-6 border border-outline-variant/10 shadow-sm">
            <h3 class="font-serif text-lg mb-6 flex items-center">
              <TrendingUpIcon class="w-4 h-4 mr-2 text-primary" /> 热门板块
            </h3>
            <div class="space-y-2">
              <button v-for="cat in categories" :key="cat.name"
                class="w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-all"
                :class="activeCategory === cat.name ? 'bg-primary/5 text-primary font-bold' : 'text-secondary hover:bg-secondary/5'"
                @click="activeCategory = cat.name">
                <span class="flex items-center">
                  {{ cat.name }}
                  <span v-if="cat.hot"
                    class="ml-2 px-1.5 py-0.5 bg-primary/10 text-primary text-[8px] rounded uppercase">Hot</span>
                </span>
                <span class="text-[10px] text-secondary/40">{{ cat.post_count }}</span>
              </button>
            </div>
          </div>

          <div class="bg-primary/5 rounded-xl p-6 border border-primary/10">
            <h4 class="text-xs font-bold text-primary uppercase tracking-widest mb-3">论坛公告</h4>
            <p class="text-xs text-secondary/70 leading-relaxed">
              “筑迹”第二届古建筑建模大赛现已开启，诚邀各位筑匠共谱华章。
            </p>
          </div>
        </aside>

        <!-- Main Content: Post List -->
        <main class="lg:col-span-7 space-y-6">
          <!-- Filter Tabs & Search -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
            <div class="flex items-center space-x-8 border-b border-outline-variant/10 flex-grow">
              <button v-for="tab in tabs" :key="tab" class="pb-3 text-sm font-medium transition-all relative"
                :class="activeTab === tab ? 'text-primary' : 'text-secondary/60 hover:text-secondary'"
                @click="activeTab = tab">
                {{ tab }}
                <div v-if="activeTab === tab" class="absolute bottom-0 left-0 right-0 h-0.5 bg-primary"></div>
              </button>
            </div>

            <div class="relative">
              <input v-model="searchQuery" type="text" placeholder="搜索论坛内容..."
                class="bg-white border border-outline-variant/20 rounded-full py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-primary/40 w-full sm:w-64 transition-all" />
              <SearchIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-secondary/40" />
            </div>
          </div>

          <!-- Posts -->
          <div v-if="postsLoading" class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div v-for="i in 4" :key="i"
              class="bg-white rounded-xl overflow-hidden border border-outline-variant/10 animate-pulse">
              <div class="aspect-[4/3] bg-secondary/5"></div>
              <div class="p-6 space-y-3">
                <div class="h-4 bg-secondary/5 rounded w-3/4"></div>
                <div class="h-3 bg-secondary/5 rounded w-1/2"></div>
              </div>
            </div>
          </div>
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <PostCard v-for="post in filteredPosts" :key="post.id" :post="post" @click="goToDetail" />
            <p v-if="filteredPosts.length === 0" class="col-span-2 text-center text-secondary/40 text-sm py-12">暂无相关帖子
            </p>
          </div>
        </main>

        <!-- Right Sidebar: Stats & Badges -->
        <aside class="lg:col-span-3 space-y-6">
          <div
            class="bg-white rounded-2xl p-8 mb-6 border border-outline-variant/10 shadow-sm flex flex-col items-center justify-center min-h-[160px]">

            <p class="text-xs text-secondary/40 mb-5 text-center tracking-widest font-light">
              想分享关于古建的独特见解？
            </p>

            <button @click="openPublishModal" class="w-full max-w-[200px] py-3.5 bg-primary text-white rounded-xl font-bold 
           hover:shadow-xl hover:-translate-y-0.5 active:scale-95 
           transition-all duration-300 flex items-center justify-center gap-2 group">
              <PenLineIcon class="w-4 h-4 group-hover:-rotate-12 transition-transform" />
              <span class="tracking-wider">分享新见</span>
            </button>

          </div>
          <div class="bg-white rounded-xl p-8 border border-outline-variant/10 shadow-sm text-center">
            <p class="text-4xl font-serif text-primary mb-2">12,842</p>
            <p class="text-[10px] text-secondary/40 font-bold uppercase tracking-widest">活跃筑匠</p>
          </div>

          <div class="bg-white rounded-xl p-6 border border-outline-variant/10 shadow-sm">
            <h3 class="font-serif text-lg mb-6">活跃榜</h3>
            <div class="space-y-4">
              <div v-for="(user, idx) in topUsers" :key="idx" class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                  <span class="font-serif text-lg italic text-secondary/20 w-4">{{ idx + 1 }}</span>
                  <img :src="user.avatar" class="w-8 h-8 rounded-full object-cover" referrerpolicy="no-referrer" />
                  <div>
                    <p class="text-xs font-bold text-on-surface">{{ user.name }}</p>
                    <p class="text-[10px] text-secondary/40">影响力 {{ user.power }}</p>
                  </div>
                </div>
                <div class="flex space-x-1">
                  <StampIcon v-for="i in user.badges" :key="i" class="w-3 h-3 text-primary/40" />
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl p-6 border border-outline-variant/10 shadow-sm">
            <h3 class="font-serif text-lg mb-6">勋章馆</h3>
            <div class="grid grid-cols-3 gap-4">
              <div v-for="i in 6" :key="i"
                class="aspect-square bg-secondary/5 rounded-lg flex items-center justify-center group cursor-help">
                <StampIcon class="w-6 h-6 text-secondary/20 group-hover:text-primary transition-colors" />
              </div>
            </div>
          </div>
        </aside>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, inject } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import {
  TrendingUp as TrendingUpIcon,
  Search as SearchIcon,
  Stamp as StampIcon,
  PenLine as PenLineIcon,
} from 'lucide-vue-next';
import PostCard from '@/components/PostCard.vue';

const router = useRouter();
const activeCategory = ref('');
const activeTab = ref('全部动态');
const searchQuery = ref('');
const postsLoading = ref(true);

const tabs = ['全部动态', '热门', '精华帖', '最新发布'];

// ─── 分类（来自数据库） ─────────────────────────────────────────
const categories = ref<{ id: number; name: string; hot: boolean; post_count: number }[]>([]);

async function fetchCategories() {
  try {
    console.log('[DEBUG] Fetching categories...');
    const res = await axios.get('http://127.0.0.1:8000/api/forum/categories/');
    categories.value = res.data.results ?? res.data;
    console.log('[DEBUG] Categories fetched:', categories.value.length);
    if (categories.value.length && !activeCategory.value) {
      activeCategory.value = categories.value[0].name;
    }
  } catch (err) {
    console.error('[ERROR] Failed to fetch categories:', err);
    categories.value = [];
  }
}

// ─── 帖子（来自数据库） ─────────────────────────────────────────
const posts = ref<any[]>([]);

async function fetchPosts() {
  postsLoading.value = true;
  try {
    const params: Record<string, string | number> = {};
    const cat = categories.value.find(c => c.name === activeCategory.value);
    if (cat) params.category = cat.id;
    if (activeTab.value === '精华帖') {
      console.log('[DEBUG] Filtering by essence');
      params.is_essence = 'true';
    }
    if (activeTab.value === '热门') {
      console.log('[DEBUG] Sorting by heat score');
      params.ordering = '-heat_score';
    }
    if (activeTab.value === '最新发布') {
      console.log('[DEBUG] Sorting by created_at');
      params.ordering = '-created_at';
    }
    console.log('[DEBUG] Fetching posts with params:', params);
    const res = await axios.get('http://127.0.0.1:8000/api/forum/posts/', { params });
    posts.value = res.data.results ?? res.data;
    console.log('[DEBUG] Posts fetched:', posts.value.length);
    posts.value.forEach(p => console.log(`[DEBUG] Post ${p.id}: title=${p.title}, heat_score=${p.heat_score}, likes=${p.likes}, views=${p.views}`));
  } catch (err) {
    console.error('[ERROR] Failed to fetch posts:', err);
    posts.value = [];
  } finally {
    postsLoading.value = false;
  }
}

onMounted(async () => {
  await fetchCategories();
  await fetchPosts();
  fetchLeaderboard();
});

watch([activeCategory, activeTab], () => {
  fetchPosts();
});

// ─── 活跃榜（来自后端 API） ───────────────────
const topUsers = ref<any[]>([]);

async function fetchLeaderboard() {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/users/leaderboard/');
    topUsers.value = res.data;
  } catch {
    topUsers.value = [];
  }
}

// ─── 搜索（客户端过滤） ──────────────────────────────────────────
const filteredPosts = computed(() => {
  if (!searchQuery.value) return posts.value;
  const q = searchQuery.value.toLowerCase();
  return posts.value.filter(
    p => p.title.toLowerCase().includes(q) || (p.excerpt ?? '').toLowerCase().includes(q),
  );
});

const goToDetail = (id: number) => {
  router.push(`/forum/${id}`);
};
const openPublishModal = () => {
  if (!localStorage.getItem('access_token')) {
    // 未登录，触发登录弹窗（通过 inject 的 toggleAuth）
    const toggleAuth = inject<(val: boolean) => void>('toggleAuth');
    toggleAuth?.(true);
    return;
  }
  router.push('/forum/publish');
};

</script>
