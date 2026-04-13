<template>
  <div class="pt-24 pb-24 bg-surface min-h-screen">
    <div class="container mx-auto px-4">
      <div class="flex flex-col lg:flex-row gap-8">

        <!-- Sidebar Navigation -->
        <aside class="lg:w-64 shrink-0">
          <div class="bg-white rounded-3xl p-6 border border-outline-variant/10 shadow-sm sticky top-24">
            <p class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest mb-6 px-4">核心控制台</p>
            <nav class="space-y-1">
              <button v-for="item in menuItems" :key="item.id" @click="activeTab = item.id"
                class="w-full flex items-center px-4 py-3 rounded-xl transition-all"
                :class="activeTab === item.id ? 'bg-primary text-white shadow-lg shadow-primary/20' : 'text-secondary/60 hover:bg-surface hover:text-secondary'">
                <component :is="item.icon" class="w-4 h-4 mr-3" />
                <span class="text-sm font-bold">{{ item.name }}</span>
              </button>
            </nav>

            <div class="mt-12 pt-8 border-t border-outline-variant/10">
              <p class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest mb-6 px-4">系统配置</p>
              <nav class="space-y-1">
                <button v-for="item in configItems" :key="item.id" @click="activeTab = item.id"
                  class="w-full flex items-center px-4 py-3 rounded-xl transition-all"
                  :class="activeTab === item.id ? 'bg-on-surface text-white' : 'text-secondary/60 hover:bg-surface hover:text-secondary'">
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
                {{ {
                  dashboard: '工作台预览', audit: '内容审核中心', users: '用户与版主管理', quiz: '题库管理',
                  'monuments-mgmt': '古建列表', 'stamp-mgmt': '印章管理', 'articles-mgmt': '古建资料'
                }[activeTab] || '管理面板' }}
              </h1>
            </div>
            <div class="flex gap-3">
              <button
                class="px-6 py-2.5 bg-white border border-outline-variant/20 rounded-xl text-sm font-bold text-secondary hover:bg-surface transition-all">导出报告</button>
              <button
                class="px-6 py-2.5 bg-primary text-white rounded-xl text-sm font-bold shadow-lg shadow-primary/20 flex items-center">
                <PlusIcon class="w-4 h-4 mr-2" /> 发布公告
              </button>
            </div>
          </div>

          <!-- Dashboard View -->
          <div v-if="activeTab === 'dashboard'" class="space-y-8">
            <!-- Quick Stats -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div v-for="stat in stats" :key="stat.label"
                class="bg-white p-8 rounded-3xl border border-outline-variant/10 shadow-sm relative overflow-hidden">
                <div class="absolute top-0 left-0 w-1 h-full" :class="stat.color"></div>
                <div class="flex justify-between items-start mb-4">
                  <p class="text-[10px] font-bold text-secondary/40 uppercase tracking-widest">{{ stat.label }}</p>
                </div>
                <div class="flex items-baseline">
                  <span class="text-3xl font-serif text-on-surface">{{ stat.value }}</span>
                </div>
              </div>
            </div>

            <div class="space-y-6">
              <div class="flex items-center justify-between px-2">
                <h3 class="font-serif text-xl flex items-center">
                  <InboxIcon class="w-5 h-5 mr-3 text-primary" /> 待办审核
                </h3>
              </div>
              <div class="space-y-4">
                <div v-if="!submissionList.length" class="text-center py-8 text-secondary/40 text-xs">暂无待处理投稿</div>
                <div v-for="item in submissionList.slice(0, 3)" :key="item.id"
                  class="bg-white rounded-3xl p-6 border border-outline-variant/10 shadow-sm">
                  <div class="flex flex-col md:flex-row gap-6">
                    <img v-if="item.image" :src="item.image" class="w-full md:w-32 h-24 object-cover rounded-xl"
                      referrerpolicy="no-referrer" />
                    <div class="flex-grow">
                      <div class="flex items-center gap-2 mb-1">
                        <span class="text-[10px] font-bold px-2 py-0.5 rounded" :class="item.source === 'forum' ? 'bg-blue-100 text-blue-700' : 'bg-tertiary/10 text-tertiary'">{{ item.source === 'forum' ? '论坛帖子' : '共创投稿' }}</span>
                        <h4 class="font-bold text-sm">{{ item.title }}</h4>
                      </div>
                      <p class="text-[10px] text-secondary/40 mb-4">{{ item.author }} | {{ item.time }}</p>
                      <div class="flex gap-2">
                        <button @click="activeTab = 'audit'"
                          class="px-4 py-1.5 bg-primary text-white text-[10px] font-bold rounded-lg">前往审核</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Audit View -->
          <div v-if="activeTab === 'audit'" class="space-y-6">
            <!-- Source filter -->
            <div class="flex gap-3 mb-2">
              <button v-for="s in auditSourceFilters" :key="s.value"
                @click="auditSourceFilter = s.value"
                class="px-5 py-2 rounded-xl text-xs font-bold transition-all"
                :class="auditSourceFilter === s.value ? 'bg-on-surface text-white shadow-md' : 'bg-white border border-outline-variant/20 text-secondary/60 hover:bg-surface'">{{ s.label }}</button>
            </div>

            <!-- Forum Posts Section -->
            <div v-if="auditSourceFilter === 'all' || auditSourceFilter === 'forum'">
              <h3 class="font-serif text-lg mb-4 flex items-center">
                <BookOpenIcon class="w-4 h-4 mr-2 text-blue-600" /> 论坛帖子
              </h3>
              <div v-if="loadingForumPosts" class="py-8 text-center text-sm text-secondary/40 font-bold">加载中...</div>
              <div v-else-if="!forumPostList.length" class="text-center py-8 text-secondary/40">
                <InboxIcon class="w-10 h-10 mx-auto mb-3 opacity-30" />
                <p class="font-bold text-sm">暂无论坛帖子</p>
              </div>
              <div v-else class="space-y-4">
                <div v-for="item in forumPostList" :key="'forum-' + item.id"
                  class="bg-white rounded-3xl p-6 border border-outline-variant/10 shadow-sm hover:shadow-md transition-all">
                  <div class="flex flex-col md:flex-row gap-6">
                    <img v-if="item.cover" :src="item.cover" class="w-full md:w-40 h-32 object-cover rounded-2xl"
                      referrerpolicy="no-referrer" />
                    <div v-else class="w-full md:w-40 h-32 bg-surface rounded-2xl flex items-center justify-center">
                      <ImageIcon class="w-8 h-8 text-secondary/20" />
                    </div>
                    <div class="flex-grow">
                      <div class="flex justify-between items-start mb-2">
                        <div class="flex items-center gap-2">
                          <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-700">论坛</span>
                          <h4 class="font-bold text-on-surface">{{ item.title }}</h4>
                        </div>
                        <span v-if="item.is_top" class="text-[10px] font-bold px-2 py-0.5 rounded bg-tertiary/10 text-tertiary">置顶</span>
                      </div>
                      <p class="text-[10px] text-secondary/40 mb-2">作者 {{ item.author }} | {{ item.category_name }} | {{ item.time }}</p>
                      <p class="text-xs text-secondary/60 line-clamp-2 leading-relaxed mb-4">{{ item.excerpt }}</p>
                      <div class="flex items-center gap-4 text-[10px] text-secondary/40">
                        <span>👁 {{ item.views }}</span>
                        <span>❤ {{ item.likes }}</span>
                        <span>💬 {{ item.comment_count }}</span>
                      </div>
                      <div class="flex gap-3 mt-4">
                        <button @click="deleteForumPost(item.id)" class="px-4 py-1.5 text-error text-[10px] font-bold rounded-lg border border-error/20 hover:bg-error/5">删除帖子</button>
                        <button @click="toggleForumTop(item)" class="px-4 py-1.5 text-[10px] font-bold rounded-lg border border-outline-variant/20" :class="item.is_top ? 'text-secondary/60' : 'text-primary'">{{ item.is_top ? '取消置顶' : '置顶' }}</button>
                        <button @click="toggleForumEssence(item)" class="px-4 py-1.5 text-[10px] font-bold rounded-lg border border-outline-variant/20" :class="item.is_essence ? 'text-secondary/60' : 'text-primary'">{{ item.is_essence ? '取消精华' : '设为精华' }}</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- CoCreation Section -->
            <div v-if="auditSourceFilter === 'all' || auditSourceFilter === 'cocreation'" :class="auditSourceFilter === 'all' ? 'mt-10' : ''">
              <h3 class="font-serif text-lg mb-4 flex items-center">
                <StampIcon class="w-4 h-4 mr-2 text-tertiary" /> 共创投稿
              </h3>
              <!-- Status sub-filter for cocreation -->
              <div class="flex gap-3 mb-4">
                <button v-for="f in cocreationStatusFilters" :key="f.value"
                  @click="() => { cocreationStatusFilter = f.value; fetchCocreationItems(); }"
                  class="px-4 py-1.5 rounded-lg text-[10px] font-bold transition-all"
                  :class="cocreationStatusFilter === f.value ? 'bg-primary text-white shadow-md shadow-primary/20' : 'bg-white border border-outline-variant/20 text-secondary/60 hover:bg-surface'">{{ f.label }}</button>
              </div>
              <div v-if="loadingCocreation" class="py-8 text-center text-sm text-secondary/40 font-bold">加载中...</div>
              <div v-else-if="!cocreationList.length" class="text-center py-8 text-secondary/40">
                <InboxIcon class="w-10 h-10 mx-auto mb-3 opacity-30" />
                <p class="font-bold text-sm">暂无{{ cocreationStatusFilters.find(f => f.value === cocreationStatusFilter)?.label }}投稿</p>
              </div>
              <div v-else class="space-y-4">
                <div v-for="item in cocreationList" :key="'cc-' + item.id"
                  class="bg-white rounded-3xl p-6 border border-outline-variant/10 shadow-sm hover:shadow-md transition-all">
                  <div class="flex flex-col md:flex-row gap-6">
                    <img v-if="item.cover" :src="item.cover" class="w-full md:w-40 h-32 object-cover rounded-2xl"
                      referrerpolicy="no-referrer" />
                    <div v-else class="w-full md:w-40 h-32 bg-surface rounded-2xl flex items-center justify-center">
                      <ImageIcon class="w-8 h-8 text-secondary/20" />
                    </div>
                    <div class="flex-grow">
                      <div class="flex justify-between items-start mb-2">
                        <div class="flex items-center gap-2">
                          <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-tertiary/10 text-tertiary">共创</span>
                          <h4 class="font-bold text-on-surface">{{ item.title }}</h4>
                        </div>
                        <span class="text-[10px] font-bold px-2 py-0.5 rounded" :class="cocreationBadgeClass(item.status)">{{ item.status_display }}</span>
                      </div>
                      <p class="text-[10px] text-secondary/40 mb-2">作者 {{ item.author }} | 主材 {{ item.material }}</p>
                      <p class="text-xs text-secondary/60 line-clamp-2 leading-relaxed mb-4">{{ item.desc }}</p>
                      <div class="flex items-center gap-4 text-[10px] text-secondary/40 mb-4">
                        <span>❤ {{ item.likes }}</span>
                        <span>进度 {{ item.progress_percent }}%</span>
                      </div>
                      <div v-if="item.status === 'submitted'" class="flex gap-3">
                        <button @click="auditCocreation(item.id, 'reviewing', 25)" class="px-4 py-1.5 bg-primary text-white text-[10px] font-bold rounded-lg">通过初审</button>
                        <button @click="auditCocreation(item.id, 'rejected', 0)" class="px-4 py-1.5 text-error text-[10px] font-bold rounded-lg border border-error/20 hover:bg-error/5">驳回</button>
                      </div>
                      <div v-else-if="item.status === 'reviewing'" class="flex gap-3">
                        <button @click="auditCocreation(item.id, 'sampling', 50)" class="px-4 py-1.5 bg-primary text-white text-[10px] font-bold rounded-lg">进入打样</button>
                      </div>
                      <div v-else-if="item.status === 'sampling'" class="flex gap-3">
                        <button @click="auditCocreation(item.id, 'producing', 75)" class="px-4 py-1.5 bg-primary text-white text-[10px] font-bold rounded-lg">进入投产</button>
                      </div>
                      <div v-else-if="item.status === 'producing'" class="flex gap-3">
                        <button @click="auditCocreation(item.id, 'adopted', 100)" class="px-4 py-1.5 bg-green-600 text-white text-[10px] font-bold rounded-lg">正式采纳</button>
                      </div>
                      <p v-else class="text-xs text-secondary/40 italic">{{ item.status === 'adopted' ? '✓ 已采纳' : item.status === 'rejected' ? '✕ 已驳回' : '' }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Users & Moderators View -->
          <div v-if="activeTab === 'users'" class="space-y-6">
            <div class="flex gap-3">
              <button v-for="t in userTabs" :key="t.value" @click="userRoleFilter = t.value"
                class="px-5 py-2 rounded-xl text-xs font-bold transition-all"
                :class="userRoleFilter === t.value ? 'bg-primary text-white shadow-md shadow-primary/20' : 'bg-white border border-outline-variant/20 text-secondary/60 hover:bg-surface'">{{
                  t.label }}</button>
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
                          <img v-if="user.avatar" :src="user.avatar" class="w-full h-full object-cover"
                            referrerpolicy="no-referrer" />
                          <div v-else
                            class="w-full h-full flex items-center justify-center text-xs font-bold text-secondary/40">
                            {{ (user.name || '?')[0] }}</div>
                        </div>
                        <div>
                          <p class="text-sm font-bold">{{ user.name }}</p>
                          <p class="text-[10px] text-secondary/40">{{ user.email }}</p>
                        </div>
                      </div>
                    </td>
                    <td class="px-8 py-6">
                      <span class="px-3 py-1 rounded-full text-[10px] font-bold" :class="user.roleBg">{{ user.role
                      }}</span>
                    </td>
                    <td class="px-8 py-6">
                      <div class="flex items-center">
                        <div class="w-1.5 h-1.5 rounded-full mr-2" :class="user.active ? 'bg-green-500' : 'bg-red-500'">
                        </div>
                        <span class="text-xs text-secondary/60">{{ user.active ? '活跃' : '禁用' }}</span>
                      </div>
                    </td>
                    <td class="px-8 py-6">
                      <div class="flex gap-3 items-center">
                        <select :value="user._rawRole"
                          @change="onSetRole(user.id, ($event.target as HTMLSelectElement).value)"
                          class="text-xs font-bold text-primary border-none bg-transparent cursor-pointer focus:ring-0">
                          <option value="user">普通用户</option>
                          <option value="moderator">版主</option>
                        </select>
                        <button @click="onBanToggle(user)" class="text-xs font-bold hover:underline"
                          :class="user.active ? 'text-error' : 'text-primary'">{{ user.active ? '禁用' : '启用' }}</button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Quiz View -->
          <div v-if="activeTab === 'quiz'" class="space-y-6">
            <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
              <select v-model="quizMonumentFilter"
                class="bg-white border border-outline-variant/10 rounded-xl px-4 py-2.5 text-sm focus:ring-1 focus:ring-primary/20">
                <option value="">全部古建</option>
                <option v-for="m in monumentList" :key="m.id" :value="m.id">{{ m.name }}</option>
              </select>
              <button @click="openQuizModal(null)"
                class="px-6 py-2.5 bg-primary text-white text-xs font-bold rounded-xl flex items-center shadow-lg shadow-primary/20">
                <PlusIcon class="w-4 h-4 mr-2" /> 添加古建题
              </button>
            </div>

            <div v-if="!filteredQuiz.length" class="text-center py-16 text-secondary/40">
              <BookOpenIcon class="w-12 h-12 mx-auto mb-4 opacity-30" />
              <p class="font-bold text-sm text-secondary/40">暂无题目，点击“新增题目”开始录入</p>
            </div>

            <div class="space-y-4">
              <div v-for="q in filteredQuiz" :key="q.id"
                class="bg-white rounded-2xl p-6 border border-outline-variant/10 shadow-sm hover:shadow-md transition-all">
                <div class="flex gap-4">
                  <img v-if="q.image" :src="q.image" class="w-24 h-24 object-cover rounded-xl shrink-0"
                    referrerpolicy="no-referrer" />
                  <div class="flex-grow">
                    <div class="flex items-start justify-between mb-3">
                      <p class="text-sm font-bold text-on-surface leading-snug mr-4">{{ q.description }}</p>
                      <div class="flex gap-3 shrink-0">
                        <button @click="openQuizModal(q)"
                          class="text-[10px] font-bold text-primary hover:underline">编辑</button>
                        <button @click="deleteQuiz(q.id)"
                          class="text-[10px] font-bold text-error hover:underline">删除</button>
                      </div>
                    </div>
                    <div class="flex flex-wrap gap-2 text-[10px]">
                      <template v-for="opt in (q.options || [])" :key="opt.id">
                        <span :class="opt.is_correct
                          ? 'px-3 py-1 bg-green-100 text-green-700 rounded-full font-bold'
                          : 'px-3 py-1 bg-surface text-secondary/60 rounded-full'">
                          {{ opt.is_correct ? '✓ ' : '' }}{{ opt.label }}
                        </span>
                      </template>
                      <span class="px-3 py-1 bg-blue-50 text-blue-600 rounded-full">
                        {{ q.question_type === 'multi' ? '多选' : '单选' }} · {{ q.points }}分
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Monuments Management View -->
          <div v-if="activeTab === 'monuments-mgmt'" class="space-y-6">
            <div class="flex justify-between items-center">
              <p class="text-xs text-secondary/40 font-bold">已发布和未发布的全部古建筑</p>
              <button @click="openMonumentModal(null)"
                class="px-6 py-2.5 bg-primary text-white text-xs font-bold rounded-xl flex items-center shadow-lg shadow-primary/20">
                <PlusIcon class="w-4 h-4 mr-2" /> 新增古建
              </button>
            </div>
            <div v-if="!mgmtMonumentList.length" class="text-center py-16 text-secondary/40">
              <LandmarkIcon class="w-12 h-12 mx-auto mb-4 opacity-30" />
              <p class="font-bold text-sm">暂无古建数据</p>
            </div>
            <div class="bg-white rounded-3xl border border-outline-variant/10 shadow-sm overflow-hidden">
              <table class="w-full text-left border-collapse">
                <thead class="bg-surface">
                  <tr>
                    <th class="px-6 py-4 text-[10px] font-bold text-secondary/40 uppercase tracking-widest">名称</th>
                    <th class="px-6 py-4 text-[10px] font-bold text-secondary/40 uppercase tracking-widest">朝代</th>
                    <th class="px-6 py-4 text-[10px] font-bold text-secondary/40 uppercase tracking-widest">状态</th>
                    <th class="px-6 py-4 text-[10px] font-bold text-secondary/40 uppercase tracking-widest">操作</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-outline-variant/10">
                  <tr v-for="m in mgmtMonumentList" :key="m.id" class="hover:bg-surface/50 transition-colors">
                    <td class="px-6 py-4">
                      <div class="flex items-center gap-3">
                        <img v-if="m.cover_image" :src="m.cover_image" class="w-10 h-10 rounded-lg object-cover"
                          referrerpolicy="no-referrer" />
                        <div v-else class="w-10 h-10 rounded-lg bg-secondary/10 flex items-center justify-center">
                          <LandmarkIcon class="w-4 h-4 text-secondary/30" />
                        </div>
                        <span class="text-sm font-bold">{{ m.name }}</span>
                      </div>
                    </td>
                    <td class="px-6 py-4 text-xs text-secondary/60">{{ m.dynasty || '-' }}</td>
                    <td class="px-6 py-4">
                      <span class="text-[10px] font-bold px-2 py-0.5 rounded"
                        :class="m.is_published ? 'bg-green-100 text-green-700' : 'bg-secondary/10 text-secondary/60'">
                        {{ m.is_published ? '已发布' : '草稿' }}
                      </span>
                    </td>
                    <td class="px-6 py-4 flex gap-3">
                      <button @click="openMonumentModal(m)"
                        class="text-[10px] font-bold text-primary hover:underline">编辑</button>
                      <button @click="toggleMonumentPublish(m)" class="text-[10px] font-bold hover:underline"
                        :class="m.is_published ? 'text-secondary/40' : 'text-green-600'">
                        {{ m.is_published ? '取消发布' : '发布' }}
                      </button>
                      <button @click="deleteMonument(m.id)"
                        class="text-[10px] font-bold text-error hover:underline">删除</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Stamp Management View -->
          <div v-if="activeTab === 'stamp-mgmt'" class="space-y-6">
            <div class="flex justify-between items-center">
              <p class="text-xs text-secondary/40 font-bold">印章与套色图层管理</p>
              <button @click="openStampModal(null)"
                class="px-6 py-2.5 bg-primary text-white text-xs font-bold rounded-xl flex items-center shadow-lg shadow-primary/20">
                <PlusIcon class="w-4 h-4 mr-2" /> 新增印章
              </button>
            </div>
            <div v-if="!mgmtStampList.length" class="text-center py-16 text-secondary/40">
              <StampIcon class="w-12 h-12 mx-auto mb-4 opacity-30" />
              <p class="font-bold text-sm">暂无印章数据</p>
            </div>
            <div class="space-y-6">
              <div v-for="stamp in mgmtStampList" :key="stamp.id"
                class="bg-white rounded-3xl p-6 border border-outline-variant/10 shadow-sm">
                <div class="flex justify-between items-start mb-4">
                  <div>
                    <h4 class="font-bold text-sm">{{ stamp.name }}</h4>
                    <p class="text-[10px] text-secondary/40">关联古建: {{ stamp.monument_name || '未关联' }} · {{
                      stamp.color_layers?.length || 0 }} 个图层</p>
                  </div>
                  <div class="flex gap-3">
                    <button @click="openStampModal(stamp)"
                      class="text-[10px] font-bold text-primary hover:underline">编辑</button>
                    <button @click="deleteStamp(stamp.id)"
                      class="text-[10px] font-bold text-error hover:underline">删除</button>
                  </div>
                </div>
                <!-- Layers -->
                <div class="space-y-3">
                  <div v-for="layer in (stamp.color_layers || [])" :key="layer.id"
                    class="flex items-center gap-4 p-3 bg-surface rounded-xl">
                    <GripIcon class="w-4 h-4 text-secondary/20 shrink-0" />
                    <div class="w-4 h-4 rounded-full shrink-0" :style="{ backgroundColor: layer.color }"></div>
                    <span class="text-xs font-bold flex-grow">{{ layer.layer_name }} (第{{ layer.layer_index }}层)</span>
                    <span class="text-[10px] text-secondary/40">{{ layer.blend_mode }}</span>
                    <img v-if="layer.svg_url" :src="layer.svg_url" class="h-8 w-8 object-contain"
                      referrerpolicy="no-referrer" />
                    <button @click="deleteStampLayer(layer.id, stamp.id)"
                      class="text-secondary/30 hover:text-error transition-colors">
                      <TrashIcon class="w-3.5 h-3.5" />
                    </button>
                  </div>
                  <button @click="openLayerModal(stamp.id)"
                    class="w-full py-3 border border-dashed border-outline-variant/30 rounded-xl text-xs font-bold text-primary hover:bg-primary/5 transition-all flex items-center justify-center gap-2">
                    <UploadIcon class="w-3.5 h-3.5" /> 新增图层
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Articles Management View -->
          <div v-if="activeTab === 'articles-mgmt'" class="space-y-6">
            <div class="flex justify-between items-center">
              <p class="text-xs text-secondary/40 font-bold">古建文章与答题页面管理</p>
              <button @click="openArticleModal(null)"
                class="px-6 py-2.5 bg-primary text-white text-xs font-bold rounded-xl flex items-center shadow-lg shadow-primary/20">
                <PlusIcon class="w-4 h-4 mr-2" /> 新增文章
              </button>
            </div>
            <div v-if="!mgmtArticleList.length" class="text-center py-16 text-secondary/40">
              <FileTextIcon class="w-12 h-12 mx-auto mb-4 opacity-30" />
              <p class="font-bold text-sm">暂无文章数据</p>
            </div>
            <div class="space-y-6">
              <div v-for="article in mgmtArticleList" :key="article.id"
                class="bg-white rounded-3xl p-6 border border-outline-variant/10 shadow-sm">
                <div class="flex justify-between items-start mb-4">
                  <div>
                    <h4 class="font-bold text-sm">{{ article.title }}</h4>
                    <p class="text-[10px] text-secondary/40">关联古建: {{ article.monument_name || '未关联' }} · {{
                      article.pages?.length
                      || 0 }} 页</p>
                  </div>
                  <div class="flex gap-3 items-center">
                    <button @click="checkArticleConsistency(article.id)"
                      class="text-[10px] font-bold text-secondary/40 hover:text-primary flex items-center gap-1">
                      <AlertCircleIcon class="w-3 h-3" /> 一致性检测
                    </button>
                    <button @click="openArticleModal(article)"
                      class="text-[10px] font-bold text-primary hover:underline">编辑</button>
                    <button @click="deleteArticle(article.id)"
                      class="text-[10px] font-bold text-error hover:underline">删除</button>
                  </div>
                </div>
                <!-- Pages List -->
                <div class="space-y-3">
                  <div v-for="page in (article.pages || [])" :key="page.id"
                    class="bg-surface rounded-xl overflow-hidden">
                    <div class="flex items-center justify-between p-4 cursor-pointer"
                      @click="togglePageExpand(page.id)">
                      <div class="flex items-center gap-3">
                        <ChevronRightIcon class="w-4 h-4 text-secondary/30 transition-transform"
                          :class="expandedPages.has(page.id) ? 'rotate-90' : ''" />
                        <span class="text-xs font-bold">第{{ page.page_number }}页</span>
                        <span class="text-[10px] text-secondary/40">{{ (page.quiz_questions || []).length }}道题目</span>
                      </div>
                      <div class="flex gap-2">
                        <button @click.stop="openPageModal(article.id, page)"
                          class="text-[10px] font-bold text-primary hover:underline">编辑</button>
                        <button @click.stop="deletePage(page.id, article.id)"
                          class="text-[10px] font-bold text-error hover:underline">删除</button>
                      </div>
                    </div>
                    <div v-if="expandedPages.has(page.id)" class="px-4 pb-4 border-t border-outline-variant/10">
                      <div class="text-xs text-secondary/60 leading-relaxed mt-3 line-clamp-4" v-html="page.content">
                      </div>
                      <div v-if="page.quiz_questions?.length" class="mt-3 space-y-2">
                        <div v-for="q in page.quiz_questions" :key="q.id"
                          class="flex items-center gap-2 text-[10px] text-secondary/40">
                          <CheckCircleIcon class="w-3 h-3 text-primary" />
                          <span>{{ q.description }} ({{ q.points }}分)</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <button @click="openPageModal(article.id, null)"
                    class="w-full py-3 border border-dashed border-outline-variant/30 rounded-xl text-xs font-bold text-primary hover:bg-primary/5 transition-all flex items-center justify-center gap-2">
                    <PlusIcon class="w-3.5 h-3.5" /> 新增页面
                  </button>
                </div>
              </div>
            </div>
          </div>

        </main>
      </div>
    </div>
  </div>
  <!-- Monument Modal -->
  <Teleport to="body">
    <div v-if="showMonumentModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      @click.self="showMonumentModal = false">
      <div class="bg-white rounded-3xl p-8 w-full max-w-lg mx-4 shadow-2xl max-h-[90vh] overflow-y-auto">
        <h3 class="font-serif text-xl mb-6">{{ editingMonumentId ? '编辑古建' : '新增古建' }}</h3>
        <div class="space-y-4">
          <input v-model="monumentForm.name" type="text" placeholder="古建名称"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
          <input v-model="monumentForm.dynasty" type="text" placeholder="朝代（如：宋代）"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
          <input v-model="monumentForm.location" type="text" placeholder="所在位置"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
          <textarea v-model="monumentForm.description" placeholder="简介描述" rows="3"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20 resize-none"></textarea>
          <div class="flex items-center gap-4">
            <label
              class="cursor-pointer px-4 py-2 bg-surface rounded-xl text-xs font-bold text-secondary hover:bg-secondary/10 transition-all">
              <input type="file" accept="image/*" class="hidden" @change="onMonumentCoverChange" />
              {{ monumentCoverPreview ? '更换封面' : '上传封面' }}
            </label>
            <img v-if="monumentCoverPreview" :src="monumentCoverPreview" class="h-16 rounded-xl object-cover"
              referrerpolicy="no-referrer" />
          </div>
          <label class="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" v-model="monumentForm.is_published" class="accent-primary" />
            <span class="text-sm">发布</span>
          </label>
        </div>
        <div class="flex gap-3 mt-8">
          <button @click="showMonumentModal = false"
            class="flex-1 py-3 bg-surface rounded-xl text-sm font-bold text-secondary">取消</button>
          <button @click="saveMonument" :disabled="monumentSaving"
            class="flex-1 py-3 bg-primary text-white text-sm font-bold rounded-xl shadow-lg shadow-primary/20 disabled:opacity-60">
            {{ monumentSaving ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
  <!-- Stamp Modal -->
  <Teleport to="body">
    <div v-if="showStampModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      @click.self="showStampModal = false">
      <div class="bg-white rounded-3xl p-8 w-full max-w-lg mx-4 shadow-2xl max-h-[90vh] overflow-y-auto">
        <h3 class="font-serif text-xl mb-6">{{ editingStampId ? '编辑印章' : '新增印章' }}</h3>
        <div class="space-y-4">
          <input v-model="stampForm.name" type="text" placeholder="印章名称"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
          <select v-model="stampForm.monument"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20">
            <option :value="null">请选择关联古建</option>
            <option v-for="m in mgmtMonumentList" :key="m.id" :value="m.id">{{ m.name }}</option>
          </select>
          <textarea v-model="stampForm.description" placeholder="印章描述" rows="2"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20 resize-none"></textarea>
        </div>
        <div class="flex gap-3 mt-8">
          <button @click="showStampModal = false"
            class="flex-1 py-3 bg-surface rounded-xl text-sm font-bold text-secondary">取消</button>
          <button @click="saveStamp" :disabled="stampSaving"
            class="flex-1 py-3 bg-primary text-white text-sm font-bold rounded-xl shadow-lg shadow-primary/20 disabled:opacity-60">
            {{ stampSaving ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
  <!-- Layer Modal -->
  <Teleport to="body">
    <div v-if="showLayerModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      @click.self="showLayerModal = false">
      <div class="bg-white rounded-3xl p-8 w-full max-w-lg mx-4 shadow-2xl max-h-[90vh] overflow-y-auto">
        <h3 class="font-serif text-xl mb-6">新增图层</h3>
        <div class="space-y-4">
          <input v-model="layerForm.layer_name" type="text" placeholder="图层名称（如：素胎底框）"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
          <div class="grid grid-cols-2 gap-4">
            <input v-model.number="layerForm.layer_index" type="number" min="1" placeholder="图层序号"
              class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
            <input v-model="layerForm.color" type="color"
              class="w-full h-[52px] bg-surface border-none rounded-xl p-2 cursor-pointer" />
          </div>
          <select v-model="layerForm.blend_mode"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20">
            <option value="multiply">multiply</option>
            <option value="normal">normal</option>
            <option value="screen">screen</option>
            <option value="overlay">overlay</option>
            <option value="darken">darken</option>
            <option value="color-burn">color-burn</option>
          </select>
          <div class="flex items-center gap-4">
            <label
              class="cursor-pointer px-4 py-2 bg-surface rounded-xl text-xs font-bold text-secondary hover:bg-secondary/10 transition-all">
              <input type="file" accept=".svg,image/svg+xml,image/*" class="hidden" @change="onLayerSvgChange" />
              {{ layerSvgPreview ? '更换SVG' : '上传SVG图层' }}
            </label>
            <img v-if="layerSvgPreview" :src="layerSvgPreview" class="h-16 object-contain"
              referrerpolicy="no-referrer" />
          </div>
        </div>
        <div class="flex gap-3 mt-8">
          <button @click="showLayerModal = false"
            class="flex-1 py-3 bg-surface rounded-xl text-sm font-bold text-secondary">取消</button>
          <button @click="saveLayer" :disabled="layerSaving"
            class="flex-1 py-3 bg-primary text-white text-sm font-bold rounded-xl shadow-lg shadow-primary/20 disabled:opacity-60">
            {{ layerSaving ? '保存中...' : '保存图层' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
  <!-- Article Modal -->
  <Teleport to="body">
    <div v-if="showArticleModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      @click.self="showArticleModal = false">
      <div class="bg-white rounded-3xl p-8 w-full max-w-lg mx-4 shadow-2xl max-h-[90vh] overflow-y-auto">
        <h3 class="font-serif text-xl mb-6">{{ editingArticleId ? '编辑文章' : '新增文章' }}</h3>
        <div class="space-y-4">
          <input v-model="articleForm.title" type="text" placeholder="文章标题"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
          <select v-model="articleForm.monument"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20">
            <option :value="null">选择关联古建</option>
            <option v-for="m in mgmtMonumentList" :key="m.id" :value="m.id">{{ m.name }}</option>
          </select>
        </div>
        <div class="flex gap-3 mt-8">
          <button @click="showArticleModal = false"
            class="flex-1 py-3 bg-surface rounded-xl text-sm font-bold text-secondary">取消</button>
          <button @click="saveArticle" :disabled="articleSaving"
            class="flex-1 py-3 bg-primary text-white text-sm font-bold rounded-xl shadow-lg shadow-primary/20 disabled:opacity-60">
            {{ articleSaving ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
  <!-- Page Modal -->
  <Teleport to="body">
    <div v-if="showPageModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      @click.self="showPageModal = false">
      <div class="bg-white rounded-3xl p-8 w-full max-w-2xl mx-4 shadow-2xl max-h-[90vh] overflow-y-auto">
        <h3 class="font-serif text-xl mb-6">{{ editingPageId ? '编辑页面' : '新增页面' }}</h3>
        <div class="space-y-4">
          <input v-model.number="pageForm.page_number" type="number" min="1" placeholder="页码（如：1）"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
          <textarea v-model="pageForm.content" placeholder="页面内容（支持HTML）" rows="10"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20 resize-none font-mono"></textarea>
        </div>
        <div class="flex gap-3 mt-8">
          <button @click="showPageModal = false"
            class="flex-1 py-3 bg-surface rounded-xl text-sm font-bold text-secondary">取消</button>
          <button @click="savePage" :disabled="pageSaving"
            class="flex-1 py-3 bg-primary text-white text-sm font-bold rounded-xl shadow-lg shadow-primary/20 disabled:opacity-60">
            {{ pageSaving ? '保存中...' : '保存页面' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
  <!-- Quiz 编辑古建题 -->
  <Teleport to="body">
    <div v-if="showQuizModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      @click.self="showQuizModal = false">
      <div class="bg-white rounded-3xl p-8 w-full max-w-lg mx-4 shadow-2xl max-h-[90vh] overflow-y-auto">
        <h3 class="font-serif text-xl mb-6">{{ editingQuizId ? '编辑古建题' : '添加古建题' }}</h3>
        <div class="space-y-4">
          <textarea v-model="quizForm.description" placeholder="古建题描述" rows="3"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20 resize-none"></textarea>
          <div class="grid grid-cols-2 gap-4">
            <select v-model="quizForm.question_type"
              class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20">
              <option value="single">单选题</option>
              <option value="multi">多选题</option>
            </select>
            <input v-model.number="quizForm.points" type="number" min="1" placeholder="答对积分"
              class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20" />
          </div>
          <div class="space-y-2">
            <p class="text-xs font-bold text-secondary/50">选项（勾选复选框为正确答案）</p>
            <div v-for="(opt, idx) in quizForm.options" :key="idx" class="flex items-center gap-3">
              <input type="checkbox" v-model="opt.is_correct" class="accent-primary shrink-0" />
              <input v-model="opt.label" type="text" :placeholder="`选项 ${idx + 1}`"
                class="flex-1 bg-surface border-none rounded-xl p-3 text-sm focus:ring-1 focus:ring-primary/20" />
              <button v-if="quizForm.options.length > 2" @click="removeQuizOption(idx)" type="button"
                class="text-red-400 hover:text-red-600 shrink-0">
                <XIcon class="w-4 h-4" />
              </button>
            </div>
            <button @click="addQuizOption" type="button"
              class="text-xs font-bold text-primary hover:underline flex items-center gap-1 mt-1">
              <PlusIcon class="w-3 h-3" /> 添加选项
            </button>
          </div>
          <select v-model="quizForm.monument"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20">
            <option :value="null">请选择关联古建</option>
            <option v-for="m in monumentList" :key="m.id" :value="m.id">{{ m.name }}</option>
          </select>
          <select v-model="quizForm.article_page"
            class="w-full bg-surface border-none rounded-xl p-4 text-sm focus:ring-1 focus:ring-primary/20">
            <option :value="null">不绑定文章页（可选）</option>
            <option v-for="p in articlePageList" :key="p.id" :value="p.id">
              第 {{ p.page_number }} 页（{{ p.id }}）
            </option>
          </select>
          <div class="flex items-center gap-4">
            <label
              class="cursor-pointer px-4 py-2 bg-surface rounded-xl text-xs font-bold text-secondary hover:bg-secondary/10 transition-all">
              <input type="file" accept="image/*" class="hidden" @change="onQuizImageChange" />
              {{ quizImagePreview ? '更换图片' : '上传图片，可选 ' }}
            </label>
            <img v-if="quizImagePreview" :src="quizImagePreview" class="h-16 rounded-xl object-cover"
              referrerpolicy="no-referrer" />
          </div>
        </div>
        <div class="flex gap-3 mt-8">
          <button @click="showQuizModal = false"
            class="flex-1 py-3 bg-surface rounded-xl text-sm font-bold text-secondary hover:bg-secondary/10 transition-all">取消</button>
          <button @click="saveQuiz" :disabled="quizSaving"
            class="flex-1 py-3 bg-primary text-white text-sm font-bold rounded-xl shadow-lg shadow-primary/20 disabled:opacity-60">
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
  Landmark as LandmarkIcon,
  Stamp as StampIcon,
  FileText as FileTextIcon,
  Trash2 as TrashIcon,
  ChevronDown as ChevronDownIcon,
  ChevronRight as ChevronRightIcon,
  GripVertical as GripIcon,
  Upload as UploadIcon,
  AlertCircle as AlertCircleIcon,
  CheckCircle as CheckCircleIcon,
} from 'lucide-vue-next';
import service from '../api/request';

const activeTab = ref('dashboard');

const menuItems = [
  { id: 'dashboard', name: '数据大盘', icon: DashboardIcon },
  { id: 'audit', name: '内容审核', icon: AuditIcon },
  { id: 'users', name: '用户管理', icon: UsersIcon },
];
const configItems = [
  { id: 'quiz', name: '题库管理', icon: BookOpenIcon },
  { id: 'monuments-mgmt', name: '古建列表', icon: LandmarkIcon },
  { id: 'stamp-mgmt', name: '印章管理', icon: StampIcon },
  { id: 'articles-mgmt', name: '古建资料', icon: FileTextIcon },
];

const stats = ref([
  { label: '今日新增投稿', value: '-', color: 'bg-primary' },
  { label: '待审核任务', value: '-', color: 'bg-tertiary' },
  { label: '活跃工匠数', value: '-', color: 'bg-on-surface' },
]);
const keywords = ['历史争议', '恶意广告', '违规外链'];

const auditSourceFilters = [
  { value: 'all', label: '全部' },
  { value: 'forum', label: '论坛帖子' },
  { value: 'cocreation', label: '共创投稿' },
];
const auditSourceFilter = ref('all');

// Forum posts in audit
const forumPostList = ref<any[]>([]);
const loadingForumPosts = ref(false);

const fetchForumPosts = async () => {
  loadingForumPosts.value = true;
  try {
    const res = await service.get('/forum/posts/') as any;
    forumPostList.value = res.results || res;
  } catch { forumPostList.value = []; }
  finally { loadingForumPosts.value = false; }
};

const deleteForumPost = async (id: number) => {
  if (!confirm('确定删除该帖子？')) return;
  try {
    await service.delete(`/forum/posts/${id}/`);
    fetchForumPosts();
  } catch { alert('删除失败'); }
};

const toggleForumTop = async (item: any) => {
  try {
    await service.patch(`/forum/posts/${item.id}/`, { is_top: !item.is_top });
    fetchForumPosts();
  } catch { alert('操作失败'); }
};

const toggleForumEssence = async (item: any) => {
  try {
    await service.patch(`/forum/posts/${item.id}/`, { is_essence: !item.is_essence });
    fetchForumPosts();
  } catch { alert('操作失败'); }
};

// CoCreation items in audit
const cocreationList = ref<any[]>([]);
const loadingCocreation = ref(false);
const cocreationStatusFilters = [
  { value: '', label: '全部' },
  { value: 'submitted', label: '待审核' },
  { value: 'reviewing', label: '初审中' },
  { value: 'sampling', label: '打样中' },
  { value: 'producing', label: '试产中' },
  { value: 'adopted', label: '已采纳' },
  { value: 'rejected', label: '已驳回' },
];
const cocreationStatusFilter = ref('');

const fetchCocreationItems = async () => {
  loadingCocreation.value = true;
  try {
    const params: any = {};
    if (cocreationStatusFilter.value) params.status = cocreationStatusFilter.value;
    const res = await service.get('/cocreation/items/', { params }) as any;
    cocreationList.value = res.results || res;
  } catch { cocreationList.value = []; }
  finally { loadingCocreation.value = false; }
};

const cocreationBadgeClass = (status: string) => {
  if (status === 'submitted') return 'bg-tertiary/10 text-tertiary';
  if (status === 'adopted') return 'bg-green-100 text-green-700';
  if (status === 'rejected') return 'bg-red-100 text-red-700';
  return 'bg-blue-100 text-blue-700';
};

const auditCocreation = async (id: number, decision: string, progress: number) => {
  try {
    await service.post(`/cocreation/items/${id}/audit/`, {
      status: decision,
      progress_percent: progress,
    });
    fetchCocreationItems();
    fetchDashboardStats();
  } catch { alert('操作失败'); }
};

// Old submissions (monument submissions) for dashboard preview
const submissionList = ref<any[]>([]);
const loadingSubmissions = ref(false);
const feedbackMap = ref<Record<number, string>>({});

const fetchSubmissions = async () => {
  // Combine forum posts + cocreation for dashboard preview
  const items: any[] = [];
  try {
    const forumRes = await service.get('/forum/posts/', { params: { ordering: '-created_at' } }) as any;
    const forumPosts = (forumRes.results || forumRes).slice(0, 3);
    for (const p of forumPosts) {
      items.push({ id: 'f-' + p.id, title: p.title, author: p.author, time: p.time, image: p.cover, source: 'forum' });
    }
  } catch {}
  try {
    const ccRes = await service.get('/cocreation/items/', { params: { status: 'submitted' } }) as any;
    const ccItems = (ccRes.results || ccRes).slice(0, 3);
    for (const c of ccItems) {
      items.push({ id: 'c-' + c.id, title: c.title, author: c.author, time: '', image: c.cover, source: 'cocreation' });
    }
  } catch {}
  submissionList.value = items;
};

const fetchDashboardStats = async () => {
  try {
    const res = await service.get('/system/dashboard/') as any;
    stats.value = [
      { label: '今日新增投稿', value: String(res.today_submissions ?? 0), color: 'bg-primary' },
      { label: '待审核任务', value: String(res.pending_audit ?? 0), color: 'bg-tertiary' },
      { label: '活跃工匠数', value: String(res.active_users ?? 0), color: 'bg-on-surface' },
    ];
  } catch (e) {
    console.error('Failed to fetch dashboard stats:', e);
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
  const res = await service.get('/users/users/') as any;
  userList.value = (res.results || res).map((u: any) => ({
    ...u,
    _rawRole: roleDisplayToRaw[u.role] ?? 'user',
  }));
};

const onBanToggle = async (user: any) => {
  try {
    await service.post(`/users/users/${user.id}/${user.active ? 'ban' : 'unban'}/`);
    fetchUsers();
  } catch {
    alert('操作失败');
  }
};

const onSetRole = async (userId: number, role: string) => {
  try {
    await service.post(`/users/users/${userId}/set-role/`, { role });
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
  const res = await service.get('/quiz/questions/') as any;
  quizList.value = res.results || res;
};

const fetchMonuments = async () => {
  const res = await service.get('/monuments/monuments/') as any;
  monumentList.value = (res.results || res).filter((m: any) => m.is_published);
  console.log('Monuments:', monumentList.value);
};

const showQuizModal = ref(false);
const editingQuizId = ref<number | null>(null);
const quizForm = ref({
  description: '',
  question_type: 'single' as 'single' | 'multi',
  monument: null as number | null,
  points: 10,
  article_page: null as number | null,
  // 选项列表：至少需要展示 correct_answer + distractor_a + distractor_b
  options: [
    { label: '', is_correct: true, order: 0 },   // 正确答案
    { label: '', is_correct: false, order: 1 },  // 干扰A
    { label: '', is_correct: false, order: 2 },  // 干扰B
  ],
});
const quizImageFile = ref<File | null>(null);
const quizImagePreview = ref('');
const quizSaving = ref(false);

const openQuizModal = (quiz: any) => {
  if (quiz) {
    editingQuizId.value = quiz.id;
    quizForm.value = {
      description: quiz.description,
      question_type: quiz.question_type || 'single',
      monument: quiz.monument,
      points: quiz.points ?? 10,
      article_page: quiz.article_page ?? null,
      options: quiz.options?.length
        ? quiz.options.map((o: any) => ({ label: o.label, is_correct: o.is_correct, order: o.order }))
        : [{ label: '', is_correct: true, order: 0 }, { label: '', is_correct: false, order: 1 }, { label: '', is_correct: false, order: 2 }],
    };
    quizImagePreview.value = quiz.image || '';
  } else {
    editingQuizId.value = null;
    quizForm.value = {
      description: '',
      question_type: 'single',
      monument: null,
      points: 10,
      article_page: null,
      options: [
        { label: '', is_correct: true, order: 0 },
        { label: '', is_correct: false, order: 1 },
        { label: '', is_correct: false, order: 2 },
      ],
    };
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
  if (!quizForm.value.description.trim()) {
    alert('请填写题目描述');
    return;
  }
  const hasCorrect = quizForm.value.options.some((o: any) => o.is_correct && o.label.trim());
  if (!hasCorrect) {
    alert('请至少填写并勾选一个正确答案');
    return;
  }
  quizSaving.value = true;
  try {
    // 第一步：保存题目本身
    const fd = new FormData();
    fd.append('description', quizForm.value.description);
    fd.append('question_type', quizForm.value.question_type);
    fd.append('points', String(quizForm.value.points));
    if (quizForm.value.monument) fd.append('monument', String(quizForm.value.monument));
    if (quizImageFile.value) fd.append('image', quizImageFile.value);
    if (quizForm.value.article_page) fd.append('article_page', String(quizForm.value.article_page));
    let questionId = editingQuizId.value;
    if (questionId) {
      await service.patch(`/quiz/questions/${questionId}/`, fd);
    } else {
      const res = await service.post('/quiz/questions/', fd) as any;
      questionId = res.id;
    }

    // 第二步：删除旧选项，重建新选项
    const existingRes = await service.get(`/quiz/options/?question=${questionId}`) as any;
    const existingOptions = existingRes.results || existingRes;
    for (const opt of existingOptions) {
      await service.delete(`/quiz/options/${opt.id}/`);
    }
    for (const [i, opt] of quizForm.value.options.entries()) {
      if (!opt.label.trim()) continue;
      const ofd = new FormData();
      ofd.append('question', String(questionId));
      ofd.append('label', opt.label);
      ofd.append('is_correct', String(opt.is_correct));
      ofd.append('order', String(i));
      await service.post('/quiz/options/', ofd);
    }

    showQuizModal.value = false;
    fetchQuizList();
  } catch {
    alert('保存失败');
  } finally {
    quizSaving.value = false;
  }
};

const addQuizOption = () => {
  quizForm.value.options.push({ label: '', is_correct: false, order: quizForm.value.options.length });
};

const removeQuizOption = (index: number) => {
  quizForm.value.options.splice(index, 1);
};

const deleteQuiz = async (id: number) => {
  if (!confirm('确定删除此题目？')) return;
  try {
    await service.delete(`/quiz/questions/${id}/`);
    fetchQuizList();
  } catch {
    alert('删除失败');
  }
};

onMounted(() => {
  fetchDashboardStats();
  fetchSubmissions();
  fetchForumPosts();
  fetchCocreationItems();
  fetchUsers();
  fetchQuizList();
  fetchMonuments();
  fetchMgmtMonuments();
  fetchMgmtStamps();
  fetchMgmtArticles();
});

// ===== Monuments Management =====
const mgmtMonumentList = ref<any[]>([]);
const showMonumentModal = ref(false);
const editingMonumentId = ref<number | null>(null);
const monumentForm = ref({ name: '', dynasty: '', location: '', description: '', is_published: false });
const monumentCoverFile = ref<File | null>(null);
const monumentCoverPreview = ref('');
const monumentSaving = ref(false);

const fetchMgmtMonuments = async () => {
  try {
    const res = await service.get('/monuments/monuments/') as any;
    mgmtMonumentList.value = res.results || res;
  } catch { mgmtMonumentList.value = []; }
};

const openMonumentModal = (m: any) => {
  if (m) {
    editingMonumentId.value = m.id;
    monumentForm.value = { name: m.name, dynasty: m.dynasty || '', location: m.location || '', description: m.desc || '', is_published: m.is_published };
    monumentCoverPreview.value = m.cover_image || '';
  } else {
    editingMonumentId.value = null;
    monumentForm.value = { name: '', dynasty: '', location: '', description: '', is_published: false };
    monumentCoverPreview.value = '';
  }
  monumentCoverFile.value = null;
  showMonumentModal.value = true;
};

const onMonumentCoverChange = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (file) { monumentCoverFile.value = file; monumentCoverPreview.value = URL.createObjectURL(file); }
};

const saveMonument = async () => {
  if (!monumentForm.value.name.trim()) { alert('请填写古建名称'); return; }
  monumentSaving.value = true;

  try {
    const fd = new FormData();
    fd.append('name', monumentForm.value.name);
    fd.append('dynasty', monumentForm.value.dynasty);
    fd.append('location', monumentForm.value.location);
    fd.append('desc', monumentForm.value.description);
    fd.append('is_published', String(monumentForm.value.is_published));
    if (monumentCoverFile.value) fd.append('cover_image', monumentCoverFile.value);

    // ✅ 第一步：在发送前打印！
    console.log("--- [DEBUG] 准备发送的数据 ---");
    for (let [key, value] of fd.entries()) {
      console.log(`${key}:`, value);
    }

    // ✅ 第二步：发送请求
    let res;
    if (editingMonumentId.value) {
      res = await service.patch(`/monuments/monuments/${editingMonumentId.value}/`, fd);
    } else {
      res = await service.post('/monuments/monuments/', fd);
    }

    // ✅ 第三步：请求成功后的反馈
    console.log("--- [DEBUG] 后端返回响应 ---", res);

    showMonumentModal.value = false;
    fetchMgmtMonuments();
    fetchMonuments();
    alert('保存成功');

  } catch (error: any) {
    console.error("--- [DEBUG] 请求失败 ---");
    // 打印后端返回的字段校验错误（比如 description 为什么没存上）
    console.log("后端报错详情:", error.response?.data);
    alert('保存失败，请看控制台错误信息');
  } finally {
    monumentSaving.value = false;
  }
};

const toggleMonumentPublish = async (m: any) => {
  try {
    await service.patch(`/monuments/monuments/${m.id}/`, { is_published: !m.is_published });
    fetchMgmtMonuments();
    fetchMonuments();
  } catch { alert('操作失败'); }
};

const deleteMonument = async (id: number) => {
  if (!confirm('确定删除此古建？关联的印章和文章也将受到影响。')) return;
  try { await service.delete(`/monuments/monuments/${id}/`); fetchMgmtMonuments(); } catch { alert('删除失败'); }
};

// ===== Stamp Management =====
const mgmtStampList = ref<any[]>([]);
const showStampModal = ref(false);
const editingStampId = ref<number | null>(null);
const stampForm = ref({ name: '', monument: null as number | null, description: '' });
const stampSaving = ref(false);

const showLayerModal = ref(false);
const layerStampId = ref<number | null>(null);
const layerForm = ref({ layer_name: '', layer_index: 1, color: '#970010', blend_mode: 'multiply' });
const layerSvgFile = ref<File | null>(null);
const layerSvgPreview = ref('');
const layerSaving = ref(false);

const fetchMgmtStamps = async () => {
  try {
    const res = await service.get('/stamps/stamps/') as any;
    mgmtStampList.value = res.results || res;
  } catch { mgmtStampList.value = []; }
};

const openStampModal = (s: any) => {
  if (s) {
    editingStampId.value = s.id;
    stampForm.value = { name: s.name, monument: s.monument, description: s.description || '' };
  } else {
    editingStampId.value = null;
    stampForm.value = { name: '', monument: null, description: '' };
  }
  showStampModal.value = true;
};

const saveStamp = async () => {
  if (!stampForm.value.name.trim()) { alert('请填写印章名称'); return; }
  stampSaving.value = true;
  try {
    const data: any = { name: stampForm.value.name, description: stampForm.value.description };
    if (stampForm.value.monument) data.monument = stampForm.value.monument;
    if (editingStampId.value) {
      await service.patch(`/stamps/stamps/${editingStampId.value}/`, data);
    } else {
      await service.post('/stamps/stamps/', data);
    }
    showStampModal.value = false;
    fetchMgmtStamps();
  } catch { alert('保存失败'); }
  finally { stampSaving.value = false; }
};

const deleteStamp = async (id: number) => {
  if (!confirm('确定删除此印章？')) return;
  try { await service.delete(`/stamps/stamps/${id}/`); fetchMgmtStamps(); } catch { alert('删除失败'); }
};

const openLayerModal = (stampId: number) => {
  layerStampId.value = stampId;
  layerForm.value = { layer_name: '', layer_index: 1, color: '#970010', blend_mode: 'multiply' };
  layerSvgFile.value = null;
  layerSvgPreview.value = '';
  showLayerModal.value = true;
};

const onLayerSvgChange = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (file) { layerSvgFile.value = file; layerSvgPreview.value = URL.createObjectURL(file); }
};

const saveLayer = async () => {
  if (!layerForm.value.layer_name.trim()) { alert('请填写图层名称'); return; }
  layerSaving.value = true;
  try {
    const fd = new FormData();
    fd.append('stamp', String(layerStampId.value));
    fd.append('layer_name', layerForm.value.layer_name);
    fd.append('layer_index', String(layerForm.value.layer_index));
    fd.append('color', layerForm.value.color);
    fd.append('blend_mode', layerForm.value.blend_mode);
    if (layerSvgFile.value) fd.append('svg_file', layerSvgFile.value);
    await service.post('/stamps/layers/', fd);
    showLayerModal.value = false;
    fetchMgmtStamps();
  } catch { alert('保存失败'); }
  finally { layerSaving.value = false; }
};

const deleteStampLayer = async (layerId: number, stampId: number) => {
  if (!confirm('确定删除此图层？')) return;
  try { await service.delete(`/stamps/layers/${layerId}/`); fetchMgmtStamps(); } catch { alert('删除失败'); }
};

// ===== Articles Management =====
const mgmtArticleList = ref<any[]>([]);
const expandedPages = ref<Set<number>>(new Set());
const showArticleModal = ref(false);
const editingArticleId = ref<number | null>(null);
const articleForm = ref({ title: '', monument: null as number | null });
const articleSaving = ref(false);

const showPageModal = ref(false);
const editingPageId = ref<number | null>(null);
const pageArticleId = ref<number | null>(null);
const pageForm = ref({ page_number: 1, content: '' });
const pageSaving = ref(false);

const articlePageList = computed(() => {
  if (!quizForm.value.monument) return [];

  const relatedArticles = mgmtArticleList.value.filter(
    (a: any) => a.monument === quizForm.value.monument
  );
  return relatedArticles.flatMap((a: any) =>
    (a.pages || []).map((p: any) => ({
      ...p,
      article_title: a.title,
      // 生成一个有意义的标签用于显示
      label: `《${a.title}》- 第 ${p.page_number} 页 (ID: ${p.id})`
    }))
  );
});

const fetchMgmtArticles = async () => {
  try {
    const res = await service.get('/monuments/articles/') as any;
    mgmtArticleList.value = res.results || res;
  } catch { mgmtArticleList.value = []; }
};

const togglePageExpand = (pageId: number) => {
  if (expandedPages.value.has(pageId)) expandedPages.value.delete(pageId);
  else expandedPages.value.add(pageId);
};

const openArticleModal = (a: any) => {
  if (a) {
    editingArticleId.value = a.id;
    articleForm.value = { title: a.title, monument: a.monument };
  } else {
    editingArticleId.value = null;
    articleForm.value = { title: '', monument: null };
  }
  showArticleModal.value = true;
};

const saveArticle = async () => {
  if (!articleForm.value.title.trim()) { alert('请填写文章标题'); return; }
  articleSaving.value = true;
  try {
    const data: any = { title: articleForm.value.title };
    if (articleForm.value.monument) data.monument = articleForm.value.monument;
    if (editingArticleId.value) {
      await service.patch(`/monuments/articles/${editingArticleId.value}/`, data);
    } else {
      await service.post('/monuments/articles/', data);
    }
    showArticleModal.value = false;
    fetchMgmtArticles();
  } catch { alert('保存失败'); }
  finally { articleSaving.value = false; }
};

const deleteArticle = async (id: number) => {
  if (!confirm('确定删除此文章？关联页面和题目也将受到影响。')) return;
  try { await service.delete(`/monuments/articles/${id}/`); fetchMgmtArticles(); } catch { alert('删除失败'); }
};

const checkArticleConsistency = async (id: number) => {
  try {
    const res = await service.get(`/monuments/articles/${id}/consistency-check/`) as any;
    const issues = res.issues || [];
    if (!issues.length) {
      alert('✅ 检测通过：文章结构完整，所有页面均已关联题目。');
    } else {
      alert('⚠️ 发现以下问题：\n' + issues.join('\n'));
    }
  } catch { alert('检测请求失败'); }
};

const openPageModal = (articleId: number, page: any) => {
  pageArticleId.value = articleId;
  if (page) {
    editingPageId.value = page.id;
    pageForm.value = { page_number: page.page_number, content: page.content || '' };
  } else {
    editingPageId.value = null;
    pageForm.value = { page_number: 1, content: '' };
  }
  showPageModal.value = true;
};

const savePage = async () => {
  pageSaving.value = true;
  try {
    const data = { article: pageArticleId.value, page_number: pageForm.value.page_number, content: pageForm.value.content };
    if (editingPageId.value) {
      await service.patch(`/monuments/article-pages/${editingPageId.value}/`, data);
    } else {
      await service.post('/monuments/article-pages/', data);
    }
    showPageModal.value = false;
    fetchMgmtArticles();
  } catch { alert('保存失败'); }
  finally { pageSaving.value = false; }
};

const deletePage = async (pageId: number, articleId: number) => {
  if (!confirm('确定删除此页面？')) return;
  try { await service.delete(`/monuments/article-pages/${pageId}/`); fetchMgmtArticles(); } catch { alert('删除失败'); }
};
</script>