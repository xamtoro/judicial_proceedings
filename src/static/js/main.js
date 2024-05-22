document.getElementById('judicialForm').addEventListener('submit', function() {
    document.getElementById('loadingOverlay').style.display = 'flex';
});

window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        window.location.reload();
    }
});

document.querySelector('.btn-outline-danger').addEventListener('click', function() {
    document.getElementById('judicialForm').reset();
});