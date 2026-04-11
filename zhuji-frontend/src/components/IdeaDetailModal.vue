<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-center justify-center" @click.self="$emit('close')">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>

      <!-- Modal Content -->
      <div class="relative bg-white rounded-3xl max-w-2xl w-full mx-4 max-h-[85vh] overflow-y-auto shadow-2xl">
        <!-- Close Button -->
        <button 
          @click="$emit('close')" 
          class="absolute top-6 right-6 z-10 w-10 h-10 bg-surface rounded-full flex items-center justify-center hover:bg-secondary/10 transition-colors"
        >
          <XIcon class="w-5 h-5 text-secondary" />
        </button>

        <!-- Cover Image -->
        <div v-if="item.cover" class="w-full h-64 overflow-hidden rounded-t-3xl">
          <img :src="item.cover" class="w-full h-full object-cover" referrerpolicy="no-referrer" />
        </div>

        <div class="p-10">
          <!-- Header -->
          <div class="flex items-start justify-between mb-8">
            <div>
              <h2 class="font-serif text-3xl text-on-surface mb-2">{{ item.title }}</h2>
              <div class="flex items-center space-x-3">
                <img v-if="item.avatar" :src="item.avatar" class="w-6 h-6 rounded-full" referrerpolicy="no-referrer" />
                <span class="text-xs text-secondary/60">{{ item.author }}</span>
                <span 
                  class="text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded"
                  :class="item.status === 'adopted' ? 'bg-green-100 text-green-700' : 'bg-secondary/10 text-secondary/60'"
                >
                  {{ item.status_display }}
                </span>
              </div>
            </div>
            <div class="flex items-center space-x-1 text-secondary/40">
              <HeartIcon class="w-4 h-4" />
              <span class="text-sm">{{ item.likes }}</span>
            </div>
          </div>

          <!-- Material Tag -->
          <div class="mb-6">
            <span class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest">主材</span>
            <span class="ml-2 px-3 py-1 bg-tertiary/10 text-tertiary text-xs font-bold rounded-full">{{ item.material }}</span>
          </div>

          <!-- Description -->
          <div class="mb-8">
            <h3 class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest mb-3">设计初衷</h3>
            <p class="text-sm text-secondary/80 leading-relaxed whitespace-pre-wrap">{{ item.desc }}</p>
          </div>

          <!-- Progress -->
          <div v-if="item.progress_percent !== undefined" class="mb-8">
            <div class="flex justify-between text-[10px] font-bold text-secondary/40 uppercase tracking-widest mb-2">
              <span>官方反馈进度</span>
              <span>{{ item.progress_percent }}%</span>
            </div>
            <div class="w-full h-1.5 bg-secondary/5 rounded-full overflow-hidden">
              <div class="h-full bg-primary transition-all duration-1000" :style="{ width: `${item.progress_percent}%` }"></div>
            </div>
            <div class="flex justify-between text-[9px] text-secondary/40 mt-2">
              <span v-for="step in ['提交', '初审', '打样', '投产']" :key="step">{{ step }}</span>
            </div>
          </div>

          <!-- Featured Badge -->
          <div v-if="item.featured" class="inline-block px-4 py-2 bg-primary/10 text-primary text-xs font-bold rounded-full">
            本周精选
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { X as XIcon, Heart as HeartIcon } from 'lucide-vue-next';

defineProps<{
  item: {
    id: number;
    title: string;
    author: string;
    avatar?: string;
    cover?: string;
    material: string;
    desc: string;
    featured: boolean;
    likes: number;
    status: string;
    status_display: string;
    progress_percent: number;
  };
}>();

defineEmits(['close']);
</script>
