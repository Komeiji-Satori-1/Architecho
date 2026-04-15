<template>
  <div class="min-h-screen flex flex-col">
    <Navbar />
    <main class="flex-grow">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <!-- 全局登录弹窗 -->
    <AuthModal v-if="showAuth" @close="showAuth = false" />
    
    <footer class="bg-white py-12 border-t border-outline-variant/10">
      <div class="container mx-auto px-4 text-center">
        <h2 class="font-serif text-2xl mb-4">筑迹</h2>
        <div class="flex justify-center space-x-8 text-secondary text-sm mb-8">
          <a href="#" class="hover:text-primary transition-colors" @click.prevent="openFooterModal('about')">关于我们</a>
          <a href="#" class="hover:text-primary transition-colors" @click.prevent="openFooterModal('rules')">社区准则</a>
          <a href="#" class="hover:text-primary transition-colors" @click.prevent="openFooterModal('privacy')">隐私政策</a>
          <a href="#" class="hover:text-primary transition-colors" @click.prevent="openFooterModal('contact')">联系我们</a>
        </div>
        <p class="text-secondary/60 text-xs">© 2026 筑迹古建筑社区. 传承千年匠心.</p>
      </div>
    </footer>

    <!-- Footer 信息弹窗 -->
    <Teleport to="body">
      <transition name="modal-fade">
        <div v-if="footerModal" class="footer-modal-overlay" @click.self="footerModal = null">
          <div class="footer-modal">
            <button class="footer-modal-close" @click="footerModal = null">✕</button>
            <h3 class="font-serif text-2xl mb-4 text-on-surface">{{ footerContent[footerModal].title }}</h3>
            <div class="text-secondary text-sm leading-relaxed space-y-3" v-html="footerContent[footerModal].body"></div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, provide } from 'vue';
import Navbar from '@/components/Navbar.vue';
import AuthModal from '@/components/AuthModal.vue';

const showAuth = ref(false);

// 提供给子组件控制登录弹窗
provide('toggleAuth', (val: boolean) => {
  showAuth.value = val;
});

// Footer 弹窗
type FooterKey = 'about' | 'rules' | 'privacy' | 'contact';
const footerModal = ref<FooterKey | null>(null);

const footerContent: Record<FooterKey, { title: string; body: string }> = {
  about: {
    title: '关于我们',
    body: `
      <p>「筑迹」是一个致力于中国古建筑文化传承与保护的数字社区平台。我们相信，每一座古建筑都承载着先人的智慧与匠心，是中华文明不可替代的物质记忆。</p>
      <p>我们的使命是借助现代数字技术，让古建筑的美与价值被更多人看见、了解和热爱。在这里，你可以探索各地的古建筑遗产，参与知识问答，收集专属印章，也可以与志同道合的爱好者交流心得。</p>
      <p>无论你是建筑学者、文化遗产工作者，还是对传统建筑抱有好奇的普通人，「筑迹」都欢迎你的加入。让我们一起，为千年匠心留下数字时代的印迹。</p>
    `,
  },
  rules: {
    title: '社区准则',
    body: `
      <p><strong>1. 尊重与友善</strong><br/>尊重每一位社区成员，禁止人身攻击、歧视性言论和恶意挑衅。保持理性、建设性的对话氛围。</p>
      <p><strong>2. 内容真实</strong><br/>分享的古建筑信息应尽量准确可靠，鼓励标注资料来源。对于未经证实的内容，请注明为个人观点或推测。</p>
      <p><strong>3. 原创与版权</strong><br/>鼓励原创内容。转载他人作品需注明出处并尊重原作者版权，严禁未经授权的商业使用。</p>
      <p><strong>4. 保护遗产</strong><br/>禁止发布任何可能危及古建筑安全的信息，包括但不限于非法进入、破坏性拍摄方式等。</p>
      <p><strong>5. 合规守法</strong><br/>遵守中华人民共和国相关法律法规，不发布违法违规内容。违规账号将被限制或永久封禁。</p>
    `,
  },
  privacy: {
    title: '隐私政策',
    body: `
      <p><strong>信息收集</strong><br/>我们仅收集为提供服务所必需的信息，包括注册时的基本账户信息（用户名、邮箱）及您在平台上的互动数据（如浏览记录、点赞评论等）。</p>
      <p><strong>信息使用</strong><br/>您的信息仅用于提供和改善平台服务，如个性化内容推荐、社区互动功能等。我们不会将您的个人信息出售或出租给任何第三方。</p>
      <p><strong>信息保护</strong><br/>我们采用行业标准的安全措施保护您的数据，包括数据加密传输与存储。尽管如此，互联网传输无法保证绝对安全，我们将持续更新安全策略。</p>
      <p><strong>您的权利</strong><br/>您有权随时查阅、修改或删除您的个人信息。如需注销账户，请通过联系我们页面提交申请，我们将在合理时间内处理。</p>
      <p><strong>政策更新</strong><br/>本隐私政策可能不定期更新，更新后将在本页面公示。继续使用本平台即视为同意最新版本的隐私政策。</p>
    `,
  },
  contact: {
    title: '联系我们',
    body: `
      <p>如果您有任何问题、建议或合作意向，欢迎通过以下方式与我们取得联系：</p>
      <p>📮 <strong>电子邮箱</strong>：lixinde202@gmail.com</p>
      <p>💬 <strong>社区反馈</strong>：您也可以在社区论坛的「建议与反馈」板块发帖，我们会定期查看并回复。</p>
      <p>🕐 <strong>工作时间</strong>：周一至周五 9:00 - 18:00（法定节假日除外）</p>
      <p>我们珍视每一份来自用户的声音，通常会在 1-3 个工作日内回复您的消息。感谢您对「筑迹」的支持与关注！</p>
    `,
  },
};

function openFooterModal(key: FooterKey) {
  footerModal.value = key;
}
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.container {
  max-width: 1280px;
}

/* Footer 弹窗样式 */
.footer-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.footer-modal {
  background: #fff;
  border-radius: 16px;
  max-width: 560px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  padding: 2rem 2.5rem;
  position: relative;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.footer-modal-close {
  position: absolute;
  top: 1rem;
  right: 1.25rem;
  font-size: 1.1rem;
  color: #999;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.2s;
  line-height: 1;
}

.footer-modal-close:hover {
  color: #333;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.25s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
