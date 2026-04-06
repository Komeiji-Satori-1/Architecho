<template>
  <div class="relative w-full h-fit bg-white rounded-2xl p-8 border border-outline-variant/10 shadow-sm overflow-hidden group">
    
    <div class="absolute inset-0 opacity-[0.03] pointer-events-none">
      <div class="grid grid-cols-6 gap-4 p-4">
        <div v-for="i in 36" :key="i" class="w-full aspect-square border border-on-surface"></div>
      </div>
    </div>

    <div class="relative z-10 flex flex-col">
      <div class="flex items-center justify-between mb-6">
        <div>
          <p class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest mb-1">当前集章进度</p>
          <h3 class="font-serif text-2xl">{{ title }}</h3>
        </div>
        <div class="w-12 h-12 bg-primary/5 rounded-full flex items-center justify-center shrink-0">
          <StampIcon class="w-6 h-6 text-primary" />
        </div>
      </div>

      <div v-if="showProgress" class="flex flex-col justify-center mb-8">
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

      <div class="pt-6 border-t border-outline-variant/10">
        <div v-if="showProgress" class="flex flex-col justify-center mb-8">
          <p class="text-xs text-secondary/60 leading-relaxed mb-6">
            {{ description }}
          </p>
        </div>
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
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { Stamp as StampIcon, ArrowRight as ArrowRightIcon } from 'lucide-vue-next';

const router = useRouter();

// 接收 Props 并赋值给 props 变量，以便在 computed 中使用
const props = defineProps<{
  title: string;
  progress: number;
  collected: number;
  total: number;
  description: string;
}>();

// 定义显示进度的条件逻辑
const showProgress = computed(() => {
  return props.title !== '暂未开始探索' && props.title !== '未登录';
});
console.log('StampLayer props:', props);
console.log('showProgress:', showProgress.value);
const handleClick = () => {
  router.push('/stamps');
};
</script>