<script>
document.addEventListener('click', function(e){
  if(e.target.classList.contains('reply-link')){
    e.preventDefault();
    const id = e.target.getAttribute('data-id');
    document.getElementById('parent_id').value = id;
    document.getElementById('comment-form').scrollIntoView({behavior: 'smooth'});
  }
});
</script>
