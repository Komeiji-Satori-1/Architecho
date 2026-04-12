<template>
  <div 
    class="group bg-white rounded-xl overflow-hidden border border-outline-variant/10 hover:shadow-xl transition-all duration-500 cursor-pointer"
    @click="handleClick"
  >
    <div class="aspect-[4/3] overflow-hidden relative">
      <img 
        :src="post.cover || 'https://picsum.photos/seed/forum/400/300'" 
        :alt="post.title" 
        class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
        referrerpolicy="no-referrer"
      />
      <div class="absolute top-4 left-4 bg-primary/90 text-white text-[10px] px-2 py-1 rounded font-bold uppercase tracking-widest">
        {{ post.category_name }}
      </div>
    </div>
    
    <div class="p-6">
      <h3 class="font-serif text-xl mb-3 line-clamp-2 group-hover:text-primary transition-colors">
        {{ post.title }}
      </h3>
      
      <div class="flex items-center justify-between mt-4">
        <div class="flex items-center space-x-2">
          <div class="w-6 h-6 rounded-full bg-secondary/10 flex items-center justify-center text-[10px] font-bold text-secondary">
            {{ post.author.charAt(0) }}
          </div>
          <span class="text-xs text-secondary/60">{{ post.author }}</span>
        </div>
        
        <div class="flex items-center space-x-3 text-secondary/40 text-[10px]">
          <span class="flex items-center">
            <EyeIcon class="w-3 h-3 mr-1" /> {{ post.views }}
          </span>
          <span class="flex items-center">
            <MessageSquareIcon class="w-3 h-3 mr-1" /> {{ post.comment_count }}
          </span>
          <span class="flex items-center" v-if="post.likes > 0">
            ❤️ {{ post.likes }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Eye as EyeIcon, MessageSquare as MessageSquareIcon } from 'lucide-vue-next';

interface Post {
  id: number;
  title: string;
  cover: string | null;
  category_name: string;
  author: string;
  author_avatar?: string | null;
  views: number;
  comment_count: number;
  likes: number;
  heat_score?: number;
}

const props = defineProps<{
  post: Post;
}>();

const emit = defineEmits(['click']);

const handleClick = () => {
  console.log(`[DEBUG] Clicking post ${props.post.id}: ${props.post.title}`);
  emit('click', props.post.id);
};
</script>
