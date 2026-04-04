<template>
  <div class="pt-20">
    <!-- Hero Section / Carousel Placeholder -->
    <section class="relative h-[80vh] overflow-hidden bg-on-surface">
      <div class="absolute inset-0">
        <img 
          src="https://picsum.photos/seed/architecture/1920/1080" 
          class="w-full h-full object-cover opacity-60 scale-105"
          referrerpolicy="no-referrer"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-on-surface via-transparent to-transparent"></div>
      </div>
      
      <div class="container mx-auto px-4 h-full relative z-10 flex flex-col justify-center items-center text-center">
        <div class="inline-block px-4 py-1 bg-tertiary text-white text-[10px] font-bold uppercase tracking-widest mb-6">
          本月推荐
        </div>
        <h1 class="font-serif text-6xl md:text-8xl text-white mb-8 tracking-tight leading-tight">
          大唐遗风：<br/>五台山佛光寺
        </h1>
        <p class="text-white/80 text-lg max-w-2xl mb-12 leading-relaxed font-light">
          穿越千年的斗拱结构，触摸中华木构建筑的巅峰。加入本月共创计划，重塑经典文创，延续匠心之美。
        </p>
        <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-6">
          <button class="px-10 py-4 bg-primary text-white font-bold rounded-lg hover:bg-primary-container transition-all flex items-center">
            开始探索 <ArrowRightIcon class="ml-2 w-4 h-4" />
          </button>
          <button class="px-10 py-4 bg-white/10 backdrop-blur-md text-white font-bold rounded-lg hover:bg-white/20 transition-all border border-white/20">
            了解集章
          </button>
        </div>
      </div>

      <!-- Carousel Indicators -->
      <div class="absolute bottom-12 left-1/2 -translate-x-1/2 flex space-x-3">
        <div v-for="i in 3" :key="i" class="w-12 h-1 rounded-full transition-all" :class="i === 1 ? 'bg-white' : 'bg-white/30'"></div>
      </div>
    </section>

    <!-- Main Content -->
    <section class="py-24 bg-surface">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
          
          <!-- Left: Stamp Progress -->
          <div class="lg:col-span-4">
            <StampLayer 
              title="应县木塔"
              :progress="60"
              :collected="6"
              :total="10"
              description="距离解锁“木构大师”称号还需收集 4 枚印记。本周任务：完成五台山建筑群打卡。"
              @click="handleStampClick"
            />
          </div>

          <!-- Center: Forum Hot Topics -->
          <div class="lg:col-span-5">
            <div class="flex items-center justify-between mb-10">
              <h2 class="font-serif text-3xl flex items-center">
                <MessageSquareIcon class="w-6 h-6 mr-3 text-primary" /> 筑匠论坛热门
              </h2>
              <a href="#" class="text-xs font-bold text-primary hover:underline">查看全部</a>
            </div>
            
            <div class="space-y-8">
              <div v-for="(topic, index) in hotTopics" :key="index" class="flex items-start group cursor-pointer">
                <span class="font-serif text-4xl text-secondary/10 mr-6 group-hover:text-primary/20 transition-colors">0{{ index + 1 }}</span>
                <div>
                  <h3 class="font-serif text-lg mb-2 group-hover:text-primary transition-colors">{{ topic.title }}</h3>
                  <div class="flex items-center space-x-4 text-[10px] text-secondary/40 font-bold uppercase tracking-widest">
                    <span>作者：{{ topic.author }}</span>
                    <span>{{ topic.reads }} 阅读</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right: Co-creation Status -->
          <div class="lg:col-span-3">
            <div class="bg-primary p-8 rounded-2xl text-white h-full relative overflow-hidden">
              <div class="relative z-10">
                <h2 class="font-serif text-2xl mb-8">共创动态</h2>
                
                <div class="space-y-8">
                  <div class="p-4 bg-white/10 rounded-xl border border-white/10">
                    <div class="flex items-center text-[10px] font-bold uppercase tracking-widest mb-2">
                      <CheckCircleIcon class="w-3 h-3 mr-2" /> 官方采纳
                    </div>
                    <p class="text-xs text-white/80 leading-relaxed">
                      用户 @墨香 提交的“天坛祈年殿积木套装”已被列入试产计划。
                    </p>
                  </div>
                  
                  <div class="p-4 bg-white/10 rounded-xl border border-white/10">
                    <div class="flex items-center text-[10px] font-bold uppercase tracking-widest mb-2">
                      <MegaphoneIcon class="w-3 h-3 mr-2" /> 新挑战开启
                    </div>
                    <p class="text-xs text-white/80 leading-relaxed">
                      “宋代园林主题”周边设计挑战赛今日正式启动。
                    </p>
                  </div>
                </div>

                <button class="w-full mt-12 py-4 bg-white text-primary font-bold rounded-lg hover:bg-surface transition-all flex items-center justify-center">
                  <PenToolIcon class="w-4 h-4 mr-2" /> 我也要贡献灵感
                </button>
              </div>
              
              <!-- Decorative Pattern -->
              <div class="absolute -bottom-10 -right-10 w-40 h-40 border-8 border-white/5 rounded-full"></div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- Editorial Section -->
    <section class="py-32 bg-white overflow-hidden">
      <div class="container mx-auto px-4">
        <div class="flex flex-col lg:flex-row items-center gap-20">
          <div class="lg:w-1/2 relative">
            <div class="aspect-[3/4] rounded-3xl overflow-hidden shadow-2xl">
              <img 
                src="https://picsum.photos/seed/roof/800/1200" 
                class="w-full h-full object-cover"
                referrerpolicy="no-referrer"
              />
            </div>
            <div class="absolute -bottom-10 -right-10 bg-surface p-8 rounded-2xl shadow-xl max-w-xs border border-outline-variant/10">
              <div class="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                <CompassIcon class="w-5 h-5 text-primary" />
              </div>
              <h4 class="font-serif text-lg mb-2">营造技艺解析</h4>
              <p class="text-xs text-secondary/60 leading-relaxed">
                深入了解中国传统木结构的灵魂——斗拱。不仅是结构支撑，更是流动的艺术韵律。
              </p>
            </div>
          </div>
          
          <div class="lg:w-1/2">
            <div class="w-16 h-1 bg-primary mb-12"></div>
            <h2 class="font-serif text-5xl md:text-7xl mb-12 leading-tight">
              不仅仅是保存<br/>
              更是<span class="text-primary italic">新生</span>
            </h2>
            <p class="text-secondary/80 text-lg mb-12 leading-relaxed font-light">
              “筑迹”致力于连接古建爱好者与现代设计师。我们通过数字化的印记采集与大众参与的共创模式，让沉寂在历史深处的木构建筑，在数字时代焕发出全新的生命力。
            </p>
            
            <div class="grid grid-cols-2 gap-12">
              <div>
                <p class="text-4xl font-serif text-on-surface mb-2">450+</p>
                <p class="text-xs text-secondary/40 font-bold uppercase tracking-widest">已录入古建</p>
              </div>
              <div>
                <p class="text-4xl font-serif text-on-surface mb-2">12k</p>
                <p class="text-xs text-secondary/40 font-bold uppercase tracking-widest">社区筑匠</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { 
  ArrowRight as ArrowRightIcon, 
  MessageSquare as MessageSquareIcon,
  CheckCircle as CheckCircleIcon,
  Megaphone as MegaphoneIcon,
  PenTool as PenToolIcon,
  Compass as CompassIcon
} from 'lucide-react';
import StampLayer from '@/components/StampLayer.vue';

const router = useRouter();

const hotTopics = [
  { title: '营造法式的构造之美：解读斗拱的数学密码', author: '梁下客', reads: '1.2k' },
  { title: '大唐古建筑寻踪：山西那些尚未被发现的瑰宝', author: '山野行者', reads: '980' },
  { title: '故宫红墙：寻找最完美的矿物颜料配比', author: '宫廷画师', reads: '856' }
];

const handleStampClick = () => {
  console.log('Stamp progress clicked');
  // TODO: 跳转至详情页
};
</script>
