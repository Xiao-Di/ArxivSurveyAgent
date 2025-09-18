<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900/20 to-slate-900">
    <!-- Animated Background Boxes -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <!-- Floating background boxes with 3D effect -->
      <div
        class="absolute top-20 left-20 w-72 h-72 bg-gradient-to-br from-blue-500/10 to-purple-600/10 rounded-2xl rotate-12 animate-float-3d">
        <div class="absolute inset-0 bg-gradient-to-br from-blue-400/5 to-purple-500/5 rounded-2xl rotate-[-12deg]">
        </div>
      </div>
      <div
        class="absolute top-40 right-32 w-96 h-96 bg-gradient-to-br from-purple-500/10 to-pink-600/10 rounded-2xl -rotate-6 animate-float-3d-delayed">
        <div class="absolute inset-0 bg-gradient-to-br from-purple-400/5 to-pink-500/5 rounded-2xl rotate-6"></div>
      </div>
      <div
        class="absolute bottom-32 left-40 w-80 h-80 bg-gradient-to-br from-cyan-500/10 to-blue-600/10 rounded-2xl rotate-3 animate-float-3d-delay-2">
        <div class="absolute inset-0 bg-gradient-to-br from-cyan-400/5 to-blue-500/5 rounded-2xl rotate-[-3deg]"></div>
      </div>
      <div
        class="absolute bottom-20 right-20 w-64 h-64 bg-gradient-to-br from-green-500/10 to-teal-600/10 rounded-2xl -rotate-12 animate-float-3d-delay-3">
        <div class="absolute inset-0 bg-gradient-to-br from-green-400/5 to-teal-500/5 rounded-2xl rotate-12"></div>
      </div>

      <!-- Grid pattern overlay -->
      <div class="absolute inset-0 opacity-10">
        <div class="h-full w-full"
          style="background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,0.15) 1px, transparent 0); background-size: 40px 40px;">
        </div>
      </div>

      <!-- Animated gradient orbs -->
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse-slow"></div>
      <div
        class="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-pulse-slow-delayed">
      </div>
    </div>

    <div class="relative z-10 flex flex-col min-h-screen">
      <!-- Resizable Navbar -->
      <nav
        class="flex items-center justify-between p-6 lg:p-8 max-w-7xl mx-auto w-full transition-all duration-300 hover:shadow-2xl hover:bg-white/5 backdrop-blur-md rounded-2xl m-4">
        <div class="flex items-center space-x-4">
          <div class="relative group">
            <div class="relative">
              <div
                class="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-glow transition-all duration-300 group-hover:scale-105">
                <span class="text-white text-xl font-bold tracking-tight">P</span>
              </div>
              <div
                class="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl opacity-0 group-hover:opacity-20 transition-opacity duration-300 blur-lg">
              </div>
            </div>
          </div>
          <div>
            <h1 class="text-xl font-bold text-white tracking-tight group-hover:text-blue-400 transition-colors">
              PaperSurveyAgent</h1>
            <p class="text-sm text-blue-200 font-medium">基于LLM的文献检索Agent</p>
          </div>
        </div>

        <!-- Hover Border Gradient Button -->
        <div class="relative group">
          <div
            class="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl blur opacity-75 group-hover:opacity-100 transition duration-300">
          </div>
          <button @click="startJourney"
            class="relative px-8 py-3 bg-slate-800 text-white font-medium rounded-xl leading-none flex items-center space-x-2 hover:bg-slate-700 transition-all duration-300 hover:scale-105">
            <span>进入应用</span>
            <el-icon class="transform group-hover:translate-x-1 transition-transform duration-300">
              <ArrowRightBold />
            </el-icon>
          </button>
        </div>
      </nav>

      <div ref="heroSection" class="flex-1 flex items-center justify-center px-6 lg:px-8 text-center">
        <div class="max-w-4xl mx-auto">
          <div class="mb-16 lg:mb-20">
            <!-- Status Badge with glow effect -->
            <div
              class="inline-flex items-center px-6 py-3 bg-white/10 backdrop-blur-md border border-white/20 rounded-full text-blue-300 text-sm font-semibold mb-8 shadow-lg">
              <div class="relative mr-3">
                <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <div class="absolute inset-0 w-2 h-2 bg-green-400 rounded-full animate-ping opacity-30"></div>
              </div>
              <el-icon class="mr-2 text-blue-400" :size="16">
                <Star />
              </el-icon>
              PaperSurveyAgent AI 驱动的学术研究平台
            </div>

            <h1 class="text-5xl lg:text-7xl font-bold text-white mb-8 leading-tight">
              智能文献
              <span class="gradient-text-primary block lg:inline">检索引擎</span>
            </h1>

            <p class="text-xl lg:text-2xl text-blue-200 mb-12 max-w-3xl mx-auto leading-relaxed">
              基于大语言模型的学术研究助手，让文献检索与综述变得简单高效。
              <br class="hidden lg:block">
              支持自然语言查询、文献检索、智能相关性分析、一键生成专业报告。
            </p>

            <div class="flex flex-col lg:flex-row gap-6 justify-center items-center">
              <!-- Main CTA with Hover Border Gradient -->
              <div class="relative group">
                <div
                  class="absolute -inset-1 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl blur opacity-75 group-hover:opacity-100 transition duration-300">
                </div>
                <button @click="startJourney"
                  class="relative px-10 py-5 bg-slate-800 text-white font-semibold rounded-2xl leading-none flex items-center justify-center space-x-3 hover:bg-slate-700 transition-all duration-300 hover:scale-105 hover:shadow-2xl">
                  <span class="text-lg">开始使用 PaperSurveyAgent</span>
                  <el-icon class="transform group-hover:translate-x-1 transition-transform duration-300 text-xl">
                    <Promotion />
                  </el-icon>
                </button>
              </div>

              <!-- Secondary CTA with Hover Border Gradient -->
              <div class="relative group">
                <div
                  class="absolute -inset-1 bg-gradient-to-r from-purple-500 to-pink-600 rounded-2xl blur opacity-75 group-hover:opacity-100 transition duration-300">
                </div>
                <button @click="scrollToFeatures"
                  class="relative px-10 py-5 bg-slate-800/80 backdrop-blur-md text-blue-200 font-semibold rounded-2xl leading-none flex items-center justify-center space-x-3 hover:bg-slate-700/80 hover:text-white transition-all duration-300 hover:scale-105 hover:shadow-2xl">
                  <span class="text-lg">了解更多功能</span>
                  <el-icon class="transform group-hover:translate-x-1 transition-transform duration-300 text-xl">
                    <InfoFilled />
                  </el-icon>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <section class="py-20 lg:py-24 bg-slate-800/50 backdrop-blur-sm" ref="featuresSection">
        <div class="max-w-6xl mx-auto px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-4xl lg:text-5xl font-bold text-white mb-6">核心功能</h2>
            <p class="text-xl text-blue-200 max-w-2xl mx-auto">强大的AI技术栈，为学术研究提供全方位支持</p>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div v-for="(feature, index) in features" :key="index" class="feature-card group relative">
              <div
                class="relative p-8 lg:p-10 bg-slate-800/60 backdrop-blur-md border border-white/10 rounded-3xl shadow-soft hover:shadow-2xl hover:border-blue-500/30 transition-all duration-300 hover:scale-105">
                <div
                  class="w-16 h-16 bg-gradient-to-br from-blue-500/20 to-purple-600/20 rounded-2xl flex items-center justify-center mb-6 border border-white/10">
                  <component :is="feature.icon" class="w-8 h-8 text-blue-400" />
                </div>
                <h3 class="text-xl font-bold text-white mb-4">{{ feature.title }}</h3>
                <p class="text-blue-200 leading-relaxed">{{ feature.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section ref="statsSection"
        class="py-16 lg:py-20 bg-gradient-to-r from-slate-800 via-purple-900/30 to-slate-800 text-white">
        <div class="max-w-6xl mx-auto px-6 lg:px-8">
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-8">
            <div v-for="(stat, index) in stats" :key="index" class="text-center">
              <div class="text-4xl lg:text-5xl font-bold mb-2 text-blue-400">{{ stat.value }}</div>
              <div class="text-blue-200 font-medium">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </section>

      <footer class="py-12 lg:py-16 bg-slate-900/80 backdrop-blur-md border-t border-white/10">
        <div class="max-w-6xl mx-auto px-6 lg:px-8">
          <div class="text-center">
            <div class="flex items-center justify-center space-x-3 mb-6">
              <div
                class="w-10 h-10 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-xl flex items-center justify-center">
                <span class="text-white text-lg font-bold">P</span>
              </div>
              <span class="text-2xl font-bold text-white">PaperSurveyAgent</span>
            </div>
            <p class="text-blue-200 font-medium">© {{ new Date().getFullYear() }} PaperSurveyAgent. 基于LLM的文献检索Agent.
            </p>
            <p class="text-sm text-blue-300">Powered by AI • Built for Researchers • Made with ❤️</p>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, markRaw } from 'vue'
import { useRouter } from 'vue-router'
import {
  Search,
  DataAnalysis,
  Document,
  ArrowRightBold,
  Promotion,
  InfoFilled,
  Star
} from '@element-plus/icons-vue'

const router = useRouter()
const featuresSection = ref<HTMLElement | null>(null)
const heroSection = ref<HTMLElement | null>(null)
const statsSection = ref<HTMLElement | null>(null)

const features = [
  {
    icon: markRaw(Search),
    title: '智能检索',
    description: '支持自然语言查询，多数据源整合，精准匹配相关文献。基于先进的语义理解技术，让搜索更加智能和精准。'
  },
  {
    icon: markRaw(DataAnalysis),
    title: 'AI分析',
    description: 'LLM分析文献内容，自动提取关键信息和趋势。智能识别研究热点，发现潜在的研究机会。'
  },
  {
    icon: markRaw(Document),
    title: '智能总结',
    description: '一键生成专业的文献综述报告，大幅提升研究效率。自动整理文献脉络，生成结构化的研究报告。'
  }
]

const stats = [
  { value: '10M+', label: '文献数据库' },
  { value: '95.6%', label: '检索准确率' },
  { value: '<10s', label: '平均响应时间' },
  { value: '24/7', label: '全天候服务' }
]

const startJourney = () => {
  console.log('🚀 Starting journey to search page...')
  router.push('/search')
}

const scrollToFeatures = () => {
  featuresSection.value?.scrollIntoView({
    behavior: 'smooth',
    block: 'start'
  })
}
</script>

<style scoped>
/* 3D Float Animation for Background Boxes */
@keyframes float-3d {

  0%,
  100% {
    transform: translateY(0px) rotate(0deg) translateZ(0px);
  }

  25% {
    transform: translateY(-20px) rotate(1deg) translateZ(10px);
  }

  50% {
    transform: translateY(-10px) rotate(0deg) translateZ(20px);
  }

  75% {
    transform: translateY(-15px) rotate(-1deg) translateZ(10px);
  }
}

.animate-float-3d {
  animation: float-3d 8s ease-in-out infinite;
  transform-style: preserve-3d;
}

.animate-float-3d-delayed {
  animation: float-3d 10s ease-in-out infinite;
  animation-delay: -2s;
  transform-style: preserve-3d;
}

.animate-float-3d-delay-2 {
  animation: float-3d 12s ease-in-out infinite;
  animation-delay: -4s;
  transform-style: preserve-3d;
}

.animate-float-3d-delay-3 {
  animation: float-3d 9s ease-in-out infinite;
  animation-delay: -1s;
  transform-style: preserve-3d;
}

/* Slow pulse animations */
@keyframes pulse-slow {

  0%,
  100% {
    opacity: 0.2;
    transform: scale(1);
  }

  50% {
    opacity: 0.3;
    transform: scale(1.1);
  }
}

.animate-pulse-slow {
  animation: pulse-slow 6s ease-in-out infinite;
}

.animate-pulse-slow-delayed {
  animation: pulse-slow 8s ease-in-out infinite;
  animation-delay: -2s;
}

/* Shadow glow effect */
.shadow-glow {
  box-shadow: 0 0 30px rgba(59, 130, 246, 0.6),
    0 0 60px rgba(147, 51, 234, 0.4);
}

/* Hover lift effect for cards */
.feature-card:hover {
  transform: translateY(-8px) scale(1.02);
}

/* Enhanced gradient text */
.gradient-text-primary {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 3s ease-in-out infinite;
}

@keyframes gradientShift {

  0%,
  100% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }
}

/* Resizable navbar effect */
nav {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

nav:hover {
  transform: scale(1.02);
}

/* Glassmorphism enhancement */
.glass-effect {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Custom scrollbar for dark theme */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
}
</style>
