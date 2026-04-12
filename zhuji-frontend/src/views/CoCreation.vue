<template>
  <div class="pt-24 pb-24 bg-surface min-h-screen">
    <div class="container mx-auto px-4">
      <!-- Header -->
      <header class="mb-16 flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div>
          <h1 class="font-serif text-5xl text-primary mb-2">筑品共创</h1>
          <p class="text-secondary/40 text-xs font-bold uppercase tracking-[0.3em]">Collaborative Creation & Modern Heritage</p>
        </div>
        
        <!-- Tab Switcher -->
        <div class="flex bg-white p-1 rounded-xl border border-outline-variant/10 shadow-sm">
          <button 
            v-for="tab in ['众创灵感', '发起创意']" 
            :key="tab"
            class="px-8 py-2.5 rounded-lg text-sm font-bold transition-all"
            :class="activeTab === tab ? 'bg-primary text-white shadow-lg shadow-primary/20' : 'text-secondary/60 hover:text-secondary'"
            @click="activeTab = tab"
          >
            {{ tab }}
          </button>
        </div>
      </header>

      <!-- Tab 1: Inspiration Square (Waterfall Flow) -->
      <div v-if="activeTab === '众创灵感'" class="space-y-12">
        <div class="columns-1 md:columns-2 lg:columns-3 gap-8 space-y-8">
          <div 
            v-for="item in coCreations" 
            :key="item.id"
            class="break-inside-avoid group cursor-pointer"            @click="openDetail(item)"          >
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
                    <span class="text-[10px]">{{ formatLikes(item.likes) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="flex justify-center">
          <button class="px-12 py-4 border border-outline-variant/20 rounded-full text-xs font-bold text-secondary hover:bg-white transition-all flex items-center">
            浏览更多作品 <ChevronDownIcon class="ml-2 w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- Tab 2: Submission Form -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-12">
        <!-- Form -->
        <div class="lg:col-span-7">
          <div class="bg-white rounded-3xl p-12 border border-outline-variant/10 shadow-sm">
            <h2 class="font-serif text-3xl mb-12 flex items-center">
              <PlusCircleIcon class="w-8 h-8 mr-4 text-primary" /> 发起新创意
            </h2>
            
            <form @submit.prevent="handleSubmit" class="space-y-10">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="space-y-3">
                  <label class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest">筑品名称</label>
                  <input 
                    v-model="form.name"
                    type="text" 
                    placeholder="输入作品名称..." 
                    class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-2 focus:ring-primary/20"
                  />
                </div>
                <div class="space-y-3">
                  <label class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest">主材选择</label>
                  <select 
                    v-model="form.material"
                    class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-2 focus:ring-primary/20 appearance-none"
                  >
                    <option value="原木">原木</option>
                    <option value="青砖">青砖</option>
                    <option value="石材">石材</option>
                    <option value="金属">金属</option>
                  </select>
                </div>
              </div>

              <div class="space-y-3">
                <label class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest">创意描述</label>
                <textarea 
                  v-model="form.desc"
                  rows="5" 
                  placeholder="描述你的灵感来源与设计理念..." 
                  class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-2 focus:ring-primary/20 resize-none"
                ></textarea>
              </div>

              <div class="space-y-3">
                <label class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest">封面图</label>
                <div 
                  @click="selectCover"
                  class="w-full h-48 bg-surface border-2 border-dashed border-outline-variant/20 rounded-xl flex flex-col items-center justify-center text-secondary/40 hover:text-primary hover:border-primary/40 transition-all cursor-pointer overflow-hidden"
                >
                  <img v-if="form.coverPreview" :src="form.coverPreview" class="w-full h-full object-cover" />
                  <template v-else>
                    <ImageIcon class="w-8 h-8 mb-2" />
                    <span class="text-[10px] font-bold uppercase">上传封面图</span>
                  </template>
                </div>
              </div>

              <div class="space-y-3">
                <label class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest">灵感图上传</label>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                  <div 
                    v-for="(img, idx) in form.imagePreviews" 
                    :key="idx"
                    class="aspect-square bg-surface rounded-xl overflow-hidden relative group"
                  >
                    <img :src="img" class="w-full h-full object-cover" />
                    <button @click="removeImage(idx)" class="absolute top-2 right-2 bg-on-surface/80 text-white p-1 rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
                      <XIcon class="w-3 h-3" />
                    </button>
                  </div>
                  <button 
                    type="button"
                    @click="addImage"
                    class="aspect-square bg-surface border-2 border-dashed border-outline-variant/20 rounded-xl flex flex-col items-center justify-center text-secondary/40 hover:text-primary hover:border-primary/40 transition-all"
                  >
                    <ImageIcon class="w-6 h-6 mb-2" />
                    <span class="text-[10px] font-bold uppercase">上传图片</span>
                  </button>
                </div>
              </div>

              <button 
                type="submit"

                class="w-full py-5 bg-primary text-white font-bold rounded-xl shadow-xl shadow-primary/20 hover:bg-primary-container transition-all"
              >
                提交申请
              </button>
            </form>
          </div>
        </div>

        <!-- Progress Sidebar -->
        <div class="lg:col-span-5 space-y-8">
          <div class="bg-white rounded-3xl p-8 border border-outline-variant/10 shadow-sm">
            <h3 class="font-serif text-xl mb-8">创意进度</h3>
            
            <div class="space-y-10">
              <div v-for="progress in myProgress" :key="progress.id" class="relative">
                <div class="flex items-start space-x-4 mb-6">
                  <img :src="progress.cover" class="w-16 h-16 rounded-xl object-cover" referrerpolicy="no-referrer" />
                  <div>
                    <h4 class="font-bold text-on-surface mb-1">{{ progress.title }}</h4>
                    <span 
                      class="text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded"
                      :class="progress.status === 'adopted' ? 'bg-green-100 text-green-700' : 'bg-secondary/10 text-secondary/60'"
                    >
                      {{ progress.status === 'adopted' ? '已采纳' : '待审核' }}
                    </span>
                  </div>
                </div>
                
                <!-- Progress Bar -->
                <div class="space-y-4">
                  <div class="flex justify-between text-[10px] font-bold text-secondary/40 uppercase tracking-widest">
                    <span>官方反馈进度</span>
                    <span>{{ progress.progress_percent }}%</span>
                  </div>
                  <div class="w-full h-1.5 bg-secondary/5 rounded-full overflow-hidden">
                    <div 
                      class="h-full bg-primary transition-all duration-1000"
                      :style="{ width: `${progress.progress_percent}%` }"
                    ></div>
                  </div>
                  <div class="flex justify-between text-[9px] text-secondary/40">
                    <span v-for="step in ['提交', '初审', '打样', '投产']" :key="step">{{ step }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-tertiary p-8 rounded-3xl text-white relative overflow-hidden">
            <div class="relative z-10">
              <h3 class="font-serif text-xl mb-4">共创指南</h3>
              <p class="text-xs opacity-80 leading-relaxed mb-8">
                所有被采纳的创意都将进入“筑迹”官方供应链，设计师将获得销售分成及专属“筑匠”勋章。
              </p>
              <button class="text-xs font-bold underline underline-offset-4">查看详细规则</button>
            </div>
            <div class="absolute -bottom-10 -right-10 w-40 h-40 border-8 border-white/5 rounded-full"></div>
          </div>
        </div>
      </div>

    </div>

    <!-- Detail Modal -->
    <IdeaDetailModal 
      v-if="detailVisible" 
      :item="detailItem" 
      @close="detailVisible = false" 
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, inject, onMounted } from 'vue';
import { 
  Heart as HeartIcon, 
  ChevronDown as ChevronDownIcon, 
  PlusCircle as PlusCircleIcon,
  Image as ImageIcon,
  X as XIcon
} from 'lucide-vue-next';
import request from '../api/request';
import IdeaDetailModal from '../components/IdeaDetailModal.vue';

const activeTab = ref('众创灵感');
const toggleAuth = inject<(val: boolean) => void>('toggleAuth');
const form = reactive({
  name: '',
  material: '原木',
  desc: '',
  images: [] as File[],
  imagePreviews: [] as string[],
  cover: null as File | null,
  coverPreview: '' as string,
});

const coCreations = ref<any[]>([]);
const myProgress = ref<any[]>([]);
const loading = ref(false);
const detailVisible = ref(false);
const detailItem = ref<any>(null);

const fetchCoCreations = async () => {
  try {
    const data: any = await request.get('/cocreation/items/');
    coCreations.value = data.results || data;
  } catch (e) {
    console.error('Failed to fetch coCreations:', e);
  }
};

const fetchMyProgress = async () => {
  if (!localStorage.getItem('access_token')) return;
  try {
    const data: any = await request.get('/cocreation/my-progress/');
    myProgress.value = data;
  } catch (e) {
    console.error('Failed to fetch myProgress:', e);
  }
};

onMounted(async () => {
  if (!localStorage.getItem('access_token')) {
    toggleAuth?.(true);
  }
  await fetchCoCreations();
  await fetchMyProgress();
});

const addImage = () => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  input.multiple = true;
  input.onchange = (e: Event) => {
    const files = (e.target as HTMLInputElement).files;
    if (!files) return;
    for (const file of Array.from(files)) {
      form.images.push(file);
      form.imagePreviews.push(URL.createObjectURL(file));
    }
  };
  input.click();
};

const removeImage = (idx: number) => {
  URL.revokeObjectURL(form.imagePreviews[idx]);
  form.images.splice(idx, 1);
  form.imagePreviews.splice(idx, 1);
};

const selectCover = () => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  input.onchange = (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;
    if (form.coverPreview) URL.revokeObjectURL(form.coverPreview);
    form.cover = file;
    form.coverPreview = URL.createObjectURL(file);
  };
  input.click();
};

const formatLikes = (likes: number) => {
  if (likes >= 1000) {
    return (likes / 1000).toFixed(1) + 'k';
  }
  return likes.toString();
};

const openDetail = (item: any) => {
  detailItem.value = item;
  detailVisible.value = true;
};

const handleSubmit = async () => {
  if (!localStorage.getItem('access_token')) {
    toggleAuth?.(true);
    return;
  }
  const fd = new FormData();
  fd.append('title', form.name);
  fd.append('material', form.material);
  fd.append('desc', form.desc);
  if (form.cover) {
    fd.append('cover', form.cover);
  }
  for (const img of form.images) {
    fd.append('images', img);
  }
  try {
    loading.value = true;
    await request.post('/cocreation/items/', fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    alert('创意已提交，请耐心等待官方初审。');
    form.name = '';
    form.desc = '';
    form.images = [];
    form.imagePreviews.forEach(u => URL.revokeObjectURL(u));
    form.imagePreviews = [];
    if (form.coverPreview) URL.revokeObjectURL(form.coverPreview);
    form.cover = null;
    form.coverPreview = '';
    await fetchMyProgress();
  } catch (e) {
    console.error('Failed to submit:', e);
    alert('提交失败，请重试');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Waterfall flow adjustments */
.break-inside-avoid {
  break-inside: avoid;
}
</style>
