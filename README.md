# Gardenia

栀花（Gardenia）的个人网站：一个以夜色与暖灯为基调的中文单页站点。

## 技术栈

- [Astro](https://astro.build/) 静态站点，构建产物为纯静态 HTML / CSS / JS，可直接托管在任意静态平台。
- 页面不含 React island，交互由少量原生脚本完成（滚动显现、导航状态、首屏氛围效果等）。
- 样式使用 scoped CSS 与 `src/styles/tokens.css` 中的设计变量，类名遵循 BEM。
- 包管理器为 pnpm（CI 使用 pnpm 11、Node.js 22）。

## 本地开发

```bash
pnpm install
pnpm dev
```

开发服务器默认运行在 `http://localhost:4321`。

## 构建与预览

```bash
pnpm build
pnpm preview
```

`pnpm build` 输出到 `dist/`；`pnpm preview` 用于在本地预览构建结果。

## 目录结构

```
src/
├── pages/          # 页面入口（当前为单页 index.astro）
├── layouts/        # HTML 外壳、全局样式与字体引入
├── components/     # 导航、首屏、关于、页脚与氛围效果
├── styles/         # tokens.css（设计变量）与 global.css
└── assets/photos/  # 参与构建的照片
public/             # 原样拷贝的静态资源（站点图标、噪点纹理、第三方图标）
images/             # 原始素材归档，构建不引用
docs/               # 项目评审与改进建议
.github/workflows/  # CI 配置
```

## 图片管线

照片存放在 `src/assets/photos/`，通过 `astro:assets` 的 `<Image>` / `<Picture>` 组件引用。构建时会按组件声明的 `widths` / `sizes` 自动生成多尺寸 AVIF / WebP，并按需设置首屏图的 `loading="eager"` 与其余图片的懒加载。

`public/` 下的资源会原样拷贝，不经过图片优化；`images/` 仅用于归档原始素材（如原始照片），页面与构建流程都不引用它。

## 字体

- 正文使用系统字体栈（`PingFang SC`、`Microsoft YaHei` 等），不额外下载正文字体。
- 标题使用自托管的 LXGW WenKai 子集：`public/fonts/lxgw-wenkai-regular.woff2`，约 74 KB，覆盖当前站内文案（汉字、拉丁字母与常用标点）。`@font-face` 定义在 `src/styles/global.css`。
- 字体依据 SIL Open Font License 1.1 使用，许可全文见 [`public/fonts/OFL.txt`](./public/fonts/OFL.txt)；它不属于代码的 MIT 授权。
- 修改或新增文案后需要重新生成子集，否则新字符会回退到系统楷体：

```bash
pip install fonttools brotli
python scripts/subset-font.py path/to/LXGWWenKai-Regular.ttf
```

字体变量定义在 `src/styles/tokens.css` 的 `--font-display` 与 `--font-body`。

## 个性化素材

- `public/og.jpg` 是 1200×630 的分享预览图；`public/favicon.ico`、`favicon-32.png`、`apple-touch-icon.png` 为站点图标。
- 修改文案或品牌后，可以按需重新生成这些素材；它们不参与构建流程，放在 `public/` 会被原样拷贝。

## 部署与 `Astro.site`

站点是纯静态输出，可部署到 Vercel、Cloudflare Pages、GitHub Pages 等任意静态托管：构建命令 `pnpm build`，输出目录 `dist`。

canonical 与 `og:url` 依赖 Astro 的 `site` 配置。只有在 `astro.config.mjs` 中设置了站点地址后，这些标签才会输出：

```js
export default defineConfig({
  site: 'https://example.com/',
  // ...
});
```

未设置 `site` 时，页面不会生成 canonical / `og:url`，分享链接也缺少绝对地址。部署前请把示例地址替换为实际域名。

仓库包含 `.github/workflows/ci.yml`：在 push 到 `main` 及 Pull Request 时，使用 pnpm 11 与 Node.js 22 执行 `pnpm install --frozen-lockfile` 和 `pnpm build`。

## 许可证

本仓库采用分层授权：

- **代码**：MIT License，见 [`LICENSE`](./LICENSE)。
- **照片与图片**：保留所有权利，见 [`LICENSE-IMAGES`](./LICENSE-IMAGES)。包括 `images/`、`src/assets/photos/`、站点图标等，未经书面许可不得复制、修改或再分发。
- **第三方品牌图标**：`public/icons/` 中的 Bilibili、小红书图标归各自权利人所有，参见 [`NOTICE`](./NOTICE)。
- **标题字体**：LXGW WenKai 子集，SIL Open Font License 1.1，见 [`public/fonts/OFL.txt`](./public/fonts/OFL.txt)。

可以基于 MIT 许可复用源码，但图片不在授权范围内。
