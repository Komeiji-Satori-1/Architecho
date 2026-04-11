<template>
  <div class="pt-24 pb-24 bg-surface min-h-screen">
    <div class="container mx-auto px-4">
      <!-- Header -->
      <header class="mb-12">
        <h1 class="font-serif text-4xl text-primary mb-2">搜索结果</h1>
        <p class="text-secondary/60 text-sm">
          关键词「<span class="text-primary font-bold">{{ keyword }}</span>」共找到
          <span class="font-bold">{{ totalCount }}</span> 条结果
        </p>
      </header>

      <!-- Main Layout -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-10">
        <!-- Left Sidebar: Category Nav -->
        <aside class="lg:col-span-3">
          <div class="bg-white rounded-2xl p-6 border border-outline-variant/10 shadow-sm sticky top-24">
            <h3 class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest mb-6">分类筛选</h3>
            <div class="space-y-2">
              <button
                v-for="cat in categories"
                :key="cat.key"
                class="w-full text-left px-4 py-3 rounded-xl text-sm font-medium transition-all flex items-center justify-between"
                :class="activeCategory === cat.key ? 'bg-primary text-white shadow-lg shadow-primary/20' : 'text-secondary/70 hover:bg-surface'"
                @click="activeCategory = cat.key"
              >
                <span class="flex items-center">
                  <component :is="cat.icon" class="w-4 h-4 mr-3" />
                  {{ cat.label }}
                </span>
                <span 
                  class="text-[10px] font-bold px-2 py-0.5 rounded-full"
                  :class="activeCategory === cat.key ? 'bg-white/20' : 'bg-secondary/10'"
                >
                  {{ cat.count }}
                </span>
              </button>
            </div>
          </div>
        </aside>

        <!-- Right Content -->
        <main class="lg:col-span-9">
          <div v-if="loading" class="text-center py-20 text-secondary/40">
            <div class="inline-block w-8 h-8 border-2 border-primary/30 border-t-primary rounded-full animate-spin mb-4"></div>
            <p class="text-sm">搜索中...</p>
          </div>

          <div v-else-if="!totalCount" class="text-center py-20">
            <SearchIcon class="w-16 h-16 text-secondary/20 mx-auto mb-6" />
            <p class="text-secondary/40 text-sm">未找到相关结果，换个关键词试试</p>
          </div>

          <!-- Posts -->
          <div v-else-if="activeCategory === 'posts'">
            <div class="flex items-center justify-between mb-8">
              <h2 class="font-serif text-2xl">帖子</h2>
              <span class="text-[10px] text-secondary/40 font-bold uppercase tracking-widest">{{ posts.length }} Results</span>
            </div>
            <div v-if="!posts.length" class="text-center py-12 text-secondary/40 text-sm">暂无匹配帖子</div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
              <PostCard
                v-for="post in posts"
                :key="post.id"
                :post="post"
                @click="goToPost"
              />
            </div>
          </div>

          <!-- Monuments -->
          <div v-else-if="activeCategory === 'monuments'">
            <div class="flex items-center justify-between mb-8">
              <h2 class="font-serif text-2xl">古建筑</h2>
              <span class="text-[10px] text-secondary/40 font-bold uppercase tracking-widest">{{ monuments.length }} Results</span>
            </div>
            <div v-if="!monuments.length" class="text-center py-12 text-secondary/40 text-sm">暂无匹配古建筑</div>
            <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div
                v-for="building in monuments"
                :key="building.id"
                class="group cursor-pointer"
                @click="openMonumentArchive(building)"
              >
                <div class="aspect-[3/4] rounded-2xl overflow-hidden relative mb-4 shadow-lg">
                  <img
                    :src="building.cover_image || 'https://picsum.photos/seed/default/600/800'"
                    class="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700 group-hover:scale-110"
                    referrerpolicy="no-referrer"
                  />
                  <div class="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm px-3 py-1 rounded text-[10px] font-bold text-secondary">
                    {{ building.location }}
                  </div>
                </div>
                <h3 class="font-serif text-xl mb-2 group-hover:text-primary transition-colors">{{ building.name }}</h3>
                <p class="text-xs text-secondary/60 line-clamp-2 leading-relaxed">{{ building.desc }}</p>
                <button class="mt-4 text-[10px] font-bold text-primary uppercase tracking-widest flex items-center">
                  探索档案 <ArrowRightIcon class="ml-2 w-3 h-3" />
                </button>
              </div>
            </div>
          </div>

          <!-- CoCreations -->
          <div v-else-if="activeCategory === 'cocreations'">
            <div class="flex items-center justify-between mb-8">
              <h2 class="font-serif text-2xl">筑品文创</h2>
              <span class="text-[10px] text-secondary/40 font-bold uppercase tracking-widest">{{ cocreations.length }} Results</span>
            </div>
            <div v-if="!cocreations.length" class="text-center py-12 text-secondary/40 text-sm">暂无匹配文创</div>
            <div v-else class="columns-1 md:columns-2 lg:columns-3 gap-8 space-y-8">
              <div
                v-for="item in cocreations"
                :key="item.id"
                class="break-inside-avoid group cursor-pointer"
                @click="openCoCreationDetail(item)"
              >
                <div class="bg-white rounded-2xl overflow-hidden border border-outline-variant/10 hover:shadow-xl transition-all duration-500">
                  <div class="relative overflow-hidden">
                    <img
                      :src="item.cover"
                      class="w-full h-auto object-cover group-hover:scale-105 transition-transform duration-700"
                      referrerpolicy="no-referrer"
                    />
                    <div v-if="item.featured" class="absolute top-4 left-4 bg-primary text-white text-[8px] px-2 py-1 font-bold uppercase tracking-widest">
                      本周精选
                    </div>
                  </div>
                  <div class="p-6">
                    <h3 class="font-serif text-xl mb-3 group-hover:text-primary transition-colors">{{ item.title }}</h3>
                    <div class="flex items-center justify-between">
                      <div class="flex items-center space-x-2">
                        <img :src="item.avatar" class="w-5 h-5 rounded-full" referrerpolicy="no-referrer" />
                        <span class="text-[10px] text-secondary/60">{{ item.author }}</span>
                      </div>
                      <div class="flex items-center space-x-1 text-secondary/40">
                        <HeartIcon class="w-3 h-3" />
                        <span class="text-[10px]">{{ item.likes }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>

    <!-- Monument Archive Modal -->
    <transition name="modal">
      <div v-if="selectedMonument" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-on-surface/60 backdrop-blur-md" @click="selectedMonument = null"></div>
        <div class="relative w-full max-w-4xl bg-white rounded-3xl overflow-hidden shadow-2xl flex flex-col md:flex-row max-h-[90vh]">
          <div class="md:w-1/2 h-64 md:h-auto relative">
            <img :src="selectedMonument.cover_image || 'https://picsum.photos/seed/default/600/800'" class="w-full h-full object-cover" referrerpolicy="no-referrer" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-8 left-8 text-white">
              <h2 class="font-serif text-4xl mb-2">{{ selectedMonument.name }}</h2>
              <p class="text-sm opacity-80">{{ selectedMonument.location }}</p>
            </div>
          </div>
          <div class="md:w-1/2 p-12 overflow-y-auto">
            <div class="flex items-center justify-between mb-8">
              <span class="text-[10px] font-bold text-primary uppercase tracking-widest">档案详情 / Archive</span>
              <button @click="selectedMonument = null" class="text-secondary/40 hover:text-primary transition-colors">
                <XIcon class="w-6 h-6" />
              </button>
            </div>
            <div class="space-y-8">
              <div>
                <h3 class="font-serif text-xl mb-4">{{ selectedMonument.name }}</h3>
                <p class="text-sm text-secondary/60 leading-relaxed">{{ selectedMonument.full_desc || selectedMonument.desc }}</p>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div class="bg-surface rounded-xl p-4">
                  <p class="text-[10px] text-secondary/40 font-bold uppercase tracking-widest mb-1">朝代</p>
                  <p class="font-serif text-lg">{{ selectedMonument.dynasty || '—' }}</p>
                </div>
                <div class="bg-surface rounded-xl p-4">
                  <p class="text-[10px] text-secondary/40 font-bold uppercase tracking-widest mb-1">结构</p>
                  <p class="font-serif text-lg">{{ selectedMonument.structure_type || '—' }}</p>
                </div>
              </div>
              <button
                v-if="selectedMonument.has_article"
                @click="startChallenge(selectedMonument)"
                class="w-full py-4 bg-primary text-white font-bold text-sm rounded-xl shadow-xl shadow-primary/20 hover:bg-primary-container transition-all"
              >
                开始挑战
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- CoCreation Detail Modal -->
    <IdeaDetailModal
      v-if="detailVisible"
      :item="detailItem"
      @close="detailVisible = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  Search as SearchIcon,
  MessageSquare as MessageSquareIcon,
  Landmark as LandmarkIcon,
  Palette as PaletteIcon,
  Heart as HeartIcon,
  ArrowRight as ArrowRightIcon,
  X as XIcon,
} from 'lucide-vue-next';
import service from '../api/request';
import PostCard from '../components/PostCard.vue';
import IdeaDetailModal from '../components/IdeaDetailModal.vue';

const route = useRoute();
const router = useRouter();

const keyword = ref('');
const loading = ref(false);
const posts = ref<any[]>([]);
const monuments = ref<any[]>([]);
const cocreations = ref<any[]>([]);
const activeCategory = ref('posts');

const selectedMonument = ref<any>(null);
const detailVisible = ref(false);
const detailItem = ref<any>(null);

const totalCount = computed(() => posts.value.length + monuments.value.length + cocreations.value.length);

const categories = computed(() => [
  { key: 'posts', label: '帖子', icon: MessageSquareIcon, count: posts.value.length },
  { key: 'monuments', label: '古建筑', icon: LandmarkIcon, count: monuments.value.length },
  { key: 'cocreations', label: '筑品文创', icon: PaletteIcon, count: cocreations.value.length },
]);

const doSearch = async (q: string) => {
  if (!q) return;
  loading.value = true;
  try {
    const res = await service.get('/api/search/', { params: { q } }) as any;
    posts.value = res.posts || [];
    monuments.value = res.monuments || [];
    cocreations.value = res.cocreations || [];
    // auto-select first non-empty category
    if (posts.value.length) activeCategory.value = 'posts';
    else if (monuments.value.length) activeCategory.value = 'monuments';
    else if (cocreations.value.length) activeCategory.value = 'cocreations';
    else activeCategory.value = 'posts';
  } catch {
    posts.value = [];
    monuments.value = [];
    cocreations.value = [];
  } finally {
    loading.value = false;
  }
};

const goToPost = (id: number) => {
  router.push(`/forum/${id}`);
};

const openMonumentArchive = (building: any) => {
  selectedMonument.value = building;
};

const startChallenge = (building: any) => {
  selectedMonument.value = null;
  router.push(`/stamps/article/${building.id}`);
};

const openCoCreationDetail = (item: any) => {
  detailItem.value = item;
  detailVisible.value = true;
};

watch(() => route.query.q, (q) => {
  keyword.value = (q as string) || '';
  doSearch(keyword.value);
}, { immediate: true });

onMounted(() => {
  keyword.value = (route.query.q as string) || '';
  if (keyword.value) doSearch(keyword.value);
});
</script>

<style scoped>
.modal-enter-active, .modal-leave-active {
  transition: all 0.3s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
</style>
