<template>
  <div class="pt-24 pb-24 bg-surface min-h-screen">
    <div class="container mx-auto px-4">
      <!-- Header -->
      <header class="mb-16">
        <h1 class="font-serif text-5xl text-primary mb-2">集章印记</h1>
        <p class="text-secondary/40 text-xs font-bold uppercase tracking-[0.3em]">Stamp Discovery &amp; Architectural Journey</p>
      </header>

      <!-- Discovery Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
        
        <!-- Left: Exploration Window -->
        <div class="lg:col-span-8 space-y-12">
          <!-- Dynasty Scroll Exploration -->
          <div class="bg-white/50 rounded-3xl p-8 border border-outline-variant/10">
            <div class="flex items-center justify-between mb-8">
              <div>
                <p class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest mb-1">Exploration</p>
                <h2 class="font-serif text-2xl">朝代卷轴 · 探索视窗</h2>
              </div>
              <button 
                @click="showAllModal = true"
                class="px-5 py-2.5 bg-primary text-white text-xs font-bold rounded-xl shadow-lg shadow-primary/20 flex items-center"
              >
                <CompassIcon class="w-4 h-4 mr-2" /> 探索更多
              </button>
            </div>

            <!-- Dynasty Timeline Bar -->
            <div class="flex items-center gap-2 mb-8 overflow-x-auto pb-2">
              <div v-for="d in dynastyList" :key="d" 
                class="shrink-0 px-4 py-1.5 rounded-full text-[10px] font-bold cursor-pointer transition-all"
                :class="d === '全部' ? 'bg-primary text-white' : 'bg-surface text-secondary/60 hover:bg-primary/10'"
              >{{ d }}</div>
            </div>

            <div v-if="!topBuildings.length" class="text-center py-12 text-secondary/40 text-sm">暂无探索中的古建筑</div>
            <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div 
                v-for="building in topBuildings" 
                :key="building.id"
                class="group cursor-pointer"
                @click="openArchive(building)"
              >
                <div class="aspect-[3/4] rounded-2xl overflow-hidden relative mb-4 shadow-lg">
                  <img 
                    :src="building.cover_image || 'https://picsum.photos/seed/default/600/800'" 
                    class="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700 group-hover:scale-110"
                    referrerpolicy="no-referrer"
                  />
                  <div class="absolute top-4 right-0 text-white text-[10px] px-3 py-1 font-bold vertical-text"
                    :class="building.status === 'in_progress' ? 'bg-primary' : building.status === 'completed' ? 'bg-tertiary' : 'bg-secondary/60'"
                  >
                    {{ statusLabel(building.status) }}
                  </div>
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

          <!-- Journey Guide -->
          <div class="bg-primary/5 rounded-3xl p-12 border border-primary/10 relative overflow-hidden">
            <div class="relative z-10">
              <div class="inline-block px-3 py-1 bg-primary text-white text-[10px] font-bold uppercase tracking-widest mb-6">Journey</div>
              <h2 class="font-serif text-3xl mb-4">探索流程指引</h2>
              <div class="space-y-6">
                <div class="flex items-start gap-4">
                  <div class="w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center text-sm font-bold shrink-0">1</div>
                  <div>
                    <p class="font-bold text-sm mb-1">选择古建筑</p>
                    <p class="text-xs text-secondary/60">点击上方卡片或"探索更多"，选择你感兴趣的古建筑</p>
                  </div>
                </div>
                <div class="flex items-start gap-4">
                  <div class="w-8 h-8 bg-primary/60 text-white rounded-full flex items-center justify-center text-sm font-bold shrink-0">2</div>
                  <div>
                    <p class="font-bold text-sm mb-1">阅读详细文章</p>
                    <p class="text-xs text-secondary/60">在资料模态框中点击"开始挑战"，进入翻页阅读模式</p>
                  </div>
                </div>
                <div class="flex items-start gap-4">
                  <div class="w-8 h-8 bg-primary/30 text-white rounded-full flex items-center justify-center text-sm font-bold shrink-0">3</div>
                  <div>
                    <p class="font-bold text-sm mb-1">答题解锁印章</p>
                    <p class="text-xs text-secondary/60">每翻一页触发答题，答对可解锁一层套色印章，集齐印章获得线上奖励</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full -translate-y-1/2 translate-x-1/2"></div>
          </div>
        </div>

        <!-- Right: Stamp Collection -->
        <div class="lg:col-span-4 space-y-8">
          <!-- Collection Stats -->
          <div class="bg-white rounded-3xl p-8 border border-outline-variant/10 shadow-sm">
            <div class="flex items-end justify-between mb-4">
              <div>
                <p class="text-[10px] text-secondary/40 font-bold uppercase tracking-widest mb-1">Collection</p>
                <h3 class="font-serif text-xl">我的集章册</h3>
              </div>
              <span class="text-3xl font-serif text-primary">{{ stampProgress.collected || 0 }}/{{ stampProgress.total || 0 }}</span>
            </div>
            <div class="w-full h-1 bg-secondary/10 rounded-full overflow-hidden mb-4">
              <div class="h-full bg-primary transition-all duration-1000" :style="{ width: (stampProgress.progress || 0) + '%' }"></div>
            </div>
            <p class="text-[10px] text-secondary/60 leading-relaxed">
              {{ stampProgress.description || '开始探索古建筑，收集精美印章吧！' }}
            </p>
          </div>

          <!-- Stamp Preview -->
          <div class="bg-white rounded-3xl p-8 border border-outline-variant/10 shadow-sm sticky top-24">
            <h2 class="font-serif text-2xl mb-2">套色印记</h2>
            <p class="text-[10px] text-secondary/40 font-bold uppercase tracking-widest mb-8">Color Overlay Stamping</p>
            
            <!-- SVG Stamp Display -->
            <div class="aspect-square bg-surface rounded-2xl mb-8 flex items-center justify-center relative overflow-hidden p-8">
              <div class="relative w-full h-full">
                <template v-if="stampLayers.length">
                  <transition v-for="layer in stampLayers" :key="layer.layer_index" name="stamp-layer">
                    <img 
                      v-if="(stampProgress.collected || 0) >= layer.layer_index && layer.svg_url"
                      :src="layer.svg_url"
                      class="absolute inset-0 w-full h-full object-contain"
                      :style="{ mixBlendMode: layer.blend_mode || 'multiply', opacity: 0.85, filter: 'blur(0.5px)' }"
                    />
                  </transition>
                </template>
                <!-- Fallback static SVG -->
                <template v-else>
                  <transition name="stamp-layer">
                    <svg v-if="(stampProgress.collected || 0) >= 1" viewBox="0 0 100 100" class="absolute inset-0 w-full h-full text-secondary/20 fill-current">
                      <path d="M20 80 L20 40 L50 20 L80 40 L80 80 Z" /><rect x="35" y="50" width="30" height="30" />
                    </svg>
                  </transition>
                  <transition name="stamp-layer">
                    <svg v-if="(stampProgress.collected || 0) >= 2" viewBox="0 0 100 100" class="absolute inset-0 w-full h-full text-primary fill-current" style="mix-blend-mode: multiply; opacity: 0.8;">
                      <path d="M25 75 L25 45 L50 30 L75 45 L75 75 Z" />
                    </svg>
                  </transition>
                  <transition name="stamp-layer">
                    <svg v-if="(stampProgress.collected || 0) >= 3" viewBox="0 0 100 100" class="absolute inset-0 w-full h-full text-tertiary fill-current" style="mix-blend-mode: multiply; opacity: 0.8;">
                      <circle cx="50" cy="45" r="5" /><rect x="45" y="60" width="10" height="10" />
                    </svg>
                  </transition>
                </template>
                <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/paper-fibers.png')] opacity-20 pointer-events-none"></div>
              </div>
              <div v-if="stampProgress.collected === stampProgress.total && stampProgress.total > 0" class="absolute top-8 right-8 bg-tertiary text-white text-[8px] px-2 py-1 rotate-12 font-bold shadow-lg">
                现世认证
              </div>
            </div>

            <!-- Progress Steps -->
            <div class="space-y-4 mb-8">
              <div 
                v-for="(step, idx) in displaySteps" 
                :key="idx"
                class="flex items-center space-x-4"
                :class="step.is_complete ? 'opacity-100' : 'opacity-30'"
              >
                <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: step.color }"></div>
                <span class="text-xs font-medium" :class="step.is_complete ? 'text-primary' : 'text-secondary'">
                  {{ step.name }} {{ step.is_complete ? '(已完成)' : '(未解锁)' }}
                </span>
              </div>
            </div>

            <p class="text-[10px] text-secondary/40 text-center mb-4">阅读文章并答对题目即可逐层解锁</p>
          </div>
        </div>

      </div>
    </div>

    <!-- Archive Modal -->
    <transition name="modal">
      <div v-if="selectedBuilding" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-on-surface/60 backdrop-blur-md" @click="selectedBuilding = null"></div>
        <div class="relative w-full max-w-4xl bg-white rounded-3xl overflow-hidden shadow-2xl flex flex-col md:flex-row max-h-[90vh]">
          <div class="md:w-1/2 h-64 md:h-auto relative">
            <img :src="selectedBuilding.cover_image || 'https://picsum.photos/seed/default/600/800'" class="w-full h-full object-cover" referrerpolicy="no-referrer" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-8 left-8 text-white">
              <h2 class="font-serif text-4xl mb-2">{{ selectedBuilding.name }}</h2>
              <p class="text-sm opacity-80">{{ selectedBuilding.location }}</p>
            </div>
          </div>
          <div class="md:w-1/2 p-12 overflow-y-auto">
            <div class="flex items-center justify-between mb-8">
              <span class="text-[10px] font-bold text-primary uppercase tracking-widest">档案详情 / Archive</span>
              <button @click="selectedBuilding = null" class="text-secondary/40 hover:text-primary transition-colors">
                <XIcon class="w-6 h-6" />
              </button>
            </div>
            
            <div class="space-y-8">
              <div>
                <h3 class="font-serif text-xl mb-4">{{ selectedBuilding.name }}</h3>
                <p class="text-sm text-secondary/70 leading-relaxed">{{ selectedBuilding.desc }}</p>
              </div>

              <div>
                <h3 class="font-serif text-lg mb-4">详细描述</h3>
                <p class="text-sm text-secondary/70 leading-relaxed">{{ selectedBuilding.full_desc }}</p>
              </div>
              
              <div class="grid grid-cols-2 gap-4">
                <div class="bg-surface p-4 rounded-xl">
                  <p class="text-[10px] font-bold text-secondary/40 uppercase mb-2">建造年代</p>
                  <p class="text-sm font-serif">{{ selectedBuilding.era || '未知' }}</p>
                </div>
                <div class="bg-surface p-4 rounded-xl">
                  <p class="text-[10px] font-bold text-secondary/40 uppercase mb-2">结构类型</p>
                  <p class="text-sm font-serif">{{ selectedBuilding.structure_type || '未知' }}</p>
                </div>
              </div>

              <button 
                v-if="selectedBuilding.has_article"
                @click="startChallenge(selectedBuilding)"
                class="w-full py-4 bg-primary text-white font-bold rounded-xl hover:bg-primary-container transition-all shadow-lg shadow-primary/20 flex items-center justify-center"
              >
                <BookOpenIcon class="w-4 h-4 mr-2" /> 开始挑战
              </button>
              <p v-else class="text-xs text-secondary/40 text-center py-4 border border-dashed border-outline-variant/20 rounded-xl">
                该古建暂无详细文章，敬请期待
              </p>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Explore More Modal -->
    <transition name="modal">
      <div v-if="showAllModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-on-surface/60 backdrop-blur-md" @click="showAllModal = false"></div>
        <div class="relative w-full max-w-5xl bg-white rounded-3xl overflow-hidden shadow-2xl max-h-[90vh] flex flex-col">
          <div class="p-8 border-b border-outline-variant/10 flex items-center justify-between shrink-0">
            <div>
              <h2 class="font-serif text-2xl">所有古建筑</h2>
              <p class="text-[10px] text-secondary/40 font-bold uppercase tracking-widest mt-1">All Monuments</p>
            </div>
            <button @click="showAllModal = false" class="text-secondary/40 hover:text-primary transition-colors">
              <XIcon class="w-6 h-6" />
            </button>
          </div>
          <div class="p-8 overflow-y-auto">
            <div v-if="!allBuildings.length" class="text-center py-12 text-secondary/40 text-sm">暂无古建筑数据</div>
            <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              <div 
                v-for="building in allBuildings" 
                :key="building.id"
                class="group cursor-pointer bg-surface rounded-2xl p-4 hover:bg-primary/5 transition-all"
                @click="showAllModal = false; openArchive(building)"
              >
                <div class="aspect-[4/3] rounded-xl overflow-hidden relative mb-3">
                  <img 
                    :src="building.cover_image || 'https://picsum.photos/seed/default/400/300'" 
                    class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    referrerpolicy="no-referrer"
                  />
                  <div class="absolute top-2 right-2 text-[9px] font-bold px-2 py-0.5 rounded"
                    :class="building.status === 'completed' ? 'bg-tertiary text-white' : building.status === 'in_progress' ? 'bg-primary text-white' : 'bg-white/80 text-secondary'"
                  >{{ statusLabel(building.status) }}</div>
                </div>
                <h4 class="font-serif text-sm font-bold mb-1">{{ building.name }}</h4>
                <p class="text-[10px] text-secondary/50">{{ building.location }} · {{ building.dynasty || building.era }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, inject, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { 
  ArrowRight as ArrowRightIcon, 
  X as XIcon, 
  Compass as CompassIcon,
  BookOpen as BookOpenIcon,
} from 'lucide-vue-next';
import service from '../api/request';

const router = useRouter();
const toggleAuth = inject<(val: boolean) => void>('toggleAuth');

const topBuildings = ref<any[]>([]);
const allBuildings = ref<any[]>([]);
const selectedBuilding = ref<any>(null);
const showAllModal = ref(false);
const stampProgress = ref<any>({});
const stampLayers = ref<any[]>([]);

const dynastyList = ['全部', '唐', '宋', '辽', '金', '元', '明', '清'];

const statusLabel = (status: string) => {
  const map: Record<string, string> = { pending: '未开始', in_progress: '进行中', completed: '已解锁' };
  return map[status] || '未开始';
};

const displaySteps = computed(() => {
  const stamps = stampProgress.value?.stamps;
  if (stamps && stamps.length) {
    const colors = ['#970010', '#624300', '#1a5c3a', '#2a4d8f', '#7b4b94'];
    return stamps.map((s: any, i: number) => ({
      name: s.monument_name || s.name,
      color: colors[i % colors.length],
      is_complete: s.is_complete,
    }));
  }
  return [
    { name: '探索古建筑', color: '#e2e2e2', is_complete: false },
  ];
});

const fetchDiscovery = async () => {
  try {
    const res = await service.get('/api/monuments/discovery/') as any;
    const list = res.results || res;
    topBuildings.value = list.slice(0, 3);
  } catch { /* ignore */ }
};

const fetchAllMonuments = async () => {
  try {
    const res = await service.get('/api/monuments/discovery/', { params: { include_completed: 'true' } }) as any;
    allBuildings.value = res.results || res;
  } catch { /* ignore */ }
};

const fetchStampProgress = async () => {
  try {
    const res = await service.get('/api/stamps/my-overall-progress/') as any;
    stampProgress.value = res;
  } catch {
    stampProgress.value = { collected: 0, total: 0, progress: 0, description: '开始探索古建筑，收集精美印章吧！' };
  }
};

const openArchive = (building: any) => {
  selectedBuilding.value = building;
};

const startChallenge = (building: any) => {
  selectedBuilding.value = null;
  router.push(`/stamps/article/${building.id}`);
};

onMounted(() => {
  if (!localStorage.getItem('access_token')) {
    toggleAuth?.(true);
    return;
  }
  fetchDiscovery();
  fetchAllMonuments();
  fetchStampProgress();
});
</script>

<style scoped>
.vertical-text {
  writing-mode: vertical-rl;
  letter-spacing: 0.2em;
}
.stamp-layer-enter-active {
  transition: all 1s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.stamp-layer-enter-from {
  opacity: 0;
  transform: scale(1.5) rotate(15deg);
}
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.4s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
.modal-enter-active .relative, .modal-leave-active .relative {
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.modal-enter-from .relative, .modal-leave-to .relative {
  transform: scale(0.9) translateY(20px);
}
</style>
