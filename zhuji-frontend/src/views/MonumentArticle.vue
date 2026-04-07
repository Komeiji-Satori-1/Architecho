<template>
  <div class="pt-24 pb-24 bg-surface min-h-screen">
    <div class="container mx-auto px-4">

      <!-- Loading -->
      <div v-if="loading" class="text-center py-24">
        <p class="text-secondary/40 text-sm font-bold">正在加载文章...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="text-center py-24">
        <p class="text-secondary/40 text-sm font-bold mb-4">{{ error }}</p>
        <button @click="$router.push('/stamps')" class="px-6 py-2.5 bg-primary text-white text-xs font-bold rounded-xl">返回集章印记</button>
      </div>

      <!-- Article Content -->
      <template v-else-if="article">
        <!-- Header -->
        <div class="max-w-5xl mx-auto mb-12">
          <button @click="$router.push('/stamps')" class="text-[10px] font-bold text-primary uppercase tracking-widest mb-6 flex items-center hover:translate-x-1 transition-transform">
            <ArrowLeftIcon class="w-3 h-3 mr-2" /> 返回集章印记
          </button>
          <h1 class="font-serif text-4xl md:text-5xl mb-4">{{ article.title }}</h1>
          <p class="text-secondary/40 text-xs font-bold uppercase tracking-widest">{{ article.monument_name }} · 详细文章</p>
        </div>

        <div class="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-12">
          <!-- Left: Article Pages -->
          <div class="lg:col-span-8">
            <!-- Current Page Content -->
            <div class="bg-white rounded-2xl p-8 md:p-12 border border-outline-variant/10 shadow-sm mb-8">
              <div class="flex items-center justify-between mb-8">
                <span class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest">
                  第 {{ currentPageIndex + 1 }} / {{ pages.length }} 页
                </span>
                <span class="text-[10px] font-bold text-primary uppercase tracking-widest">
                  {{ article.monument_name }}
                </span>
              </div>

              <div class="prose prose-slate max-w-none text-secondary/80 leading-loose" v-html="currentPage?.content || ''"></div>

              <!-- Page Navigation -->
              <div class="mt-12 pt-8 border-t border-outline-variant/10 flex items-center justify-between">
                <button 
                  v-if="currentPageIndex > 0"
                  @click="goToPrevPage"
                  class="px-6 py-3 bg-surface text-secondary text-sm font-bold rounded-xl hover:bg-secondary/10 transition-all flex items-center"
                >
                  <ArrowLeftIcon class="w-4 h-4 mr-2" /> 上一页
                </button>
                <div v-else></div>

                <button 
                  v-if="currentPageIndex < pages.length - 1"
                  @click="goToNextPage"
                  class="px-6 py-3 bg-primary text-white text-sm font-bold rounded-xl shadow-lg shadow-primary/20 hover:bg-primary-container transition-all flex items-center"
                  :disabled="pageQuizPending"
                >
                  下一页 <ArrowRightIcon class="w-4 h-4 ml-2" />
                </button>
                <div v-else-if="allCompleted" class="flex gap-3">
                  <button 
                    @click="$router.push('/profile?tab=rewards')"
                    class="px-6 py-3 bg-tertiary text-white text-sm font-bold rounded-xl shadow-lg shadow-tertiary/20 flex items-center"
                  >
                    <GiftIcon class="w-4 h-4 mr-2" /> 领取线上奖励
                  </button>
                </div>
              </div>
            </div>

            <!-- Quiz Section (appears between pages) -->
            <transition name="quiz-slide">
              <div v-if="showQuiz && currentQuiz" class="bg-white rounded-2xl p-8 md:p-12 border border-primary/20 shadow-lg mb-8">
                <div class="flex items-center gap-3 mb-8">
                  <div class="px-3 py-1 bg-primary text-white text-[10px] font-bold uppercase tracking-widest rounded">
                    {{ currentQuiz.question_type === 'multi' ? '多选题' : '单选题' }}
                  </div>
                  <span class="text-[10px] text-secondary/40 font-bold">答对 +{{ currentQuiz.points }} 积分</span>
                </div>

                <!-- Question -->
                <p class="text-lg font-serif mb-4">{{ currentQuiz.description }}</p>
                <img v-if="currentQuiz.image" :src="currentQuiz.image" class="w-full max-w-md rounded-xl mb-6" referrerpolicy="no-referrer" />

                <!-- Options -->
                <div class="space-y-3 mb-8">
                  <div 
                    v-for="opt in currentQuiz.options" 
                    :key="opt.id"
                    class="flex items-center gap-4 p-4 rounded-xl border-2 cursor-pointer transition-all"
                    :class="optionClass(opt)"
                    @click="toggleOption(opt)"
                  >
                    <div class="w-6 h-6 rounded-full border-2 flex items-center justify-center shrink-0"
                      :class="isSelected(opt.id) ? 'border-primary bg-primary text-white' : 'border-secondary/20'"
                    >
                      <CheckIcon v-if="isSelected(opt.id)" class="w-3 h-3" />
                    </div>
                    <div class="flex items-center gap-3 flex-grow">
                      <img v-if="opt.image" :src="opt.image" class="w-16 h-16 object-cover rounded-lg" referrerpolicy="no-referrer" />
                      <span class="text-sm">{{ opt.label }}</span>
                    </div>
                  </div>
                </div>

                <!-- Submit -->
                <div v-if="!quizSubmitted" class="flex gap-4">
                  <button 
                    @click="submitQuizAnswer"
                    :disabled="!selectedOptionIds.length || quizSubmitting"
                    class="flex-grow py-4 bg-primary text-white font-bold rounded-xl hover:bg-primary-container transition-all disabled:opacity-50"
                  >
                    {{ quizSubmitting ? '提交中...' : '确认提交' }}
                  </button>
                </div>

                <!-- Result -->
                <div v-else class="p-6 rounded-xl" :class="quizResult?.is_correct ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'">
                  <div class="flex items-center gap-3 mb-2">
                    <CheckCircleIcon v-if="quizResult?.is_correct" class="w-5 h-5 text-green-600" />
                    <XCircleIcon v-else class="w-5 h-5 text-red-600" />
                    <span class="font-bold text-sm" :class="quizResult?.is_correct ? 'text-green-700' : 'text-red-700'">
                      {{ quizResult?.is_correct ? '答对了！匠心独具。' : '回答有误，再接再厉。' }}
                    </span>
                  </div>
                  <p v-if="quizResult?.is_correct" class="text-xs text-green-600">
                    获得 {{ quizResult.points_earned }} 积分
                    <span v-if="quizResult.stamp_unlocked"> · 印章解锁新图层！</span>
                  </p>
                  <button 
                    v-if="currentPageIndex < pages.length - 1"
                    @click="dismissQuizAndNext"
                    class="mt-4 px-6 py-2 bg-primary text-white text-xs font-bold rounded-lg"
                  >继续阅读下一页</button>
                </div>
              </div>
            </transition>
          </div>

          <!-- Right: Stamp Progress -->
          <div class="lg:col-span-4">
            <div class="bg-white rounded-3xl p-8 border border-outline-variant/10 shadow-sm sticky top-24">
              <h2 class="font-serif text-2xl mb-2">套色印记</h2>
              <p class="text-[10px] text-secondary/40 font-bold uppercase tracking-widest mb-8">Color Overlay Stamping</p>
              
              <!-- SVG Stamp Display -->
              <div class="aspect-square bg-surface rounded-2xl mb-8 flex items-center justify-center relative overflow-hidden p-8">
                <div class="relative w-full h-full">
                  <template v-if="stampData.color_layers?.length">
                    <transition v-for="layer in stampData.color_layers" :key="layer.layer_index" name="stamp-layer">
                      <img 
                        v-if="(stampData.collected || 0) >= layer.layer_index && layer.svg_url"
                        :src="layer.svg_url"
                        class="absolute inset-0 w-full h-full object-contain"
                        :style="{ mixBlendMode: layer.blend_mode || 'multiply', opacity: 0.85, filter: 'blur(0.5px)' }"
                      />
                    </transition>
                  </template>
                  <template v-else>
                    <transition name="stamp-layer">
                      <svg v-if="(stampData.collected || 0) >= 1" viewBox="0 0 100 100" class="absolute inset-0 w-full h-full text-secondary/20 fill-current">
                        <path d="M20 80 L20 40 L50 20 L80 40 L80 80 Z" /><rect x="35" y="50" width="30" height="30" />
                      </svg>
                    </transition>
                    <transition name="stamp-layer">
                      <svg v-if="(stampData.collected || 0) >= 2" viewBox="0 0 100 100" class="absolute inset-0 w-full h-full text-primary fill-current" style="mix-blend-mode: multiply; opacity: 0.8;">
                        <path d="M25 75 L25 45 L50 30 L75 45 L75 75 Z" />
                      </svg>
                    </transition>
                    <transition name="stamp-layer">
                      <svg v-if="(stampData.collected || 0) >= 3" viewBox="0 0 100 100" class="absolute inset-0 w-full h-full text-tertiary fill-current" style="mix-blend-mode: multiply; opacity: 0.8;">
                        <circle cx="50" cy="45" r="5" /><rect x="45" y="60" width="10" height="10" />
                      </svg>
                    </transition>
                  </template>
                  <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/paper-fibers.png')] opacity-20 pointer-events-none"></div>
                </div>
                <!-- Completion badge -->
                <div v-if="allCompleted" class="absolute top-6 right-6 bg-tertiary text-white text-[8px] px-2 py-1 rotate-12 font-bold shadow-lg">
                  现世认证
                </div>
              </div>

              <!-- Progress Steps -->
              <div class="space-y-4 mb-8">
                <div 
                  v-for="(step, idx) in stampStepsList" 
                  :key="idx"
                  class="flex items-center space-x-4"
                  :class="(stampData.collected || 0) > idx ? 'opacity-100' : 'opacity-30'"
                >
                  <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: step.color }"></div>
                  <span class="text-xs font-medium" :class="(stampData.collected || 0) === Number(idx) + 1 ? 'text-primary' : 'text-secondary'">
                    {{ step.name }} {{ (stampData.collected || 0) > idx ? '✓' : '' }}
                  </span>
                </div>
              </div>

              <div class="text-center">
                <p class="text-[10px] text-secondary/40 mb-2">进度 {{ stampData.collected || 0 }}/{{ stampData.total || 0 }}</p>
                <div class="w-full h-1.5 bg-secondary/10 rounded-full overflow-hidden">
                  <div class="h-full bg-primary transition-all duration-1000" :style="{ width: (stampData.progress || 0) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- Stamp Completion Celebration -->
    <transition name="modal">
      <div v-if="showCelebration" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-on-surface/70 backdrop-blur-md" @click="showCelebration = false"></div>
        <div class="relative bg-white rounded-3xl p-12 text-center max-w-md shadow-2xl">
          <div class="w-20 h-20 bg-tertiary/10 rounded-full flex items-center justify-center mx-auto mb-6">
            <AwardIcon class="w-10 h-10 text-tertiary" />
          </div>
          <h2 class="font-serif text-3xl mb-4">印章收集完成！</h2>
          <p class="text-sm text-secondary/60 mb-8">恭喜你完成了「{{ article?.monument_name }}」的全部探索，获得精美印章一枚。</p>
          <div class="flex gap-4">
            <button @click="showCelebration = false" class="flex-1 py-3 bg-surface text-secondary font-bold rounded-xl text-sm">继续浏览</button>
            <button @click="$router.push('/profile?tab=rewards')" class="flex-1 py-3 bg-tertiary text-white font-bold rounded-xl text-sm shadow-lg shadow-tertiary/20">
              领取线上奖励
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  ArrowLeft as ArrowLeftIcon,
  ArrowRight as ArrowRightIcon,
  Check as CheckIcon,
  CheckCircle as CheckCircleIcon,
  XCircle as XCircleIcon,
  Gift as GiftIcon,
  Award as AwardIcon,
} from 'lucide-vue-next';
import service from '../api/request';

const route = useRoute();
const router = useRouter();

const loading = ref(true);
const error = ref('');
const article = ref<any>(null);
const pages = ref<any[]>([]);
const currentPageIndex = ref(0);
const stampData = ref<any>({});
const showCelebration = ref(false);

// Quiz state
const showQuiz = ref(false);
const currentQuiz = ref<any>(null);
const selectedOptionIds = ref<number[]>([]);
const quizSubmitted = ref(false);
const quizSubmitting = ref(false);
const quizResult = ref<any>(null);
const answeredPages = ref<Set<number>>(new Set());

const currentPage = computed(() => pages.value[currentPageIndex.value]);
const pageQuizPending = computed(() => {
  const page = currentPage.value;
  if (!page?.quiz_questions?.length) return false;
  return !answeredPages.value.has(page.id);
});

const allCompleted = computed(() => {
  return stampData.value.collected > 0 && stampData.value.collected >= stampData.value.total;
});

const stampStepsList = computed(() => {
  if (stampData.value.color_layers?.length) {
    return stampData.value.color_layers.map((l: any) => ({ name: l.layer_name, color: l.color }));
  }
  return [
    { name: '第一层：素胎底框', color: '#e2e2e2' },
    { name: '第二层：朱砂描红', color: '#970010' },
    { name: '第三层：琉璃缀金', color: '#624300' },
  ];
});

const monumentId = computed(() => Number(route.params.monumentId));

const fetchArticle = async () => {
  try {
    const res = await service.get(`/api/monuments/articles/by-monument/${monumentId.value}/`) as any;
    article.value = res;
    pages.value = (res.pages || []).sort((a: any, b: any) => a.page_number - b.page_number);
  } catch {
    error.value = '该古建暂无详细文章。';
  }
};

const fetchStamp = async () => {
  try {
    const res = await service.get(`/api/stamps/my-progress/monument/${monumentId.value}/`) as any;
    stampData.value = res;
  } catch {
    stampData.value = { collected: 0, total: 0, progress: 0 };
  }
};

const isSelected = (optId: number) => selectedOptionIds.value.includes(optId);

const toggleOption = (opt: any) => {
  if (quizSubmitted.value) return;
  if (currentQuiz.value?.question_type === 'multi') {
    const idx = selectedOptionIds.value.indexOf(opt.id);
    if (idx >= 0) selectedOptionIds.value.splice(idx, 1);
    else selectedOptionIds.value.push(opt.id);
  } else {
    selectedOptionIds.value = [opt.id];
  }
};

const optionClass = (opt: any) => {
  if (quizSubmitted.value) {
    const correctIds: number[] = quizResult.value?.correct_option_ids || [];
    if (correctIds.includes(opt.id)) return 'border-green-400 bg-green-50';
    if (isSelected(opt.id) && !correctIds.includes(opt.id)) return 'border-red-400 bg-red-50';
    return 'border-transparent';
  }
  return isSelected(opt.id) ? 'border-primary bg-primary/5' : 'border-outline-variant/10 hover:border-primary/30';
};

const submitQuizAnswer = async () => {
  if (!currentQuiz.value || !selectedOptionIds.value.length) return;
  quizSubmitting.value = true;
  try {
    const res = await service.post('/api/quiz/submit-answer/', {
      question_id: currentQuiz.value.id,
      selected_option_ids: selectedOptionIds.value,
    }) as any;
    quizResult.value = res;
    quizSubmitted.value = true;
    answeredPages.value.add(currentPage.value.id);

    // Refresh stamp progress
    await fetchStamp();

    // If stamp just completed, show celebration
    if (res.stamp_unlocked && stampData.value.collected >= stampData.value.total) {
      setTimeout(() => { showCelebration.value = true; }, 1500);
    }
  } catch (err: any) {
    const detail = err?.response?.data?.detail || '提交失败';
    alert(detail);
  } finally {
    quizSubmitting.value = false;
  }
};

const goToNextPage = () => {
  const page = currentPage.value;
  // If current page has quiz and not answered, show quiz
  if (page?.quiz_questions?.length && !answeredPages.value.has(page.id)) {
    currentQuiz.value = page.quiz_questions[0];
    selectedOptionIds.value = [];
    quizSubmitted.value = false;
    quizResult.value = null;
    showQuiz.value = true;
    return;
  }
  advanceToNextPage();
};

const advanceToNextPage = () => {
  showQuiz.value = false;
  currentQuiz.value = null;
  if (currentPageIndex.value < pages.value.length - 1) {
    currentPageIndex.value++;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

const goToPrevPage = () => {
  showQuiz.value = false;
  currentQuiz.value = null;
  if (currentPageIndex.value > 0) {
    currentPageIndex.value--;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

const dismissQuizAndNext = () => {
  advanceToNextPage();
};

onMounted(async () => {
  if (!localStorage.getItem('access_token')) {
    router.push('/stamps');
    return;
  }
  await Promise.all([fetchArticle(), fetchStamp()]);
  loading.value = false;
});
</script>

<style scoped>
.stamp-layer-enter-active {
  transition: all 1s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.stamp-layer-enter-from {
  opacity: 0;
  transform: scale(1.5) rotate(15deg);
}
.quiz-slide-enter-active {
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.quiz-slide-enter-from {
  opacity: 0;
  transform: translateY(30px);
}
.quiz-slide-leave-active {
  transition: all 0.3s ease;
}
.quiz-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.4s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
</style>
