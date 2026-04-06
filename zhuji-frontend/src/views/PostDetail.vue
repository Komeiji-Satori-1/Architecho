<template>
  <div class="pt-24 pb-24 bg-surface min-h-screen">
    <div class="container mx-auto px-4">
      <div class="max-w-4xl mx-auto">
        
        <!-- Post Header -->
        <div class="bg-white rounded-2xl p-8 md:p-12 border border-outline-variant/10 shadow-sm mb-8">
          <div class="flex items-center justify-between mb-8">
            <div class="flex items-center space-x-4">
              <div class="relative">
                <img :src="post.author_avatar" class="w-12 h-12 rounded-full object-cover" referrerpolicy="no-referrer" />
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
                :class="post.is_top ? 'bg-primary text-white' : 'bg-secondary/5 text-secondary hover:bg-secondary/10'"
              >
                {{ post.is_top ? '取消置顶' : '置顶' }}
              </button>
              <button 
                @click="toggleEssence"
                class="px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-widest transition-all"
                :class="post.is_essence ? 'bg-tertiary text-white' : 'bg-secondary/5 text-secondary hover:bg-secondary/10'"
              >
                {{ post.is_essence ? '取消加精' : '加精' }}
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
              <button @click="handleLike" class="flex items-center text-secondary/40 hover:text-primary transition-colors">
                <HeartIcon class="w-5 h-5 mr-2" /> <span class="text-sm">{{ post.likes }}</span>
              </button>
              <button @click="handleShare" class="flex items-center text-secondary/40 hover:text-primary transition-colors">
                <ShareIcon class="w-5 h-5 mr-2" /> <span class="text-sm">分享</span>
              </button>
            </div>
            <div class="text-xs text-secondary/40 uppercase tracking-widest">
              最后编辑于 {{ post.last_edit }}
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

              <!-- 评论图片预览 -->
              <div v-if="commentImages.length" class="flex flex-wrap gap-2 mt-3">
                <div
                  v-for="(img, idx) in commentImages"
                  :key="idx"
                  class="relative w-16 h-16 rounded-lg overflow-hidden group"
                >
                  <img :src="img.preview" class="w-full h-full object-cover" />
                  <button
                    @click="removeCommentImage(idx)"
                    class="absolute inset-0 bg-black/40 text-white text-xs flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                  >&#x2715;</button>
                </div>
                <div
                  v-if="commentImages.length < 5"
                  @click="triggerCommentImageUpload"
                  class="w-16 h-16 rounded-lg border-2 border-dashed border-secondary/10 flex items-center justify-center cursor-pointer hover:border-primary/20 transition-colors text-secondary/30 text-lg"
                >+</div>
              </div>

              <div class="flex items-center justify-between mt-4 pt-4 border-t border-outline-variant/5">
                <div class="flex items-center space-x-4 text-secondary/40">
                  <ImageIcon
                    class="w-4 h-4 cursor-pointer hover:text-primary transition-colors"
                    @click="triggerCommentImageUpload"
                    :class="commentImages.length >= 5 ? 'opacity-30 cursor-not-allowed' : ''"
                  />
                  <LinkIcon class="w-4 h-4 cursor-pointer hover:text-primary" />
                  <AtSignIcon class="w-4 h-4 cursor-pointer hover:text-primary" />
                  <span v-if="commentImages.length" class="text-[10px] text-primary/60">{{ commentImages.length }}/5 张图片</span>
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
            <!-- 隐藏的图片上传输入 -->
            <input
              ref="commentImageInputRef"
              type="file"
              accept="image/*"
              multiple
              class="hidden"
              @change="handleCommentImageChange"
            />
          </div>

          <!-- Comment List -->
          <div class="space-y-10">
            <div v-for="comment in comments" :key="comment.id" class="group">
              <div class="flex items-start space-x-4">
                <img :src="comment.author_avatar" class="w-10 h-10 rounded-full object-cover" referrerpolicy="no-referrer" />
                <div class="flex-grow">
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center">
                      <span class="text-sm font-bold text-on-surface mr-2">{{ comment.author }}</span>
                      <StampIcon class="w-3 h-3 text-primary/40" />
                    </div>
                    <span class="text-[10px] text-secondary/40 uppercase tracking-widest">{{ comment.time }}</span>
                  </div>
                  <p class="text-sm text-secondary/80 leading-relaxed mb-4">{{ comment.text }}</p>
                  
                  <!-- 评论配图 -->
                  <div v-if="comment.images && comment.images.length" class="flex flex-wrap gap-2 mb-4">
                    <img
                      v-for="(img, idx) in comment.images"
                      :key="idx"
                      :src="img.image_url"
                      class="w-24 h-24 object-cover rounded-lg cursor-pointer hover:opacity-90 transition-opacity"
                      referrerpolicy="no-referrer"
                    />
                  </div>

                  <div class="flex items-center space-x-6 text-[10px] font-bold text-secondary/40 uppercase tracking-widest">
                    <button @click="handleCommentLike" class="hover:text-primary transition-colors">赞同 ({{ comment.likes }})</button>
                    <button class="hover:text-primary transition-colors" @click="replyTo(comment)">回复</button>
                    <button
                      v-if="canDeleteComment(comment)"
                      class="text-red-400 hover:text-red-600 transition-colors"
                      @click="deleteComment(comment)"
                    >删除</button>
                  </div>

                  <!-- Nested Replies (Level 2) -->
                  <div v-if="comment.replies && comment.replies.length" class="mt-6 space-y-6 pl-6 border-l-2 border-outline-variant/5">
                    <div v-for="reply in comment.replies" :key="reply.id" class="flex items-start space-x-3">
                      <img :src="reply.author_avatar" class="w-8 h-8 rounded-full object-cover" referrerpolicy="no-referrer" />
                      <div>
                        <div class="flex items-center space-x-2 mb-1">
                          <span class="text-xs font-bold text-on-surface">{{ reply.author }}</span>
                          <span class="text-[10px] text-secondary/40">回复</span>
                          <span class="text-xs font-bold text-primary">{{ comment.author }}</span>
                        </div>
                        <p class="text-xs text-secondary/70 leading-relaxed">{{ reply.text }}</p>
                        <div class="mt-2 flex items-center space-x-4 text-[9px] font-bold text-secondary/30 uppercase tracking-widest">
                          <span>{{ reply.time }}</span>
                          <button class="hover:text-primary" @click="handleCommentLike">赞同</button>
                          <button class="hover:text-primary" @click="replyTo(reply)">回复</button>
                          <button
                            v-if="canDeleteComment(reply)"
                            class="text-red-400 hover:text-red-500"
                            @click="deleteReply(comment, reply)"
                          >删除</button>
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
import { ref, inject, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios'; // 确保已安装 axios
import { 
  Heart as HeartIcon, 
  Share as ShareIcon, 
  MessageSquare as MessageSquareIcon,
  Stamp as StampIcon,
  Image as ImageIcon,
  Link as LinkIcon,
  AtSign as AtSignIcon
} from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();
const toggleAuth = inject<(val: boolean) => void>('toggleAuth');

// 权限校验
const requireAuth = (callback: () => void) => {
  if (!localStorage.getItem('access_token')) {
    toggleAuth?.(true);
    return;
  }
  callback();
};

const currentUser = ref<{ username: string; role: string } | null>(null);
const isAdmin = computed(() => currentUser.value?.role === 'superadmin');
const commentInput = ref('');
const hasDraft = ref(false);
const commentImages = ref<{ file: File; preview: string }[]>([]);
const commentImageInputRef = ref<HTMLInputElement | null>(null);
const loading = ref(true);

const is_top = ref(false);
const is_essence = ref(false);

// 1. 初始化数据结构（对应后端 Serializer）
const post = ref<any>({
  id: null,
  title: '',
  author: '',
  author_avatar: '',
  category: '',
  time: '',
  last_edit: '',
  likes: 0,
  is_top: false,
  is_essence: false,
  content: [],
  cover: null,
  comment_count: 0,
  images: []
});

const comments = ref<any[]>([]);

// 2. 获取数据逻辑
const fetchPostDetail = async () => {
  try {
    loading.value = true;
    const res = await axios.get(`/api/forum/posts/${route.params.id}/`);
    const data = res.data;
    console.log('后端返回的原始数据:', res.data);
    // 处理后端 content (TextField) 转为前端数组
    // 如果后端存的是富文本，建议直接用 v-html；如果是纯文本换行，则 split
    if (typeof data.content === 'string') {
      data.content = data.content.split('\n').filter((p: string) => p.trim() !== '');
    }

    post.value = data;
    console.log('当前帖子图片列表:', post.value.images);
  } catch (error) {
    console.error('获取帖子失败:', error);
  } finally {
    loading.value = false;
  }
};

const fetchComments = async () => {
  try {
    // 假设评论接口为 /api/forum/comments/?post=id
    const res = await axios.get('/api/forum/comments/', { 
      params: { post: route.params.id } 
    });
    comments.value = res.data.results || res.data;
    console.log('处理后的评论列表:', comments.value);
  } catch (error) {
    console.error('获取评论失败:', error);
  }
};

onMounted(async () => {
  fetchPostDetail();
  fetchComments();

  const cached = localStorage.getItem(`post_draft_${route.params.id}`);
  if (cached) {
    commentInput.value = cached;
    hasDraft.value = true;
  }

  const token = localStorage.getItem('access_token');
  if (token) {
    try {
      const res = await axios.get('/api/users/me/');
      currentUser.value = res.data;
    } catch {}
  }
});

// 3. 管理员操作 (Patch 请求)
const updatePostStatus = async (payload: object) => {
  try {
    const res = await axios.patch(`/api/forum/posts/${post.value.id}/`, payload);
    // 局部更新本地数据
    Object.assign(post.value, res.data);
  } catch (error) {
    alert('操作失败');
  }
};

const togglePin = () => requireAuth(() => {
  updatePostStatus({ is_top: !post.value.is_top });
});

const toggleEssence = () => requireAuth(() => {
  updatePostStatus({ is_essence: !post.value.is_essence });
});

const handleShare = () => {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(window.location.href);
    alert('链接已复制！');
  }
};

const handleCommentLike = () => requireAuth(() => {});

// 4. 互动操作
const handleLike = async () => requireAuth(async () => {
  try {
    // 假设后端 ViewSet 有自定义 action 'like'
    await axios.post(`/api/forum/posts/${post.value.id}/like/`);
    post.value.likes++;
  } catch (error) {
    console.error('点赞失败');
  }
});

const handleDelete = () => requireAuth(async () => {
  if (confirm('确定要删除这篇作品吗？')) {
    await axios.delete(`/api/forum/posts/${post.value.id}/`);
    router.push('/forum');
  }
});

// 5. 评论逻辑
const submitComment = async () => {
  requireAuth(async () => {
    if (!commentInput.value.trim()) return;
    try {
      const res = await axios.post('/api/forum/comments/', {
        post: post.value.id,
        text: commentInput.value
      });
      // 上传评论图片（仅一级评论支持）
      if (commentImages.value.length) {
        const formData = new FormData();
        commentImages.value.forEach((img) => formData.append('images', img.file));
        await axios.post(`/api/forum/comments/${res.data.id}/images/`, formData, {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });
        commentImages.value.forEach((img) => URL.revokeObjectURL(img.preview));
        commentImages.value = [];
      }
      fetchComments();
      localStorage.removeItem(`post_draft_${route.params.id}`);
      commentInput.value = '';
      hasDraft.value = false;
    } catch (error) {
      alert('发布失败');
    }
  });
};

const saveDraft = () => {
  if (commentInput.value) {
    localStorage.setItem(`post_draft_${route.params.id}`, commentInput.value);
    hasDraft.value = true;
  } else {
    localStorage.removeItem(`post_draft_${route.params.id}`);
    hasDraft.value = false;
  }
};

const replyTo = (comment: any) => {
  requireAuth(() => {
    commentInput.value = `@${comment.author} `;
    saveDraft();
  });
};

// 6. 评论图片上传辅助
const triggerCommentImageUpload = () => {
  if (commentImages.value.length >= 5) return;
  commentImageInputRef.value?.click();
};

const handleCommentImageChange = (e: Event) => {
  const files = Array.from((e.target as HTMLInputElement).files || []);
  const remaining = 5 - commentImages.value.length;
  files.slice(0, remaining).forEach((file) => {
    commentImages.value.push({ file, preview: URL.createObjectURL(file) });
  });
  (e.target as HTMLInputElement).value = '';
};

const removeCommentImage = (idx: number) => {
  URL.revokeObjectURL(commentImages.value[idx].preview);
  commentImages.value.splice(idx, 1);
};

// 7. 评论删除权限与操作
const canDeleteComment = (comment: any) => {
  return currentUser.value && (
    currentUser.value.username === comment.author ||
    currentUser.value.role === 'superadmin'
  );
};

// 删除一级评论（后端 CASCADE 自动清除其下二级回复）
const deleteComment = (comment: any) => {
  requireAuth(async () => {
    if (!confirm('确定删除此评论？其下所有回复也将同时删除。')) return;
    try {
      await axios.delete(`/api/forum/comments/${comment.id}/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });
      comments.value = comments.value.filter((c: any) => c.id !== comment.id);
    } catch {
      alert('删除失败');
    }
  });
};

// 删除二级回复（仅移除当前回复，不影响回复链其他项）
const deleteReply = (parentComment: any, reply: any) => {
  requireAuth(async () => {
    if (!confirm('确定删除此回复？')) return;
    try {
      await axios.delete(`/api/forum/comments/${reply.id}/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });
      parentComment.replies = parentComment.replies.filter((r: any) => r.id !== reply.id);
    } catch {
      alert('删除失败');
    }
  });
};
</script>

<style scoped>
@reference "tailwindcss";

.prose p {
  @apply mb-6;
}
</style>
