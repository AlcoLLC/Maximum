document.addEventListener('DOMContentLoaded', function () {
  map_cfg.mapWidth = 0;
  var map = new FlaMap(map_cfg);
  map.drawOnDomReady('map-container');
});

document.addEventListener('DOMContentLoaded', function () {
  const targetNode = document.getElementById('map-container');
  if (!targetNode) return;

  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === 1) {
          if (node.matches('a.fm-scale-plus, a.fm-scale-minus')) {
            node.remove();
          }
          node.querySelectorAll &&
            node.querySelectorAll('a.fm-scale-plus, a.fm-scale-minus').forEach((el) => el.remove());
        }
      });
    });
  });

  observer.observe(targetNode, { childList: true, subtree: true });
});
