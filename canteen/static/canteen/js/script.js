document.addEventListener('DOMContentLoaded', function() {
    const notifBell = document.getElementById('notifBell');
    const notifDropdown = document.getElementById('notifDropdown');

    if (notifBell && notifDropdown) {
        // Toggle dropdown
        notifBell.addEventListener('click', function(e) {
            e.stopPropagation();
            notifDropdown.classList.toggle('active');
        });

        // Close when clicking outside
        document.addEventListener('click', function(e) {
            if (!notifDropdown.contains(e.target) && !notifBell.contains(e.target)) {
                notifDropdown.classList.remove('active');
            }
        });

        // Handle notification item click
        const notifItems = document.querySelectorAll('.notif-item');
        notifItems.forEach(item => {
            item.addEventListener('click', function() {
                const type = this.getAttribute('data-type');
                const id = this.getAttribute('data-id');
                
                // If we are on the monitor pages, we might want to trigger the modal
                // But generally, we can just redirect to the filtered feed or mark as read
                
                // For now, let's mark it as read via the existing endpoint
                fetch(`/activity/read/${type}/${id}/`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            // Optionally redirect to the specific monitor page
                            if (type === 'Concern') window.location.href = '/monitor/concerns/';
                            else if (type === 'Rating') window.location.href = '/monitor/ratings/';
                            else if (type === 'Suggestion') window.location.href = '/monitor/suggestions/';
                        }
                    });
            });
        });
    }
});
