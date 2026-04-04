<template>
  <div class="pt-24 pb-24 bg-surface min-h-screen">
    <div class="container mx-auto px-4">
      <div class="max-w-4xl mx-auto">
        
        <!-- Post Header -->
        <div class="bg-white rounded-2xl p-8 md:p-12 border border-outline-variant/10 shadow-sm mb-8">
          <div class="flex items-center justify-between mb-8">
            <div class="flex items-center space-x-4">
              <div class="relative">
                <img :src="post.authorAvatar" class="w-12 h-12 rounded-full object-cover" referrerpolicy="no-referrer" />
                <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-white rounded-full flex items-center justify-center shadow-sm">
                  <StampIcon class="w-3 h-3 text-primary" />
                </div>
              </div>
              <div>
                <div class="flex items-center">
                  <span class="font-bold text-on-surface mr-2">{{ post.author }}</span>
                  <span class="px-2 py-0.5 bg-secondary/10 text-secondary text-[10px] rounded uppercase tracking-widest">筑匠大师</span>
                </div>
                <p class="text-xs text-secondary/40 uppercase tracking-widest">{{ post.time }} 发布于 {{ post.category }}</p>
              </div>
            </div>
            
            <!-- Admin Actions -->
            <div v-if="isAdmin" class="flex items-center space-x-2">
              <button 
                @click="togglePin"
                class="px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-widest transition-all"
                :class="post.isTop ? 'bg-primary text-white' : 'bg-secondary/5 text-secondary hover:bg-secondary/10'"
              >
                {{ post.isTop ? '取消置顶' : '置顶' }}
              </button>
              <button 
                @click="toggleEssence"
                class="px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-widest transition-all"
                :class="post.isEssence ? 'bg-tertiary text-white' : 'bg-secondary/5 text-secondary hover:bg-secondary/10'"
              >
                {{ post.isEssence ? '取消加精' : '加精' }}
              </button>
              <button 
                @click="handleDelete"
                class="px-3 py-1.5 bg-red-50 text-red-600 rounded-lg text-[10px] font-bold uppercase tracking-widest hover:bg-red-100 transition-all"
              >
                删除
              </button>
            </div>
          </div>

          <h1 class="font-serif text-3xl md:text-5xl mb-8 leading-tight">{{ post.title }}</h1>
          
          <!-- Rich Text Content Placeholder -->
          <div class="prose prose-slate max-w-none text-secondary/80 leading-loose space-y-6">
            <p v-for="(p, i) in post.content" :key="i">{{ p }}</p>
            <div v-if="post.images" class="grid grid-cols-1 gap-4 py-8">
              <img 
                v-for="(img, idx) in post.images" 
                :key="idx" 
                :src="img" 
                class="w-full rounded-2xl shadow-lg"
                referrerpolicy="no-referrer"
              />
            </div>
          </div>

          <div class="mt-12 pt-12 border-t border-outline-variant/10 flex items-center justify-between">
            <div class="flex items-center space-x-8">
              <button class="flex items-center text-secondary/40 hover:text-primary transition-colors">
                <HeartIcon class="w-5 h-5 mr-2" /> <span class="text-sm">{{ post.likes }}</span>
              </button>
              <button class="flex items-center text-secondary/40 hover:text-primary transition-colors">
                <ShareIcon class="w-5 h-5 mr-2" /> <span class="text-sm">分享</span>
              </button>
            </div>
            <div class="text-xs text-secondary/40 uppercase tracking-widest">
              最后编辑于 {{ post.lastEdit }}
            </div>
          </div>
        </div>

        <!-- Comment Section -->
        <div class="bg-white rounded-2xl p-8 md:p-12 border border-outline-variant/10 shadow-sm">
          <h2 class="font-serif text-2xl mb-10 flex items-center">
            <MessageSquareIcon class="w-6 h-6 mr-3 text-primary" /> 见解 ({{ comments.length }})
          </h2>

          <!-- Comment Input with Cache -->
          <div class="mb-12">
            <div class="bg-surface rounded-xl p-4 border border-outline-variant/10">
              <textarea 
                v-model="commentInput"
                placeholder="执笔绘筑，共话千年..." 
                class="w-full bg-transparent border-none focus:ring-0 text-sm min-h-[120px] resize-none"
                @input="saveDraft"
              ></textarea>
              <div class="flex items-center justify-between mt-4 pt-4 border-t border-outline-variant/5">
                <div class="flex items-center space-x-4 text-secondary/40">
                  <ImageIcon class="w-4 h-4 cursor-pointer hover:text-primary" />
                  <LinkIcon class="w-4 h-4 cursor-pointer hover:text-primary" />
                  <AtSignIcon class="w-4 h-4 cursor-pointer hover:text-primary" />
                </div>
                <button 
                  @click="submitComment"
                  class="px-8 py-2.5 bg-primary text-white text-sm font-bold rounded-lg hover:bg-primary-container transition-all shadow-md shadow-primary/10"
                >
                  发布见解
                </button>
              </div>
            </div>
            <p v-if="hasDraft" class="text-[10px] text-primary/60 mt-2 italic">已自动保存草稿</p>
          </div>

          <!-- Comment List -->
          <div class="space-y-10">
            <div v-for="comment in comments" :key="comment.id" class="group">
              <div class="flex items-start space-x-4">
                <img :src="comment.avatar" class="w-10 h-10 rounded-full object-cover" referrerpolicy="no-referrer" />
                <div class="flex-grow">
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center">
                      <span class="text-sm font-bold text-on-surface mr-2">{{ comment.author }}</span>
                      <StampIcon class="w-3 h-3 text-primary/40" />
                    </div>
                    <span class="text-[10px] text-secondary/40 uppercase tracking-widest">{{ comment.time }}</span>
                  </div>
                  <p class="text-sm text-secondary/80 leading-relaxed mb-4">{{ comment.text }}</p>
                  
                  <div class="flex items-center space-x-6 text-[10px] font-bold text-secondary/40 uppercase tracking-widest">
                    <button class="hover:text-primary transition-colors">赞同 ({{ comment.likes }})</button>
                    <button class="hover:text-primary transition-colors" @click="replyTo(comment)">回复</button>
                    <button v-if="isAdmin" class="text-red-400 hover:text-red-600 transition-colors">删除</button>
                  </div>

                  <!-- Nested Replies (Level 2) -->
                  <div v-if="comment.replies && comment.replies.length" class="mt-6 space-y-6 pl-6 border-l-2 border-outline-variant/5">
                    <div v-for="reply in comment.replies" :key="reply.id" class="flex items-start space-x-3">
                      <img :src="reply.avatar" class="w-8 h-8 rounded-full object-cover" referrerpolicy="no-referrer" />
                      <div>
                        <div class="flex items-center space-x-2 mb-1">
                          <span class="text-xs font-bold text-on-surface">{{ reply.author }}</span>
                          <span class="text-[10px] text-secondary/40">回复</span>
                          <span class="text-xs font-bold text-primary">{{ comment.author }}</span>
                        </div>
                        <p class="text-xs text-secondary/70 leading-relaxed">{{ reply.text }}</p>
                        <div class="mt-2 flex items-center space-x-4 text-[9px] font-bold text-secondary/30 uppercase tracking-widest">
                          <span>{{ reply.time }}</span>
                          <button class="hover:text-primary">赞同</button>
                          <button class="hover:text-primary">回复</button>
                        </div>
                      </div>
                    </div>
                  </div>

                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { 
  Heart as HeartIcon, 
  Share as ShareIcon, 
  MessageSquare as MessageSquareIcon,
  Stamp as StampIcon,
  Image as ImageIcon,
  Link as LinkIcon,
  AtSign as AtSignIcon
} from 'lucide-react';

const route = useRoute();
const router = useRouter();
const isAdmin = ref(true); // 模拟管理员权限
const commentInput = ref('');
const hasDraft = ref(false);

const post = ref({
  id: route.params.id,
  title: '解析《营造法式》中的斗拱模数化设计',
  author: '营造大师_老李',
  authorAvatar: 'https://picsum.photos/seed/user1/100/100',
  category: '营造法式',
  time: '2024-03-20',
  lastEdit: '2024-03-21 14:30',
  likes: 856,
  isTop: true,
  isEssence: true,
  content: [
    '《营造法式》作为中国古代建筑的巅峰之作，其核心灵魂在于“材份制”。这不仅是一套比例系统，更是一套高度模数化的设计语言。',
    '在斗拱的构造中，每一块木料的尺寸都与“材”的等级紧密相连。这种设计确保了即便是在千里之外，工匠们也能根据同一套图纸，精准地复刻出结构严密的建筑。',
    '通过对十一踩斗拱的受力分析，我们可以发现，古人巧妙地利用了木材的韧性与榫卯的柔性连接，实现了极佳的抗震性能。'
  ],
  images: [
    'https://picsum.photos/seed/arch1/1200/800',
    'https://picsum.photos/seed/arch2/1200/800'
  ]
});

const comments = ref([
  {
    id: 1,
    author: '云栖墨客',
    avatar: 'https://picsum.photos/seed/u1/100/100',
    time: '2小时前',
    text: '老李的文章总能切中要害。材份制确实是理解中国古建的钥匙。',
    likes: 24,
    replies: [
      {
        id: 101,
        author: '木构灵魂',
        avatar: 'https://picsum.photos/seed/u2/100/100',
        time: '1小时前',
        text: '同意。而且这种模数化思维，其实与现代的BIM技术有异曲同工之妙。'
      }
    ]
  },
  {
    id: 2,
    author: '丹青绘影',
    avatar: 'https://picsum.photos/seed/u3/100/100',
    time: '5小时前',
    text: '期待下一篇关于彩画等级的解析！',
    likes: 12,
    replies: []
  }
]);

onMounted(() => {
  const cached = localStorage.getItem(`post_draft_${route.params.id}`);
  if (cached) {
    commentInput.value = cached;
    hasDraft.value = true;
  }
});

const saveDraft = () => {
  if (commentInput.value) {
    localStorage.setItem(`post_draft_${route.params.id}`, commentInput.value);
    hasDraft.value = true;
  } else {
    localStorage.removeItem(`post_draft_${route.params.id}`);
    hasDraft.value = false;
  }
};

const submitComment = () => {
  if (!commentInput.value.trim()) return;
  
  console.log('Submitting comment:', commentInput.value);
  // TODO: 实现真实提交逻辑
  
  localStorage.removeItem(`post_draft_${route.params.id}`);
  commentInput.value = '';
  hasDraft.value = false;
  alert('见解已发布！');
};

const togglePin = () => {
  post.value.isTop = !post.value.isTop;
};

const toggleEssence = () => {
  post.value.isEssence = !post.value.isEssence;
};

const handleDelete = () => {
  if (confirm('确定要删除这篇传世之作吗？')) {
    console.log('Post deleted');
    router.push('/forum');
  }
};

const replyTo = (comment: any) => {
  commentInput.value = `@${comment.author} `;
  saveDraft();
};
</script>

<style scoped>
@reference "tailwindcss";

.prose p {
  @apply mb-6;
}
</style>
