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
                {{ activeTab === 'dashboard' ? '工作台预览' : activeTab === 'audit' ? '内容审核中心' : activeTab === 'users' ? '用户与版主管理' : activeTab === 'ai' ? 'AI 监管配置' : '题库管理' }}
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
                  <div v-if="!submissionList.length" class="text-center py-8 text-secondary/40 text-xs">暂无待处理投稿</div>
                  <div v-for="item in submissionList.slice(0, 1)" :key="item.id" class="bg-white rounded-3xl p-6 border border-outline-variant/10 shadow-sm">
                    <div class="flex flex-col md:flex-row gap-6">
                      <img v-if="item.image" :src="item.image" class="w-full md:w-32 h-24 object-cover rounded-xl" referrerpolicy="no-referrer" />
                      <div class="flex-grow">
                        <h4 class="font-bold text-sm mb-1">{{ item.title }}</h4>
                        <p class="text-[10px] text-secondary/40 mb-4">{{ item.author }} | {{ item.time }}</p>
                        <div class="flex gap-2">
                          <button @click="quickApprove(item.id)" class="px-4 py-1.5 bg-primary text-white text-[10px] font-bold rounded-lg">快速通过</button>
                          <button @click="activeTab = 'audit'" class="px-4 py-1.5 bg-surface text-secondary text-[10px] font-bold rounded-lg border border-outline-variant/20">全部审核</button>
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
            <div class="flex gap-3">
              <button
                v-for="f in auditFilters"
                :key="f.value"
                @click="() => { auditStatusFilter = f.value; fetchSubmissions(); }"
                class="px-5 py-2 rounded-xl text-xs font-bold transition-all"
                :class="auditStatusFilter === f.value ? 'bg-primary text-white shadow-md shadow-primary/20' : 'bg-white border border-outline-variant/20 text-secondary/60 hover:bg-surface'"
              >{{ f.label }}</button>
            </div>

            <div v-if="loadingSubmissions" class="py-16 text-center text-sm text-secondary/40 font-bold">鍔犺浇涓?..</div>

            <div v-else-if="!submissionList.length" class="text-center py-16 text-secondary/40">
              <InboxIcon class="w-12 h-12 mx-auto mb-4 opacity-30" />
              <p class="font-bold text-sm">暂无{{ auditFilters.find(f => f.value === auditStatusFilter)?.label }}内容</p>
            </div>

            <template v-else>
              <div v-for="item in submissionList" :key="item.id" class="bg-white rounded-3xl p-6 border border-outline-variant/10 shadow-sm hover:shadow-md transition-all">
                <div class="flex flex-col md:flex-row gap-6">
                  <img v-if="item.image" :src="item.image" class="w-full md:w-40 h-32 object-cover rounded-2xl" referrerpolicy="no-referrer" />
                  <div v-else class="w-full md:w-40 h-32 bg-surface rounded-2xl flex items-center justify-center">
                    <ImageIcon class="w-8 h-8 text-secondary/20" />
                  </div>
                  <div class="flex-grow">
                    <div class="flex justify-between items-start mb-2">
                      <h4 class="font-bold text-on-surface">{{ item.title }}</h4>
                      <span class="text-[10px] font-bold px-2 py-0.5 rounded uppercase" :class="statusBadgeClass(item.raw_status)">{{ item.status }}</span>
                    </div>
                    <p class="text-[10px] text-secondary/40 mb-4">作者{{ item.author }} | 提交时间{{ item.time }}</p>
                    <p class="text-xs text-secondary/60 line-clamp-2 leading-relaxed mb-6">{{ item.desc }}</p>
                    <div v-if="item.raw_status === 'pending'" class="flex gap-3">
                      <input
                        v-model="feedbackMap[item.id]"
                        type="text"
                        placeholder="输入审核反馈..."
                        class="flex-grow bg-surface border-none rounded-xl px-4 py-2 text-xs focus:ring-1 focus:ring-primary/20"
                      />
                      <button @click="auditOne(item.id, 'rejected')" class="p-2 text-secondary/40 hover:text-error transition-colors"><XIcon class="w-5 h-5" /></button>
                      <button @click="auditOne(item.id, 'approved')" class="px-6 py-2 bg-primary text-white text-xs font-bold rounded-xl">通过</button>
                    </div>
                    <p v-else class="text-xs text-secondary/40 italic">{{ item.raw_status === 'approved' ? '✓ 已通过' : '✕ 已驳回'}}</p>
                  </div>
                </div>
              </div>
            </template>
          </div>

          <!-- Users & Moderators View -->
          <div v-if="activeTab === 'users'" class="space-y-6">
            <div class="flex gap-3">
              <button
                v-for="t in userTabs"
                :key="t.value"
                @click="userRoleFilter = t.value"
                class="px-5 py-2 rounded-xl text-xs font-bold transition-all"
                :class="userRoleFilter === t.value ? 'bg-primary text-white shadow-md shadow-primary/20' : 'bg-white border border-outline-variant/20 text-secondary/60 hover:bg-surface'"
              >{{ t.label }}</button>
            </div>

            <div class="bg-white rounded-3xl border border-outline-variant/10 shadow-sm overflow-hidden">
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
                  <tr v-if="!filteredUsers.length">
                    <td colspan="4" class="px-8 py-12 text-center text-sm text-secondary/40 font-bold">暂无用户</td>
                  </tr>
                  <tr v-for="user in filteredUsers" :key="user.id" class="hover:bg-surface/50 transition-colors">
                    <td class="px-8 py-6">
                      <div class="flex items-center">
                        <div class="w-10 h-10 rounded-full bg-secondary/10 mr-4 overflow-hidden">
                          <img v-if="user.avatar" :src="user.avatar" class="w-full h-full object-cover" referrerpolicy="no-referrer" />
                          <div v-else class="w-full h-full flex items-center justify-center text-xs font-bold text-secondary/40">{{ (user.name || '?')[0] }}</div>
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
                        <span class="text-xs text-secondary/60">{{ user.active ? '活跃' : '禁用' }}</span>
                      </div>
                    </td>
                    <td class="px-8 py-6">
                      <div class="flex gap-3 items-center">
                        <select
                          :value="user._rawRole"
                          @change="onSetRole(user.id, ($event.target as HTMLSelectElement).value)"
                          class="text-xs font-bold text-primary border-none bg-transparent cursor-pointer focus:ring-0"
                        >
                          <option value="user">普通用户</option>
                          <option value="moderator">版主</option>
                        </select>
                        <button
                          @click="onBanToggle(user)"
                          class="text-xs font-bold hover:underline"
                          :class="user.active ? 'text-error' : 'text-primary'"
                        >{{ user.active ? '禁用' : '启用' }}</button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- AI Config View -->
          <div v-if="activeTab === 'ai'" class="max-w-2xl space-y-8">
            <div class="bg-white rounded-3xl p-8 border border-outline-variant/10 shadow-sm">
              <h3 class="font-serif text-lg mb-6 flex items-center">
                <ShieldCheckIcon class="w-5 h-5 mr-3 text-primary" /> AI 配置管理
              </h3>
              <div class="space-y-6">
                <div class="flex flex-wrap gap-2">
                  <span v-for="word in keywords" :key="word" class="px-4 py-2 bg-surface rounded-xl text-xs flex items-center font-bold">
                    {{ word }} <XIcon class="ml-2 w-3 h-3 text-secondary/20 cursor-pointer hover:text-error" />
                  </span>
                  <button class="px-4 py-2 border border-dashed border-outline-variant/40 rounded-xl text-xs font-bold text-primary hover:bg-primary/5 transition-all">+ 添加关键词</button>
                </div>
                <div class="pt-6 border-t border-outline-variant/10">
                  <label class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest block mb-4">自动检测敏感度</label>
                  <input type="range" class="w-full accent-primary" min="1" max="100" value="75" />
                  <div class="flex justify-between mt-2 text-[10px] font-bold text-secondary/40">
                    <span>低</span>
                    <span>高</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quiz View -->
          <div v-if="activeTab === 'quiz'" class="space-y-6">
            <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
              <select
                v-model="quizMonumentFilter"
                class="bg-white border border-outline-variant/10 rounded-xl px-4 py-2.5 text-sm focus:ring-1 focus:ring-primary/20"
              >
                <option value="">全部古建</option>
                <option v-for="m in monumentList" :key="m.id" :value="m.id">{{ m.name }}</option>
              </select>
              <button @click="openQuizModal(null)" class="px-6 py-2.5 bg-primary text-white text-xs font-bold rounded-xl flex items-center shadow-lg shadow-primary/20">
                <PlusIcon class="w-4 h-4 mr-2" /> 添加古建题
              </button>
            </div>

            <div v-if="!filteredQuiz.length" class="text-center py-16 text-secondary/40">
              <BookOpenIcon class="w-12 h-12 mx-auto mb-4 opacity-30" />
              <p class="font-bold text-sm text-secondary/40">暂无题目，点击“新增题目”开始录入</p>
            </div>

            <div class="space-y-4">
              <div v-for="q in filteredQuiz" :key="q.id" class="bg-white rounded-2xl p-6 border border-outline-variant/10 shadow-sm hover:shadow-md transition-all">
                <div class="flex gap-4">
                  <img v-if="q.image" :src="q.image" class="w-24 h-24 object-cover rounded-xl shrink-0" referrerpolicy="no-referrer" />
                  <div class="flex-grow">
                    <div class="flex items-start justify-between mb-3">
                      <p class="text-sm font-bold text-on-surface leading-snug mr-4">{{ q.description }}</p>
                      <div class="flex gap-3 shrink-0">
                        <button @click="openQuizModal(q)" class="text-[10px] font-bold text-primary hover:underline">编辑</button>
                        <button @click="deleteQuiz(q.id)" class="text-[10px] font-bold text-error hover:underline">删除</button>
                      </div>
                    </div>
                    <div class="flex flex-wrap gap-2 text-[10px]">
                      <span class="px-3 py-1 bg-green-100 text-green-700 rounded-full font-bold">正确答案: {{ q.correct_answer }}</span>
                      <span class="px-3 py-1 bg-surface text-secondary/60 rounded-full">A: {{ q.distractor_a }}</span>
                      <span class="px-3 py-1 bg-surface text-secondary/60 rounded-full">B: {{ q.distractor_b }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </main>
      </div>
    </div>
  </div>
  <!-- Quiz 缂栬緫妯℃€佹 -->
  <Teleport to="body">
    <div v-if="showQuizModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40" @click.self="showQuizModal = false">
      <div class="bg-white rounded-3xl p-8 w-full max-w-lg mx-4 shadow-2xl max-h-[90vh] overflow-y-auto">
        <h3 class="font-serif text-xl mb-6">{{ editingQuizId ? '编辑古建题' : '添加古建题' }}</h3>
        <div class="space-y-4">
          <textarea v-model="quizForm.description" placeholder="古建题描述" rows="3" class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20 resize-none"></textarea>
          <input v-model="quizForm.correct_answer" type="text" placeholder="正确答案" class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
          <div class="grid grid-cols-2 gap-4">
            <input v-model="quizForm.distractor_a" type="text" placeholder="干扰选项A" class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
            <input v-model="quizForm.distractor_b" type="text" placeholder="干扰选项B" class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
          </div>
          <select v-model="quizForm.monument" class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20">
            <option :value="null">请选择关联古建</option>
            <option v-for="m in monumentList" :key="m.id" :value="m.id">{{ m.name }}</option>
          </select>
          <div class="flex items-center gap-4">
            <label class="cursor-pointer px-4 py-2 bg-surface rounded-xl text-xs font-bold text-secondary hover:bg-secondary/10 transition-all">
              <input type="file" accept="image/*" class="hidden" @change="onQuizImageChange" />
              {{ quizImagePreview ? '更换图片' : '上传图片，可选 ' }}
            </label>
            <img v-if="quizImagePreview" :src="quizImagePreview" class="h-16 rounded-xl object-cover" referrerpolicy="no-referrer" />
          </div>
        </div>
        <div class="flex gap-3 mt-8">
          <button @click="showQuizModal = false" class="flex-1 py-3 bg-surface rounded-xl text-sm font-bold text-secondary hover:bg-secondary/10 transition-all">取消</button>
          <button @click="saveQuiz" :disabled="quizSaving" class="flex-1 py-3 bg-primary text-white text-sm font-bold rounded-xl shadow-lg shadow-primary/20 disabled:opacity-60">
            {{ quizSaving ? '保存中...' : '保存古建题' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import {
  LayoutDashboard as DashboardIcon,
  ShieldCheck as ShieldCheckIcon,
  Users as UsersIcon,
  FileSearch as AuditIcon,
  BookOpen as BookOpenIcon,
  Plus as PlusIcon,
  Inbox as InboxIcon,
  X as XIcon,
  Image as ImageIcon,
} from 'lucide-vue-next';
import service from '../api/request';

const activeTab = ref('dashboard');

const menuItems = [
  { id: 'dashboard', name: '数据大盘', icon: DashboardIcon },
  { id: 'audit', name: '内容审核', icon: AuditIcon },
  { id: 'users', name: '用户管理', icon: UsersIcon },
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
const keywords = ['历史争议', '恶意广告', '违规外链'];

const auditFilters = [
  { value: 'pending', label: '待处理' },
  { value: 'approved', label: '已通过' },
  { value: 'rejected', label: '已驳回' },
];
const reverseStatusMap: Record<string, string> = {
  '待处理': 'pending', '已通过': 'approved', '已驳回': 'rejected',
};
const submissionList = ref<any[]>([]);
const loadingSubmissions = ref(false);
const auditStatusFilter = ref('pending');
const feedbackMap = ref<Record<number, string>>({});

const fetchSubmissions = async () => {
  loadingSubmissions.value = true;
  try {
    const res = await service.get('/api/monuments/submissions/', {
      params: { status: auditStatusFilter.value },
    }) as any;
    submissionList.value = (res.results || res).map((item: any) => ({
      ...item,
      raw_status: reverseStatusMap[item.status] ?? item.status,
    }));
  } finally {
    loadingSubmissions.value = false;
  }
};

const statusBadgeClass = (rawStatus: string) => {
  if (rawStatus === 'pending') return 'bg-tertiary/10 text-tertiary';
  if (rawStatus === 'approved') return 'bg-green-100 text-green-700';
  return 'bg-red-100 text-red-700';
};

const auditOne = async (id: number, decision: string) => {
  try {
    await service.post(`/api/monuments/submissions/${id}/audit/`, {
      status: decision,
      feedback: feedbackMap.value[id] || '',
    });
    fetchSubmissions();
  } catch {
    alert('操作失败');
  }
};

const quickApprove = async (id: number) => {
  try {
    await service.post(`/api/monuments/submissions/${id}/quick-approve/`);
    fetchSubmissions();
  } catch {
    alert('操作失败');
  }
};

const userTabs = [
  { value: 'user', label: '普通用户' },
  { value: 'moderator', label: '版主' },
];
const roleDisplayToRaw: Record<string, string> = {
  '超级管理员': 'superadmin', '版主': 'moderator', '普通用户': 'user',
};
const userList = ref<any[]>([]);
const userRoleFilter = ref('user');
const filteredUsers = computed(() =>
  userList.value.filter((u: any) =>
    userRoleFilter.value === 'moderator' ? u.role === '版主' : u.role === '普通用户'
  )
);

const fetchUsers = async () => {
  const res = await service.get('/api/users/users/') as any;
  userList.value = (res.results || res).map((u: any) => ({
    ...u,
    _rawRole: roleDisplayToRaw[u.role] ?? 'user',
  }));
};

const onBanToggle = async (user: any) => {
  try {
    await service.post(`/api/users/users/${user.id}/${user.active ? 'ban' : 'unban'}/`);
    fetchUsers();
  } catch {
    alert('操作失败');
  }
};

const onSetRole = async (userId: number, role: string) => {
  try {
    await service.post(`/api/users/users/${userId}/set-role/`, { role });
    fetchUsers();
  } catch {
    alert('操作失败');
  }
};

const quizList = ref<any[]>([]);
const monumentList = ref<any[]>([]);
const quizMonumentFilter = ref<number | ''>('');
const filteredQuiz = computed(() => {
  if (!quizMonumentFilter.value) return quizList.value;
  return quizList.value.filter((q: any) => q.monument === quizMonumentFilter.value);
});

const fetchQuizList = async () => {
  const res = await service.get('/api/quiz/questions/') as any;
  quizList.value = res.results || res;
};

const fetchMonuments = async () => {
  const res = await service.get('/api/monuments/monuments/') as any;
  monumentList.value = (res.results || res).filter((m: any) => m.is_published);
};

const showQuizModal = ref(false);
const editingQuizId = ref<number | null>(null);
const quizForm = ref({ description: '', correct_answer: '', distractor_a: '', distractor_b: '', monument: null as number | null });
const quizImageFile = ref<File | null>(null);
const quizImagePreview = ref('');
const quizSaving = ref(false);

const openQuizModal = (quiz: any) => {
  if (quiz) {
    editingQuizId.value = quiz.id;
    quizForm.value = {
      description: quiz.description,
      correct_answer: quiz.correct_answer,
      distractor_a: quiz.distractor_a,
      distractor_b: quiz.distractor_b,
      monument: quiz.monument,
    };
    quizImagePreview.value = quiz.image || '';
  } else {
    editingQuizId.value = null;
    quizForm.value = { description: '', correct_answer: '', distractor_a: '', distractor_b: '', monument: null };
    quizImagePreview.value = '';
  }
  quizImageFile.value = null;
  showQuizModal.value = true;
};

const onQuizImageChange = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (file) {
    quizImageFile.value = file;
    quizImagePreview.value = URL.createObjectURL(file);
  }
};

const saveQuiz = async () => {
  if (!quizForm.value.description.trim() || !quizForm.value.correct_answer.trim()) {
    alert('请填写题目描述和正确答案');
    return;
  }
  quizSaving.value = true;
  try {
    const fd = new FormData();
    fd.append('description', quizForm.value.description);
    fd.append('correct_answer', quizForm.value.correct_answer);
    fd.append('distractor_a', quizForm.value.distractor_a);
    fd.append('distractor_b', quizForm.value.distractor_b);
    if (quizForm.value.monument) fd.append('monument', String(quizForm.value.monument));
    if (quizImageFile.value) fd.append('image', quizImageFile.value);
    if (editingQuizId.value) {
      await service.patch(`/api/quiz/questions/${editingQuizId.value}/`, fd);
    } else {
      await service.post('/api/quiz/questions/', fd);
    }
    showQuizModal.value = false;
    fetchQuizList();
  } catch {
    alert('保存失败');
  } finally {
    quizSaving.value = false;
  }
};

const deleteQuiz = async (id: number) => {
  if (!confirm('确定删除此题目？')) return;
  try {
    await service.delete(`/api/quiz/questions/${id}/`);
    fetchQuizList();
  } catch {
    alert('删除失败');
  }
};

onMounted(() => {
  fetchSubmissions();
  fetchUsers();
  fetchQuizList();
  fetchMonuments();
});
</script>