<template>
  <div class="pt-24 pb-24 bg-surface min-h-screen">
    <div class="container mx-auto px-4">
      <div class="flex flex-col lg:flex-row gap-8">
        
        <!-- Sidebar Navigation -->
        <aside class="lg:w-64 shrink-0">
          <div class="bg-white rounded-3xl p-6 border border-outline-variant/10 shadow-sm sticky top-24">
            <p class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest mb-6 px-4">核心控制台</p>
            <nav class="space-y-1">
              <button 
                v-for="item in menuItems" 
                :key="item.id"
                @click="activeTab = item.id"
                class="w-full flex items-center px-4 py-3 rounded-xl transition-all"
                :class="activeTab === item.id ? 'bg-primary text-white shadow-lg shadow-primary/20' : 'text-secondary/60 hover:bg-surface hover:text-secondary'"
              >
                <component :is="item.icon" class="w-4 h-4 mr-3" />
                <span class="text-sm font-bold">{{ item.name }}</span>
              </button>
            </nav>

            <div class="mt-12 pt-8 border-t border-outline-variant/10">
              <p class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest mb-6 px-4">系统配置</p>
              <nav class="space-y-1">
                <button 
                  v-for="item in configItems" 
                  :key="item.id"
                  @click="activeTab = item.id"
                  class="w-full flex items-center px-4 py-3 rounded-xl transition-all"
                  :class="activeTab === item.id ? 'bg-on-surface text-white' : 'text-secondary/60 hover:bg-surface hover:text-secondary'"
                >
                  <component :is="item.icon" class="w-4 h-4 mr-3" />
                  <span class="text-sm font-bold">{{ item.name }}</span>
                </button>
              </nav>
            </div>
          </div>
        </aside>

        <!-- Main Content -->
        <main class="flex-grow space-y-8">
          
          <!-- Header -->
          <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
            <div>
              <p class="text-[10px] font-bold text-primary uppercase tracking-widest mb-2">Master Admin Panel</p>
              <h1 class="font-serif text-4xl text-on-surface">
                {{ activeTab === 'dashboard' ? '工作台概览' : activeTab === 'audit' ? '内容审核中心' : activeTab === 'users' ? '用户与版主管理' : activeTab === 'ai' ? 'AI 监管配置' : '题库管理' }}
              </h1>
            </div>
            <div class="flex gap-3">
              <button class="px-6 py-2.5 bg-white border border-outline-variant/20 rounded-xl text-sm font-bold text-secondary hover:bg-surface transition-all">导出报告</button>
              <button class="px-6 py-2.5 bg-primary text-white rounded-xl text-sm font-bold shadow-lg shadow-primary/20 flex items-center">
                <PlusIcon class="w-4 h-4 mr-2" /> 发布公告
              </button>
            </div>
          </div>

          <!-- Dashboard View -->
          <div v-if="activeTab === 'dashboard'" class="space-y-8">
            <!-- Quick Stats -->
            <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6">
              <div v-for="stat in stats" :key="stat.label" class="bg-white p-8 rounded-3xl border border-outline-variant/10 shadow-sm relative overflow-hidden">
                <div class="absolute top-0 left-0 w-1 h-full" :class="stat.color"></div>
                <div class="flex justify-between items-start mb-4">
                  <p class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest">{{ stat.label }}</p>
                  <span class="text-[10px] font-bold px-2 py-0.5 rounded" :class="stat.trendClass">{{ stat.trend }}</span>
                </div>
                <div class="flex items-baseline">
                  <span class="text-3xl font-serif text-on-surface">{{ stat.value }}</span>
                  <span v-if="stat.unit" class="text-xs text-secondary/40 ml-1">{{ stat.unit }}</span>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 xl:grid-cols-12 gap-8">
              <!-- Left: Audit Stream -->
              <div class="xl:col-span-8 space-y-6">
                <div class="flex items-center justify-between px-2">
                  <h3 class="font-serif text-xl flex items-center">
                    <InboxIcon class="w-5 h-5 mr-3 text-primary" /> 待办审核
                  </h3>
                </div>
                <div class="space-y-4">
                  <div v-for="item in auditItems.slice(0, 1)" :key="item.id" class="bg-white rounded-3xl p-6 border border-outline-variant/10 shadow-sm">
                    <div class="flex flex-col md:flex-row gap-6">
                      <img :src="item.image" class="w-full md:w-32 h-24 object-cover rounded-xl" referrerpolicy="no-referrer" />
                      <div class="flex-grow">
                        <h4 class="font-bold text-sm mb-1">{{ item.title }}</h4>
                        <p class="text-[10px] text-secondary/40 mb-4">{{ item.author }} | {{ item.time }}</p>
                        <div class="flex gap-2">
                          <button class="px-4 py-1.5 bg-primary text-white text-[10px] font-bold rounded-lg">快速通过</button>
                          <button class="px-4 py-1.5 bg-surface text-secondary text-[10px] font-bold rounded-lg border border-outline-variant/20">详情</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Right: System Health -->
              <div class="xl:col-span-4 bg-white rounded-3xl p-8 border border-outline-variant/10 shadow-sm">
                <h3 class="font-serif text-lg mb-6">系统健康度</h3>
                <div class="space-y-6">
                  <div v-for="i in 3" :key="i" class="flex items-center justify-between">
                    <span class="text-xs text-secondary/60">节点 {{ i }} 负载</span>
                    <div class="w-32 h-1 bg-secondary/5 rounded-full">
                      <div class="h-full bg-primary" :style="{ width: (30 + i * 15) + '%' }"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Audit View -->
          <div v-if="activeTab === 'audit'" class="space-y-6">
            <div v-for="item in auditItems" :key="item.id" class="bg-white rounded-3xl p-6 border border-outline-variant/10 shadow-sm hover:shadow-md transition-all">
              <div class="flex flex-col md:flex-row gap-6">
                <img :src="item.image" class="w-full md:w-40 h-32 object-cover rounded-2xl" referrerpolicy="no-referrer" />
                <div class="flex-grow">
                  <div class="flex justify-between items-start mb-2">
                    <h4 class="font-bold text-on-surface">{{ item.title }}</h4>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-tertiary/10 text-tertiary uppercase">{{ item.status }}</span>
                  </div>
                  <p class="text-[10px] text-secondary/40 mb-4">投稿人：{{ item.author }} | 提交于 {{ item.time }}</p>
                  <p class="text-xs text-secondary/60 line-clamp-2 leading-relaxed mb-6">{{ item.desc }}</p>
                  
                  <div class="flex gap-3">
                    <input type="text" placeholder="输入审核反馈建议..." class="flex-grow bg-surface border-none rounded-xl px-4 py-2 text-xs focus:ring-1 focus:ring-primary/20" />
                    <button class="p-2 text-secondary/40 hover:text-error transition-colors"><XIcon class="w-5 h-5" /></button>
                    <button class="px-6 py-2 bg-primary text-white text-xs font-bold rounded-xl">通过</button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Users & Moderators View -->
          <div v-if="activeTab === 'users'" class="bg-white rounded-3xl border border-outline-variant/10 shadow-sm overflow-hidden">
            <table class="w-full text-left border-collapse">
              <thead class="bg-surface">
                <tr>
                  <th class="px-8 py-4 text-[10px] font-bold text-secondary/40 uppercase tracking-widest">用户</th>
                  <th class="px-8 py-4 text-[10px] font-bold text-secondary/40 uppercase tracking-widest">角色</th>
                  <th class="px-8 py-4 text-[10px] font-bold text-secondary/40 uppercase tracking-widest">状态</th>
                  <th class="px-8 py-4 text-[10px] font-bold text-secondary/40 uppercase tracking-widest">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-outline-variant/10">
                <tr v-for="user in userList" :key="user.id" class="hover:bg-surface/50 transition-colors">
                  <td class="px-8 py-6">
                    <div class="flex items-center">
                      <div class="w-10 h-10 rounded-full bg-secondary/10 mr-4 overflow-hidden">
                        <img :src="user.avatar" class="w-full h-full object-cover" referrerpolicy="no-referrer" />
                      </div>
                      <div>
                        <p class="text-sm font-bold">{{ user.name }}</p>
                        <p class="text-[10px] text-secondary/40">{{ user.email }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-8 py-6">
                    <span class="px-3 py-1 rounded-full text-[10px] font-bold" :class="user.roleBg">{{ user.role }}</span>
                  </td>
                  <td class="px-8 py-6">
                    <div class="flex items-center">
                      <div class="w-1.5 h-1.5 rounded-full mr-2" :class="user.active ? 'bg-green-500' : 'bg-red-500'"></div>
                      <span class="text-xs text-secondary/60">{{ user.active ? '正常' : '已封禁' }}</span>
                    </div>
                  </td>
                  <td class="px-8 py-6">
                    <div class="flex gap-3">
                      <button class="text-xs font-bold text-primary hover:underline">编辑权限</button>
                      <button class="text-xs font-bold text-error hover:underline">{{ user.active ? '封禁' : '解封' }}</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- AI Config View -->
          <div v-if="activeTab === 'ai'" class="max-w-2xl space-y-8">
            <div class="bg-white rounded-3xl p-8 border border-outline-variant/10 shadow-sm">
              <h3 class="font-serif text-lg mb-6 flex items-center">
                <ShieldCheckIcon class="w-5 h-5 mr-3 text-primary" /> 敏感词库管理
              </h3>
              <div class="space-y-6">
                <div class="flex flex-wrap gap-2">
                  <span v-for="word in keywords" :key="word" class="px-4 py-2 bg-surface rounded-xl text-xs flex items-center font-bold">
                    {{ word }} <XIcon class="ml-2 w-3 h-3 text-secondary/20 cursor-pointer hover:text-error" />
                  </span>
                  <button class="px-4 py-2 border border-dashed border-outline-variant/40 rounded-xl text-xs font-bold text-primary hover:bg-primary/5 transition-all">+ 新增敏感词</button>
                </div>
                <div class="pt-6 border-t border-outline-variant/10">
                  <label class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest block mb-4">自动拦截强度</label>
                  <input type="range" class="w-full accent-primary" min="1" max="100" value="75" />
                  <div class="flex justify-between mt-2 text-[10px] font-bold text-secondary/40">
                    <span>宽松</span>
                    <span>严苛</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quiz View -->
          <div v-if="activeTab === 'quiz'" class="max-w-2xl">
            <div class="bg-white rounded-3xl p-8 border border-outline-variant/10 shadow-sm">
              <h3 class="font-serif text-lg mb-6 flex items-center">
                <BookOpenIcon class="w-5 h-5 mr-3 text-primary" /> 题库录入
              </h3>
              <div class="space-y-6">
                <div class="aspect-video bg-surface border-2 border-dashed border-outline-variant/20 rounded-2xl flex flex-col items-center justify-center text-secondary/40 cursor-pointer hover:border-primary/40 transition-all">
                  <ImageIcon class="w-8 h-8 mb-2" />
                  <span class="text-xs font-bold">上传题目参考图</span>
                </div>
                <div class="space-y-4">
                  <input type="text" placeholder="题目描述 (例如：请辨认图中斗拱的类型)" class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
                  <input type="text" placeholder="正确答案" class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
                  <div class="grid grid-cols-2 gap-4">
                    <input type="text" placeholder="干扰项 A" class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
                    <input type="text" placeholder="干扰项 B" class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
                  </div>
                </div>
                <button class="w-full py-4 bg-primary text-white text-sm font-bold rounded-xl shadow-lg shadow-primary/20">保存并发布</button>
              </div>
            </div>
          </div>

        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { 
  LayoutDashboard as DashboardIcon,
  ShieldCheck as ShieldCheckIcon,
  Users as UsersIcon,
  FileSearch as AuditIcon,
  Settings as SettingsIcon,
  BookOpen as BookOpenIcon,
  Plus as PlusIcon,
  Inbox as InboxIcon,
  X as XIcon,
  Image as ImageIcon,
  CheckCircle as CheckCircleIcon
} from 'lucide-vue-next';

const activeTab = ref('dashboard');

const menuItems = [
  { id: 'dashboard', name: '数据大盘', icon: DashboardIcon },
  { id: 'audit', name: '内容审核', icon: AuditIcon },
  { id: 'users', name: '版主管理', icon: UsersIcon },
];

const configItems = [
  { id: 'ai', name: 'AI 监管', icon: ShieldCheckIcon },
  { id: 'quiz', name: '题库管理', icon: BookOpenIcon },
];

const stats = [
  { label: '今日新增投稿', value: '1,284', trend: '+12.5%', trendClass: 'bg-green-100 text-green-700', color: 'bg-primary' },
  { label: '待审核任务', value: '42', trend: '紧急', trendClass: 'bg-red-100 text-red-700', color: 'bg-tertiary' },
  { label: '活跃工匠数', value: '8,912', trend: '稳定', trendClass: 'bg-blue-100 text-blue-700', color: 'bg-on-surface' },
  { label: 'AI 拦截率', value: '156', unit: '次/日', trend: '99.8%', trendClass: 'bg-green-100 text-green-700', color: 'bg-primary' },
];

const auditItems = [
  { 
    id: 1, 
    title: '苏州园林叠石技法解析', 
    author: '@墨染匠心', 
    time: '14:20', 
    status: '待处理', 
    image: 'https://picsum.photos/seed/a1/400/300',
    desc: '本文详尽描述了苏州留园内冠云峰的堆叠手法，结合了宋代《营造法式》中的相关记载...'
  },
  { 
    id: 2, 
    title: '世界建筑大观 - 泰姬陵', 
    author: '@GlobalVoyager', 
    time: '11:05', 
    status: '已驳回', 
    image: 'https://picsum.photos/seed/a2/400/300',
    desc: '由于本社区核心关注中国古建筑传承，海外建筑投稿建议移步“全球视野”子板块...'
  },
];

const keywords = ['历史争议', '恶意广告', '违规外链'];

const userList = [
  { id: 1, name: '营造大师张', email: 'zhang@zhuji.com', role: '超级管理员', roleBg: 'bg-primary/10 text-primary', active: true, avatar: 'https://picsum.photos/seed/u1/100/100' },
  { id: 2, name: '李工', email: 'li@zhuji.com', role: '版主', roleBg: 'bg-tertiary/10 text-tertiary', active: true, avatar: 'https://picsum.photos/seed/u2/100/100' },
  { id: 3, name: '匿名破坏者', email: 'spam@bad.com', role: '普通用户', roleBg: 'bg-secondary/10 text-secondary', active: false, avatar: 'https://picsum.photos/seed/u3/100/100' },
];
</script>
