# 工具与 IDE 配置标准

> 版本: v1.0 | 更新: 2026-06

## 概述

本文定义项目统一的工具链和 IDE 配置标准，确保所有团队成员使用一致的开发工具配置，消除工具差异带来的问题。

## 工具分类

```yaml
基础工具链:
  - Git (版本控制)
  - Maven / pnpm (构建)
  - Docker (容器化)
  - IDE (编码)

辅助工具:
  - Postman / Insomnia (API 调试)
  - DBeaver / DataGrip (数据库)
  - Redis Insight (缓存)
  - Kafka Tool (消息队列)

效率工具:
  - jq (JSON 处理)
  - yq (YAML 处理)
  - httpie (HTTP 客户端)
  - fzf (模糊搜索)
  - ripgrep (快速搜索)
```

## Git 配置

### 全局配置

```bash
git config --global user.name "Your Name"
git config --global user.email "your.name@company.com"
git config --global init.defaultBranch main
git config --global core.autocrlf input
git config --global core.editor "code --wait"
git config --global pull.rebase true
git config --global fetch.prune true
git config --global diff.algorithm histogram
git config --global push.default current
```

### 别名配置

```bash
git config --global alias.ci "commit -s"
git config --global alias.co "checkout"
git config --global alias.br "branch"
git config --global alias.st "status -sb"
git config --global alias.lg "log --graph --oneline --all --decorate"
git config --global alias.unstage "reset HEAD --"
git config --global alias.amend "commit --amend --no-edit"
git config --global alias.prune "remote prune origin"
```

### Git Hooks

项目级 hooks（通过 `lefthook` 或 `husky` 管理）：

```yaml
pre-commit:
  commands:
    lint:
      run: npx eslint {staged_files}
    format:
      run: npx prettier --check {staged_files}
    secrets:
      run: npx trufflehog --no-verification

pre-push:
  commands:
    test:
      run: npm run test:ci
    build:
      run: npm run build
```

## IDE 统一配置

### IntelliJ IDEA

推荐的配置（通过 `.idea` 目录版本化管理）：

```xml
<!-- code-style.xml -->
<code_scheme name="Project" version="173">
  <option name="LINE_SEPARATOR" value="&#10;" />
  <JavaCodeStyleSettings>
    <option name="CLASS_COUNT_TO_USE_IMPORT_ON_DEMAND" value="99" />
    <option name="JD_ALIGN_EXCEPTION_COMMENTS" value="false" />
  </JavaCodeStyleSettings>
  <codeStyleSettings language="JAVA">
    <option name="RIGHT_MARGIN" value="120" />
    <option name="BLANK_LINES_AROUND_CLASS" value="1" />
    <indentOptions>
      <option name="INDENT_SIZE" value="4" />
      <option name="CONTINUATION_INDENT_SIZE" value="4" />
      <option name="TAB_SIZE" value="4" />
    </indentOptions>
  </codeStyleSettings>
</code_scheme>
```

保存时自动操作：

```xml
<!-- 保存时动作 -->
<component name="SaveActions">
  <option name="ACTIVATE_ON_SAVE" value="true" />
  <option name="OPTIMIZE_IMPORTS" value="true" />
  <option name="REFORMAT_CODE" value="true" />
  <option name="REARRANGE_CODE" value="false" />
</component>
```

### VS Code

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.rulers": [120],
  "editor.tabSize": 2,
  "files.eol": "\n",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "typescript.preferences.importModuleSpecifier": "relative",
  "eslint.validate": ["typescript", "vue", "javascript"]
}
```

## Linter & Formatter 配置

### ESLint (前端)

```javascript
// eslint.config.js
export default [
  {
    rules: {
      "no-console": ["warn", { allow: ["warn", "error"] }],
      "no-unused-vars": "error",
      "@typescript-eslint/explicit-function-return-type": "warn",
      "vue/component-name-in-template-casing": ["error", "PascalCase"],
    },
  },
];
```

### Prettier (前端)

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "endOfLine": "lf",
  "arrowParens": "always"
}
```

### CheckStyle (后端)

```xml
<!-- checkstyle.xml -->
<module name="Checker">
  <module name="LineLength">
    <property name="max" value="120"/>
  </module>
  <module name="TreeWalker">
    <module name="UnusedImports"/>
    <module name="CustomImportOrder">
      <property name="customImportOrderRules"
        value="STATIC###THIRD_PARTY_PACKAGE###STANDARD_JAVA_PACKAGE"/>
    </module>
    <module name="MethodLength">
      <property name="max" value="40"/>
    </module>
  </module>
</module>
```

## 命令行工具

### 推荐 Shell 配置

```bash
# ~/.zshrc 或 ~/.bashrc
export EDITOR="code --wait"
export VISUAL="code --wait"

# 配置 Maven 多线程构建
export MAVEN_OPTS="-Xmx2g -XX:MaxMetaspaceSize=512m"
export MAVEN_ARGS="--threads 1C"

# 配置 Docker 资源
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```

### 效率脚本

```bash
# 快速搜索代码
alias q='rg --type-add "web:*.{ts,vue,js,tsx,jsx}" -t web'

# 快速打开项目
alias proj='cd ~/workspace/alive-engineering-standard'

# 快速查看 Git 日志
alias glog='git log --oneline --graph --all --decorate -20'

# Docker 清理
alias dclean='docker system prune -af --volumes'
```

## 工具版本锁定

项目根目录维护工具版本声明：

```yaml
# .tool-versions (asdf)
java 21.0.2-tem
nodejs 20.12.0
python 3.11.8
maven 3.9.6
```

```json
// .nvmrc
20
```

## 工具审计

- 每季度检查工具链版本，确保所有工具在安全支持期内
- 使用 `asdf` 统一管理运行时版本（替代 SDKMAN + nvm + fvm 的组合）
- IDE 配置文件纳入版本控制，确保团队一致

## 相关文档

- [环境搭建](./012_Project_Environment.md)
- [技术选型](./011_Project_TechStack.md)
- [新人入职](./019_Project_Onboarding.md)
