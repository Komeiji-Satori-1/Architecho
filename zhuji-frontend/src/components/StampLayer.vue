<template>
  <div class="relative w-full aspect-square bg-white rounded-2xl p-8 border border-outline-variant/10 shadow-sm overflow-hidden group">
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-[0.03] pointer-events-none">
      <div class="grid grid-cols-6 gap-4 p-4">
        <div v-for="i in 36" :key="i" class="w-full aspect-square border border-on-surface"></div>
      </div>
    </div>

    <div class="relative z-10 h-full flex flex-col">
      <div class="flex items-center justify-between mb-8">
        <div>
          <p class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest mb-1">当前集章进度</p>
          <h3 class="font-serif text-2xl">{{ title }}</h3>
        </div>
        <div class="w-12 h-12 bg-primary/5 rounded-full flex items-center justify-center">
          <StampIcon class="w-6 h-6 text-primary" />
        </div>
      </div>

      <div class="flex-grow flex flex-col justify-center">
        <div class="flex items-end justify-between mb-2">
          <span class="text-4xl font-serif text-primary">{{ progress }}%</span>
          <span class="text-xs text-secondary/60">已收集 {{ collected }}/{{ total }}</span>
        </div>
        <div class="w-full h-2 bg-secondary/10 rounded-full overflow-hidden">
          <div 
            class="h-full bg-primary transition-all duration-1000 ease-out"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
      </div>

      <div class="mt-8 pt-8 border-t border-outline-variant/10">
        <p class="text-xs text-secondary/60 leading-relaxed mb-6">
          {{ description }}
        </p>
        <button 
          @click="handleClick"
          class="text-xs font-bold text-primary flex items-center group-hover:translate-x-2 transition-transform"
        >
          查看进度详情 <ArrowRightIcon class="ml-2 w-3 h-3" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Stamp as StampIcon, ArrowRight as ArrowRightIcon } from 'lucide-react';

defineProps<{
  title: string;
  progress: number;
  collected: number;
  total: number;
  description: string;
}>();

const emit = defineEmits(['click']);

const handleClick = () => {
  emit('click');
  // TODO: 跳转至详情页
};
</script>
