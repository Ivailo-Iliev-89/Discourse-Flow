function setParent(id, username) {

    const parentInput = document.getElementById('parent_id');
  
    if (parentInput) {
        parentInput.value = id;
    }
  
    const formFields = document.getElementById('comment-fields');
    let info = document.getElementById('reply-info');

    if (!info) {
        info = document.createElement('div');
        info.id = 'reply-info';
        info.className = 'alert alert-info py-2 px-3 mb-3 d-flex justify-content-between align-items-center shadow-sm';
        const form = document.getElementById('comment-form');
        form.insertBefore(info, form.firstChild);
    }

    info.innerHTML = `
        <span>Reply to <strong>${username}</strong></span>
        <button type="button" class="btn btn-sm btn-outline-secondary rounded-pill" onclick="cancelReply()">Cancel</button>
    `;
    document.getElementById('comment-form').scrollIntoView({ behavior: 'smooth' });
}

function cancelReply() {
    const parentInput = document.getElementById('parent_id');
    if (parentInput) {
        parentInput.value = '';
    }
  
    const info = document.getElementById('reply-info');
    if (info) {
        info.remove();
    }
}
