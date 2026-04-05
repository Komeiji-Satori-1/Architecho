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
              <button 
                v-for="cat in categories" 
                :key="cat.name"
                class="w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-all"
                :class="activeCategory === cat.name ? 'bg-primary/5 text-primary font-bold' : 'text-secondary hover:bg-secondary/5'"
                @click="activeCategory = cat.name"
              >
                <span class="flex items-center">
                  {{ cat.name }}
                  <span v-if="cat.hot" class="ml-2 px-1.5 py-0.5 bg-primary/10 text-primary text-[8px] rounded uppercase">Hot</span>
                </span>
                <span class="text-[10px] text-secondary/40">{{ cat.count }}</span>
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
              <button 
                v-for="tab in tabs" 
                :key="tab"
                class="pb-3 text-sm font-medium transition-all relative"
                :class="activeTab === tab ? 'text-primary' : 'text-secondary/60 hover:text-secondary'"
                @click="activeTab = tab"
              >
                {{ tab }}
                <div v-if="activeTab === tab" class="absolute bottom-0 left-0 right-0 h-0.5 bg-primary"></div>
              </button>
            </div>
            
            <div class="relative">
              <input 
                v-model="searchQuery"
                type="text" 
                placeholder="搜索论坛内容..." 
                class="bg-white border border-outline-variant/20 rounded-full py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-primary/40 w-full sm:w-64 transition-all"
              />
              <SearchIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-secondary/40" />
            </div>
          </div>

          <!-- Posts -->
          <div class="space-y-4">
            <div 
              v-for="post in filteredPosts" 
              :key="post.id"
              class="bg-white rounded-xl p-6 border border-outline-variant/10 hover:shadow-md transition-all cursor-pointer group"
              @click="goToDetail(post.id)"
            >
              <div class="flex items-start justify-between mb-4">
                <div class="flex items-center space-x-3">
                  <div class="relative">
                    <img :src="post.authorAvatar" class="w-10 h-10 rounded-full object-cover" referrerpolicy="no-referrer" />
                    <!-- SVG Badge Placeholder -->
                    <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-white rounded-full flex items-center justify-center shadow-sm">
                      <StampIcon class="w-2.5 h-2.5 text-primary" />
                    </div>
                  </div>
                  <div>
                    <div class="flex items-center">
                      <span class="text-sm font-bold text-on-surface mr-2">{{ post.author }}</span>
                      <span v-if="post.isTop" class="px-1.5 py-0.5 bg-primary text-white text-[8px] rounded font-bold uppercase tracking-widest mr-1">置顶</span>
                      <span v-if="post.isEssence" class="px-1.5 py-0.5 bg-tertiary text-white text-[8px] rounded font-bold uppercase tracking-widest">精</span>
                    </div>
                    <p class="text-[10px] text-secondary/40 uppercase tracking-widest">{{ post.time }} · {{ post.category }}</p>
                  </div>
                </div>
              </div>

              <h3 class="font-serif text-xl mb-3 group-hover:text-primary transition-colors">{{ post.title }}</h3>
              <p class="text-secondary/70 text-sm line-clamp-2 mb-4 leading-relaxed">
                {{ post.excerpt }}
              </p>

              <!-- Image Gallery (Optional) -->
              <div v-if="post.images && post.images.length" class="grid grid-cols-3 gap-2 mb-4 rounded-lg overflow-hidden">
                <img 
                  v-for="(img, idx) in post.images.slice(0, 3)" 
                  :key="idx" 
                  :src="img" 
                  class="aspect-video object-cover w-full"
                  referrerpolicy="no-referrer"
                />
              </div>

              <div class="flex items-center space-x-6 text-secondary/40 text-xs">
                <span class="flex items-center"><EyeIcon class="w-3.5 h-3.5 mr-1.5" /> {{ post.views }}</span>
                <span class="flex items-center"><HeartIcon class="w-3.5 h-3.5 mr-1.5" /> {{ post.likes }}</span>
                <span class="flex items-center"><MessageSquareIcon class="w-3.5 h-3.5 mr-1.5" /> {{ post.comments }}</span>
              </div>
            </div>
          </div>
        </main>

        <!-- Right Sidebar: Stats & Badges -->
        <aside class="lg:col-span-3 space-y-6">
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
              <div v-for="i in 6" :key="i" class="aspect-square bg-secondary/5 rounded-lg flex items-center justify-center group cursor-help">
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
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { 
  TrendingUp as TrendingUpIcon, 
  Search as SearchIcon,
  Eye as EyeIcon,
  Heart as HeartIcon,
  MessageSquare as MessageSquareIcon,
  Stamp as StampIcon
} from 'lucide-vue-next';

const router = useRouter();
const activeCategory = ref('营造法式');
const activeTab = ref('全部动态');
const searchQuery = ref('');

const categories = [
  { name: '营造法式', count: '2.4k', hot: true },
  { name: '古建摄影', count: '1.8k', hot: false },
  { name: '模型制作', count: '920', hot: false },
  { name: '木作工艺', count: '640', hot: false },
  { name: '彩画装饰', count: '420', hot: false }
];

const tabs = ['全部动态', '精华帖', '最新发布'];

const posts = [
  {
    id: 1,
    title: '解析《营造法式》中的斗拱模数化设计',
    excerpt: '宋代建筑的标准化程度令人惊叹，本文将从材份制入手，详细拆解十一踩斗拱的受力结构与视觉比例关系...',
    author: '营造大师_老李',
    authorAvatar: 'https://picsum.photos/seed/user1/100/100',
    category: '营造法式',
    time: '3小时前',
    views: '1.2w',
    likes: '856',
    comments: 142,
    isTop: true,
    isEssence: true
  },
  {
    id: 2,
    title: '【摄影集】午后三点的故宫红墙影',
    excerpt: '光影在斑驳的红墙上流转，仿佛能听到历史的呼吸。这组照片尝试捕捉那种静谧而厚重的力量感。',
    author: '光影筑梦师',
    authorAvatar: 'https://picsum.photos/seed/user2/100/100',
    category: '古建摄影',
    time: '昨天',
    views: '3.4k',
    likes: '512',
    comments: 89,
    images: [
      'https://picsum.photos/seed/p1/400/300',
      'https://picsum.photos/seed/p2/400/300',
      'https://picsum.photos/seed/p3/400/300'
    ]
  },
  {
    id: 3,
    title: '手作：1/20 祈年殿全榫卯模型进度更新',
    excerpt: '耗时三个月，完成了最底层的台基与一楼柱网，不含一颗铁钉，全部由微型榫卯结构嵌套而成。',
    author: '墨染木意',
    authorAvatar: 'https://picsum.photos/seed/user3/100/100',
    category: '模型制作',
    time: '2天前',
    views: '5.1k',
    likes: '1.2k',
    comments: 234,
    isEssence: true
  }
];

const topUsers = [
  { name: '云栖墨客', power: '9.8k', avatar: 'https://picsum.photos/seed/u1/100/100', badges: 3 },
  { name: '木构灵魂', power: '8.2k', avatar: 'https://picsum.photos/seed/u2/100/100', badges: 2 },
  { name: '丹青绘影', power: '7.5k', avatar: 'https://picsum.photos/seed/u3/100/100', badges: 2 }
];

const filteredPosts = computed(() => {
  return posts.filter(post => {
    const matchesSearch = post.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                         post.excerpt.toLowerCase().includes(searchQuery.value.toLowerCase());
    return matchesSearch;
  });
});

const goToDetail = (id: number) => {
  router.push(`/forum/${id}`);
};
</script>
