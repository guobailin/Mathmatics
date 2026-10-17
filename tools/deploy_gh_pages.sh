#!/usr/bin/env bash
# 一键部署到 GitHub Pages：
#   网页版（dist/web）   → https://guobailin.github.io/Mathmatics/
#   打印页（dist/print） → https://guobailin.github.io/Mathmatics/print/<模块>.html
#
# 用法：
#   bash tools/deploy_gh_pages.sh               # 构建 + 部署
#   bash tools/deploy_gh_pages.sh --skip-build  # 只部署（dist/ 已是最新时）
#
# 依赖：git、Python（pyyaml + markdown-it-py）；gh 为可选（用于等待构建结果）
set -euo pipefail
cd "$(dirname "$0")/.."

BRANCH=gh-pages
WT=.deploy-gh-pages
SITE=https://guobailin.github.io/Mathmatics/

# 1. 选择可用的 Python（需 pyyaml + markdown-it-py）
if [ -n "${PYTHON:-}" ]; then
  PY="$PYTHON"
elif python3 -c "import yaml, markdown_it" 2>/dev/null; then
  PY=python3
else
  PY=/usr/local/bin/python3   # macOS 系统 Python 通常已装齐依赖
fi

# 2. 构建（--skip-build 跳过）
if [ "${1:-}" != "--skip-build" ]; then
  echo "==> 构建产物（$PY tools/build.py）"
  "$PY" tools/build.py
fi

# 3. 在 gh-pages 工作树中装配站点：网页版在根路径，打印版在 /print/
echo "==> 装配 $BRANCH"
git fetch origin "$BRANCH"
git worktree remove --force "$WT" 2>/dev/null || true
git worktree add "$WT" "$BRANCH"
git -C "$WT" rm -rq .
cp -r dist/web/. "$WT"/
mkdir -p "$WT/print"
cp -r dist/print/. "$WT/print"/
git -C "$WT" add -A

if git -C "$WT" diff --cached --quiet; then
  echo "==> 无变化，线上已是最新"
else
  git -C "$WT" commit -q -m "deploy: 网页版 + 打印页（$(date '+%Y-%m-%d %H:%M')）"
  git push origin "$BRANCH"
  echo "==> 已推送 $BRANCH"
fi
git worktree remove "$WT"

# 4. 等待 Pages 构建完成（有 gh 时）
if command -v gh >/dev/null 2>&1; then
  echo -n "==> 等待 Pages 构建"
  for _ in $(seq 1 24); do
    S=$(gh api repos/{owner}/{repo}/pages --jq .status 2>/dev/null || echo unknown)
    [ "$S" = built ] && break
    echo -n .; sleep 5
  done
  echo " $S"
fi

echo "✅ 网页版 $SITE"
echo "✅ 打印页 ${SITE}print/m01.html"
