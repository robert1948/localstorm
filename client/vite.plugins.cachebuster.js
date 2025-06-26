// vite.plugins.cachebuster.js
export default function cacheBusterPlugin() {
  const timestamp = new Date().getTime();
  return {
    name: 'html-cache-buster',
    transformIndexHtml(html) {
      return html.replace(
        /(\.(png|jpe?g|svg|ico|webp|gif|css|js))(\?v=\d+)?/g,
        (match, p1) => `${p1}?v=${timestamp}`
      );
    },
  };
}
