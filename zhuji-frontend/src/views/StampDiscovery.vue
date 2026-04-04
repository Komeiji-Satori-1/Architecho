<template>
  <div class="pt-24 pb-24 bg-surface min-h-screen">
    <div class="container mx-auto px-4">
      <!-- Header -->
      <header class="mb-16">
        <h1 class="font-serif text-5xl text-primary mb-2">集章印记</h1>
        <p class="text-secondary/40 text-xs font-bold uppercase tracking-[0.3em]">Stamp Discovery & Architectural Journey</p>
      </header>

      <!-- Discovery Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
        
        <!-- Left: Building Cards -->
        <div class="lg:col-span-8 space-y-12">
          <div class="bg-white/50 rounded-3xl p-8 border border-outline-variant/10">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div 
                v-for="building in buildings" 
                :key="building.id"
                class="group cursor-pointer"
                @click="openArchive(building)"
              >
                <div class="aspect-[3/4] rounded-2xl overflow-hidden relative mb-4 shadow-lg">
                  <img 
                    :src="building.image" 
                    class="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700 group-hover:scale-110"
                    referrerpolicy="no-referrer"
                  />
                  <div class="absolute top-4 right-0 bg-tertiary text-white text-[10px] px-3 py-1 font-bold vertical-text">
                    {{ building.status }}
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

          <!-- Quiz Section -->
          <div class="bg-primary/5 rounded-3xl p-12 border border-primary/10 relative overflow-hidden">
            <div class="relative z-10">
              <div class="inline-block px-3 py-1 bg-primary text-white text-[10px] font-bold uppercase tracking-widest mb-6">Quiz Time</div>
              <h2 class="font-serif text-3xl mb-12">匠心考核：古建识图题</h2>
              
              <div class="bg-white rounded-2xl p-8 shadow-sm border border-outline-variant/10">
                <p class="text-lg font-serif mb-8">1. 下图中展示的斗拱结构中，哪一部分被称为“下昂”？</p>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-10">
                  <div 
                    v-for="(opt, idx) in quizOptions" 
                    :key="idx"
                    class="relative aspect-square rounded-xl overflow-hidden cursor-pointer border-4 transition-all"
                    :class="selectedOption === idx ? 'border-primary' : 'border-transparent'"
                    @click="selectedOption = idx"
                  >
                    <img :src="opt.image" class="w-full h-full object-cover" referrerpolicy="no-referrer" />
                    <div class="absolute top-4 left-4 w-8 h-8 bg-on-surface/80 text-white flex items-center justify-center font-bold rounded">
                      {{ String.fromCharCode(65 + idx) }}
                    </div>
                  </div>
                </div>
                <div class="flex space-x-4">
                  <button 
                    @click="checkAnswer"
                    class="flex-grow py-4 bg-primary text-white font-bold rounded-xl hover:bg-primary-container transition-all"
                  >
                    确认提交
                  </button>
                  <button class="px-8 py-4 bg-secondary/5 text-secondary font-bold rounded-xl hover:bg-secondary/10 transition-all">
                    跳过此题
                  </button>
                </div>
              </div>
            </div>
            <!-- Decorative Pattern -->
            <div class="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full -translate-y-1/2 translate-x-1/2"></div>
          </div>
        </div>

        <!-- Right: Stamp Collection -->
        <div class="lg:col-span-4 space-y-8">
          <div class="bg-white rounded-3xl p-8 border border-outline-variant/10 shadow-sm sticky top-24">
            <h2 class="font-serif text-2xl mb-2">套色印记</h2>
            <p class="text-[10px] text-secondary/40 font-bold uppercase tracking-widest mb-8">Color Overlay Stamping</p>
            
            <!-- SVG Stamp Display -->
            <div class="aspect-square bg-surface rounded-2xl mb-8 flex items-center justify-center relative overflow-hidden p-12">
              <div class="relative w-full h-full">
                <!-- Layer 1: Base Outline -->
                <transition name="stamp-layer">
                  <svg v-if="unlockedLayers >= 1" viewBox="0 0 100 100" class="absolute inset-0 w-full h-full text-secondary/20 fill-current">
                    <path d="M20 80 L20 40 L50 20 L80 40 L80 80 Z" />
                    <rect x="35" y="50" width="30" height="30" />
                  </svg>
                </transition>
                <!-- Layer 2: Red Ink -->
                <transition name="stamp-layer">
                  <svg v-if="unlockedLayers >= 2" viewBox="0 0 100 100" class="absolute inset-0 w-full h-full text-primary fill-current">
                    <path d="M25 75 L25 45 L50 30 L75 45 L75 75 Z" />
                  </svg>
                </transition>
                <!-- Layer 3: Gold Detail -->
                <transition name="stamp-layer">
                  <svg v-if="unlockedLayers >= 3" viewBox="0 0 100 100" class="absolute inset-0 w-full h-full text-tertiary fill-current">
                    <circle cx="50" cy="45" r="5" />
                    <rect x="45" y="60" width="10" height="10" />
                  </svg>
                </transition>
                
                <!-- Seal Texture Overlay -->
                <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/paper-fibers.png')] opacity-20 pointer-events-none"></div>
              </div>
              
              <!-- Floating Label -->
              <div v-if="unlockedLayers === 3" class="absolute top-8 right-8 bg-tertiary text-white text-[8px] px-2 py-1 rotate-12 font-bold shadow-lg">
                现世认证
              </div>
            </div>

            <!-- Progress Steps -->
            <div class="space-y-4 mb-8">
              <div 
                v-for="(step, idx) in stampSteps" 
                :key="idx"
                class="flex items-center space-x-4"
                :class="unlockedLayers > idx ? 'opacity-100' : 'opacity-30'"
              >
                <div 
                  class="w-3 h-3 rounded-full"
                  :style="{ backgroundColor: step.color }"
                ></div>
                <span class="text-xs font-medium" :class="unlockedLayers === idx + 1 ? 'text-primary' : 'text-secondary'">
                  {{ step.name }} {{ unlockedLayers > idx ? '(已完成)' : '(未解锁)' }}
                </span>
              </div>
            </div>

            <button 
              @click="resetStamp"
              class="w-full py-4 bg-on-surface text-white text-xs font-bold uppercase tracking-widest rounded-xl hover:bg-on-surface/90 transition-all flex items-center justify-center"
            >
              <PenIcon class="w-3 h-3 mr-2" /> 执行套色
            </button>
          </div>

          <!-- Collection Stats -->
          <div class="bg-white rounded-3xl p-8 border border-outline-variant/10 shadow-sm">
            <div class="flex items-end justify-between mb-4">
              <div>
                <p class="text-[10px] text-secondary/40 font-bold uppercase tracking-widest mb-1">Collection</p>
                <h3 class="font-serif text-xl">我的集章册</h3>
              </div>
              <span class="text-3xl font-serif text-primary">12/36</span>
            </div>
            <div class="w-full h-1 bg-secondary/10 rounded-full overflow-hidden mb-4">
              <div class="w-1/3 h-full bg-primary"></div>
            </div>
            <p class="text-[10px] text-secondary/60 leading-relaxed">
              你已完成 33% 的古建探索。解锁“琉璃黄”套色需完成佛光寺的全部学习任务。
            </p>
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
            <img :src="selectedBuilding.image" class="w-full h-full object-cover" referrerpolicy="no-referrer" />
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
                <h3 class="font-serif text-xl mb-4">结构拆解</h3>
                <p class="text-sm text-secondary/70 leading-relaxed">
                  {{ selectedBuilding.fullDesc }}
                </p>
              </div>
              
              <div class="grid grid-cols-2 gap-4">
                <div class="bg-surface p-4 rounded-xl">
                  <p class="text-[10px] font-bold text-secondary/40 uppercase mb-2">建造年代</p>
                  <p class="text-sm font-serif">{{ selectedBuilding.era }}</p>
                </div>
                <div class="bg-surface p-4 rounded-xl">
                  <p class="text-[10px] font-bold text-secondary/40 uppercase mb-2">结构类型</p>
                  <p class="text-sm font-serif">{{ selectedBuilding.type }}</p>
                </div>
              </div>

              <button class="w-full py-4 border border-outline-variant/20 rounded-xl text-sm font-bold text-secondary hover:bg-surface transition-all flex items-center justify-center">
                <DownloadIcon class="w-4 h-4 mr-2" /> 下载高清资料
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { 
  ArrowRight as ArrowRightIcon, 
  Pen as PenIcon, 
  X as XIcon, 
  Download as DownloadIcon 
} from 'lucide-react';

const unlockedLayers = ref(1);
const selectedBuilding = ref<any>(null);
const selectedOption = ref<number | null>(null);

const buildings = [
  { 
    id: 1, 
    name: '佛光寺东大殿', 
    location: '山西 · 五台山', 
    status: '进行中', 
    image: 'https://picsum.photos/seed/fg1/600/800',
    desc: '“中国第一国宝”，梁思成林徽因发现的唐代木构建筑巅峰之作。',
    fullDesc: '东大殿雄斗拱雄大，出檐深远。其斗拱高度约等于柱高的二分之一。这种巨大的斗拱不仅是装饰，更是承托屋檐重量、防雨防腐的关键结构。',
    era: '唐大中十一年 (857年)',
    type: '殿堂式木构'
  },
  { 
    id: 2, 
    name: '释迦塔', 
    location: '山西 · 应县', 
    status: '已解锁', 
    image: 'https://picsum.photos/seed/yx1/600/800',
    desc: '世界最高、最古老的纯木结构幕楼式建筑。',
    fullDesc: '应县木塔全塔耗材红松木料3000立方米，重达2600多吨，纯木构、无钉铆。',
    era: '辽清宁二年 (1056年)',
    type: '楼阁式木塔'
  },
  { 
    id: 3, 
    name: '太和殿', 
    location: '北京 · 故宫', 
    status: '未开始', 
    image: 'https://picsum.photos/seed/gg1/600/800',
    desc: '东方建筑等级之极致，琉璃黄与朱砂红的权力交织。',
    fullDesc: '太和殿是紫禁城内体量最大、等级最高的建筑物，建筑规制之高，装饰之华丽，堪称中国古代建筑之首。',
    era: '清康熙三十四年 (1695年)',
    type: '重檐庑殿顶'
  }
];

const quizOptions = [
  { image: 'https://picsum.photos/seed/q1/400/400' },
  { image: 'https://picsum.photos/seed/q2/400/400' }
];

const stampSteps = [
  { name: '第一层：素胎底框', color: '#e2e2e2' },
  { name: '第二层：朱砂描红', color: '#970010' },
  { name: '第三层：琉璃缀金', color: '#624300' }
];

const openArchive = (building: any) => {
  selectedBuilding.value = building;
};

const checkAnswer = () => {
  if (selectedOption.value === 1) { // 假设 B 是正确答案
    alert('答对了！匠心独具。');
    if (unlockedLayers.value < 3) {
      unlockedLayers.value++;
    }
  } else {
    alert('再观察一下，古建筑的结构自有逻辑。');
  }
  selectedOption.value = null;
};

const resetStamp = () => {
  unlockedLayers.value = 1;
};
</script>

<style scoped>
.vertical-text {
  writing-mode: vertical-rl;
  letter-spacing: 0.2em;
}

/* Stamp Layer Animation */
.stamp-layer-enter-active {
  transition: all 1s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.stamp-layer-enter-from {
  opacity: 0;
  transform: scale(1.5) rotate(15deg);
}

/* Modal Animation */
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
