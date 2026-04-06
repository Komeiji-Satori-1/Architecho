<template>
  <div class="min-h-screen bg-[#F9F8F4] font-serif">
    <!-- 顶部导航栏 -->
    <nav class="fixed top-0 w-full h-16 flex items-center justify-between px-8 bg-white/30 backdrop-blur-md z-50 border-b border-secondary/5">
      <button @click="goBack" class="flex items-center gap-2 text-secondary/60 hover:text-primary transition-colors">
        <ArrowLeftIcon class="w-4 h-4" />
        <span class="text-sm tracking-widest">返回筑迹</span>
      </button>
      <div class="flex items-center gap-6">
        <span class="text-xs text-secondary/30 tracking-tighter italic">"凡构屋之制，皆以材为祖"</span>
        <button
          @click="handlePublish"
          :disabled="publishing || !title.trim() || !content.trim()"
          class="px-8 py-2 bg-primary text-white rounded-full text-sm font-bold active:scale-95 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {{ publishing ? '发布中…' : '发布' }}
        </button>
      </div>
    </nav>

    <!-- 主体内容 -->
    <main class="max-w-3xl mx-auto pt-32 px-6 pb-32">

      <!-- 标题 -->
      <textarea
        v-model="title"
        placeholder="在此输入标题..."
        rows="1"
        @input="autoResize($event)"
        class="w-full bg-transparent text-4xl font-bold placeholder:text-secondary/10 outline-none resize-none leading-tight tracking-tight text-secondary"
      ></textarea>

      <!-- 分类 & 标签行 -->
      <div class="flex items-center gap-4 mt-8 mb-12">
        <select
          v-model="selectedCategory"
          class="bg-transparent border-b border-primary/20 text-sm py-1 outline-none text-primary cursor-pointer"
        >
          <option value="">选择板块</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>
        <span class="text-secondary/20">|</span>
        <input
          v-model="excerpt"
          type="text"
          placeholder="添加摘要（选填，留空自动截取）..."
          class="bg-transparent text-sm outline-none placeholder:text-secondary/20 flex-1 text-secondary"
        />
      </div>

      <!-- 封面图上传 -->
      <div
        class="w-full aspect-video bg-stone-100/50 border-2 border-dashed border-secondary/10 rounded-2xl flex flex-col items-center justify-center group hover:border-primary/20 transition-colors cursor-pointer mb-12 overflow-hidden"
        @click="triggerCoverUpload"
      >
        <img v-if="coverPreview" :src="coverPreview" class="w-full h-full object-cover" />
        <template v-else>
          <ImageIcon class="w-8 h-8 text-secondary/20 group-hover:text-primary/40 transition-colors" />
          <p class="mt-4 text-xs text-secondary/30 tracking-widest">点击上传古建影像（选填）</p>
        </template>
        <input
          ref="coverInputRef"
          type="file"
          accept="image/*"
          class="hidden"
          @change="handleCoverChange"
        />
      </div>

      <!-- 正文 -->
      <textarea
        v-model="content"
        placeholder="记录你的发现...&#10;&#10;分享你对这处古建的所思所感，让更多筑匠看见这片历史遗珠。"
        class="w-full min-h-[500px] bg-transparent text-lg leading-loose outline-none resize-none placeholder:text-secondary/10 text-secondary"
      ></textarea>

      <!-- 字数提示 -->
      <div class="flex justify-between items-center mt-8 pt-6 border-t border-secondary/5 text-xs text-secondary/30">
        <span>{{ content.length }} 字</span>
        <span v-if="errorMsg" class="text-red-400">{{ errorMsg }}</span>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ArrowLeft as ArrowLeftIcon, Image as ImageIcon } from 'lucide-vue-next';

const router = useRouter();

// ─── 表单数据 ──
const title = ref('');
const content = ref('');
const excerpt = ref('');
const selectedCategory = ref<number | ''>('');
const coverFile = ref<File | null>(null);
const coverPreview = ref('');
const publishing = ref(false);
const errorMsg = ref('');

// ─── 板块列表 ──
const categories = ref<{ id: number; name: string }[]>([]);

onMounted(async () => {
  // 验证登录
  if (!localStorage.getItem('access_token')) {
    router.replace('/forum');
    return;
  }
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/forum/categories/');
    categories.value = res.data.results ?? res.data;
  } catch {
    categories.value = [];
  }
});

// ─── 封面图 ──
const coverInputRef = ref<HTMLInputElement | null>(null);

const triggerCoverUpload = () => {
  coverInputRef.value?.click();
};

const handleCoverChange = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;
  coverFile.value = file;
  coverPreview.value = URL.createObjectURL(file);
};

// ─── 标题自动行高 ──
const autoResize = (e: Event) => {
  const el = e.target as HTMLTextAreaElement;
  el.style.height = 'auto';
  el.style.height = el.scrollHeight + 'px';
};

// ─── 发布 ──
const handlePublish = async () => {
  errorMsg.value = '';
  if (!title.value.trim()) { errorMsg.value = '请填写标题'; return; }
  if (!content.value.trim()) { errorMsg.value = '请填写正文'; return; }

  publishing.value = true;
  try {
    const token = localStorage.getItem('access_token');
    const formData = new FormData();
    formData.append('title', title.value.trim());
    formData.append('content', content.value.trim());
    // 摘要：有填则用，没有则截取正文前80字
    formData.append('excerpt', excerpt.value.trim() || content.value.trim().slice(0, 80));
    if (selectedCategory.value) {
      formData.append('category', String(selectedCategory.value));
    }
    if (coverFile.value) {
      formData.append('cover', coverFile.value);
    }

    const res = await axios.post('http://127.0.0.1:8000/api/forum/posts/', formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    });

    // 发布成功 → 跳转到帖子详情页
    router.push(`/forum/${res.data.id}`);
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || '发布失败，请稍后重试';
  } finally {
    publishing.value = false;
  }
};

const goBack = () => {
  router.back();
};
</script>
