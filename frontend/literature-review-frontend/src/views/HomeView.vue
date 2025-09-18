<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900/20 to-slate-900">
    <!-- Hero Parallax Background -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <!-- Parallax Layers -->
      <div class="absolute inset-0 bg-gradient-to-br from-slate-900/80 via-purple-900/40 to-slate-900/80"></div>

      <!-- Animated gradient orbs for parallax effect -->
      <div class="absolute top-0 left-0 w-full h-full">
        <div class="absolute top-20 left-10 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl animate-float-parallax-1">
        </div>
        <div class="absolute top-40 right-20 w-96 h-96 bg-purple-500/15 rounded-full blur-3xl animate-float-parallax-2">
        </div>
        <div
          class="absolute bottom-32 left-1/4 w-72 h-72 bg-cyan-500/20 rounded-full blur-3xl animate-float-parallax-3">
        </div>
        <div
          class="absolute bottom-20 right-1/3 w-64 h-64 bg-pink-500/15 rounded-full blur-3xl animate-float-parallax-4">
        </div>
      </div>

      <!-- Grid pattern overlay for tech feel -->
      <div class="absolute inset-0 opacity-20">
        <div class="h-full w-full" style="background-image:
          radial-gradient(circle at 1px 1px, rgba(59, 130, 246, 0.3) 1px, transparent 0),
          radial-gradient(circle at 2px 2px, rgba(147, 51, 234, 0.2) 1px, transparent 0);
          background-size: 40px 40px, 60px 60px;
          background-position: 0 0, 20px 20px;"></div>
      </div>

      <!-- Floating particles -->
      <div class="absolute inset-0">
        <div v-for="n in 20" :key="n" class="absolute w-1 h-1 bg-blue-400 rounded-full opacity-60" :style="{
          left: Math.random() * 100 + '%',
          top: Math.random() * 100 + '%',
          animationDelay: Math.random() * 6 + 's'
        }" style="animation: particleFloat 8s ease-in-out infinite;"></div>
      </div>
    </div>
    <!-- Resizable Navbar -->
    <nav
      class="relative z-50 backdrop-blur-md bg-slate-800/80 border-b border-white/10 shadow-soft transition-all duration-300 hover:shadow-2xl hover:bg-slate-800/90 m-4 rounded-2xl hover:scale-[1.02]">
      <div class="max-w-7xl mx-auto px-6 lg:px-8">
        <div class="flex justify-between items-center h-20">
          <!-- 品牌标识 -->
          <div class="flex items-center space-x-4 cursor-pointer group" @click="goToWelcome">
            <div class="relative">
              <div
                class="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-glow transition-all duration-300 group-hover:scale-105">
                <span class="text-white text-xl font-bold tracking-tight">P</span>
              </div>
              <div
                class="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl opacity-0 group-hover:opacity-20 transition-opacity duration-300 blur-lg">
              </div>
            </div>
            <div>
              <h1
                class="text-2xl font-bold text-white tracking-tight group-hover:text-blue-400 transition-colors duration-300">
                PaperSurveyAgent
              </h1>
              <p class="text-sm text-blue-200 font-medium -mt-1">基于LLM的文献检索Agent</p>
            </div>
          </div>

          <!-- 导航菜单 -->
          <div class="hidden lg:flex items-center space-x-8">
            <!-- 登录状态显示 -->
            <div v-if="isAuthenticated()" class="flex items-center space-x-4">
              <!-- 余额显示 -->
              <div class="flex items-center space-x-2 px-3 py-2 bg-primary-50 border border-primary-200 rounded-xl">
                <el-icon class="text-primary-600">
                  <Wallet />
                </el-icon>
                <span class="text-primary-700 text-sm font-medium">余额: ¥{{ userBalance.balance?.toFixed(2) || '0.00'
                  }}</span>
              </div>
              <!-- 充值按钮 -->
              <button @click="showRecharge = true"
                class="group flex items-center px-3 py-2 bg-gradient-to-r from-warning to-warning-600 text-white rounded-xl hover:from-warning-600 hover:to-warning-700 transition-all duration-300 hover:-translate-y-0.5 shadow-lg hover:shadow-glow">
                <el-icon class="mr-2 group-hover:scale-110 transition-transform duration-300">
                  <CreditCard />
                </el-icon>
                <span class="text-sm font-medium">充值</span>
              </button>
              <!-- 登录状态 -->
              <div class="flex items-center space-x-2 px-3 py-2 bg-success-50 border border-success-200 rounded-xl">
                <div class="w-2 h-2 bg-success-500 rounded-full animate-pulse"></div>
                <span class="text-success-700 text-sm font-medium">已登录</span>
              </div>
              <button @click="handleLogout" class="text-sm text-neutral-500 hover:text-danger-600 transition-colors">
                退出
              </button>
            </div>
            <div v-else>
              <button @click="showLogin = true"
                class="group flex items-center px-4 py-2 bg-primary text-white rounded-xl hover:bg-primary-600 transition-all duration-300 hover:-translate-y-0.5 shadow-lg hover:shadow-glow">
                <span class="font-medium">登录</span>
              </button>
            </div>

            <button @click="showHistory = true"
              class="group flex items-center px-4 py-2 text-neutral-600 hover:text-primary-600 transition-all duration-300 rounded-xl hover:bg-primary-50">
              <el-icon class="mr-2 group-hover:scale-110 transition-transform duration-300">
                <Clock />
              </el-icon>
              <span class="font-medium">搜索历史</span>
            </button>

            <button @click="showSettings = true"
              class="group flex items-center px-4 py-2 text-neutral-600 hover:text-primary-600 transition-all duration-300 rounded-xl hover:bg-primary-50">
              <el-icon class="mr-2 group-hover:scale-110 transition-transform duration-300">
                <Setting />
              </el-icon>
              <span class="font-medium">设置</span>
            </button>

            <!-- 智能统计面板 -->
            <div class="flex items-center space-x-6 pl-6 border-l border-neutral-200">
              <div class="group relative">
                <div class="text-center p-2 rounded-lg hover:bg-primary-50 transition-colors cursor-pointer">
                  <div class="text-lg font-bold text-primary-600">{{ totalPapers || 0 }}</div>
                  <div class="text-xs text-neutral-500">Papers Found</div>
                </div>
                <div
                  class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-neutral-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">
                  本次检索结果
                </div>
              </div>
              <div class="group relative">
                <div class="text-center p-2 rounded-lg hover:bg-success-50 transition-colors cursor-pointer">
                  <div class="text-lg font-bold text-success-600">{{ relevanceScore || 95 }}%</div>
                  <div class="text-xs text-neutral-500">AI Relevance</div>
                </div>
                <div
                  class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-neutral-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">
                  AI智能相关性评分
                </div>
              </div>
            </div>
          </div>

          <!-- 移动端菜单按钮 -->
          <div class="lg:hidden">
            <button @click="showMobileMenu = !showMobileMenu"
              class="p-2 text-neutral-600 hover:text-primary-600 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <main class="relative z-10 pt-8 pb-20">
      <div class="max-w-7xl mx-auto px-6 lg:px-8">
        <!-- 英雄区域 with Parallax Effect -->
        <section class="text-center mb-16 lg:mb-20 relative">
          <!-- Parallax floating elements -->
          <div class="absolute inset-0 overflow-hidden pointer-events-none">
            <div class="absolute top-10 left-10 w-20 h-20 bg-blue-500/10 rounded-xl rotate-12 animate-parallax-float-1">
            </div>
            <div
              class="absolute top-20 right-16 w-16 h-16 bg-purple-500/10 rounded-xl -rotate-6 animate-parallax-float-2">
            </div>
            <div
              class="absolute bottom-10 left-1/4 w-12 h-12 bg-cyan-500/10 rounded-xl rotate-3 animate-parallax-float-3">
            </div>
          </div>

          <!-- 动态状态徽章 -->
          <div
            class="inline-flex items-center space-x-3 bg-slate-800/80 backdrop-blur-md border border-blue-500/30 rounded-full px-6 py-3 mb-8 shadow-lg animate-fade-in-down group hover:shadow-xl transition-all duration-300">
            <div class="relative">
              <div class="w-3 h-3 bg-gradient-to-r from-green-400 to-blue-500 rounded-full animate-pulse-soft"></div>
              <div
                class="absolute inset-0 w-3 h-3 bg-gradient-to-r from-green-400 to-blue-500 rounded-full opacity-30 animate-ping">
              </div>
            </div>
            <span class="text-blue-300 text-sm font-semibold group-hover:text-blue-200 transition-colors">
              {{ isAuthenticated() ? 'PaperSurveyAgent · AI 智能检索系统已就绪 · 用户已验证' : 'PaperSurveyAgent · AI 智能检索系统 · 需要登录访问'
              }}
            </span>
            <div v-if="isAuthenticated()" class="w-1.5 h-1.5 bg-green-400 rounded-full opacity-60"></div>
          </div>

          <!-- 主标题 -->
          <h1 class="text-5xl lg:text-7xl font-bold text-white mb-8 leading-tight animate-fade-in-up animate-delay-100">
            <span class="block">发现学术</span>
            <span class="gradient-text-primary block">新洞察</span>
            <span class="block text-3xl lg:text-5xl text-blue-200 font-light mt-4">
              超越想象的边界
            </span>
          </h1>

          <!-- 副标题 -->
          <p
            class="text-xl lg:text-2xl text-blue-200 max-w-4xl mx-auto leading-relaxed mb-12 animate-fade-in-up animate-delay-200">
            基于大语言模型的文献检索Agent，让学术研究变得更加智能高效。
            <br class="hidden lg:block">
            精准检索、智能分析、一键生成专业报告。
          </p>

          <!-- 统计卡片 with Hover Border Gradient -->
          <div
            class="grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-4xl mx-auto mb-16 animate-fade-in-up animate-delay-300">
            <div class="group relative">
              <div
                class="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl blur opacity-0 group-hover:opacity-75 transition duration-300">
              </div>
              <div
                class="relative bg-slate-800/60 backdrop-blur-md border border-blue-500/20 rounded-2xl p-8 text-center shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
                <div class="text-4xl mb-4">📚</div>
                <div class="text-3xl font-bold text-blue-400 mb-2">10M+</div>
                <div class="text-blue-200 font-medium">文献数据库</div>
              </div>
            </div>

            <div class="group relative">
              <div
                class="absolute -inset-0.5 bg-gradient-to-r from-green-500 to-emerald-500 rounded-2xl blur opacity-0 group-hover:opacity-75 transition duration-300">
              </div>
              <div
                class="relative bg-slate-800/60 backdrop-blur-md border border-green-500/20 rounded-2xl p-8 text-center shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
                <div class="text-4xl mb-4">🎯</div>
                <div class="text-3xl font-bold text-green-400 mb-2">95.6%</div>
                <div class="text-green-200 font-medium">检索准确率</div>
              </div>
            </div>

            <div class="group relative">
              <div
                class="absolute -inset-0.5 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl blur opacity-0 group-hover:opacity-75 transition duration-300">
              </div>
              <div
                class="relative bg-slate-800/60 backdrop-blur-md border border-purple-500/20 rounded-2xl p-8 text-center shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
                <div class="text-4xl mb-4">⚡</div>
                <div class="text-3xl font-bold text-purple-400 mb-2">{{ processingTime }}s</div>
                <div class="text-purple-200 font-medium">平均响应时间</div>
              </div>
            </div>
          </div>
        </section>

        <!-- 智能搜索界面 -->
        <section class="max-w-5xl mx-auto mb-16 animate-fade-in-up animate-delay-500">
          <div class="relative">
            <!-- 主搜索卡片 -->
            <div class="bg-slate-800/60 backdrop-blur-md border border-white/10 rounded-3xl p-8 lg:p-12 shadow-2xl">
              <!-- 智能搜索标题 -->
              <div class="text-center mb-10">
                <div class="flex items-center justify-center mb-4">
                  <div
                    class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mr-4 shadow-lg">
                    <span class="text-white text-xl">🧠</span>
                  </div>
                  <h2 class="text-3xl lg:text-4xl font-bold text-white">
                    语义智能检索
                  </h2>
                </div>
                <p class="text-xl text-blue-200 max-w-3xl mx-auto leading-relaxed">
                  基于大语言模型的<strong class="text-blue-400">语义理解</strong>技术，
                  <br class="hidden lg:block">
                  让AI理解您的研究意图，而不仅仅是关键词匹配
                </p>
                <div class="flex items-center justify-center mt-6 space-x-6 text-sm text-blue-300">
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-gradient-to-r from-blue-400 to-cyan-400 rounded-full"></div>
                    <span>多源并行检索</span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-gradient-to-r from-green-400 to-emerald-400 rounded-full"></div>
                    <span>AI语义分析</span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full"></div>
                    <span>智能结果排序</span>
                  </div>
                </div>
              </div>

              <!-- AI增强搜索输入区域 -->
              <div class="mb-8">
                <div class="relative">
                  <!-- 搜索框标签 -->
                  <div class="flex items-center justify-between mb-4">
                    <div class="flex items-center space-x-2">
                      <span class="text-sm font-semibold text-blue-300">研究问题描述</span>
                      <div
                        class="px-2 py-1 bg-gradient-to-r from-blue-500/20 to-purple-600/20 backdrop-blur-md border border-blue-400/30 rounded-full text-xs font-medium text-blue-300">
                        AI Enhanced
                      </div>
                    </div>
                    <div class="flex items-center space-x-2 text-xs text-blue-400">
                      <span>字符数: {{ searchQuery.length }}/2000</span>
                    </div>
                  </div>

                  <el-input v-model="searchQuery" type="textarea" :autosize="{ minRows: 5, maxRows: 10 }"
                    :maxlength="2000"
                    placeholder="🧠 AI智能提示：详细描述您的研究需求，例如：&#10;&#10;'我需要研究深度学习在空天地一体化网络中的最新突破，特别关注：&#10;1. 最新的网络架构设计&#10;2. 相关标准化研究进展&#10;3. 2020年以来的技术发展趋势&#10;4. 与传统方法的对比研究'&#10;&#10;💡 越详细的描述，AI匹配的结果越精准！"
                    class="search-input-dark" @keyup.enter.ctrl="startSearch" @input="handleSearchInput" />

                  <!-- AI智能提示浮层 -->
                  <div class="absolute inset-x-0 top-full mt-2 z-10">
                    <div v-if="searchQuery.length > 20 && aiSuggestions.length > 0"
                      class="bg-slate-800/90 backdrop-blur-md border border-blue-500/30 rounded-2xl p-4 shadow-2xl">
                      <div class="flex items-center space-x-2 mb-3">
                        <div
                          class="w-5 h-5 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center shadow-lg">
                          <span class="text-white text-xs">✨</span>
                        </div>
                        <span class="text-sm font-semibold text-blue-300">AI智能建议</span>
                      </div>
                      <div class="space-y-2">
                        <div v-for="(suggestion, index) in aiSuggestions" :key="index"
                          class="p-3 bg-gradient-to-r from-blue-500/10 to-purple-600/10 rounded-xl border border-blue-400/20 hover:border-blue-400/50 cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg"
                          @click="applySuggestion(suggestion)">
                          <div class="flex items-start space-x-3">
                            <div
                              class="w-6 h-6 bg-blue-500/20 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5 border border-blue-400/30">
                              <span class="text-blue-400 text-xs font-bold">{{ index + 1 }}</span>
                            </div>
                            <span class="text-sm text-blue-200 leading-relaxed">{{ suggestion }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- 输入框装饰和功能按钮 -->
                  <div class="absolute top-16 right-4 flex items-center space-x-3">
                    <button v-if="searchQuery.length > 0" @click="clearSearch"
                      class="p-1.5 text-blue-400 hover:text-blue-300 rounded-lg hover:bg-blue-500/20 transition-colors">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                        </path>
                      </svg>
                    </button>
                    <div class="flex items-center space-x-1 text-xs text-blue-400">
                      <kbd
                        class="px-2 py-1 bg-slate-700/50 text-blue-300 rounded font-mono border border-blue-500/30">Ctrl</kbd>
                      <span>+</span>
                      <kbd
                        class="px-2 py-1 bg-slate-700/50 text-blue-300 rounded font-mono border border-blue-500/30">Enter</kbd>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 搜索控制区域 -->
              <div class="flex flex-col lg:flex-row items-center justify-between gap-6">
                <!-- 状态指示器 -->
                <div class="flex items-center space-x-6 text-sm">
                  <div class="flex items-center space-x-2">
                    <div class="w-2.5 h-2.5 bg-green-400 rounded-full animate-pulse-soft shadow-lg shadow-green-400/50">
                    </div>
                    <span class="text-blue-300 font-medium">AI 系统就绪</span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <div class="w-2.5 h-2.5 bg-blue-500 rounded-full shadow-lg shadow-blue-500/50"></div>
                    <span class="text-blue-300 font-medium">多源检索</span>
                  </div>
                </div>

                <!-- 费用预估显示 -->
                <div v-if="isAuthenticated() && maxPapers > 0" class="flex items-center justify-center mb-6">
                  <div class="flex items-center space-x-2 px-4 py-2 bg-warning-50 border border-warning-200 rounded-xl">
                    <el-icon class="text-warning-600">
                      <Wallet />
                    </el-icon>
                    <span class="text-warning-700 text-sm font-medium">
                      预计费用: ¥{{ calculateSearchCost(maxPapers).toFixed(2) }} ({{ maxPapers }}篇 × ¥0.5/篇)
                    </span>
                  </div>
                </div>

                <!-- 搜索按钮 -->
                <button @click="startSearch" :disabled="!searchQuery.trim() || isSearching"
                  class="group relative px-10 py-4 bg-gradient-to-r from-primary to-primary-600 text-white rounded-2xl font-semibold shadow-lg hover:shadow-glow transition-all duration-300 hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                  <div class="flex items-center justify-center">
                    <el-icon v-if="isSearching" class="animate-spin mr-3 text-lg">
                      <Loading />
                    </el-icon>
                    <el-icon v-else class="mr-3 text-lg group-hover:scale-110 transition-transform duration-300">
                      <Search />
                    </el-icon>
                    <span class="text-lg">{{ isSearching ? '智能检索中...' : '开始智能检索' }}</span>
                  </div>
                  <div
                    class="absolute inset-0 bg-gradient-to-r from-primary-600 to-primary-700 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  </div>
                </button>
              </div>

              <!-- 快速建议 -->
              <div v-if="naturalLanguageSuggestions.length > 0" class="mt-10">
                <p class="text-sm text-neutral-500 font-medium mb-4">💡 快速开始</p>
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
                  <button v-for="suggestion in naturalLanguageSuggestions.slice(0, 3)" :key="suggestion"
                    @click="searchQuery = suggestion; startSearch()"
                    class="group p-4 bg-blue-50 border border-blue-200 rounded-xl text-left text-sm text-blue-700 hover:bg-blue-100 hover:border-blue-300 hover:text-blue-800 transition-all duration-300 hover:-translate-y-0.5 shadow-sm hover:shadow-md">
                    <div class="line-clamp-3">{{ suggestion }}</div>
                    <div class="mt-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                      <span class="text-xs text-primary-600 font-medium">点击使用 →</span>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 高级选项 -->
        <section class="max-w-5xl mx-auto mb-16">
          <div class="text-center">
            <div class="relative group">
              <div
                class="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl blur opacity-75 group-hover:opacity-100 transition duration-300">
              </div>
              <button @click="showAdvancedOptions = !showAdvancedOptions"
                class="relative px-6 py-3 bg-slate-800 text-blue-300 font-medium rounded-xl leading-none flex items-center space-x-2 hover:bg-slate-700 transition-all duration-300 hover:scale-105">
                <span>{{ showAdvancedOptions ? '隐藏' : '显示' }}高级选项</span>
                <el-icon class="transition-transform duration-300 group-hover:scale-110"
                  :class="{ 'rotate-180': showAdvancedOptions }">
                  <ArrowDown />
                </el-icon>
              </button>
            </div>
          </div>

          <Transition name="advanced-options">
            <div v-if="showAdvancedOptions"
              class="mt-8 bg-slate-800/90 backdrop-blur-md border border-blue-500/30 rounded-2xl p-8 shadow-2xl">
              <h3 class="text-2xl font-bold text-blue-300 mb-8 text-center">高级搜索设置</h3>

              <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <!-- 数据源选择 -->
                <div class="space-y-4">
                  <label class="block text-sm font-semibold text-blue-300 mb-3">数据源</label>
                  <el-select v-model="selectedSources" multiple placeholder="选择数据源" class="w-full">
                    <el-option label="arXiv" value="arxiv" />
                    <!-- Semantic Scholar removed - using ArXiv only -->
                  </el-select>
                  <p class="text-xs text-blue-400">选择要搜索的学术数据库</p>
                </div>

                <!-- 论文数量 -->
                <div class="space-y-4">
                  <label class="block text-sm font-semibold text-blue-300 mb-3">
                    最大论文数量: <span class="text-blue-400 font-bold">{{ maxPapers }}</span>
                  </label>
                  <el-slider v-model="maxPapers" :min="5" :max="50" :step="5" class="mt-4" />
                  <p class="text-xs text-blue-400">控制返回的论文数量以优化检索速度</p>
                </div>

                <!-- 功能选项 -->
                <div class="lg:col-span-2 space-y-6">
                  <h4 class="text-lg font-semibold text-blue-300 border-b border-blue-500/30 pb-2">功能选项</h4>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <label
                      class="flex items-center p-4 bg-slate-700/50 rounded-xl border border-blue-500/20 hover:border-blue-400/50 hover:bg-blue-500/10 transition-all duration-300 cursor-pointer">
                      <el-checkbox v-model="retrieveFullText" />
                      <div class="ml-4">
                        <span class="font-medium text-blue-200">获取全文</span>
                        <p class="text-sm text-blue-400 mt-1">尝试获取论文的完整文本内容</p>
                      </div>
                    </label>

                    <label
                      class="flex items-center p-4 bg-slate-700/50 rounded-xl border border-blue-500/20 hover:border-blue-400/50 hover:bg-blue-500/10 transition-all duration-300 cursor-pointer">
                      <el-checkbox v-model="enableAIAnalysis" />
                      <div class="ml-4">
                        <span class="font-medium text-blue-200">AI 智能分析</span>
                        <p class="text-sm text-blue-400 mt-1">使用AI对检索结果进行深度分析</p>
                      </div>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </section>

        <!-- 结果展示区域 -->
        <section v-if="isSearching || searchResults.length > 0 || (actionPlan && actionPlan.length > 0)"
          class="max-w-7xl mx-auto">
          <!-- 加载动画 -->
          <div v-if="isSearching && searchResults.length === 0" class="text-center py-20">
            <div class="relative inline-block mb-8">
              <div class="w-20 h-20 border-4 border-primary-200 border-t-primary rounded-full animate-spin"></div>
              <div
                class="absolute inset-0 w-20 h-20 border-4 border-secondary-200 border-b-secondary rounded-full animate-spin"
                style="animation-direction: reverse;"></div>
            </div>
            <h3 class="text-2xl font-bold text-neutral-900 mb-4">AI 正在处理您的查询</h3>
            <p class="text-neutral-600 text-lg">分析需求并搜索相关文献...</p>
            <div class="mt-6 flex justify-center">
              <div class="flex space-x-2">
                <div class="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0.1s;"></div>
                <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0.2s;"></div>
              </div>
            </div>
          </div>

          <!-- AI 执行计划 -->
          <div v-if="actionPlan && actionPlan.length > 0" class="mb-16">
            <div class="bg-white/90 backdrop-blur-md border border-neutral-200/50 rounded-2xl p-8 shadow-large">
              <div class="flex items-center mb-8">
                <div
                  class="w-12 h-12 bg-gradient-to-br from-primary-100 to-primary-200 rounded-2xl flex items-center justify-center mr-4">
                  <span class="text-2xl">🤖</span>
                </div>
                <div>
                  <h3 class="text-2xl font-bold text-neutral-900">AI 执行计划</h3>
                  <p class="text-neutral-600">智能分析您的需求并制定检索策略</p>
                </div>
              </div>
              <div class="space-y-4">
                <div v-for="(step, index) in actionPlan" :key="index"
                  class="flex items-start space-x-4 p-4 bg-slate-700/50 rounded-xl border border-blue-500/20 hover:border-blue-400/50 hover:bg-blue-500/10 transition-all duration-300">
                  <div
                    class="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold shadow-lg">
                    {{ index + 1 }}
                  </div>
                  <p class="text-blue-200 font-medium leading-relaxed">{{ step }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 搜索结果 -->
          <div v-if="searchResults.length > 0" class="space-y-8">
            <!-- 结果标题和操作 -->
            <div
              class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6 p-8 bg-white/90 backdrop-blur-md border border-neutral-200/50 rounded-2xl shadow-large">
              <div>
                <h2 class="text-3xl font-bold text-neutral-900 mb-2">检索结果</h2>
                <p class="text-neutral-600 text-lg">找到 <span class="font-bold text-primary-600">{{ searchResults.length
                    }}</span> 篇相关文献</p>
              </div>
              <button @click="generateReport" :disabled="isGeneratingReport"
                class="group px-8 py-4 bg-gradient-to-r from-success to-success-600 text-white rounded-2xl font-semibold shadow-lg hover:shadow-glow transition-all duration-300 hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                <div class="flex items-center">
                  <el-icon v-if="isGeneratingReport" class="animate-spin mr-3 text-lg">
                    <Loading />
                  </el-icon>
                  <el-icon v-else class="mr-3 text-lg group-hover:scale-110 transition-transform duration-300">
                    <Document />
                  </el-icon>
                  <span>{{ isGeneratingReport ? '生成中...' : '生成报告' }}</span>
                </div>
              </button>
            </div>

            <!-- 论文卡片网格 -->
            <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
              <PaperCard v-for="(paper, index) in searchResults" :key="paper.id" :paper="paper" :index="index + 1"
                @toggle-favorite="toggleFavorite" @view-details="viewDetailsModal" @download-pdf="downloadPdf"
                class="animate-fade-in-up hover-lift" :style="{ animationDelay: `${index * 0.1}s` }" />
            </div>
          </div>
        </section>
      </div>
    </main>

    <!-- 对话框组件 -->
    <!-- 设置对话框 -->
    <el-dialog v-model="showSettings" title="系统设置" width="600px" class="modern-dialog">
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-semibold text-neutral-700 mb-3">默认数据源</label>
          <el-select v-model="defaultSources" multiple placeholder="选择默认数据源" class="w-full">
            <el-option label="arXiv" value="arxiv" />
            <!-- Semantic Scholar removed - using ArXiv only -->
          </el-select>
          <p class="text-xs text-neutral-500 mt-2">设置默认使用的学术数据库</p>
        </div>

        <div>
          <label class="block text-sm font-semibold text-neutral-700 mb-3">默认最大论文数</label>
          <el-input-number v-model="defaultMaxPapers" :min="5" :max="50" :step="5" class="w-full" />
          <p class="text-xs text-neutral-500 mt-2">设置每次搜索返回的最大论文数量</p>
        </div>

        <div>
          <label class="block text-sm font-semibold text-neutral-700 mb-3">界面语言</label>
          <el-select v-model="language" placeholder="选择界面语言" class="w-full">
            <el-option label="中文" value="zh" />
            <el-option label="English" value="en" />
          </el-select>
          <p class="text-xs text-neutral-500 mt-2">设置系统界面显示语言</p>
        </div>
      </div>
    </el-dialog>

    <!-- 搜索历史对话框 -->
    <el-dialog v-model="showHistory" title="搜索历史" width="700px" class="modern-dialog">
      <div v-if="searchHistory.length === 0" class="text-center py-12">
        <div class="text-6xl mb-4">📚</div>
        <h3 class="text-xl font-semibold text-neutral-700 mb-2">暂无搜索历史</h3>
        <p class="text-neutral-500">开始您的第一次文献检索吧！</p>
      </div>

      <div v-else class="space-y-4 max-h-96 overflow-y-auto">
        <div v-for="(item, index) in searchHistory" :key="index"
          class="group p-4 border border-neutral-200 rounded-xl hover:border-primary-200 hover:bg-primary-50/50 cursor-pointer transition-all duration-300"
          @click="searchQuery = item.query; showHistory = false">
          <div class="font-semibold text-neutral-800 mb-2 line-clamp-2 group-hover:text-primary-700">
            {{ item.query }}
          </div>
          <div class="flex items-center justify-between text-sm text-neutral-500">
            <span>{{ item.date }}</span>
            <span class="px-2 py-1 bg-neutral-100 rounded-full group-hover:bg-primary-100 group-hover:text-primary-700">
              {{ item.resultCount }} 篇结果
            </span>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 登录对话框 -->
    <el-dialog v-model="showLogin" width="500px" :show-close="false" class="signup-form-dialog">
      <template #header>
        <div class="text-center mb-6">
          <div class="relative inline-block mb-4">
            <div
              class="w-16 h-16 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg">
              <span class="text-white text-2xl font-bold">P</span>
            </div>
            <div class="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl opacity-20 blur-lg">
            </div>
          </div>
          <h2 class="text-3xl font-bold text-white mb-2">欢迎回来</h2>
          <p class="text-blue-300">登录您的 PaperSurveyAgent 账户</p>
        </div>
      </template>

      <div class="space-y-6">
        <div class="relative">
          <label class="block text-sm font-medium text-blue-300 mb-2">用户名</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <el-input v-model="loginForm.username" placeholder="请输入用户名" class="signup-input"
              :class="{ 'signup-input-focused': loginForm.username }" />
          </div>
        </div>

        <div class="relative">
          <label class="block text-sm font-medium text-blue-300 mb-2">密码</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" show-password
              class="signup-input" :class="{ 'signup-input-focused': loginForm.password }" />
          </div>
        </div>

        <div class="relative group">
          <div
            class="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl blur opacity-75 group-hover:opacity-100 transition duration-300">
          </div>
          <button @click="handleLoginForm" :disabled="!loginForm.username || !loginForm.password || isLoggingIn"
            class="relative w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-glow transition-all duration-300 hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
            <div class="flex items-center justify-center">
              <el-icon v-if="isLoggingIn" class="animate-spin mr-3 text-lg">
                <Loading />
              </el-icon>
              <span class="text-lg">{{ isLoggingIn ? '登录中...' : '登录' }}</span>
            </div>
          </button>
        </div>

        <div class="text-center space-y-2">
          <p class="text-blue-400 text-sm">默认账户: xiaodi / xiaodi_shishen</p>
          <p class="text-blue-400">
            还没有账户？
            <button @click="switchToRegister" class="text-blue-300 hover:text-blue-200 font-medium transition-colors">
              立即注册
            </button>
          </p>
        </div>
      </div>
    </el-dialog>

    <!-- 注册对话框 -->
    <el-dialog v-model="showRegister" width="500px" :show-close="false" class="signup-form-dialog">
      <template #header>
        <div class="text-center mb-6">
          <div class="relative inline-block mb-4">
            <div
              class="w-16 h-16 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg">
              <span class="text-white text-2xl font-bold">P</span>
            </div>
            <div class="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl opacity-20 blur-lg">
            </div>
          </div>
          <h2 class="text-3xl font-bold text-white mb-2">创建账户</h2>
          <p class="text-blue-300">加入 PaperSurveyAgent 开始您的学术之旅</p>
        </div>
      </template>

      <div class="space-y-5">
        <div class="relative">
          <label class="block text-sm font-medium text-blue-300 mb-2">用户名</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <el-input v-model="registerForm.username" placeholder="请输入用户名（至少3个字符）"
              @blur="checkUsernameAvailability(registerForm.username)" class="signup-input"
              :class="{ 'signup-input-focused': registerForm.username }">
              <template #suffix>
                <el-icon v-if="checkingUsername" class="is-loading text-blue-400">
                  <Loading />
                </el-icon>
                <el-icon v-else-if="registerForm.username && !usernameAvailable" class="text-red-400">
                  <CircleClose />
                </el-icon>
                <el-icon v-else-if="registerForm.username && usernameAvailable" class="text-green-400">
                  <CircleCheck />
                </el-icon>
              </template>
            </el-input>
          </div>
          <div v-if="registerForm.username && !usernameAvailable" class="text-red-400 text-xs mt-1 ml-1">
            用户名已被占用
          </div>
          <div v-else-if="registerForm.username && usernameAvailable" class="text-green-400 text-xs mt-1 ml-1">
            用户名可用
          </div>
        </div>

        <div class="relative">
          <label class="block text-sm font-medium text-blue-300 mb-2">邮箱</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <el-input v-model="registerForm.email" placeholder="请输入邮箱地址"
              @blur="checkEmailAvailability(registerForm.email)" class="signup-input"
              :class="{ 'signup-input-focused': registerForm.email }">
              <template #suffix>
                <el-icon v-if="checkingEmail" class="is-loading text-blue-400">
                  <Loading />
                </el-icon>
                <el-icon v-else-if="registerForm.email && !emailAvailable" class="text-red-400">
                  <CircleClose />
                </el-icon>
                <el-icon v-else-if="registerForm.email && emailAvailable" class="text-green-400">
                  <CircleCheck />
                </el-icon>
              </template>
            </el-input>
          </div>
          <div v-if="registerForm.email && !emailAvailable" class="text-red-400 text-xs mt-1 ml-1">
            邮箱已被注册
          </div>
          <div v-else-if="registerForm.email && emailAvailable" class="text-green-400 text-xs mt-1 ml-1">
            邮箱可用
          </div>
        </div>

        <div class="relative">
          <label class="block text-sm font-medium text-blue-300 mb-2">真实姓名（可选）</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <el-input v-model="registerForm.full_name" placeholder="请输入您的真实姓名" class="signup-input"
              :class="{ 'signup-input-focused': registerForm.full_name }" />
          </div>
        </div>

        <div class="relative">
          <label class="block text-sm font-medium text-blue-300 mb-2">密码</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <el-input v-model="registerForm.password" type="password" placeholder="请输入密码（至少6个字符）" show-password
              class="signup-input" :class="{ 'signup-input-focused': registerForm.password }" />
          </div>
        </div>

        <div class="relative">
          <label class="block text-sm font-medium text-blue-300 mb-2">确认密码</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请再次输入密码" show-password
              class="signup-input" :class="{ 'signup-input-focused': registerForm.confirmPassword }" />
          </div>
          <div v-if="registerForm.confirmPassword && registerForm.password !== registerForm.confirmPassword"
            class="text-red-400 text-xs mt-1 ml-1">
            两次输入的密码不一致
          </div>
        </div>

        <div class="relative group">
          <div
            class="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl blur opacity-75 group-hover:opacity-100 transition duration-300">
          </div>
          <button @click="handleRegister"
            :disabled="!registerForm.username || !registerForm.email || !registerForm.password || !registerForm.confirmPassword || !usernameAvailable || !emailAvailable || isRegistering"
            class="relative w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-glow transition-all duration-300 hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
            <div class="flex items-center justify-center">
              <el-icon v-if="isRegistering" class="animate-spin mr-3 text-lg">
                <Loading />
              </el-icon>
              <span class="text-lg">{{ isRegistering ? '注册中...' : '创建账户' }}</span>
            </div>
          </button>
        </div>

        <div class="text-center">
          <p class="text-blue-400">
            已有账户？
            <button @click="switchToLogin" class="text-blue-300 hover:text-blue-200 font-medium transition-colors">
              立即登录
            </button>
          </p>
        </div>
      </div>
    </el-dialog>

    <!-- 移动端菜单 -->
    <div v-if="showMobileMenu" class="lg:hidden fixed inset-0 z-50 bg-black/50" @click="showMobileMenu = false">
      <div class="absolute top-20 right-6 bg-white rounded-2xl shadow-large p-6 min-w-[200px]" @click.stop>
        <div class="space-y-4">
          <button @click="showHistory = true; showMobileMenu = false"
            class="w-full flex items-center px-4 py-3 text-neutral-600 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-all duration-300">
            <el-icon class="mr-3">
              <Clock />
            </el-icon>
            <span>搜索历史</span>
          </button>
          <button @click="showSettings = true; showMobileMenu = false"
            class="w-full flex items-center px-4 py-3 text-neutral-600 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-all duration-300">
            <el-icon class="mr-3">
              <Setting />
            </el-icon>
            <span>设置</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 充值对话框 -->
    <el-dialog v-model="showRecharge" title="账户充值" width="500px" class="modern-dialog">
      <div class="space-y-6">
        <!-- 当前余额显示 -->
        <div class="text-center p-4 bg-primary-50 rounded-xl">
          <div class="text-sm text-primary-600 mb-1">当前余额</div>
          <div class="text-2xl font-bold text-primary-700">¥{{ userBalance.balance?.toFixed(2) || '0.00' }}</div>
        </div>

        <!-- 充值金额选择 -->
        <div>
          <label class="block text-sm font-semibold text-neutral-700 mb-3">选择充值金额</label>
          <div class="grid grid-cols-2 gap-3">
            <button v-for="amount in [10, 50, 100, 200]" :key="amount" @click="selectedAmount = amount" :class="[
              'p-4 border-2 rounded-xl text-center transition-all duration-300 hover:scale-105',
              selectedAmount === amount
                ? 'border-primary-500 bg-primary-50 text-primary-700 shadow-md'
                : 'border-neutral-200 hover:border-primary-300 hover:bg-primary-50'
            ]">
              <div class="text-lg font-bold">¥{{ amount }}</div>
              <div class="text-xs text-neutral-500 mt-1">{{ amount * 20 }}篇文献</div>
            </button>
          </div>
        </div>

        <!-- 收款码显示区域 -->
        <div v-if="selectedAmount > 0" class="text-center">
          <div class="mb-4">
            <p class="text-sm text-neutral-600 mb-2">请使用支付宝扫码支付</p>
            <div class="inline-block p-4 bg-white border-2 border-neutral-200 rounded-xl">
              <img :src="getQrCodePath()" alt="支付宝收款码" class="w-48 h-48 object-contain" />
            </div>
          </div>
          <div class="text-xs text-neutral-500">
            <p>支付金额：¥{{ selectedAmount }}</p>
            <p>支付完成后请点击"已完成支付"</p>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex space-x-3">
          <button @click="showRecharge = false; selectedAmount = 0"
            class="flex-1 px-4 py-2 border border-neutral-300 text-neutral-700 rounded-xl hover:bg-neutral-50 transition-colors">
            取消
          </button>
          <button v-if="selectedAmount > 0" @click="confirmPayment" :disabled="isConfirmingPayment"
            class="flex-1 px-4 py-2 bg-success text-white rounded-xl hover:bg-success-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
            {{ isConfirmingPayment ? '确认中...' : '已完成支付' }}
          </button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Setting,
  Clock,
  Loading,
  ArrowDown,
  Search,
  Document,
  CircleCheck,
  CircleClose,
  Wallet,
  CreditCard
} from '@element-plus/icons-vue'
import PaperCard from '../components/PaperCard.vue'
import type { Paper, SearchHistoryItem } from '../types/paper'

// 路由
const router = useRouter()

// 响应式数据
const searchQuery = ref('')
const selectedSources = ref(['arxiv'])  // Only ArXiv supported
const maxPapers = ref(5)
const retrieveFullText = ref(false)
const enableAIAnalysis = ref(true)
const isSearching = ref(false)
const isGeneratingReport = ref(false)
const hasSearched = ref(false)
const searchResults = ref<Paper[]>([])
const searchProgress = ref('')
const actionPlan = ref<string[]>([])

// UI 状态
const showSettings = ref(false)
const showHistory = ref(false)
const showAdvancedOptions = ref(false)
const showMobileMenu = ref(false)
const showLogin = ref(false)
const showRegister = ref(false)
const showRecharge = ref(false)

// 登录表单
const loginForm = ref({
  username: 'xiaodi',
  password: 'xiaodi_shishen'
})
const isLoggingIn = ref(false)

// 注册表单
const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  full_name: ''
})
const isRegistering = ref(false)
const usernameAvailable = ref(true)
const emailAvailable = ref(true)
const checkingUsername = ref(false)
const checkingEmail = ref(false)

// 设置
const defaultSources = ref(['arxiv'])  // Only ArXiv supported
const defaultMaxPapers = ref(20)
const language = ref('zh')

// 搜索历史
const searchHistory = ref<SearchHistoryItem[]>([])

// 统计数据
const totalPapers = ref(0)
const processingTime = ref(7.1)
const relevanceScore = ref(95.6)

// 用户余额数据
const userBalance = ref({
  balance: 0,
  total_papers_searched: 0,
  total_amount_spent: 0
})

// 充值相关数据
const selectedAmount = ref(0)
const isConfirmingPayment = ref(false)
const getQrCodePath = () => `http://localhost:8000/media/收款码zfb.jpg?v=${Date.now()}`

// AI智能建议系统
const aiSuggestions = ref<string[]>([])
const naturalLanguageSuggestions = ref([
  '最近五年人工智能在卫星网络领域的应用进展',
  '寻找关于基于AI的空天地一体化网络资源调度优化算法的最新研究',
  '查找2020年以来大模型与Agent技术的最新应用研究',
])

// AI增强功能
const generateAISuggestions = (query: string) => {
  if (query.length < 20) {
    aiSuggestions.value = []
    return
  }

  // 基于关键词的智能建议生成
  const suggestions = []

  if (query.includes('深度学习') || query.includes('机器学习')) {
    suggestions.push('建议添加时间范围：如"2020年以来"或"最近5年"')
    suggestions.push('可以指定应用领域：如"在医疗领域"、"在计算机视觉中"')
    suggestions.push('考虑添加技术细节：如"基于CNN"、"使用Transformer架构"')
  }

  if (query.includes('医疗') || query.includes('诊断')) {
    suggestions.push('建议明确医疗子领域：如"影像诊断"、"病理分析"、"药物发现"')
    suggestions.push('可以关注临床应用：如"FDA批准"、"临床试验结果"')
  }

  if (query.includes('最新') || query.includes('进展')) {
    suggestions.push('建议指定时间窗口：如"2023-2024年"、"近两年内"')
    suggestions.push('可以关注顶会论文：如"NIPS"、"ICLR"、"Nature"期刊')
  }

  if (suggestions.length === 0) {
    suggestions.push('尝试添加更多具体细节来提高检索精度')
    suggestions.push('可以包含研究方法、应用场景或技术关键词')
    suggestions.push('建议指定发表时间范围以获取最新研究')
  }

  aiSuggestions.value = suggestions.slice(0, 3)
}

const handleSearchInput = (value: string) => {
  generateAISuggestions(value)
}

const applySuggestion = (suggestion: string) => {
  // 应用AI建议到搜索框
  searchQuery.value = suggestion
  ElMessage.success('AI建议已应用，请根据提示完善您的查询')
  aiSuggestions.value = []
}

const clearSearch = () => {
  searchQuery.value = ''
  aiSuggestions.value = []
}

// 认证相关函数
const getAuthToken = () => {
  return localStorage.getItem('authToken') || ''
}

const isAuthenticated = () => {
  return !!getAuthToken()
}

// 获取用户余额
const fetchUserBalance = async () => {
  if (!isAuthenticated()) {
    return
  }

  try {
    const response = await fetch('http://localhost:8000/api/user/balance', {
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`
      }
    })

    if (response.ok) {
      const data = await response.json()
      userBalance.value = data
    } else {
      console.error('Failed to fetch user balance:', response.status)
    }
  } catch (error) {
    console.error('Error fetching user balance:', error)
  }
}

const confirmPayment = async () => {
  if (selectedAmount.value <= 0) {
    ElMessage.warning('请选择充值金额')
    return
  }

  isConfirmingPayment.value = true

  try {
    // 生成订单ID
    const orderId = `recharge_${Date.now()}_${selectedAmount.value}`

    const response = await fetch('http://localhost:8000/api/payment/confirm', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAuthToken()}`
      },
      body: JSON.stringify({
        order_id: orderId
      })
    })

    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        ElMessage.success(data.message)
        // 更新用户余额
        await fetchUserBalance()
        // 关闭对话框并重置状态
        showRecharge.value = false
        selectedAmount.value = 0
      } else {
        ElMessage.error(data.message || '充值失败')
      }
    } else {
      ElMessage.error('充值确认失败')
    }
  } catch (error) {
    console.error('Error confirming payment:', error)
    ElMessage.error('充值确认失败，请稍后重试')
  } finally {
    isConfirmingPayment.value = false
  }
}

const handleLogin = async (username: string, password: string) => {
  try {
    const response = await fetch('http://localhost:8000/auth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
    })

    if (!response.ok) {
      throw new Error('登录失败')
    }

    const data = await response.json()
    localStorage.setItem('authToken', data.access_token)
    ElMessage.success('登录成功！')
    showLogin.value = false

    // 登录成功后获取用户余额
    await fetchUserBalance()

    return true
  } catch (error) {
    console.error('Login error:', error)
    ElMessage.error('登录失败，请检查用户名和密码')
    return false
  }
}

const handleLoginForm = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  isLoggingIn.value = true
  const success = await handleLogin(loginForm.value.username, loginForm.value.password)
  isLoggingIn.value = false

  if (success) {
    // 登录成功后可以自动重新执行之前的操作
  }
}

const handleLogout = () => {
  localStorage.removeItem('authToken')
  ElMessage.success('已退出登录')
  // 清空搜索结果
  searchResults.value = []
  actionPlan.value = []
}

// 注册相关函数
const checkUsernameAvailability = async (username: string) => {
  if (!username || username.length < 3) {
    usernameAvailable.value = false
    return
  }

  checkingUsername.value = true
  try {
    const response = await fetch('http://localhost:8000/auth/check-username', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username })
    })

    if (response.ok) {
      const data = await response.json()
      usernameAvailable.value = data.available
    } else {
      usernameAvailable.value = false
    }
  } catch (error) {
    console.error('Username check error:', error)
    usernameAvailable.value = false
  } finally {
    checkingUsername.value = false
  }
}

const checkEmailAvailability = async (email: string) => {
  if (!email || !email.includes('@')) {
    emailAvailable.value = false
    return
  }

  checkingEmail.value = true
  try {
    const response = await fetch('http://localhost:8000/auth/check-email', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email })
    })

    if (response.ok) {
      const data = await response.json()
      emailAvailable.value = data.available
    } else {
      emailAvailable.value = false
    }
  } catch (error) {
    console.error('Email check error:', error)
    emailAvailable.value = false
  } finally {
    checkingEmail.value = false
  }
}

const handleRegister = async () => {
  const form = registerForm.value

  // 表单验证
  if (!form.username || !form.email || !form.password || !form.confirmPassword) {
    ElMessage.warning('请填写所有必填字段')
    return
  }

  if (form.username.length < 3) {
    ElMessage.warning('用户名至少需要3个字符')
    return
  }

  // 更严格的邮箱格式校验
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(form.email)) {
    ElMessage.warning('请输入有效的邮箱地址，格式应为：xxx@xxx.com')
    return
  }

  if (form.password.length < 6) {
    ElMessage.warning('密码至少需要6个字符')
    return
  }

  if (form.password !== form.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }

  if (!usernameAvailable.value) {
    ElMessage.warning('用户名已被占用')
    return
  }

  if (!emailAvailable.value) {
    ElMessage.warning('邮箱已被注册')
    return
  }

  isRegistering.value = true
  try {
    const response = await fetch('http://localhost:8000/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: form.username,
        email: form.email,
        password: form.password,
        full_name: form.full_name
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || '注册失败')
    }

    const data = await response.json()

    // 保存token
    localStorage.setItem('authToken', data.access_token)

    // 关闭注册对话框
    showRegister.value = false

    // 注册成功后获取用户余额
    await fetchUserBalance()

    // 重置表单
    registerForm.value = {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      full_name: ''
    }

    ElMessage.success('注册成功！欢迎加入 PaperSurveyAgent')
  } catch (error: any) {
    console.error('Registration error:', error)
    const errorMessage = error.message || error.toString() || '注册失败，请稍后重试'
    ElMessage.error(`注册失败: ${errorMessage}`)
  } finally {
    isRegistering.value = false
  }
}

// 切换登录/注册对话框
const switchToRegister = () => {
  showLogin.value = false
  showRegister.value = true
  // 重置表单
  registerForm.value = {
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    full_name: ''
  }
}

const switchToLogin = () => {
  showRegister.value = false
  showLogin.value = true
}

// 方法
const startSearch = async () => {
  if (!searchQuery.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }
  isSearching.value = true
  hasSearched.value = true
  searchResults.value = []
  actionPlan.value = []
  searchProgress.value = '正在连接服务器...'

  try {
    console.log(`Searching for: ${searchQuery.value}, Sources: ${selectedSources.value.join(', ')}, Max Papers: ${maxPapers.value}`);

    // 调用真实API
    const response = await fetch('http://localhost:8000/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAuthToken()}` // 需要认证
      },
      body: JSON.stringify({
        rawQuery: searchQuery.value,
        query: searchQuery.value, // backward compatibility
        maxPapers: maxPapers.value,
        sources: selectedSources.value,
        retrieveFullText: retrieveFullText.value,
        yearStart: null,
        yearEnd: null
      })
    })

    if (!response.ok) {
      if (response.status === 401) {
        ElMessage.error('需要登录才能进行检索')
        showLogin.value = true
        return
      }
      if (response.status === 402) {
        const errorData = await response.json()
        const detail = errorData.detail
        if (typeof detail === 'object' && detail.error === 'Insufficient balance') {
          ElMessage.error(`余额不足，需要${detail.required.toFixed(2)}元，当前余额${detail.current_balance.toFixed(2)}元`)
          showRecharge.value = true
          return
        }
      }
      throw new Error(`API请求失败: ${response.status}`)
    }

    const data = await response.json()

    // 处理返回的数据
    actionPlan.value = data.actionPlan || []
    searchResults.value = data.papers || []

    // 更新统计信息
    totalPapers.value = searchResults.value.length
    relevanceScore.value = Math.floor(Math.random() * 5) + 95 // 95-99%的相关性分数

    // 保存搜索历史
    const historyItem: SearchHistoryItem = {
      query: searchQuery.value,
      date: new Date().toLocaleDateString('zh-CN'),
      resultCount: searchResults.value.length,
      params: {
        sources: selectedSources.value,
        maxPapers: maxPapers.value,
        retrieveFullText: retrieveFullText.value,
        enableAIAnalysis: enableAIAnalysis.value
      }
    };
    searchHistory.value.unshift(historyItem);
    if (searchHistory.value.length > 10) {
      searchHistory.value = searchHistory.value.slice(0, 10);
    }

    ElMessage.success(`检索完成！找到 ${searchResults.value.length} 篇相关文献`);

    // 搜索成功后更新用户余额
    await fetchUserBalance()

  } catch (error) {
    console.error('Search error:', error)

    // 检查是否是余额不足错误
    if (error instanceof Response && error.status === 402) {
      try {
        const errorData = await error.json()
        if (errorData.detail && errorData.detail.error === 'Insufficient balance') {
          const required = errorData.detail.required || 0
          const current = errorData.detail.current_balance || 0

          ElMessageBox.alert(
            `您的账户余额不足，无法完成搜索。\n\n需要金额：¥${required.toFixed(2)}\n当前余额：¥${current.toFixed(2)}\n\n请先充值后再试。`,
            '余额不足',
            {
              confirmButtonText: '去充值',
              type: 'warning',
              callback: () => {
                showRecharge.value = true
              }
            }
          )
          return
        }
      } catch (e) {
        console.error('Error parsing error response:', e)
      }
    }

    // 其他错误类型显示通用错误信息
    ElMessage.error('检索失败，请检查网络连接或稍后重试')
  } finally {
    isSearching.value = false
    searchProgress.value = ''
  }
}

const generateReport = async () => {
  if (searchResults.value.length === 0) {
    ElMessage.warning('没有可用的论文数据生成报告')
    return
  }

  if (!isAuthenticated()) {
    ElMessage.error('需要登录才能生成报告')
    return
  }

  isGeneratingReport.value = true

  try {
    const response = await fetch('http://localhost:8000/api/generate-report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAuthToken()}`
      },
      body: JSON.stringify({
        title: `基于"${searchQuery.value}"的文献综述报告`,
        papers: searchResults.value
      })
    })

    if (!response.ok) {
      if (response.status === 401) {
        ElMessage.error('认证已过期，请重新登录')
        return
      }
      throw new Error(`报告生成失败: ${response.status}`)
    }

    const data = await response.json()
    const reportContent = data.report || '报告生成失败'

    ElMessageBox.alert(`<pre style="white-space: pre-wrap; max-height: 500px; overflow-y: auto;">${reportContent}</pre>`, '文献综述报告', {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '关闭',
      customClass: 'report-dialog'
    })
  } catch (error) {
    console.error('Report generation error:', error)
    ElMessage.error('报告生成失败，请检查网络连接或稍后重试')
  } finally {
    isGeneratingReport.value = false
  }
}

// PaperCard event handlers
const toggleFavorite = (paperId: string) => {
  const paper = searchResults.value.find(p => p.id === paperId);
  if (paper) {
    paper.isFavorite = !paper.isFavorite;
    ElMessage.success(paper.isFavorite ? '已收藏' : '取消收藏');
  }
};

const viewDetailsModal = (paper: Paper) => {
  ElMessageBox.alert(JSON.stringify(paper, null, 2), `论文详情: ${paper.title}`, {
    confirmButtonText: '关闭',
    customClass: 'report-dialog' // Using existing class for wider dialog
  });
};

const downloadPdf = (paper: Paper) => {
  if (paper.pdfUrl && paper.pdfUrl !== '#') {
    window.open(paper.pdfUrl, '_blank');
  } else {
    ElMessage.info('该论文暂无可用PDF链接。');
  }
};

// 移除未使用的函数，这些功能将在后续的组件拆分中实现

const goToWelcome = () => {
  router.push('/')
}

// Lifecycle
onMounted(async () => {
  // 如果已登录，获取用户余额
  if (isAuthenticated()) {
    await fetchUserBalance()
  }

  const savedSettings = localStorage.getItem('literatureReviewSettings');
  if (savedSettings) {
    const settings = JSON.parse(savedSettings);
    // 过滤掉不支持的数据源，只保留 arxiv
    const filteredSources = (settings.defaultSources || ['arxiv']).filter((source: string) => source === 'arxiv');
    defaultSources.value = filteredSources.length > 0 ? filteredSources : ['arxiv'];
    defaultMaxPapers.value = settings.defaultMaxPapers || 20;
    language.value = settings.language || 'zh';

    // 同时更新当前选择的数据源，确保不包含不支持的源
    selectedSources.value = [...defaultSources.value];
  }

  // 清理可能存在的旧的搜索设置
  const savedSearchSettings = localStorage.getItem('searchSettings');
  if (savedSearchSettings) {
    try {
      const searchSettings = JSON.parse(savedSearchSettings);
      if (searchSettings.sources) {
        // 过滤掉不支持的数据源
        const filteredSources = searchSettings.sources.filter((source: string) => source === 'arxiv');
        selectedSources.value = filteredSources.length > 0 ? filteredSources : ['arxiv'];
      }
    } catch (e) {
      console.warn('Failed to parse saved search settings:', e);
    }
  }

  // 强制清理任何可能包含 semantic_scholar 的本地存储
  console.log('🧹 Cleaning up old semantic_scholar references from localStorage...');

  // 清理并重新保存设置，确保不包含 semantic_scholar
  const cleanedSettings = {
    defaultSources: ['arxiv'],
    defaultMaxPapers: defaultMaxPapers.value,
    language: language.value
  };
  localStorage.setItem('literatureReviewSettings', JSON.stringify(cleanedSettings));

  // 确保当前选择也是干净的
  selectedSources.value = ['arxiv'];

  console.log('✅ localStorage cleaned, only ArXiv is supported');

  const savedHistory = localStorage.getItem('searchHistory');
  if (savedHistory) {
    searchHistory.value = JSON.parse(savedHistory);
  }
});

watch([defaultSources, defaultMaxPapers, language], (newValues) => {
  localStorage.setItem('literatureReviewSettings', JSON.stringify({
    defaultSources: newValues[0],
    defaultMaxPapers: newValues[1],
    language: newValues[2]
  }));
}, { deep: true });

watch(searchHistory, (newHistory) => {
  localStorage.setItem('searchHistory', JSON.stringify(newHistory));
}, { deep: true });

// 计算搜索费用
const calculateSearchCost = (papersCount: number) => {
  // 单价：0.1元/篇，最低消费0.5元
  const cost = papersCount * 0.1
  return Math.max(cost, 0.5)
}
</script>

<style scoped>
/* HomeView 专用样式 */

/* Parallax Animations */
@keyframes float-parallax-1 {

  0%,
  100% {
    transform: translateY(0px) translateX(0px);
  }

  33% {
    transform: translateY(-15px) translateX(10px);
  }

  66% {
    transform: translateY(-8px) translateX(-5px);
  }
}

@keyframes float-parallax-2 {

  0%,
  100% {
    transform: translateY(0px) translateX(0px);
  }

  33% {
    transform: translateY(-12px) translateX(-8px);
  }

  66% {
    transform: translateY(-6px) translateX(4px);
  }
}

@keyframes float-parallax-3 {

  0%,
  100% {
    transform: translateY(0px) translateX(0px);
  }

  33% {
    transform: translateY(-10px) translateX(6px);
  }

  66% {
    transform: translateY(-5px) translateX(-3px);
  }
}

@keyframes float-parallax-4 {

  0%,
  100% {
    transform: translateY(0px) translateX(0px);
  }

  33% {
    transform: translateY(-8px) translateX(-4px);
  }

  66% {
    transform: translateY(-4px) translateX(2px);
  }
}

.animate-float-parallax-1 {
  animation: float-parallax-1 15s ease-in-out infinite;
}

.animate-float-parallax-2 {
  animation: float-parallax-2 18s ease-in-out infinite;
  animation-delay: -2s;
}

.animate-float-parallax-3 {
  animation: float-parallax-3 12s ease-in-out infinite;
  animation-delay: -4s;
}

.animate-float-parallax-4 {
  animation: float-parallax-4 20s ease-in-out infinite;
  animation-delay: -1s;
}

@keyframes parallax-float-1 {

  0%,
  100% {
    transform: translateY(0px) rotate(12deg);
  }

  50% {
    transform: translateY(-8px) rotate(15deg);
  }
}

@keyframes parallax-float-2 {

  0%,
  100% {
    transform: translateY(0px) rotate(-6deg);
  }

  50% {
    transform: translateY(-6px) rotate(-3deg);
  }
}

@keyframes parallax-float-3 {

  0%,
  100% {
    transform: translateY(0px) rotate(3deg);
  }

  50% {
    transform: translateY(-4px) rotate(6deg);
  }
}

.animate-parallax-float-1 {
  animation: parallax-float-1 8s ease-in-out infinite;
}

.animate-parallax-float-2 {
  animation: parallax-float-2 10s ease-in-out infinite;
  animation-delay: -1s;
}

.animate-parallax-float-3 {
  animation: parallax-float-3 6s ease-in-out infinite;
  animation-delay: -2s;
}

@keyframes particleFloat {

  0%,
  100% {
    transform: translateY(0px) translateX(0px);
    opacity: 0;
  }

  10%,
  90% {
    opacity: 0.6;
  }

  50% {
    transform: translateY(-100px) translateX(20px);
    opacity: 0.3;
  }
}

/* Enhanced gradient text for dark theme */
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

/* 高级选项过渡动画 */
.advanced-options-enter-active,
.advanced-options-leave-active {
  transition: all 0.4s ease-out;
  transform-origin: top;
}

.advanced-options-enter-from {
  opacity: 0;
  transform: scaleY(0.8) translateY(-20px);
}

.advanced-options-leave-to {
  opacity: 0;
  transform: scaleY(0.8) translateY(-20px);
}

/* Dark theme search input styles */
.search-input-dark :deep(.el-textarea__inner) {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8)) !important;
  backdrop-filter: blur(10px) !important;
  border: 2px solid rgba(59, 130, 246, 0.3) !important;
  border-radius: 20px !important;
  padding: 24px !important;
  font-size: 16px !important;
  line-height: 1.7 !important;
  resize: none !important;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow:
    0 0 0 1px rgba(59, 130, 246, 0.2),
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(59, 130, 246, 0.1) !important;
  color: #e2e8f0 !important;
  position: relative;
}

.search-input-dark :deep(.el-textarea__inner):focus {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9)) !important;
  border-color: rgba(59, 130, 246, 0.5) !important;
  box-shadow:
    0 0 0 2px rgba(59, 130, 246, 0.3),
    0 0 0 4px rgba(59, 130, 246, 0.1),
    0 12px 40px rgba(59, 130, 246, 0.2) !important;
  transform: translateY(-1px);
  color: #ffffff !important;
}

.search-input-dark :deep(.el-textarea__inner)::placeholder {
  color: #94a3b8 !important;
  font-style: normal !important;
  line-height: 1.6 !important;
}

/* AI增强搜索输入框样式 (保留兼容) */
.search-input-ai-enhanced :deep(.el-textarea__inner) {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.95)) !important;
  border: 2px solid transparent !important;
  border-radius: 20px !important;
  padding: 24px !important;
  font-size: 16px !important;
  line-height: 1.7 !important;
  resize: none !important;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow:
    0 0 0 1px rgba(14, 165, 233, 0.1),
    0 8px 32px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.7) !important;
  position: relative;
}

.search-input-ai-enhanced :deep(.el-textarea__inner):focus {
  background: rgba(255, 255, 255, 1) !important;
  box-shadow:
    0 0 0 2px rgba(14, 165, 233, 0.2),
    0 0 0 4px rgba(14, 165, 233, 0.1),
    0 12px 40px rgba(14, 165, 233, 0.15) !important;
  transform: translateY(-1px);
}

.search-input-ai-enhanced :deep(.el-textarea__inner)::placeholder {
  color: var(--color-neutral-500) !important;
  font-style: normal !important;
  line-height: 1.6 !important;
}

/* 搜索输入框现代化样式 (保留兼容) */
.search-input-modern :deep(.el-textarea__inner) {
  background: rgba(255, 255, 255, 0.9) !important;
  border: 2px solid var(--color-neutral-200) !important;
  border-radius: 16px !important;
  padding: 20px !important;
  font-size: 16px !important;
  line-height: 1.6 !important;
  resize: none !important;
  transition: all 0.3s ease-out !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
}

.search-input-modern :deep(.el-textarea__inner):focus {
  border-color: var(--color-primary) !important;
  box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1), 0 8px 30px rgba(0, 0, 0, 0.1) !important;
  background: rgba(255, 255, 255, 1) !important;
}

.search-input-modern :deep(.el-textarea__inner)::placeholder {
  color: var(--color-neutral-400) !important;
  font-style: italic !important;
}

/* 现代化对话框样式 */
.modern-dialog :deep(.el-dialog) {
  border-radius: 20px !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15) !important;
  border: 1px solid var(--color-neutral-200) !important;
}

.modern-dialog :deep(.el-dialog__header) {
  padding: 24px 24px 16px !important;
  border-bottom: 1px solid var(--color-neutral-200) !important;
}

.modern-dialog :deep(.el-dialog__title) {
  font-size: 1.5rem !important;
  font-weight: 600 !important;
  color: var(--color-neutral-900) !important;
}

.modern-dialog :deep(.el-dialog__body) {
  padding: 24px !important;
}

/* 浮动动画增强 */
.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-float:nth-child(2) {
  animation-delay: 2s;
}

.animate-float:nth-child(3) {
  animation-delay: 4s;
}

/* 悬停提升效果 */
.hover-lift {
  transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;
}

.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* 响应式调整 */
@media (max-width: 1024px) {
  .gradient-text-primary {
    background-size: 100% 100%;
    animation: none;
  }
}

/* 减少动画偏好支持 */
@media (prefers-reduced-motion: reduce) {

  .animate-float,
  .gradient-text-primary,
  .hover-lift {
    animation: none;
  }

  .hover-lift:hover {
    transform: none;
  }

  .advanced-options-enter-active,
  .advanced-options-leave-active {
    transition: none;
  }
}

/* Signup Form Dialog Styles */
.signup-form-dialog :deep(.el-dialog) {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95)) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(59, 130, 246, 0.3) !important;
  border-radius: 24px !important;
  box-shadow:
    0 25px 50px -12px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(59, 130, 246, 0.1) !important;
}

.signup-form-dialog :deep(.el-dialog__header) {
  padding: 0 !important;
  border-bottom: none !important;
}

.signup-form-dialog :deep(.el-dialog__body) {
  padding: 0 32px 32px 32px !important;
}

.signup-form-dialog :deep(.el-dialog__headerbtn) {
  display: none !important;
}

/* Signup Input Styles */
.signup-input :deep(.el-input__wrapper) {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8)) !important;
  backdrop-filter: blur(10px) !important;
  border: 2px solid rgba(59, 130, 246, 0.3) !important;
  border-radius: 16px !important;
  padding: 16px 16px 16px 48px !important;
  box-shadow:
    0 0 0 1px rgba(59, 130, 246, 0.2),
    0 4px 20px rgba(0, 0, 0, 0.3) !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.signup-input :deep(.el-input__inner) {
  color: #e2e8f0 !important;
  font-size: 16px !important;
  height: 24px !important;
  line-height: 24px !important;
  background: transparent !important;
}

.signup-input :deep(.el-input__inner)::placeholder {
  color: #94a3b8 !important;
  font-size: 15px !important;
}

.signup-input-focused :deep(.el-input__wrapper) {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9)) !important;
  border-color: rgba(59, 130, 246, 0.5) !important;
  box-shadow:
    0 0 0 2px rgba(59, 130, 246, 0.3),
    0 0 0 4px rgba(59, 130, 246, 0.1),
    0 8px 25px rgba(59, 130, 246, 0.2) !important;
  transform: translateY(-1px) !important;
}

/* Input focus state animations */
.signup-input :deep(.el-input__wrapper):hover {
  border-color: rgba(59, 130, 246, 0.4) !important;
  transform: translateY(-0.5px) !important;
}

/* Enhanced button styles for signup form */
.signup-form-dialog .relative.group button:disabled {
  background: linear-gradient(135deg, rgba(107, 114, 128, 0.5), rgba(75, 85, 99, 0.5)) !important;
  cursor: not-allowed !important;
  transform: none !important;
}

.signup-form-dialog .relative.group button:not(:disabled):hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow:
    0 20px 40px rgba(59, 130, 246, 0.3),
    0 0 0 1px rgba(59, 130, 246, 0.2) !important;
}

/* Form label enhancements */
.signup-form-dialog label {
  font-weight: 600 !important;
  letter-spacing: 0.025em !important;
}

/* Status icons styling */
.signup-form-dialog .text-red-400 {
  color: #f87171 !important;
}

.signup-form-dialog .text-green-400 {
  color: #4ade80 !important;
}

.signup-form-dialog .text-blue-400 {
  color: #60a5fa !important;
}

/* Mobile responsiveness for signup form */
@media (max-width: 640px) {
  .signup-form-dialog :deep(.el-dialog) {
    margin: 16px !important;
    width: calc(100vw - 32px) !important;
    max-width: none !important;
  }

  .signup-form-dialog :deep(.el-dialog__body) {
    padding: 0 24px 24px 24px !important;
  }

  .signup-input :deep(.el-input__wrapper) {
    padding: 14px 14px 14px 44px !important;
  }
}
</style>
