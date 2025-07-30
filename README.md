# 🌟 星露谷物语通用汉化模组 - TranslateAll

![Stardew Valley](https://img.shields.io/badge/Stardew%20Valley-Mod-green?style=for-the-badge)
![SMAPI](https://img.shields.io/badge/SMAPI-3.14.0+-blue?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-0.0.2-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)

> 一个支持所有星露谷物语模组的通用中文翻译框架

## 📖 项目简介

TranslateAll 是一个创新的星露谷物语通用汉化模组，旨在为各种英文模组提供高质量的中文翻译支持。无论是角色对话、物品描述还是界面文本，我们都致力于为中文玩家带来完整的本土化体验。

### ✨ 主要特性

- 🚀 **通用兼容**：支持所有基于文本的星露谷物语模组
- 🎯 **智能翻译**：集成 AI 翻译助手，提高翻译效率
- 🔄 **实时更新**：翻译文件动态加载，无需重启游戏
- 🌐 **社区驱动**：开放的贡献模式，欢迎所有玩家参与翻译
- 📦 **模块化设计**：按模组独立管理翻译文件

## 🎮 支持的模组

目前已支持的模组包括：

| 模组名称 | 翻译状态 | 最后更新 |
|---------|---------|----------|
| atravita.NovaNPCTest | ✅ 完成 | 2025-07 |
| CJBok.CheatsMenu | ✅ 完成 | 2025-07 |
| TenebrousNova.EliDylan.CP | ✅ 完成 | 2025-07 |
...

*想要添加新模组翻译？查看我们的 [贡献指南](CONTRIBUTING.md)！*

## 🚀 快速开始

### 系统要求

- 星露谷物语 1.5.6+
- SMAPI 3.14.0+
- .NET 6.0

### 安装步骤

1. **下载模组**
   ```bash
   # 从 Releases 页面下载最新版本
   # 或使用 Git 克隆仓库
   git clone https://github.com/keyboard2005/Stardew-Valley-Translate-CN.git
   ```

2. **安装到游戏**
   - 将 `TranslateAll` 文件夹复制到 `星露谷物语/Mods/` 目录
   - 确保 SMAPI 已正确安装

3. **启动游戏**
   - 通过 SMAPI 启动游戏
   - 在控制台中确认模组加载成功

### 使用方法

模组安装后会自动工作，无需额外配置。翻译文件会根据已安装的模组自动加载对应的中文翻译。

## 🛠️ 项目结构

```
TranslateAll/
├── manifest.json              # 模组清单文件
├── ModEntry.cs               # 主入口代码
├── TranslateAll.dll          # 编译后的模组文件
├── translations/             # 翻译文件目录
│   ├── 模组名称/
│   │   ├── default.json     # 原文参考
│   │   └── zh.json         # 中文翻译
│   └── ...
├── ai_translate.py          # AI 翻译助手
├── name_replace.py          # 名称替换工具
└── npc_name.json           # 角色名称映射
```

## 🤝 如何贡献

我们欢迎所有形式的贡献！无论你是：

- 🌟 **翻译贡献者**：提供新的翻译或改进现有翻译
- 🐛 **问题报告者**：发现并报告翻译问题
- 💡 **功能建议者**：提出改进建议和新功能想法
- 📖 **文档完善者**：改进文档和使用指南

### 开始贡献

1. 📖 阅读我们的 [贡献指南](CONTRIBUTING.md)
2. 🍴 Fork 本仓库
3. 🌿 创建你的功能分支
4. 📝 进行翻译工作
5. 🚀 提交 Pull Request

### 贡献者

感谢所有为项目做出贡献的朋友们！

[![Contributors](https://contrib.rocks/image?repo=keyboard2005/Stardew-Valley-Translate-CN)](https://github.com/keyboard2005/Stardew-Valley-Translate-CN/graphs/contributors)

## 📊 翻译统计

| 总模组数 | 已翻译 | 进行中 | 计划中 |
|---------|--------|--------|--------|
| 10+ | 3 | 2 | 5+ |

翻译进度：![Progress](https://progress-bar.dev/30/?title=总体进度)

## 🔧 开发工具

### AI 翻译助手

使用内置的 AI 翻译工具快速生成初始翻译：

```bash
python ai_translate.py --input default.json --output zh.json
```

### 名称映射工具

批量替换角色名称：

```bash
python name_replace.py --file zh.json --mapping npc_name.json
```

## 📋 更新日志

### v0.0.2 (2025-07-30)
- ✨ 新增 AI 翻译助手
- 🐛 修复翻译文件加载问题
- 📚 完善文档和贡献指南

### v0.0.1 (2025-07-01)
- 🎉 项目初始发布
- 🌟 基础翻译框架
- 📦 支持首批模组翻译

## 📞 联系我们

- 🐛 **Bug 报告**：[GitHub Issues](https://github.com/keyboard2005/Stardew-Valley-Translate-CN/issues)
- 💬 **讨论交流**：[GitHub Discussions](https://github.com/keyboard2005/Stardew-Valley-Translate-CN/discussions)
- 📧 **邮件联系**：[项目维护者邮箱]

## 📄 开源协议

本项目采用 [MIT 协议](LICENSE) 开源。

```
MIT License

Copyright (c) 2025 keyboard2005

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

## 🙏 致谢

- **ConcernedApe**：创造了精彩的星露谷物语
- **SMAPI 团队**：提供了强大的模组框架
- **社区贡献者**：所有参与翻译工作的朋友们
- **模组作者们**：创造了丰富的游戏内容

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=keyboard2005/Stardew-Valley-Translate-CN&type=Date)](https://star-history.com/#keyboard2005/Stardew-Valley-Translate-CN&Date)

---

<div align="center">

**如果这个项目对你有帮助，请给我们一个 ⭐ Star！**

*让更多的中文玩家享受到完整的星露谷物语模组体验* 🎮✨

</div>
