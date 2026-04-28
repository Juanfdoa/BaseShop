function toggleMsg(el) {
  el.classList.toggle('open');
  const dot = el.querySelector('.unread-dot');
  if (dot && el.classList.contains('open')) {
    const msgId = el.dataset.id;
    fetch(`/admin/messages/open/${msgId}`, { method: 'POST' })
      .then(r => { if (r.ok) dot.remove(); });
  }
}